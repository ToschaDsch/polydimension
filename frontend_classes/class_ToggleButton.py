from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QIcon, QPixmap

from variables import Menus


class ToggleButton(QWidget):
    def __init__(self, image_path_1: str,
                 image_path_2: str,
                 function,
                 width: int = Menus.size_of_buttons_2,
                 parent=None):
        super().__init__(parent)
        self.setWindowTitle("Toggle QPushButton Images")
        self.resize(width, Menus.size_of_buttons_2)

        self.function = function
        self.frame: int = Menus.frame_menu_2
        self.width = width
        self.button = QPushButton()
        self.button.setFixedWidth(width)
        self.button.setFixedHeight(Menus.size_of_buttons_2)
        self.icon2 = QIcon(self.get_pixmap(path=image_path_2))
        self.icon1 = QIcon(self.get_pixmap(path=image_path_1))  # Replace with your image paths
        self.toggle = True

        self.button.setIcon(self.icon1)
        self.button.setIconSize(self.button.size())  # Optional: Adjust icon size to button

        self.button.clicked.connect(self.change_icon)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def get_pixmap(self, path: str) -> QPixmap | None:
        path = Menus.pictures_menu + path
        pixmap = QPixmap(path)

        if pixmap.isNull():
            print('No picture', path)
            return None
        else:
            new_size = QSize(self.button.width() - self.frame, self.button.height() - self.frame)
            scaled = pixmap.scaled(new_size,
                                   Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation)
            self.button.setIcon(scaled)
            self.button.setIconSize(QSize(self.width, Menus.size_of_buttons_2))
        return scaled

    def change_icon(self):
        if self.toggle:
            self.button.setIcon(self.icon2)
        else:
            self.button.setIcon(self.icon1)
        self.toggle = not self.toggle

        self.function()
