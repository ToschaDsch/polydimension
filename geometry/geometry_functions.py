import numpy as np

from geometry.class_point import Point


def get_center_from_list_of_points(list_of_points: list[Point]) -> Point:
    dimension = list_of_points[0].dimension
    summ_vector = np.empty((dimension,), float)     # TODO make it without 1
    for point in list_of_points:
        summ_vector += point.coord_0
    coordinate_of_the_center = summ_vector / len(list_of_points)
    return Point(coordinates=coordinate_of_the_center)

def get_rotate_matrix(sin: list[float], cos: list[float], dimensional: int = 3) -> np.ndarray:
    """
    :param sin: list of sin a, b, g
    :param cos: list of cos a, b, g
    :param dimensional: 3d, 4d
    :return: rotate matrix. for 3d -> Ra*Rb*Rg
    """
    r = []
    if dimensional == 3:
        r.append(np.array([[cos[0], -sin[0], 0],
                         [sin[0], cos[0], 0],
                         [0, 0, 1]
                         ]))
        r.append(np.array([[cos[1], 0 - sin[1]],
                         [0, 1, 0],
                         [sin[1], 0, cos[1]]
                         ]))
        r.append(np.array([[1, 0, 0],
                         [0, cos[2], -sin[2]],
                         [0, sin[2], cos[2]]
                         ]))
    elif dimensional == 4:
        i = 0
        r.append(np.array([[cos[i], -sin[i], 0, 0],
                         [sin[i], cos[i], 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ]))
        i =+ 1
        r.append(np.array([[cos[i], 0, - sin[i], 0],
                         [0, 1, 0, 0],
                         [sin[i], 0, cos[i], 0],
                         [0, 0, 0, 1],
                         ]))
        i =+1
        r.append(np.array([[cos[i], 0, 0, - sin[i]],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [sin[i], 0, 0, cos[i]]
                         ]))
        i = +1
        r.append(np.array([[1, 0, 0, 0],
                         [0, cos[i], -sin[i], 0],
                         [0, sin[i], cos[i], 0],
                         [0, 0, 0, 1],
                         ]))
        i = +1
        r.append(np.array([[1, 0, 0, 0],
                         [0, cos[i], 0, -sin[i]],
                         [0, 0, 1, 0],
                         [0, sin[i], 0, cos[i]],
                         ]))
        i = +1
        r.append(np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, cos[i], -sin[i]],
                         [0, 0, sin[i], cos[i]],
                         ]))
    result_matrix = np.identity(dimensional, dtype=np.float64)

    for r_i in r:
        result_matrix = np.dot(r_i, result_matrix)
    print("result matrix", result_matrix)
    return result_matrix
