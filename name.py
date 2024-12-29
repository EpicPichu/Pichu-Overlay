from PyQt5.QtCore import pyqtSignal, QObject
import subprocess

class Logger(QObject):
    log_signal = pyqtSignal(str)
    def __init__(self, path="C:/Users/EpicPichu/AppData/Roaming/.minecraft/logs/latest.log"):
        super().__init__()
        self.path = path
        self.process = None
        self.running = False

    def start_logging(self):
        """
        Start the logger in the background.
        """
        self.running = True
        command = rf'''Get-Content -Path "{self.path}" -Tail 0 -Wait | 
        Select-String -Pattern "\[CHAT\]" | 
        ForEach-Object {{ $_.Line -replace '.*\[CHAT\]', '' }} | 
        Where-Object {{ $_ -match "^[a-zA-Z0-9 _,]*$"}}
        '''
        self.process = subprocess.Popen(
            ["powershell", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            for line in self.process.stdout:
                if not self.running:
                    break
                clean_line = line.strip()
                self.log_signal.emit(clean_line)

        finally:
            if self.process:
                self.process.terminate()

    def stop_logging(self):
        """
        Stop the logger.
        """
        self.running = False
        if self.process:
            self.process.terminate()