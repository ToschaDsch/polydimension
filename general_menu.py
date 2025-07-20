from functools import partial

from PySide6 import QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QStackedLayout

from menu_lines import MenusLines
from variables import Menus


class GeneralWindow(QMainWindow):
    def __init__(self, *args):
        super(GeneralWindow, self).__init__()
        self.setWindowTitle(Menus.name_of_the_program)
        self.setFixedWidth(int(0.5 * Menus.screen_width))
        self._general_layout = QHBoxLayout()

        # variables to calculate

        # load menus
        #   menu_1 (display and menu)
        # display
        b = int(0.7 * Menus.screen_width - Menus.b_menu)
        h = int(0.7 * Menus.screen_height)
        self.canvas_section = QtGui.QPixmap(b, h)
        self.label_canvas = QLabel()
        self.label_canvas.setPixmap(self.canvas_section)
        self.painter_section = QtGui.QPainter(self.canvas_section) 
        font = QFont('Century Gothic', Menus.font_height)
        self.painter_section.setFont(font)

        self.load_display(general_layout=self._general_layout)

        # menu right
        self._layout_menu = QStackedLayout()

        # menu 1 list of objects
        widget_layout_1 = self.load_menu_1()
        self._widget_layout_1 = QWidget()
        self._layout_menu.addWidget(widget_layout_1)
        self._general_layout.addLayout(self._layout_menu)

        widget = QWidget()
        widget.setLayout(self._general_layout)

        # menu 2 (info)
        self._button_back = QPushButton()
        self._label_info = QLabel()
        self._label_info.setFixedWidth(Menus.info_height)
        self._label_info.setFixedWidth(Menus.info_width)
        widget_layout_2 = self.load_menu_2()
        self._layout_menu.addWidget(widget_layout_2)
        self._layout_menu.setCurrentIndex(0)

        self.setCentralWidget(widget)

    def load_menu_2(self) -> QWidget:
        layout_menu_2 = QVBoxLayout()
        widget_layout_2 = QWidget()
        button_back = QPushButton()
        button_back.setFixedWidth(Menus.width_of_buttons)
        button_back.clicked.connect(self.go_back_to_menu_1)
        path = Menus.pictures_menu + "back.png"
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print('No picture', path)
        else:
            button_back.setIcon(pixmap)
            button_back.setIconSize(QSize(Menus.size_of_pictures_in_the_list, Menus.size_of_pictures_in_the_list))
            button_back.setMaximumHeight(Menus.size_of_pictures_in_the_list + 10)

        layout_menu_2.addWidget(button_back)
        layout_menu_2.addWidget(self._label_info)
        widget_layout_2.setLayout(layout_menu_2)

        return widget_layout_2

    def load_display(self, general_layout: QHBoxLayout):
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.label_canvas)
        self.painter_section = QtGui.QPainter(self.canvas_section)

        general_layout.addLayout(display_layout)

    def load_menu_1(self) -> QWidget:
        """menu with list of the objects"""
        layout_menu_1 = QVBoxLayout()
        label_name = QLabel(Menus.name_of_the_program)
        layout_menu_1.addWidget(label_name)
        self.load_objects(layout_menu=layout_menu_1)
        widget_layout_1 = QWidget()
        widget_layout_1.setLayout(layout_menu_1)
        return widget_layout_1

    def go_to_info(self, path: str):
        # load new picture info
        path = Menus.pictures_info + path
        pixmap_info = QPixmap(path)
        if pixmap_info.isNull():
            self._label_info.setText('No picture')
            print('No picture', path)
        else:
            scaled = pixmap_info.scaled(self._label_info.size(),
                                        Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
            self._label_info.setPixmap(scaled)

        self._layout_menu.setCurrentIndex(1)

    def go_back_to_menu_1(self):
        self._layout_menu.setCurrentIndex(0)

    def load_objects(self, layout_menu: QVBoxLayout):
        for line in MenusLines:
            line_i = QHBoxLayout()
            # load picture
            line_i.addWidget(
                get_the_button_for_an_object(
                    path=line.value.pict,
                    name=line.value.name))
            # info
            line_i.addWidget(self.get_info_button(path_for_info=line.value.info))
            layout_menu.addLayout(line_i)

    def info_button_action(self, path_to_the_picture: str):
        self.go_to_info(path=path_to_the_picture)
        print(path_to_the_picture)

    def get_info_button(self, path_for_info: str) -> QPushButton:
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
        info_button.clicked.connect(partial(self.info_button_action, path_for_info))

        return info_button


def get_the_button_for_an_object(path: str, name: str = None) -> QPushButton:
    button_with_ico = QPushButton(name)
    button_with_ico.setFixedWidth(Menus.width_of_buttons)
    path = Menus.pictures_preview + path
    pixmap = QPixmap(path)
    if pixmap.isNull():
        print('No picture', path)
    else:
        button_with_ico.setIcon(pixmap)
        button_with_ico.setIconSize(QSize(Menus.size_of_pictures_in_the_list, Menus.size_of_pictures_in_the_list))
        button_with_ico.setMaximumHeight(Menus.size_of_pictures_in_the_list + 10)
    return button_with_ico
