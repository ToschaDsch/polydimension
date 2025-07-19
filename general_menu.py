from functools import partial

from PySide6 import QtGui
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton

from menu_lines import MenusLines
from variables import Menus


class GeneralWindow(QMainWindow):
    def __init__(self, *args):
        super(GeneralWindow, self).__init__()
        self.setWindowTitle(Menus.name_of_the_program)
        self.setFixedWidth(int(0.5 * Menus.screen_width))
        general_layout = QHBoxLayout()

        # variables to calculate#

        # load menus
        # display
        b = int(0.5 * Menus.screen_width - Menus.b_menu)
        h = int(0.5 * Menus.screen_height)
        self.canvas_section = QtGui.QPixmap(b, h)
        self.label_canvas = QLabel()
        self.label_canvas.setPixmap(self.canvas_section)
        self.painter_section = QtGui.QPainter(self.canvas_section)
        font = QFont('Century Gothic', Menus.font_height)
        self.painter_section.setFont(font)

        self.load_display(general_layout=general_layout)

        # menu right
        self.load_menu_right(general_layout=general_layout)

        widget = QWidget()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)

    def load_display(self, general_layout: QHBoxLayout):
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.label_canvas)
        self.painter_section = QtGui.QPainter(self.canvas_section)

        general_layout.addLayout(display_layout)

    def load_menu_right(self, general_layout: QHBoxLayout):
        layout_menu = QVBoxLayout()
        label_name = QLabel(Menus.name_of_the_program)
        layout_menu.addWidget(label_name)

        self.load_objects(layout_menu=layout_menu)

        general_layout.addLayout(layout_menu)

    def load_objects(self, layout_menu: QVBoxLayout):
        for line in MenusLines:
            line_i = QHBoxLayout()
            # load picture
            line_i.addWidget(
                get_the_button_for_an_object(
                    path=line.value.pict,
                    name=line.value.name))

            # info
            line_i.addWidget(get_info_button(path_for_info=line.value.info))
            layout_menu.addLayout(line_i)


def get_the_button_for_an_object(path: str, name: str = None) -> QPushButton:
    button_with_ico = QPushButton(name)
    button_with_ico.setFixedWidth(200)
    path = Menus.pictures_preview + path
    pixmap = QPixmap(path)
    if pixmap.isNull():
        print('No picture', path)
    else:
        button_with_ico.setIcon(pixmap)
        button_with_ico.setIconSize(QSize(Menus.size_of_pictures_in_the_list, Menus.size_of_pictures_in_the_list))
        button_with_ico.setMaximumHeight(Menus.size_of_pictures_in_the_list+10)
    return button_with_ico


def get_info_button(path_for_info: str) -> QPushButton:
    path_info_symbol = Menus.pictures_menu + "info.png"
    pixmap_info = QPixmap(path_info_symbol)

    info_button = QPushButton()
    info_button.setFixedWidth(Menus.size_of_pictures_in_the_list)
    info_button.setFixedHeight(Menus.size_of_pictures_in_the_list)
    if pixmap_info.isNull():
        info_button.setText('No picture')
        print('No picture', path_info_symbol)
    else:
        scaled = pixmap_info.scaled(info_button.size(),
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        info_button.setIcon(scaled)
    info_button.setIcon(pixmap_info)
    info_button.clicked.connect(partial(info_button_action, path_for_info))

    return info_button


def info_button_action(path_to_the_picture: str):
    print(path_to_the_picture)
