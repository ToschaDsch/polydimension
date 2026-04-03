from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from frontend.event_bus.event_bus import EventBus
from frontend.menus.submenus.submenu_3.menu_3_input_change_view import ChangeView
from frontend.menus.submenus.submenu_3.menu_3_shift_and_rotate import SchiftAndRotate
from variables.class_state import MyState
from variables.menus import Menus


class Menu3Input(QWidget):
    def __init__(self, bus: EventBus, state: MyState, button_back: QPushButton, parent=None):
        super().__init__(parent)
        layout_menu_2 = QVBoxLayout()
        layout_menu_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_menu_2.addWidget(QLabel(Menus.name_ot_menu_3))  # name of the menu

        self.state: MyState = state
        self.bus = bus

        # menu with options (perspective at cetera)
        menu_with_icons = ChangeView(state=self.state, bus=self.bus)
        layout_menu_2.addWidget(menu_with_icons)

        separator = QLabel()
        separator.setFixedHeight(100)
        layout_menu_2.addWidget(separator)

        # dimensions, shift, rotate
        menu_with_dimensions_shift_rotate = SchiftAndRotate(state=state, bus=bus)
        layout_menu_2.addWidget(menu_with_dimensions_shift_rotate)

        # button back
        layout_menu_2.addWidget(button_back)

        self.setLayout(layout_menu_2)


