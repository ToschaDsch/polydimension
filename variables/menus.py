from dataclasses import dataclass



@dataclass
class Menus:
    general_window = None
    screen_window = None
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

    initial_dimension = 4
    label_dimensions = str(initial_dimension) + "d"
    name_of_the_layout_displacement = "displacement"
    name_of_the_layout_rotation = "rotation"

    #paths to resources
    resource_path = "my_resources"
    pictures_path = resource_path + "//" + "pictures"
    pictures_preview = pictures_path + "//preview//"
    pictures_menu = pictures_path + "//menu//"
    pictures_info = pictures_path + "//info//"
