from dataclasses import dataclass

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_point import Point

@dataclass
class DataToCalculateColor:
    center: np.ndarray
    normal: np.ndarray
    base_color: QColor

@dataclass
class ReturnColor:
    color: "QColor"
    i_see_it: bool

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
    return give_me_return_color_my_variant(data=DataToCalculateColor(center=center.coord_n, normal=normal, base_color=base_color),
                                           light_point=lamp)

def give_me_return_color_my_variant(data: DataToCalculateColor,
                                    light_point: np.ndarray) -> ReturnColor:
    """it works only in 3d
    the function send the surface in 3d and find the light end can it be seen"""
    camera_point = np.array([0.0, 0.0, -100.0], dtype=np.float32)  # it needs to be normalized

    # --- convert to 3D ---
    center = to_vec3(data.center)
    normal = to_vec3(data.normal)

    # --- directions (broadcasting magic here) ---
    to_camera = normalize(camera_point - center)
    light_dir = to_vec3(normalize(light_point - center))

    i_see_it = np.dot(normal, to_camera) < 0.0

    # --- diffuse ---
    angle = np.dot(normal, light_dir)

    # --- lighting ---
    ambient = 0.6
    intensity = ambient + (1 - ambient) * angle

    # --- apply color ---
    shaded = np.array([data.base_color.red(), data.base_color.green(), data.base_color.blue()]) * intensity
    shaded = np.clip(shaded, 0, 255).astype(np.uint8)
    new_color = QColor(*shaded)
    new_color.setAlpha(data.base_color.alpha())

    return ReturnColor(color=new_color, i_see_it=i_see_it)


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


def normalize_batch(v):
    norm = np.linalg.norm(v, axis=1, keepdims=True)
    return v / (norm + 1e-8)


def compute_colors_batch(centers, normals, init_colors, light_point):
    """
    centers: (N, 3)
    normals: (N, 3)
    colors:  (N, 3)  [0..255]
    alphas:  (N,)
    light_point: (3,)
    """

    camera_point = np.array([0.0, 0.0, -100.0], dtype=np.float32)

    # --- direction ---
    to_camera = normalize_batch(camera_point - centers)
    light_dir = normalize_batch(light_point - centers)

    # --- visibility ---
    i_see_it = np.einsum('ij,ij->i', normals, to_camera) < 0.0

    # --- diffuse ---
    angle = np.einsum('ij,ij->i', normals, light_dir)
    angle = np.clip(angle, 0.0, 1.0)

    # --- lightning ---
    ambient = 0.6
    intensity = ambient + (1 - ambient) * angle
    intensity = intensity[:, None]  # (N,1) для broadcasting

    # --- color ---
    shaded = init_colors * intensity
    shaded = np.clip(shaded, 0, 255).astype(np.uint8)

    return shaded, i_see_it