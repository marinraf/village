from PyQt5.QtWidgets import QApplication
from village.log import log
from village.settings import settings
from village.utils import *
from gui.gui import Gui


create_directories()

app = QApplication([])
app.setStyle('Fusion')
gui = Gui(app)
app.exec()


