import itertools
import math
import xml.etree.ElementTree as et_
import json
import ast

import numpy as np
from PySide6.QtWidgets import QComboBox, QSlider, QVBoxLayout, QLabel

from variables.geometry_var import MyCoordinates
from variables.menus import Menus


def get_list_of_all_dimensions(number_of_dimensions: int = 4) -> tuple[list[str], list[str]]:
    """

    :param number_of_dimensions: 3d-nd
    :return: list of dimensions ("x", "y", "z", "x1) +
            + list of rotations ("x_y", "x_z", "x_x1", "y_z", "y_x1", "z_x1")
    """
    displacements: list[str] = ["x", "y", "z"]
    dn = number_of_dimensions - 3
    d_list = ["x"+str(i+1) for i in range(dn)]
    displacements.extend(d_list)


    rotations: list[str] = [str(x).replace("'",'') for x in itertools.combinations(displacements, 2)]

    return displacements, rotations

def correct_global_variables_by_change_dimensions(dimensions: int = 4,
                                                  list_of_displacements: list[str] = None,
                                                  list_of_rotations: list[str] = None) -> None:
    MyCoordinates.list_of_displacements = list_of_displacements
    MyCoordinates.list_of_rotations = list_of_rotations
    MyCoordinates.current_displacement = 0
    MyCoordinates.current_rotation = 0

    dn = len(MyCoordinates.list_of_rotations) - len(list(MyCoordinates.angles))
    if MyCoordinates.dimensions > len(MyCoordinates.displacement):  # append new coordinates
        np.append(MyCoordinates.displacement, 0.0)
        for i in range(dn):
            np.append(MyCoordinates.angles, 0.0)
    else:           # reduce coordinates
        np.delete(MyCoordinates.displacement, -1)
        for i in range(-dn):
            np.delete(MyCoordinates.angles, -1)




def current_displacement_changed(displacement: int = 0) -> None:
    MyCoordinates.displacement[MyCoordinates.current_displacement] = displacement
    Menus.animation.draw_all(dxi=MyCoordinates.displacement, angles=MyCoordinates.angles)
    Menus.screen_window.draw_all()

def current_rotation_changed(rotations: int = 0) -> None:
    """
    :param rotations: angle in grad -180 +180:
    :return None:
    """
    MyCoordinates.angles[MyCoordinates.current_rotation] = rotations*math.pi/180
    Menus.animation.draw_all(dxi=MyCoordinates.displacement, angles=MyCoordinates.angles)
    Menus.screen_window.draw_all()


def get_sub_layout_to_change_coordinate(name_of_the_layout: str,
                                        combobox: QComboBox,
                                        list_of_dimensions: list[str]=None,
                                        slider: QSlider=None,
                                        function_to_the_combobox=None,
                                        function_to_the_slider=None,
                                        init_position_of_the_slider: int=0) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.addWidget(QLabel(name_of_the_layout))
    # dropbox
    if list_of_dimensions is None:
        list_of_dimensions: list[str] = ["x", "y", "z", "x1"]
    combobox.clear()
    for key in list_of_dimensions:
        combobox.addItem(key)
    combobox.setCurrentIndex(0)
    combobox.currentIndexChanged.connect(function_to_the_combobox)
    layout.addWidget(combobox)
    # slider
    slider.setMinimum(-180)
    slider.setMaximum(180)
    slider.setSingleStep(1)
    slider.setSliderPosition(init_position_of_the_slider)
    slider.valueChanged.connect(function_to_the_slider)
    layout.addWidget(slider)

    return layout

def mirror_it(list_0: list[list[float]], axis: int) -> list[list[float]]:
    """the function returns a list0 + list of mirrored coordinate respectful to axe,
    if coordinate [axe] = 0, the function makes nothing"""
    new_list: list[list[float]] = []
    for i, coord in enumerate(list_0):
        new_list.append(coord.copy())
        if coord[axis] == 0:
            continue
        coord[axis] = -coord[axis]
        new_list.append(coord.copy())
    return new_list

def open_and_read_a_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read()

def parce_html_with_arrays(raw_str: str) -> str:
    # Parse XML
    tree = et_.parse(raw_str)
    root = tree.getroot()

    result = {}

    # Find all string-array tags
    for arr in root.findall("string-array"):
        name = arr.attrib.get("name")
        items = []

        for item in arr.findall("item"):
            text = item.text.strip()

            # Convert "[0, 4]" → [0, 4]
            try:
                value = ast.literal_eval(text)
            except:
                value = text

            items.append(value)

        result[name] = items

    print( result)
