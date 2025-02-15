import os
import requests

# Configuration
GITHUB_USERNAME = "EpicPichu"  # Your GitHub username
GITHUB_REPO = "Pichu-Overlay"  # Your repository name
GITHUB_BRANCH = "main"  # Change to 'master' if needed
LOCAL_FOLDER = "./"  # Folder to sync

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/"

def get_repo_files(path=""):
    """Fetch file list from GitHub repository."""
    url = GITHUB_API_URL + path + f"?ref={GITHUB_BRANCH}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # List of files/folders
    else:
        print(f"Error fetching repo files: {response.text}")
        return []

def delete_existing_files(repo_files):
    """Delete files in local folder if they also exist in the repo."""
    for item in repo_files:
        local_file_path = os.path.join(LOCAL_FOLDER, item["path"])
        
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
            print(f" - Deleted: {local_file_path}")

def download_file(file_path, download_url):
    """Download a fresh copy of a file from GitHub."""
    local_file_path = os.path.join(LOCAL_FOLDER, file_path)
    
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  # Create directories if needed

    response = requests.get(download_url)
    if response.status_code == 200:
        with open(local_file_path, "wb") as f:
            f.write(response.content)
        print(f" + Downloaded: {file_path}")
    else:
        print(f" X Failed to download {file_path}")

def sync_repo(path=""):
    """Delete existing files and download fresh copies from GitHub."""
    repo_files = get_repo_files(path)

    if not repo_files:
        print(" X No files found in repo. Exiting.")
        return

    delete_existing_files(repo_files)  # Delete existing files
    
    for item in repo_files:
        file_path = item["path"].replace("\\", "/")
        if item["type"] == "file":
            download_file(file_path, item["download_url"])
        elif item["type"] == "dir":
            sync_repo(file_path)  # Recursively process folders

if __name__ == "__main__":
    os.makedirs(LOCAL_FOLDER, exist_ok=True)
    sync_repo()
