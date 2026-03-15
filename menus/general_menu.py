from functools import partial
from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QStackedLayout, \
    QTableWidget

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawAllPrimitives, RecalculateAndDrawAllPrimitives
from graphic.class_draw import DrawAll
from graphic.class_screen_window import ScreenWindow
from menus.menu_lines import MenusLines
from frontend_classes.class_ClickableWidget import ClickableWidget
from menus.submenus.menu_3_input import Menu3Input
from objects.cube_3d import Cube3d
from variables.menus import Menus
from variables.geometry_var import MyCoordinates, CoordinatesScreen


class GeneralWindow(QMainWindow):
    def __init__(self, *args):
        super(GeneralWindow, self).__init__()
        self.setWindowTitle(Menus.name_of_the_program)
        b = int(0.5 * Menus.window_width)
        h = int(0.7 * Menus.window_height)
        self.setFixedWidth(b)
        self.setFixedHeight(h)
        self._general_layout = QHBoxLayout()
        self._general_layout.setContentsMargins(Menus.frame, Menus.frame, Menus.frame, Menus.frame)

        # variables to calculate
        self.bus = EventBus()
        self.bus.register(self)
        # load menus
        #   menu_1 (display and menu)
        # display
        b_display = b - Menus.b_menu - 2 * Menus.frame
        h_display = h - 2 * Menus.frame
        Menus.display_width = b_display
        Menus.display_height = h_display
        self.screen_window = ScreenWindow(bus=self.bus)
        self.screen_window.setFixedWidth(Menus.display_width)
        self.screen_window.setFixedHeight(Menus.display_height)
        self.load_display(general_layout=self._general_layout)

        # menu right
        self._layout_menu = QStackedLayout()

        # menu 1 list of objects
        self.table_of_the_elements = QTableWidget()
        widget_layout_1 = self.load_menu_1()
        self._general_layout.addLayout(self._layout_menu)
        self._layout_menu.addWidget(widget_layout_1)

        widget = QWidget()
        widget.setLayout(self._general_layout)

        # menu 2 (info)
        self._label_info = QLabel()
        self._label_info.setFixedHeight(Menus.info_height)
        self._label_info.setFixedWidth(Menus.info_width)
        widget_layout_2 = self.load_menu_2()
        self._layout_menu.addWidget(widget_layout_2)

        # menu 3 input
        button_back = get_button(function_to_the_button=self.go_back_to_menu_1,
                                 path="back.png", width=Menus.width_of_button_back,
                                 height=Menus.height_of_button_back)
        widget_layout_3 = Menu3Input(button_back=button_back, bus=self.bus) #self.load_menu_3()
        self._layout_menu.addWidget(widget_layout_3)
        self._layout_menu.setCurrentIndex(0)

        # draw the object
        size = 1
        self.my_object = Cube3d(size=1)
        self.animation = DrawAll(draw_object=self.my_object, initial_dimensions=4, size=size, bus=self.bus)
        self.setCentralWidget(widget)
        event = RecalculateAndDrawAllPrimitives(angles=MyCoordinates.angles,
                                                dxi=MyCoordinates.displacement,
                                                scale=CoordinatesScreen.scale)
        self.animation.draw_all(event=event)


    def load_menu_2(self) -> QWidget:
        layout_menu_2 = QVBoxLayout()
        widget_layout_2 = QWidget()
        button_back = get_button(function_to_the_button=self.go_back_to_menu_1,
                                 path="back.png", width=Menus.width_of_button_back,
                                 height=Menus.height_of_button_back)
        layout_menu_2.addWidget(self._label_info)
        layout_menu_2.addWidget(button_back)
        widget_layout_2.setLayout(layout_menu_2)

        return widget_layout_2

    def load_display(self, general_layout: QHBoxLayout):
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.screen_window)

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
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            self._label_info.setPixmap(scaled)

        self._layout_menu.setCurrentIndex(1)

    def go_back_to_menu_1(self):
        self._layout_menu.setCurrentIndex(0)

    def load_objects(self, layout_menu: QVBoxLayout):
        layout_menu.addWidget(self.table_of_the_elements)
        self.table_of_the_elements.setRowCount(len(MenusLines))

        self.table_of_the_elements.setColumnCount(2)  # pict, name clickable, info
        self.table_of_the_elements.setFixedWidth(Menus.table_1_width)
        self.table_of_the_elements.setColumnWidth(0, Menus.width_of_buttons_menu_1)
        self.table_of_the_elements.setColumnWidth(1, Menus.size_of_pictures_in_the_list)

        for i, line in enumerate(MenusLines):
            # load picture
            button_i: ClickableWidget = self.get_the_button_for_an_object(line=line)
            self.table_of_the_elements.setCellWidget(i, 0, button_i)
            # info
            info_button_i = self.get_info_button(path_for_info=line.value.info)
            self.table_of_the_elements.setCellWidget(i, 1, info_button_i)
            self.table_of_the_elements.setRowHeight(i, Menus.size_of_pictures_in_the_list)

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
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            info_button.setIcon(scaled)
        info_button.clicked.connect(partial(self.info_button_action, path_for_info))

        return info_button

    def get_the_button_for_an_object(self, line: MenusLines) -> ClickableWidget:
        path = Menus.pictures_preview + line.value.pict
        button_with_ico = ClickableWidget(text=line.value.name, image_path=path)
        button_with_ico.setFixedWidth(Menus.width_of_buttons_menu_1)
        button_with_ico.clicked.connect(partial(self.click_on_the_list_of_the_objects, line.value.dimensions,
                                                line.value.obj, line.value.size))

        return button_with_ico

    def click_on_the_list_of_the_objects(self, dimensions: int, obj: Callable, size: float):
        self._layout_menu.setCurrentIndex(2)
        self.animation.new_object(obj=obj, dimensions=dimensions, size=size)
        self.screen_window.draw_all(event=DrawAllPrimitives())



def get_button(function_to_the_button, path: str,
               width: int = Menus.size_of_buttons_menu_3,
               height: int = Menus.size_of_buttons_menu_3) -> QPushButton:
    button = QPushButton()
    button.setFixedWidth(width)
    button.setFixedHeight(height)
    button.clicked.connect(function_to_the_button)
    path = Menus.pictures_menu + path
    pixmap = QPixmap(path)
    frame = Menus.frame_menu_3
    if pixmap.isNull():
        print('No picture', path)
    else:
        new_size = QSize(button.width() - frame, button.height() - frame)
        scaled = pixmap.scaled(new_size,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        button.setIcon(scaled)
        button.setIconSize(QSize(width, Menus.size_of_buttons_menu_3))
    return button
