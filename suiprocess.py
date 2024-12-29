import subprocess

def name_logger(
    path = "C:/Users/EpicPichu/AppData/Roaming/.minecraft/logs/latest.log"
):
    # Define the PowerShell command
    command = rf'''Get-Content -Path "{path}" -Tail 0 -Wait | 
    Select-String -Pattern "\[CHAT\]" | 
    ForEach-Object {{ $_.Line -replace '.*\[CHAT\]', '' }} | 
    Where-Object {{ $_ -match "^[a-zA-Z0-9 _,]*$"}}
    '''

    # Run the command using subprocess
    process = subprocess.Popen(
        ["powershell", "-Command", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Continuously read the output
    try:
        for line in process.stdout:
            print(line.strip())  # Print each line of output
    except KeyboardInterrupt:
        process.terminate()

name_logger()