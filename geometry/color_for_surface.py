from dataclasses import dataclass

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_point import Point


@dataclass
class ReturnColor:
    color: "QColor"
    i_see_it: bool
    distance: float

def to_vec3(v: np.ndarray) -> np.ndarray:
    """Convert 4D → 3D by dropping w"""
    return v[:3]


def normalize(v) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def give_me_return_color(center: Point,
                         normal,
                         base_color: QColor,
                         lamp: np.ndarray, ) -> ReturnColor:
    return give_me_return_color_my_variant(center=center, normal=normal, base_color=base_color, lamp=lamp)

def give_me_return_color_my_variant(center: Point,
                         base_color: QColor,
                         normal: np.ndarray,
                         lamp: np.ndarray) -> ReturnColor:
    """it works only in 3d
    the function send the surface in 3d and find the light end can it be seen"""
    light_point = lamp
    camera_point = np.array([0.0, 0.0, -100.0], dtype=np.float32)  # it needs to be normalized

    # --- convert to 3D ---
    center = to_vec3(center.coord_n)
    normal = to_vec3(normal)

    # --- directions (broadcasting magic here) ---
    to_camera = normalize(camera_point - center)
    light_dir = light_point - center

    # if (distanceFromLamp > lamp.intensity) { // in dark } -- original commented out

    #vector_of_distance = np.resize(normalize_me_in_3d(vector_of_distance), (len(normal), ))
    i_see_it = np.dot(normal, to_camera) < 0.0

    light_dir = to_vec3(normalize(light_dir))
    # --- diffuse ---
    angle = np.dot(normal, light_dir)

    # --- lighting ---
    ambient = 0.6
    intensity = ambient + (1 - ambient) * angle

    # --- apply color ---
    shaded = np.array([base_color.red(), base_color.green(), base_color.blue()]) * intensity
    shaded = np.clip(shaded, 0, 255).astype(np.uint8)
    new_color = QColor(*shaded)
    new_color.setAlpha(base_color.alpha())

    return ReturnColor(color=new_color, i_see_it=i_see_it, distance=1)


def vector_product_with_center(v1: np.ndarray, v2: np.ndarray, vector_center: np.ndarray) -> np.ndarray:
    """
    the function checks where is the center and returns normal of the surface
    only for 3d space
    vector_center - the vector between center of the surface and center of the volume
    """
    vector_center=np.resize(vector_center,3,)
    vector_product = np.cross(v1, v2)
    if vector_product.dot(vector_center) > 0.0:
        return vector_product
    else:
        return np.cross(v2, v1)


def calculate_normal(points: list[Point], vector_center: np.ndarray) -> np.ndarray:
    """
    the function takes coordinate of surfaces edge and calculate normal to the surface
    """
    v1: np.ndarray = np.resize(
        np.subtract(points[1].coord_n[:3], points[0].coord_n[:3]),
        (3,))  # dx //vector v1 (point 1 - point 0)
    v2: np.ndarray = np.resize(
        np.subtract(points[2].coord_n[:3], points[1].coord_n[:3]),
        (3,))  # dx //vector v2 (point 2 - point 1)
    normal = vector_product_with_center(v1=v1, v2=v2,
                                        vector_center=np.resize(vector_center, (3,)))
    return normalize(normal)

