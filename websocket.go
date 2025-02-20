package main

import (
	"bufio"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"
	"unsafe"

	"github.com/gorilla/websocket"
)

// Repo link
const webapplink string = `https://epicpichu.github.io/Pichu-Overlay`
const version string = `0.9`

// Get the user's home directory
var homeDir, err = os.UserHomeDir()

// Define the config directory and file path
var configDir = filepath.Join(homeDir, ".pichu-overlay")
var configFile = filepath.Join(configDir, "config.txt")

var client *string
var logpath *string

var client_logpaths = map[string]string{
	"Lunar Client":   filepath.Join(homeDir, `.lunarclient\offline\multiver\logs\latest.log`),
	"Badlion Client": filepath.Join(homeDir, `\AppData\Roaming\.minecraft\logs\blclient\minecraft\latest.log`),
	"Vanilla":        filepath.Join(homeDir, `\AppData\Roaming\.minecraft\logs\latest.log`),
}

// Config handler function
func configurator() {
	defaultconfig := "client: Vanilla\nlogpath: " + client_logpaths["Vanilla"]

	// Ensure the directory exists
	err = os.MkdirAll(configDir, 0755) // Creates the directory if not exists
	if err != nil {
		fmt.Println("Error creating config directory:", err)
		return
	}

	// Check if the file exists before creating
	if _, err := os.Stat(configFile); os.IsNotExist(err) {
		fmt.Println("Config file does not exist. Creating one...")
		file, err := os.Create(configFile)
		if err != nil {
			fmt.Println("Error creating config file:", err)
			return
		}
		defer file.Close()

		if _, err = file.WriteString(defaultconfig); err != nil {
			fmt.Println("Error writing to config file:", err)
			return
		}
	}

	fileread := readConfig()
	client = &fileread[0]
	logpath = &fileread[1]
}

// Read config function
func readConfig() []string {
	file, err := os.Open(configFile)
	if err != nil {
		fmt.Println("Error creating config file:", err)
		return []string{"nil", "nil"}
	}

	var client_name, log_path string

	// Read line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// Config Processing
		if strings.HasPrefix(line, "client: ") {
			client_name = strings.SplitN(line, "client: ", 2)[1]
		}
		if strings.HasPrefix(line, "logpath: ") {
			log_path = strings.SplitN(line, "logpath: ", 2)[1]
		}
	}

	// Check for errors while reading
	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading config file:", err)
	}
	defer file.Close()
	return []string{client_name, log_path}
}

// Write config function
func writeConfig(client string, logpath string) {
	file, err := os.OpenFile(configFile, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println("Error opening config file:", err)
		return
	}
	defer file.Close()

	configstring := "client: " + client + "\nlogpath: " + logpath
	if _, err = file.WriteString(configstring); err != nil {
		fmt.Println("Error writing to config file:", err)
	}
}

// Powershell Script
var script = func(path string) string {
	return `

Get-Content -Path "` + path + `" -Tail 0 -Wait |
Select-String -Pattern "\[CHAT\]" |
ForEach-Object {
    # Extract the chat message by removing everything before [CHAT]
    $line = $_.Line -replace '.*\[CHAT\] ', ''

    # Tab check
    if (
        (($line -split ' ').Count - 1) -eq (($line -split ',').Count - 1) -and 
        ($line -match "^[a-zA-Z0-9 _,]*$")
    )   {
        if ($line -match ".*,.*,.+") {
            Write-Output "TAB: $line"
        }
    }
    # Join check
    elseif ($line -match "^BedWars .* ([a-zA-Z0-9_]+) has joined! \s?(.*)") {
        Write-Output "JOIN: $($matches[1])"
        Write-Output "PLAYERCOUNT: $($matches[2])"
    }
    # Leave check
    elseif ($line -match "^BedWars .* ([a-zA-Z0-9_]+) has quit! \s?(.*)") {
        Write-Output "LEAVE: $($matches[1])"
        Write-Output "PLAYERCOUNT: $($matches[2])"
    }
}
`

}

// Open link in browser
func openBrowser(url string) error {
	var cmd *exec.Cmd

	switch runtime.GOOS {
	case "windows":
		cmd = exec.Command("rundll32", "url.dll,FileProtocolHandler", url)
	case "darwin":
		cmd = exec.Command("open", url)
	default: // Linux and other Unix-like systems
		cmd = exec.Command("xdg-open", url)
	}

	return cmd.Start()
}

// Load Windows DLLs
var (
	comdlg32                 = syscall.NewLazyDLL("comdlg32.dll")
	getOpenFile              = comdlg32.NewProc("GetOpenFileNameW")
	user32                   = syscall.NewLazyDLL("user32.dll")
	kernel32                 = syscall.NewLazyDLL("kernel32.dll")
	getForegroundWindow      = user32.NewProc("GetForegroundWindow")
	getWindowThreadProcessId = user32.NewProc("GetWindowThreadProcessId")
	attachThreadInput        = user32.NewProc("AttachThreadInput")
	setForegroundWindow      = user32.NewProc("SetForegroundWindow")
	getCurrentThreadId       = kernel32.NewProc("GetCurrentThreadId")
)

// Bring the window to the front
func bringWindowToFront(hwnd uintptr) {
	fgThread, _, _ := getWindowThreadProcessId.Call(hwnd, 0)
	curThread, _, _ := getCurrentThreadId.Call()

	attachThreadInput.Call(fgThread, curThread, 1)
	setForegroundWindow.Call(hwnd)
	attachThreadInput.Call(fgThread, curThread, 0)
}

// File dialog function using Windows API
func openFileDialog() (string, error) {
	var ofn struct {
		lStructSize       uint32
		hwndOwner         uintptr
		hInstance         uintptr
		lpstrFilter       *uint16
		lpstrCustomFilter *uint16
		nMaxCustFilter    uint32
		nFilterIndex      uint32
		lpstrFile         *uint16
		nMaxFile          uint32
		lpstrFileTitle    *uint16
		nMaxFileTitle     uint32
		lpstrInitialDir   *uint16
		lpstrTitle        *uint16
		flags             uint32
		nFileOffset       uint16
		nFileExtension    uint16
		lpstrDefExt       *uint16
		lCustData         uintptr
		lpfnHook          uintptr
		lpTemplateName    *uint16
	}

	hwnd, _, _ := getForegroundWindow.Call()
	bringWindowToFront(hwnd)

	filePath := make([]uint16, syscall.MAX_PATH)
	title, _ := syscall.UTF16PtrFromString("Select Configuration File")

	ofn.lStructSize = uint32(unsafe.Sizeof(ofn))
	ofn.hwndOwner = hwnd
	ofn.lpstrFile = &filePath[0]
	ofn.nMaxFile = syscall.MAX_PATH
	ofn.lpstrTitle = title
	ofn.flags = 0x00000008 | 0x00001000 // OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST

	ret, _, _ := getOpenFile.Call(uintptr(unsafe.Pointer(&ofn)))
	if ret == 0 {
		return "", fmt.Errorf("no file selected")
	}
	return syscall.UTF16ToString(filePath), nil
}

// Function to run the PowerShell command and return the command object
func start_powershell(command string, conn *websocket.Conn) *exec.Cmd {
	cmd := exec.Command("powershell", "-NoProfile", "-Command", command)

	// Capture stdout
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Println("Failed to get stdout:", err)
		return nil
	}

	// Start process
	if err := cmd.Start(); err != nil {
		log.Println("Failed to start command:", err)
		return nil
	}

	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			line := scanner.Text()
			log.Println(line)

			// Send output to the WebSocket client
			err := conn.WriteMessage(websocket.TextMessage, []byte(line))
			if err != nil {
				log.Println("Error sending message:", err)
				break
			}
		}

		if err := scanner.Err(); err != nil {
			log.Println("Error reading from stdout:", err)
		}
	}()

	return cmd
}

// WebSocket upgrader (allows all origins)
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

// WebSocket handler function
func wsHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket upgrade failed:", err)
		http.Error(w, "Upgrade failed", http.StatusInternalServerError)
		return
	}
	defer conn.Close()

	log.Println("Client connected")
	conn.WriteMessage(websocket.TextMessage, []byte("CLIENT: "+*client))

	// Start the PowerShell command in a separate goroutine
	cmd := start_powershell(script(*logpath), conn)

	// Incoming Message Handler
	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Error reading message:", err)
			break
		}

		log.Printf("Received: %s\n", msg)

		if strings.HasPrefix(string(msg), "VERSION: ") {
			ver := strings.SplitN(string(msg), "VERSION: ", 2)[1]
			if ver != version {
				conn.WriteMessage(websocket.TextMessage, []byte(`OUTDATED_VER`))
			}
		}

		if strings.HasPrefix(string(msg), "CLIENT_CHANGE: ") {
			clientname := strings.SplitN(string(msg), "CLIENT_CHANGE: ", 2)[1]
			if clientname != "Custom" {
				file_path := client_logpaths[clientname]
				writeConfig(clientname, file_path)
				conn.WriteMessage(websocket.TextMessage, []byte("CLIENT: "+clientname))
			}

			if clientname == "Custom" {
				file_path, err := openFileDialog()
				if err != nil {
					file_path = "No file selected"
				}
				writeConfig(clientname, file_path)
				conn.WriteMessage(websocket.TextMessage, []byte("LOG_PATH: "+file_path))
				conn.WriteMessage(websocket.TextMessage, []byte("CLIENT: "+clientname))
			}
		}
	}

	log.Println("Client disconnected")

	// Terminate the PowerShell command when the client disconnects
	if cmd != nil {
		err := cmd.Process.Kill()
		if err != nil {
			log.Println("Failed to kill PowerShell process:", err)
		} else {
			log.Println("PowerShell process terminated.")
		}
	}

	os.Exit(0)
}

func main() {
	configurator()
	openBrowser(webapplink)
	http.HandleFunc("/ws", wsHandler)
	port := "6969"
	log.Println("WebSocket server running on ws://127.0.0.1:" + port + "/ws")
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
