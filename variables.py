from dataclasses import dataclass

from PySide6.QtGui import QColor, Qt


@dataclass
class Menus:
    general_window = None
    name_of_the_program = 'polydimension'
    screen_width: int = 100
    screen_height: int = 100

    font_height: int = 15

    table_insert: bool = False

    b_menu: int = 300
    size_of_buttons_2: int = 30
    width_of_buttons: int = 300
    width_of_button_back: int = 200

    info_height: int = 800
    info_width: int = b_menu
    size_of_pictures_in_the_list: int = 40

    resource_path = "my_resources"
    pictures_path = resource_path + "//" + "pictures"
    pictures_preview = pictures_path + "//preview//"
    pictures_menu = pictures_path + "//menu//"
    pictures_info = pictures_path + "//info//"


@dataclass
class InitiationValues:
    normal_force = 0
    eccentricity = 0  # for normal force
    n = 20
    d_e = 100
    d_n = 0.1


@dataclass
class PenThicknessToDraw:
    boards = 2
    axis = 1
    steel_section = 1
    graph_diagram = 1
    addition_lines_for_diagram = 1
    stress_concrete = 1
    stress_steel = 5
    strains_section = 1


@dataclass
class MyColors:
    carbon = QColor(0, 130, 130)
    carbon_stress = QColor(0, 180, 180)
    concrete = QColor(150, 150, 150)
    concrete_diagram = QColor(150, 0, 0)
    concrete_diagram_polygon = QColor(150, 0, 0, 120)
    concrete_boards = QColor(100, 100, 100)
    normal_force = QColor(100, 200, 0)
    axis = QColor(100, 100, 100)
    addition_lines = QColor(100, 100, 100)
    strains_section = QColor(200, 200, 200)
    label_slider_lines = QColor(100, 250, 0)
    label_slider_background = Qt.GlobalColor.lightGray


@dataclass
class TypeOfDiagram:
    concrete_linear = 'Beton linear'
    concrete_nonlinear = 'Beton nonlinear'
    steel_linear = 'Stahl linear'
    steel_nonlinear = 'Stahl nonlinear'


@dataclass
class MenuNames:
    concrete_diagram = 'Diagramm für Beton'
    steel_diagram = 'Diagramm für Stahl'
    label_n_top = 'das kleinste Teil des Betonsegments wird'
    label_n_for = 'auf'
    label_n_after = 'verteilt'
    recalculate = 'Berechnen'
    convergence = 'Konvergenz - '
    n_de_info = 'Diagramme werden auf'
    explanation_normal_force = 'Zug ist positiv'
    label_concrete = "Beton"
    label_steel = "Bewehrung"
    strengthening_concrete = "Verstärkung mit Beton oben"
    strengthening_carbon = "Verstärkung mit carbon unten"

@dataclass
class Names:
    axes_concrete = ('εc', 'σc')
    axes_steel = ('εs', 'σs')