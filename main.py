import sys, threading, asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow

from variables import *
from name import Logger
from table_constructor import table_row
from pika_stats import stats as bwstats

initial_content = start + sample_row + header + clientname + initial_end

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Instantiate the UI class
        self.ui.setupUi(self)      # Set up the UI in this window

# Start the Qt application
app = QApplication(sys.argv)
window = MainWindow()
window.ui.html_display.setHtml(initial_content)

#
def start_logger_thread(logger):
    logger_thread = threading.Thread(target=logger.start_logging, daemon=True)
    logger_thread.start()
    return logger_thread

logger = Logger()
logger_thread = start_logger_thread(logger)
#











async def fetch_stats(usernames):
    results = await asyncio.gather(*[bwstats(ign) for ign in usernames])
    return results

def fetch_table(message):
    usernames = message.split(", ")
    if len(usernames) < 2:
        return
    
    stats = asyncio.run(fetch_stats(usernames))  # Run the coroutine in the asyncio loop
    rows = ''' '''

    for players in stats:
        row = table_row(*players)
        rows += row

    output = start+rows+header+clientname+end
    window.ui.html_display.setHtml(output)

logger.log_signal.connect(fetch_table)














try:
    window.show()
    sys.exit(app.exec_())
finally:
    logger.stop_logging()