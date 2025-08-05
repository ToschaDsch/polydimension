from functools import partial

from PySide6 import QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QStackedLayout, \
    QTableWidget

from frontend_classes.class_ToggleButton import ToggleButton
from menu_lines import MenusLines
from frontend_classes.class_ClickableWidget import ClickableWidget
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
        self.table_of_the_elements = QTableWidget()
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

        # menu 3 input
        widget_layout_3 = self.load_menu_3()
        self._layout_menu.addWidget(widget_layout_3)
        self._layout_menu.setCurrentIndex(0)

        self.setCentralWidget(widget)

    def load_menu_3(self) -> QWidget:
        layout_menu_2 = QVBoxLayout()
        widget_layout_2 = QWidget()

        menu_with_icons = self.load_menu_with_icons()
        layout_menu_2.addLayout(menu_with_icons)
        button_back = get_button(function_to_the_button=self.go_back_to_menu_1,
                                 path="back.png", width=Menus.width_of_button_back)
        layout_menu_2.addWidget(button_back)
        widget_layout_2.setLayout(layout_menu_2)

        return widget_layout_2

    def load_menu_with_icons(self) -> QHBoxLayout:
        menu_with_icons = QHBoxLayout()
        button_perspective = ToggleButton(function=self.function_perspective,
                                          image_path_1="without_perspective.png",
                                          image_path_2="with_perspective.png")
        button_web = ToggleButton(function=self.function_web,
                                  image_path_1="without_lines.png",
                                  image_path_2="with_perspective.png")
        button_transparent = ToggleButton(function=self.function_transparent,
                                          image_path_1="transparent.png",
                                          image_path_2="with_perspective.png")
        button_color = ToggleButton(function=self.function_color,
                                    image_path_1="cube_color.png",
                                    image_path_2="with_perspective.png")
        menu_with_icons.addWidget(button_web)
        menu_with_icons.addWidget(button_perspective)
        menu_with_icons.addWidget(button_transparent)
        menu_with_icons.addWidget(button_color)
        return menu_with_icons

    def function_perspective(self):
        print("Perspective")

    def function_web(self):
        print("Web")

    def function_transparent(self):
        print("Transparent")

    def function_color(self):
        print("Color")

    def load_menu_2(self) -> QWidget:
        layout_menu_2 = QVBoxLayout()
        widget_layout_2 = QWidget()
        button_back = get_button(function_to_the_button=self.go_back_to_menu_1,
                                 path="back.png", width=Menus.width_of_button_back)
        layout_menu_2.addWidget(self._label_info)
        layout_menu_2.addWidget(button_back)
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
        layout_menu.addWidget(self.table_of_the_elements)
        self.table_of_the_elements.setRowCount(len(MenusLines))

        self.table_of_the_elements.setColumnCount(2)  # pict, name clickable, info
        self.table_of_the_elements.setFixedWidth(500)
        self.table_of_the_elements.setColumnWidth(0, Menus.width_of_buttons)
        self.table_of_the_elements.setColumnWidth(1, Menus.size_of_pictures_in_the_list)

        for i, line in enumerate(MenusLines):
            # load picture
            button_i: ClickableWidget = self.get_the_button_for_an_object(
                path=line.value.pict,
                name=line.value.name)
            self.table_of_the_elements.setCellWidget(i, 0, button_i)
            # info
            info_button_i = self.get_info_button(path_for_info=line.value.info)
            self.table_of_the_elements.setCellWidget(i, 1, info_button_i)
            self.table_of_the_elements.setRowHeight(i, Menus.size_of_pictures_in_the_list + 5)

    def info_button_action(self, path_to_the_picture: str):
        self.go_to_info(path=path_to_the_picture)

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

    def get_the_button_for_an_object(self, path: str, name: str = None) -> ClickableWidget:
        path = Menus.pictures_preview + path
        button_with_ico = ClickableWidget(text=name, image_path=path)
        button_with_ico.setFixedWidth(Menus.width_of_buttons)
        button_with_ico.clicked.connect(partial(self.click_on_the_list_of_the_objects, name))

        return button_with_ico

    def click_on_the_list_of_the_objects(self, name: str):
        print(name)
        self._layout_menu.setCurrentIndex(2)


def get_button(function_to_the_button, path: str,
               width: int = Menus.size_of_buttons_2, path_for_picture_2: str = None) -> QPushButton:
    button = QPushButton()
    button.setFixedWidth(width)
    button.setFixedHeight(Menus.size_of_buttons_2)
    button.clicked.connect(function_to_the_button)
    path = Menus.pictures_menu + path
    pixmap = QPixmap(path)
    frame = Menus.frame_menu_2
    if pixmap.isNull():
        print('No picture', path)
    else:
        new_size = QSize(button.width() - frame, button.height() - frame)
        scaled = pixmap.scaled(new_size,
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        button.setIcon(scaled)
        button.setIconSize(QSize(width, Menus.size_of_buttons_2))
    return button
