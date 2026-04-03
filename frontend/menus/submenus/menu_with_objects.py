from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QPushButton

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import GoToInfo, ClickOnTheListOfTheObjects
from frontend.frontend_classes.class_ClickableWidget import ClickableWidget
from frontend.menus.menu_lines import MenusLines
from variables.class_state import MyState
from variables.menus import Menus


class MenuWithObjects(QWidget):
    def __init__(self, bus: EventBus, state: MyState, parent=None, ):
        QWidget.__init__(self, parent)
        """menu with list of the objects"""
        self.bus = bus
        self.state = state
        self.table_of_the_elements = QTableWidget()
        layout_menu_1 = QVBoxLayout()
        label_name = QLabel(Menus.name_of_the_program)
        layout_menu_1.addWidget(label_name)
        self.load_objects(layout_menu=layout_menu_1)
        self.setLayout(layout_menu_1)

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
        self.bus.publish(event=GoToInfo(path=path_to_the_picture))

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
        event = ClickOnTheListOfTheObjects(dimensions=line.value.dimensions,
                                            obj=line.value.obj,
                                            size=line.value.size,
                                            dz=line.value.dz)
        button_with_ico.clicked.connect(partial(self.bus.publish, event=event))
        return button_with_ico

