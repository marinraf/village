from gui.gui import Gui
from PyQt5.QtWidgets import QApplication

from village.utils import create_directories

create_directories()

app = QApplication([])
app.setStyle("Fusion")
gui = Gui(app)
app.exec()
