import math

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSlider, QHBoxLayout

from frontend.event_bus.decorators import subscribe
from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawWithPoints, DrawWithPerspective, DrawWithWeb, DrawTransparent, DrawColorful, \
    ShiftTheSliderRotation, ShiftTheSliderDisplacement, RecalculateAndDrawAllPrimitives
from frontend.frontend_classes.class_ToggleButton import ToggleButton
from frontend.menus.single_functions import correct_global_variables_by_change_dimensions, get_list_of_all_dimensions, \
    get_sub_layout_to_change_coordinate
from variables.class_state import MyState
from variables.menus import Menus


class Menu3Input(QWidget):
    def __init__(self, bus: EventBus, state: MyState, button_back: QPushButton, parent=None):
        super().__init__(parent)
        layout_menu_2 = QVBoxLayout()
        layout_menu_2.addWidget(QLabel(Menus.name_ot_menu_3))  # name of the menu

        self.state: MyState = state
        self.bus = bus
        self.bus.register(self)
        #variables
        self.button_minus = QPushButton('-')
        self.label_dimensions = QLabel(Menus.label_dimensions)
        self.combobox_displacement = QComboBox()
        self.combobox_rotation = QComboBox()
        self.slider_displacement = QSlider(Qt.Orientation.Horizontal)
        self.slider_rotation = QSlider(Qt.Orientation.Horizontal)

        # menu with options (perspective at cetera)
        menu_with_icons = self.load_menu_with_icons()
        layout_menu_2.addLayout(menu_with_icons)
        # dimensions
        menu_with_dimensions = self.load_buttons_with_dimensions()
        layout_menu_2.addLayout(menu_with_dimensions)
        # sliders
        layout_displacement, layout_rotation = self.get_layout_displacement_and_rotation()
        layout_menu_2.addLayout(layout_displacement)
        layout_menu_2.addLayout(layout_rotation)

        # separator
        separator = QLabel()
        separator.setFixedHeight(Menus.separators_height)
        layout_menu_2.addWidget(separator)

        # button back
        layout_menu_2.addWidget(button_back)

        self.setLayout(layout_menu_2)


    def get_layout_displacement_and_rotation(self) -> tuple[QVBoxLayout, QVBoxLayout]:
        list_of_displacements, list_of_rotations = get_list_of_all_dimensions(
            number_of_dimensions=self.state.MyCoordinates.dimensions)
        layout_displacement = get_sub_layout_to_change_coordinate(
            name_of_the_layout=Menus.name_of_the_layout_displacement,
            list_of_dimensions=list_of_displacements,
            combobox=self.combobox_displacement,
            slider=self.slider_displacement,
            function_to_the_combobox=self.number_of_displacement_changed,
            function_to_the_slider=self.current_displacement_changed,
            init_position_of_the_slider=int(self.state.MyCoordinates.displacement[0]))
        layout_rotation = get_sub_layout_to_change_coordinate(
            name_of_the_layout=Menus.name_of_the_layout_rotation,
            list_of_dimensions=list_of_rotations,
            combobox=self.combobox_rotation,
            slider=self.slider_rotation,
            function_to_the_combobox=self.number_of_rotation_changed,
            function_to_the_slider=self.current_rotation_changed,
            init_position_of_the_slider=int(self.state.MyCoordinates.angles[0] * 180 / math.pi))
        return layout_displacement, layout_rotation

    def number_of_displacement_changed(self, number_of_displacement: int = 0) -> None:
        self.state.MyCoordinates.current_displacement = number_of_displacement
        current_displacement = self.state.MyCoordinates.displacement[number_of_displacement]
        self.slider_displacement.setSliderPosition(int(current_displacement))


    def number_of_rotation_changed(self, number_of_rotations: int = 0) -> None:
        self.state.MyCoordinates.current_rotation = number_of_rotations
        current_rotation = self.state.MyCoordinates.angles[number_of_rotations]
        self.slider_rotation.setSliderPosition(int(current_rotation*180/math.pi))


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
        if self.state.MyCoordinates.dimensions == 4:
            self.button_minus.setEnabled(False)
        self.state.MyCoordinates.dimensions -= 1
        self.write_dimensions_in_the_label(new_dimensions=self.state.MyCoordinates.dimensions)

    def plus_dimensions(self):
        self.state.MyCoordinates.dimensions += 1
        self.button_minus.setEnabled(True)
        self.write_dimensions_in_the_label(new_dimensions=self.state.MyCoordinates.dimensions)


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
                                                      list_of_rotations=list_of_rotations, state= self.state)

    @subscribe
    def shift_the_slider_displacement(self, event: ShiftTheSliderDisplacement) -> None:
        self.slider_displacement.setSliderPosition(event.shift)

    @subscribe
    def shift_the_slider_rotation(self, event: ShiftTheSliderRotation) -> None:
        """
        :param event:
        :return None:
        """
        self.slider_rotation.setSliderPosition(event.angle)

    def load_menu_with_icons(self) -> QVBoxLayout:
        menu_with_icons = QVBoxLayout()
        menu_with_icons_0 = QHBoxLayout()
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

        menu_with_icons_0.addWidget(button_web)
        menu_with_icons_0.addWidget(button_perspective)
        menu_with_icons_0.addWidget(button_transparent)
        menu_with_icons_0.addWidget(button_color)
        menu_with_icons_1 = QHBoxLayout()
        button_with_points = ToggleButton(function=self.function_show_with_points,
                                          list_of_paths_for_images=["with_points.png",
                                                                    "with_perspective.png"])
        menu_with_icons_1.addWidget(button_with_points)
        menu_with_icons.addLayout(menu_with_icons_0)
        menu_with_icons.addLayout(menu_with_icons_1)
        return menu_with_icons

    def function_show_with_points(self, i: int):
        self.bus.publish(event=DrawWithPoints(with_points=bool(i)))

    def function_perspective(self, i: int):
        self.bus.publish(event=DrawWithPerspective(with_perspective=bool(i)))

    def function_web(self, i: int):
        self.bus.publish(event=DrawWithWeb(with_web=bool(i)))

    def function_transparent(self, i: int):
        self.bus.publish(event=DrawTransparent(transparent=bool(i)))

    def function_color(self, i: int):
        self.bus.publish(event=DrawColorful(colorful=bool(i)))

    def current_displacement_changed(self, displacement: int = 0) -> None:
        self.state.MyCoordinates.displacement[self.state.MyCoordinates.current_displacement] = displacement
        self.bus.publish(RecalculateAndDrawAllPrimitives(dxi=self.state.MyCoordinates.displacement))

    def current_rotation_changed(self, rotations: int = 0) -> None:
        """
        :param rotations: angle in grad -180 +180:
        :return None:
        """
        self.state.MyCoordinates.angles[self.state.MyCoordinates.current_rotation] = rotations * math.pi / 180
        self.bus.publish(RecalculateAndDrawAllPrimitives(angles=self.state.MyCoordinates.angles))