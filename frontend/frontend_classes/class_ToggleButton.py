from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap

from variables.menus import Menus


class ToggleButton(QWidget):
    clicked = Signal()

    def __init__(self, list_of_paths_for_images: list[str],
                 function, name: str = "noname_button",
                 width: int = Menus.size_of_buttons_menu_3,
                 parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_name = QLabel(name)
        label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_name)
        self.label_picture = QLabel()
        layout.addWidget(self.label_picture)
        self.setLayout(layout)
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Visual cue for clickability
        self.function = function
        self.state_i = 0
        self.n_of_states = len(list_of_paths_for_images)
        # Image
        self.label_picture.setFixedSize(QSize(width, width))
        self.list_of_pixmap: list[QPixmap] = []
        for path in list_of_paths_for_images:
            self.list_of_pixmap.append(self.get_pixmap(path))
        self.label_picture.setPixmap(self.list_of_pixmap[0])


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.state_i += 1
            if self.state_i >= self.n_of_states:
                self.state_i = 0
            self.label_picture.setPixmap(self.list_of_pixmap[self.state_i])
            self.function(self.state_i)

    def get_pixmap(self, path: str) -> QPixmap | None:
        path = Menus.pictures_menu + path
        pixmap = QPixmap(path)

        if pixmap.isNull():
            print('No picture', path)
            return None
        else:
            new_size = QSize(self.label_picture.size())
            scaled = pixmap.scaled(new_size,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
        return scaled

