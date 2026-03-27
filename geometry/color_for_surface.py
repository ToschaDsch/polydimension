from dataclasses import dataclass

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_point import Point
from geometry.class_source_of_light import SourceOfLight


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
                         lamp: SourceOfLight, ) -> ReturnColor:
    return compute_surface_color(center=center, normal=normal, base_color=base_color, lamp=lamp)
    return give_me_return_color_my_variant(center=center, normal=normal, base_color=base_color, lamp=lamp)

def compute_surface_color(center: Point,
                          normal,
                          base_color: QColor,
                          lamp: SourceOfLight,):
    """
    Accepts 4D or 3D numpy arrays
    """
    light_point = lamp.coordinate.coord_0
    camera_point = np.array([0,0,100])    # it needs to be normalized

    # --- convert to 3D ---
    points = to_vec3(center.coord_n)
    normal = to_vec3(normal)

    # --- normalize -- normal- it is already normalized
    to_camera = normalize(camera_point - points)
    light_dir = normalize(light_point - points)

    # --- back-face culling ---
    i_see_it = np.sum(normal * to_camera, axis=0) > 0

    # --- diffuse ---
    diffuse = np.maximum(0.0, np.sum(normal * light_dir, axis=0))

    # --- lighting ---
    ambient = 0.8
    intensity = ambient + (1 - ambient) * diffuse

    # --- apply color ---
    shaded = np.array([base_color.red(), base_color.green(), base_color.blue()]) * intensity

    # --- clamp + hide invisible ---
    shaded[~i_see_it] = 50
    shaded = np.clip(shaded, 0, 255).astype(np.uint8)
    color = QColor(*shaded)
    color.setAlpha(base_color.alpha())

    return ReturnColor(color=color, i_see_it=i_see_it, distance=0)



def give_me_return_color_my_variant(center: Point,
                         base_color: QColor,
                         normal: np.ndarray,
                         lamp: SourceOfLight) -> ReturnColor:
    """it works only in 3d
    the function send the surface in 3d and find the light end can it be seen"""
    vector_of_distance, square_of_distance = calculate_vector_and_square_of_distance(center=center)
    distance3d: float = 0.0

    vector_from_lamp, distance_from_lamp = calculate_lamp(vector_of_distance=vector_of_distance,
                                                          lamp_coord=lamp.coordinate.coord_n)

    # if (distanceFromLamp > lamp.intensity) { // in dark } -- original commented out

    #vector_of_distance = np.resize(normalize_me_in_3d(vector_of_distance), (len(normal), ))
    vector_from_observer = np.resize(np.array([0, 10, 10]), len(normal))
    i_see_it = cos_between_two_vectors(normal, vector_from_observer) < 0.0

    vector_from_lamp = np.resize(normalize_me_in_3d(vector_from_lamp), (len(normal),))
    angle = cos_between_two_vectors(normal, vector_from_lamp)
    new_color = make_color(angle0=angle, distance=distance3d, color=base_color)
    return ReturnColor(color=new_color, i_see_it=i_see_it, distance=square_of_distance)


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

def calculate_vector_and_square_of_distance(center: Point) -> tuple[np.ndarray, float]:
    """
    the function calculates a vector to the center of the surface and average square of distance to the surface
    from center of coordinate
    """
    square_of_length = 0.0

    return center.coord_n, square_of_length

def calculate_normal(points: list[Point], vector_center: np.ndarray) -> np.ndarray:
    """
    the function takes coordinate of surfaces edge and calculate normal to the surface
    """
    v1: np.ndarray = np.resize(
        np.subtract(points[1].coord_n,points[0].coord_n),
        (3,))  # dx //vector v1 (point 1 - point 0)
    v2: np.ndarray = np.resize(
        np.subtract(points[2].coord_n, points[1].coord_n),
        (3,))  # dx //vector v2 (point 2 - point 1)
    normal = vector_product_with_center(v1=v1, v2=v2,
                                        vector_center=np.resize(vector_center, (3,)))
    return normalize(normal)

def calculate_lamp(vector_of_distance: np.ndarray, lamp_coord: np.ndarray) -> tuple[np.ndarray, float]:
    """
    the function returns not normalized vector of lamp - the point
    and the distance between
    """
    vector_from_lamp = lamp_coord - np.resize(vector_of_distance, (3,),)
    # Kotlin had sqrt(...) commented out and set distanceFromLamp = 1f
    distance_from_lamp = 1.0
    return vector_from_lamp, distance_from_lamp

def normalize_me_in_3d(vector: np.ndarray) -> np.ndarray:
    """
    the function normalizes a vector in 3d dimension
    """
    vector_3d = np.resize(vector, (3,))
    distance = np.sqrt(vector_3d.dot(vector_3d))

    a = 1.0 if distance == 0.0 else 1.0 / distance

    return vector * a

def cos_between_two_vectors(normal: np.ndarray, vector_of_distance: np.ndarray) -> float:
    """the function returns 3d scalar product"""
    return np.dot(normal, vector_of_distance)

def make_color(angle0: float, distance: float, color: QColor) -> QColor:
    if color is None:
        return QColor(*[100,100,0])
    dispersion_of_light = 0.5
    # val add = (1f - Properties.DISPERSION_OF_LIGHT) + abs(angle0) * Properties.DISPERSION_OF_LIGHT
    add = (1.0 - dispersion_of_light) + abs(angle0) * dispersion_of_light
    if (add > 0.0) and (add < 1.0):
        return QColor(*[int(color.red()* add),
                        int(color.green() * add),
                        int(color.blue() * add),
                        color.alpha()])
    else:
        return color