import math

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QSlider, QVBoxLayout, QHBoxLayout

from frontend.event_bus.decorators import subscribe
from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import RecalculateAndDrawAllPrimitives, ShiftTheSliderRotation, \
    ShiftTheSliderDisplacement
from frontend.menus.single_functions import get_list_of_all_dimensions, get_sub_layout_to_change_coordinate, \
    correct_global_variables_by_change_dimensions
from variables.class_state import MyState
from variables.menus import Menus


class SchiftAndRotate(QWidget):
    def __init__(self, state: MyState, bus: EventBus, parent=None):
        super(SchiftAndRotate, self).__init__(parent)
        self.state = state
        self.bus = bus

        # variables
        layout = QVBoxLayout()
        self.button_minus = QPushButton('-')
        self.label_dimensions = QLabel(Menus.label_dimensions)
        self.combobox_displacement = QComboBox()
        self.combobox_rotation = QComboBox()
        self.slider_displacement = QSlider(Qt.Orientation.Horizontal)
        self.slider_rotation = QSlider(Qt.Orientation.Horizontal)


        # load menus
        layout.addLayout(self.load_buttons_with_dimensions())
        for menus_input in self.get_layout_displacement_and_rotation():
            layout.addLayout(menus_input)

        self.setLayout(layout)


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