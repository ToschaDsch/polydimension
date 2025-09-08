import itertools
import math

import numpy as np

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
    MyCoordinates.angles[MyCoordinates.current_rotation] = rotations*math.pi/180
    Menus.animation.draw_all(dxi=MyCoordinates.displacement, angles=MyCoordinates.angles)
    Menus.screen_window.draw_all()