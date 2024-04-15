from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from gui.layout import Layout



class MainLayout(Layout):
    def __init__(self, window):
        super().__init__(window)
        self.draw()
              
    def draw(self):
        self.image_row = 10
        self.image_column = 10
        self.image_rows = self.num_of_rows - 20
        self.image_columns = self.num_of_columns - 20
        
        self.main_button.setDisabled(True)
        self.main_button.setStyleSheet("QPushButton {background-color: lightblue}")
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        pixmap = QPixmap('/home/mousevillage/mouse_village/resources/mouse_village.png')
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(self.image_columns * self.column_width, self.image_rows * self.row_height)
        self.addWidget(self.label, self.image_row, self.image_column, self.image_rows, self.image_columns)

