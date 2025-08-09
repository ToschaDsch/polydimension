from functools import partial

from PySide6 import QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QStackedLayout, \
    QTableWidget, QComboBox, QSlider

from frontend_classes.class_ToggleButton import ToggleButton
from menu_lines import MenusLines
from frontend_classes.class_ClickableWidget import ClickableWidget
from single_functions import get_list_of_all_dimensions, correct_global_variables_by_change_dimensions, \
    number_of_displacement_changed, current_displacement_changed, current_rotation_changed, number_of_rotation_changed
from variables import Menus, GraphicRegimes, Transparency, MyCoordinates


class GeneralWindow(QMainWindow):
    def __init__(self, *args):
        super(GeneralWindow, self).__init__()
        self.setWindowTitle(Menus.name_of_the_program)
        b = int(0.5*Menus.screen_width)
        h = int(0.7 * Menus.screen_height)
        self.setFixedWidth(b)
        self._general_layout = QHBoxLayout()
        self._general_layout.setContentsMargins(Menus.frame, Menus.frame, Menus.frame, Menus.frame)

        # variables to calculate

        # load menus
        #   menu_1 (display and menu)
        # display
        b_display = b - Menus.b_menu - 2*Menus.frame
        self.canvas_section = QtGui.QPixmap(b_display, h-2*Menus.frame)
        self.label_canvas = QLabel()
        self.label_canvas.setFixedSize(self.canvas_section.size())
        self.label_canvas.setPixmap(self.canvas_section)
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
        self._general_layout.addLayout(self._layout_menu)
        self._layout_menu.addWidget(widget_layout_1)

        widget = QWidget()
        widget.setLayout(self._general_layout)

        # menu 2 (info)
        self._label_info = QLabel()
        self._label_info.setFixedWidth(Menus.info_height)
        self._label_info.setFixedWidth(Menus.info_width)
        widget_layout_2 = self.load_menu_2()
        self._layout_menu.addWidget(widget_layout_2)

        # menu 3 input
        self.button_minus = QPushButton('-')
        self.label_dimensions = QLabel(Menus.label_dimensions)
        self.combobox_displacement = QComboBox()
        self.combobox_rotation = QComboBox()
        self.slider_displacement = QSlider(Qt.Orientation.Horizontal)
        self.slider_rotation = QSlider(Qt.Orientation.Horizontal)
        widget_layout_3 = self.load_menu_3()
        self._layout_menu.addWidget(widget_layout_3)
        self._layout_menu.setCurrentIndex(0)

        self.setCentralWidget(widget)



    def load_menu_3(self) -> QWidget:
        layout_menu_2 = QVBoxLayout()
        layout_menu_2.addWidget(QLabel(Menus.name_ot_menu_3))
        widget_layout_2 = QWidget()

        menu_with_icons = self.load_menu_with_icons()
        layout_menu_2.addLayout(menu_with_icons)
        button_back = get_button(function_to_the_button=self.go_back_to_menu_1,
                                 path="back.png", width=Menus.width_of_button_back,
                                 height=Menus.height_of_button_back)
        menu_with_dimensions = self.load_buttons_with_dimensions()
        layout_menu_2.addLayout(menu_with_dimensions)

        list_of_displacements, list_of_rotations = get_list_of_all_dimensions(number_of_dimensions=MyCoordinates.dimensions)
        layout_displacement = self.get_sub_layout_to_change_coordinate(
            name_of_the_layout=Menus.name_of_the_layout_displacement,
            list_of_dimensions=list_of_displacements,
            combobox=self.combobox_displacement,
            slider=self.slider_displacement,
            function_to_the_combobox=number_of_displacement_changed,
            function_to_the_slider=current_displacement_changed)
        layout_rotation = self.get_sub_layout_to_change_coordinate(
            name_of_the_layout=Menus.name_of_the_layout_rotation,
            list_of_dimensions=list_of_rotations,
            combobox=self.combobox_rotation,
            slider=self.slider_rotation,
            function_to_the_combobox=number_of_rotation_changed,
            function_to_the_slider=current_rotation_changed)
        layout_menu_2.addLayout(layout_displacement)
        layout_menu_2.addLayout(layout_rotation)


        # separator
        separator = QLabel()
        separator.setFixedHeight(Menus.separators_height)
        layout_menu_2.addWidget(separator)

        # button back
        layout_menu_2.addWidget(button_back)

        widget_layout_2.setLayout(layout_menu_2)

        return widget_layout_2

    def load_buttons_with_dimensions(self) -> QHBoxLayout:
        layout_dimensions = QHBoxLayout()

        self.button_minus.setFixedHeight(Menus.size_of_pictures_in_the_list)
        self.button_minus.setEnabled(False)
        self.button_minus.clicked.connect(self.minus_dimensions)
        layout_dimensions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_dimensions.setFixedHeight(Menus.size_of_pictures_in_the_list)
        button_plus = QPushButton('+')
        button_plus.setFixedHeight(Menus.size_of_pictures_in_the_list)
        layout_dimensions.addWidget(self.button_minus)
        layout_dimensions.addWidget(self.label_dimensions)
        layout_dimensions.addWidget(button_plus)
        button_plus.clicked.connect(self.plus_dimensions)
        return layout_dimensions

    def minus_dimensions(self):
        if MyCoordinates.dimensions == 4:
            self.button_minus.setEnabled(False)
        MyCoordinates.dimensions -= 1
        self.write_dimensions_in_the_label(new_dimensions=MyCoordinates.dimensions)

    def plus_dimensions(self):
        MyCoordinates.dimensions += 1
        self.button_minus.setEnabled(True)
        self.write_dimensions_in_the_label(new_dimensions=MyCoordinates.dimensions)


    def write_dimensions_in_the_label(self, new_dimensions: int):
        # correct the label
        new_string = str(str(new_dimensions) + "d")
        self.label_dimensions.setText(new_string)

        # correct combo-boxes
        list_of_displacements, list_of_rotations = get_list_of_all_dimensions(number_of_dimensions=new_dimensions)
        for combobox, list_of_items in ((self.combobox_displacement, list_of_displacements),(self.combobox_rotation, list_of_rotations)):
            combobox.clear()
            for key in list_of_items:
                combobox.addItem(key)
            combobox.setCurrentIndex(0)

        # correct global variables
        correct_global_variables_by_change_dimensions(dimensions=new_dimensions,
                                                      list_of_displacements=list_of_displacements,
                                                      list_of_rotations=list_of_rotations)



    def load_menu_with_icons(self) -> QHBoxLayout:
        menu_with_icons = QHBoxLayout()
        button_perspective = ToggleButton(function=self.function_perspective,
                                          list_of_paths_for_images=["without_perspective.png",
                                                                    "with_perspective.png"])
        button_web = ToggleButton(function=self.function_web,
                                  list_of_paths_for_images=["without_lines.png",
                                                            "with_lines.png"])
        button_transparent = ToggleButton(function=self.function_transparent,
                                          list_of_paths_for_images=["with_perspective.png",
                                                                    "sceleton.png",
                                                                    "transparent.png",
                                                                    ])
        button_color = ToggleButton(function=self.function_color,
                                    list_of_paths_for_images=["cube_color.png",
                                                                "with_lines.png"])
        menu_with_icons.addWidget(button_web)
        menu_with_icons.addWidget(button_perspective)
        menu_with_icons.addWidget(button_transparent)
        menu_with_icons.addWidget(button_color)
        return menu_with_icons

    def function_perspective(self, i: int):
        GraphicRegimes.perspective = bool(i)
        print("Perspective", i, GraphicRegimes.perspective)

    def function_web(self, i: int):
        GraphicRegimes.web = bool(i)
        print("Web", i, GraphicRegimes.web)

    def function_transparent(self, i: int):
        GraphicRegimes.transparent = list(Transparency)[i]
        print("Transparent", i, GraphicRegimes.transparent)

    def function_color(self, i: int):
        GraphicRegimes.color = bool(i)
        print("Color", i, GraphicRegimes.color)

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
        button_with_ico.clicked.connect(partial(self.click_on_the_list_of_the_objects, line.value.dimensions))

        return button_with_ico

    def click_on_the_list_of_the_objects(self, dimensions: str):
        self._layout_menu.setCurrentIndex(2)

    def get_sub_layout_to_change_coordinate(self, name_of_the_layout: str,
                                            combobox: QComboBox,
                                            list_of_dimensions: list[str]=None,
                                            slider: QSlider=None,
                                            function_to_the_combobox=None,
                                            function_to_the_slider=None) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name_of_the_layout))
        # dropbox
        if list_of_dimensions is None:
            list_of_dimensions: list[str] = ["x", "y", "z", "x1"]
        combobox.clear()
        for key in list_of_dimensions:
            combobox.addItem(key)
        combobox.setCurrentIndex(0)
        combobox.currentIndexChanged.connect(function_to_the_combobox)
        layout.addWidget(combobox)
        # slider
        slider.setMinimum(-180)
        slider.setMaximum(180)
        slider.setSingleStep(1)
        slider.setValue(0)
        slider.setSliderPosition(0)
        slider.valueChanged.connect(function_to_the_slider)


        layout.addWidget(slider)


        return layout


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
