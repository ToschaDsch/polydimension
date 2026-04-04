
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout

from frontend.event_bus.decorators import subscribe
from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import RecalculateAndDrawAllPrimitives, GoToInfo, DrawAllPrimitives, \
    ClickOnTheListOfTheObjects
from frontend.graphic.class_draw import DrawAll
from frontend.graphic.class_screen_window import ScreenWindow
from frontend.menus.single_functions import get_button
from frontend.menus.submenus.menu_3_input import Menu3Input
from frontend.menus.submenus.menu_1_table_with_objects import MenuWithObjects
from variables.class_state import MyState
from variables.menus import Menus


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
        self.state = MyState()
        self.bus.register(self)

        # load menus
        #   menu_1 (display and menu)
        # display
        self.screen_window = ScreenWindow(bus=self.bus, state=self.state, b=b, h=h)
        self._general_layout.addWidget(self.screen_window)

        # menu right
        self._layout_menu = QStackedLayout()
        self._general_layout.addLayout(self._layout_menu)

        # menu 1 list of objects
        widget_layout_1 = MenuWithObjects(state=self.state, bus=self.bus)
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
        widget_layout_3 = Menu3Input(button_back=button_back, bus=self.bus, state=self.state) #self.load_menu_3()
        self._layout_menu.addWidget(widget_layout_3)
        self._layout_menu.setCurrentIndex(0)

        # draw the object
        size = 1

        self.animation = DrawAll(initial_dimensions=4, size=size,
                                 bus=self.bus, state=self.state)
        self.setCentralWidget(widget)
        event = RecalculateAndDrawAllPrimitives(angles=self.state.MyCoordinates.angles,
                                                dxi=self.state.MyCoordinates.displacement,
                                                scale=self.state.CoordinatesScreen.scale)
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

    @subscribe
    def go_to_info(self, event: GoToInfo):
        # load new picture info
        path = Menus.pictures_info + event.path
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
        self.bus.publish(event=RecalculateAndDrawAllPrimitives())

    def go_back_to_menu_1(self):
        self._layout_menu.setCurrentIndex(0)
        self.animation.draw_all()

    @subscribe
    def click_on_the_list_of_the_objects(self, event: ClickOnTheListOfTheObjects):
        self._layout_menu.setCurrentIndex(2)
        self.animation.new_object(obj=event.obj, dimensions=event.dimensions, size=event.size, dz=event.dz)
        self.screen_window.draw_all(event=DrawAllPrimitives())






