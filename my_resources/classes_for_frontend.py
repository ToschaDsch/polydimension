from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from variables import Menus


class ClickableWidget(QWidget):
    clicked = Signal()

    def __init__(self, image_path, text, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)  # Visual cue for clickability

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)

        # Image
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print('No picture', image_path)
        size: int = Menus.size_of_pictures_in_the_list
        self.image_label.setPixmap(pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.image_label)

        # Text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(self.text_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
