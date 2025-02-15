import sys, threading, asyncio, json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_window import Ui_MainWindow

from variables import *
from player_capture import Logger
from table_constructor import table_row
from pika_stats import stats as bwstats

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Instantiate the UI class
        self.ui.setupUi(self)      # Set up the UI in this window

    def show_alert(self):
        """Show an alert window"""
        alert = QMessageBox(self)
        alert.setWindowTitle("Alert")
        alert.setText("Restart this app to apply changes.")
        alert.setIcon(QMessageBox.Information)  # Icon types: Information, Warning, Critical, Question
        alert.setStandardButtons(QMessageBox.Ok)  # Add buttons
        alert.setDefaultButton(QMessageBox.Ok)  # Set the default button

        alert.exec_()

try:
    with open(config_path, 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    with open(config_path, "w") as file:
        json.dump(config_template, file, indent=4)

client = config['Client']

if client == 'Custom': log_path = config['Custom Log Path']
else: log_path = log_paths.get(client)
client_div = div_clients.get(client)

initial_content = start + header + client_div + initial_end

# Start the Qt application
app = QApplication(sys.argv)
window = MainWindow()
window.ui.html_display.setHtml(initial_content)

#
def start_logger_thread(logger):
    logger_thread = threading.Thread(target=logger.start_logging, daemon=True)
    logger_thread.start()
    return logger_thread

logger = Logger(path=log_path)
logger_thread = start_logger_thread(logger)
#











async def fetch_stats(usernames):
    results = await asyncio.gather(*[bwstats(ign) for ign in usernames])
    return results

def fetch_table(message: str):
    if message.count(' ') != message.count(','):
        return
    
    usernames = message.split(", ")

    if len(usernames) < 2:
        return
    
    stats = asyncio.run(fetch_stats(usernames))  # Run the coroutine in the asyncio loop
    rows = ''' '''

    for players in stats:
        row = table_row(*players)
        rows += row

    output = start+rows+header+client_div+end

    window.ui.html_display.setHtml(output)

logger.log_signal.connect(fetch_table)











def write(obj, val):
    with open(config_path, 'r') as file:
        config_data = json.load(file)

    config_data[obj] = val

    with open(config_path, 'w') as file:
        json.dump(config_data, file, indent=4)

def set_lunar():
    write('Client', clients[0])
    window.show_alert()
def set_badlion():
    write('Client', clients[1])
    window.show_alert()

def set_vanilla():
    write('Client', clients[2])
    window.show_alert()

def set_custom():
    write('Client', clients[3])
    window.show_alert()


window.ui.actionLunar_Client.triggered.connect(set_lunar)
window.ui.actionBadlion_Client.triggered.connect(set_badlion)
window.ui.actionVanilla_Launcher.triggered.connect(set_vanilla)
window.ui.actionCustom.triggered.connect(set_custom)












try:
    window.show()
    sys.exit(app.exec_())
finally:
    logger.stop_logging()