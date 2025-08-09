from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap

from variables import Menus


class ToggleButton(QLabel):
    clicked = Signal()

    def __init__(self, list_of_paths_for_images: list[str],
                 function,
                 width: int = Menus.size_of_buttons_menu_3,
                 parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)  # Visual cue for clickability
        self.function = function
        self.state_i = 0
        self.n_of_states = len(list_of_paths_for_images)
        # Image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(QSize(width, width))
        self.list_of_pixmap: list[QPixmap] = []
        for path in list_of_paths_for_images:
            self.list_of_pixmap.append(self.get_pixmap(path))
        self.image_label.setPixmap(self.list_of_pixmap[0])


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.state_i += 1
            if self.state_i >= self.n_of_states:
                self.state_i = 0
            self.image_label.setPixmap(self.list_of_pixmap[self.state_i])
            self.function(self.state_i)

    def get_pixmap(self, path: str) -> QPixmap | None:
        path = Menus.pictures_menu + path
        pixmap = QPixmap(path)

        if pixmap.isNull():
            print('No picture', path)
            return None
        else:
            new_size = QSize(self.image_label.size())
            scaled = pixmap.scaled(new_size,
                                   Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation)
        return scaled

