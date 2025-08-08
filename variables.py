from dataclasses import dataclass
from enum import Enum

from PySide6.QtGui import QColor, Qt


@dataclass
class Menus:
    general_window = None
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

    size_of_buttons_menu_2: int = int(b_menu/4-frame) - 10    # menu 2 tools
    frame_menu_2: int = 10
    info_height: int = 800
    info_width: int = b_menu-2*frame
    size_of_pictures_in_the_list: int = 40
    width_of_buttons_menu_1: int = table_1_width - size_of_pictures_in_the_list - 20
    width_of_button_back: int = b_menu-2*frame
    content_margin: int = 1

    label_dimensions = "3d"

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
    carbon = QColor(0, 130, 130)



class MyCoordinates:
    dimensions: int = 3
    angles: list[float] = [0,0,0]
    displacement: list[float] = [0,0,0]

