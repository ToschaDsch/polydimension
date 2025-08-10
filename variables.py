from dataclasses import dataclass
from enum import Enum
from typing import Any

from PySide6.QtGui import QColor


class MyCoordinates:
    dimensions: int = 4
    angles: list[int] = [1, 2, 3, 4, 4, 5, 6]
    displacement: list[int] = [1, 2, 3, 4]
    list_of_displacements: list[str] = ["x", "y", "z", "x1"]
    list_of_rotations: list[str] = ["x_y", "x_z", "x_x1", "y_z", "y_x1", "z_x1"]
    current_displacement: int = 0 # x
    current_rotation: int = 0 # xy

class CoordinatesScreen:
    dx_dy = 0, 0
    df_dj = 0, 0

@dataclass
class Menus:
    general_window = None
    animation = None
    name_of_the_program = 'polydimension'
    screen_width: int = 100
    screen_height: int = 100
    frame: int = 10
    font_height: int = 15

    table_insert: bool = False

    b_menu: int = 300
    table_1_width: int = b_menu - 2*frame
    table_1_height: int = 100
    table_2_width: int = 100
    # menu 1
    size_of_pictures_in_the_list: int = 40
    width_of_buttons_menu_1: int = table_1_width - size_of_pictures_in_the_list - 20

    # menu 2 info
    info_height: int = 800
    info_width: int = b_menu - 2 * frame

    # menu 3
    name_ot_menu_3 = "displace and rotate the object"
    size_of_buttons_menu_3: int = int(b_menu / 4 - frame) - 10    # menu 2 tools
    frame_menu_3: int = 10
    separators_height: int = 300


    width_of_button_back: int = b_menu-2*frame
    height_of_button_back: int = 35
    content_margin: int = 1

    label_dimensions = str(MyCoordinates.dimensions) + "d"
    name_of_the_layout_displacement = "displacement"
    name_of_the_layout_rotation = "rotation"

    #paths to resources
    resource_path = "my_resources"
    pictures_path = resource_path + "//" + "pictures"
    pictures_preview = pictures_path + "//preview//"
    pictures_menu = pictures_path + "//menu//"
    pictures_info = pictures_path + "//info//"

class Transparency(Enum):
    transparent = 0
    full = 1
    sceleton = 2

@dataclass
class GraphicRegimes:
    perspective: bool = True
    web: bool = True
    transparency: str = Transparency.transparent
    color: bool = False


@dataclass
class PenThicknessToDraw:
    boards = 2


@dataclass
class MyColors:
    web = QColor(0, 0, 0)
    general_screen: QColor = QColor("#000000")
    carbon = QColor(0, 130, 130)


@dataclass
class TypeOfTheObjects:
    dotted = 'dotted'
    axes = 'axes'
    normal = 'normal'
    selected = 'selected'
    line = 'Line'
    light_line = 'LightLine'
    surface = 'Surface'
    temporary_surface = 'temporary_surface'
    light_surface = 'LightSurface'
    light_surface_of_a_combine_beam = "light_surface_of_a_combine_beam"
    text = 'text'
    color = 'color'
    point = 'point'

class ObjectToDraw:
    def __init__(self, self_object: Any, type_of: str = 'normal', color: QColor = QColor(50, 50, 50), text: str = '',
                 type_of_the_objects: str = TypeOfTheObjects.line):
        self.self_object = self_object
        self.type_of: str = type_of
        self.color: QColor = color
        self.text: str = text
        self.type_of_the_objects = type_of_the_objects

