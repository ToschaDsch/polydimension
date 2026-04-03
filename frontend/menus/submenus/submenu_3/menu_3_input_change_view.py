from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawWithNormals, DrawWithPoints, DrawWithPerspective, DrawWithWeb, \
    DrawTransparent, DrawColorful
from frontend.frontend_classes.class_ToggleButton import ToggleButton
from variables.class_state import MyState


class ChangeView(QWidget):
    def __init__(self, state: MyState, bus: EventBus, parent=None):
        super(ChangeView, self).__init__(parent)
        self.state = state
        self.bus = bus
        menu_with_icons = QVBoxLayout()
        menu_with_icons_0 = QHBoxLayout()
        menu_with_icons_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_perspective = ToggleButton(function=self.function_perspective,
                                          list_of_paths_for_images=["without_perspective.png",
                                                                    "with_perspective.png"],
                                          name="perspective")
        button_web = ToggleButton(function=self.function_web,
                                  list_of_paths_for_images=["without_lines.png",
                                                            "with_lines.png"],
                                  name="web")
        button_transparent = ToggleButton(function=self.function_transparent,
                                          list_of_paths_for_images=["with_perspective.png",
                                                                    "sceleton.png",
                                                                    "transparent.png",
                                                                    ],
                                          name="transparent")
        button_color = ToggleButton(function=self.function_color,
                                    list_of_paths_for_images=["cube_color.png",
                                                              "with_lines.png"],
                                    name="color")

        menu_with_icons_0.addWidget(button_web)
        menu_with_icons_0.addWidget(button_perspective)
        menu_with_icons_0.addWidget(button_transparent)
        menu_with_icons_0.addWidget(button_color)
        menu_with_icons_1 = QHBoxLayout()
        button_with_points = ToggleButton(function=self.function_show_with_points,
                                          list_of_paths_for_images=["with_points.png",
                                                                    "with_perspective.png"],
                                          name="points")
        menu_with_icons_1.addWidget(button_with_points)
        button_with_normals = ToggleButton(function=self.function_show_with_normals,
                                           list_of_paths_for_images=["with_normals.png",
                                                                     "with_perspective.png"],
                                           name="normals")
        menu_with_icons_1.addWidget(button_with_normals)

        menu_with_icons.addLayout(menu_with_icons_0)
        menu_with_icons.addLayout(menu_with_icons_1)
        self.setLayout(menu_with_icons)

    def function_show_with_normals(self, i: int):
        self.bus.publish(event=DrawWithNormals(with_normals=bool(i)))

    def function_show_with_points(self, i: int):
        self.bus.publish(event=DrawWithPoints(with_points=bool(i)))

    def function_perspective(self, i: int):
        self.bus.publish(event=DrawWithPerspective(with_perspective=bool(not i)))

    def function_web(self, i: int):
        self.bus.publish(event=DrawWithWeb(with_web=bool(not i)))

    def function_transparent(self, i: int):
        self.bus.publish(event=DrawTransparent(transparent=bool(i)))

    def function_color(self, i: int):
        self.bus.publish(event=DrawColorful(colorful=bool(i)))