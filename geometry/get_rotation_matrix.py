import numpy as np


def get_rotate_matrix(sin: list[float], cos: list[float], dimensional: int = 3) -> np.ndarray:
    """
    :param sin: list of sin a, b, g
    :param cos: list of cos a, b, g
    :param dimensional: 3d, 4d
    :return: rotate matrix. for 3d -> Ra*Rb*Rg
    """
    r = []
    if dimensional == 3:
        r[0] = np.array([[cos[0], -sin[0], 0],
                         [sin[0], cos[0], 0],
                         [0, 0, 1]
                         ])
        r[1] = np.array([[cos[1], 0 - sin[1]],
                         [0, 1, 0],
                         [sin[1], 0, cos[1]]
                         ])
        r[2] = np.array([[1, 0, 0],
                         [0, cos[2], -sin[2]],
                         [0, sin[2], cos[2]]
                         ])
    elif dimensional == 4:
        i = 0
        r[i] = np.array([[cos[i], -sin[i], 0, 0],
                         [sin[i], cos[i], 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ])
        i=+1
        r[i] = np.array([[cos[i], 0, - sin[i], 0],
                         [0, 1, 0, 0],
                         [sin[i], 0, cos[i], 0],
                         [0, 0, 0, 1],
                         ])
        i = +1
        r[i] = np.array([[cos[i], 0, 0, - sin[i]],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [sin[i], 0, 0, cos[i]]
                         ])
        i = +1
        r[i] = np.array([[1, 0, 0, 0],
                         [0, cos[i], -sin[i], 0],
                         [0, sin[i], cos[i], 0],
                         [0, 0, 0, 1],
                         ])
        i = +1
        r[i] = np.array([[1, 0, 0, 0],
                         [0, cos[i], 0, -sin[i]],
                         [0, 0, 1, 0],
                         [0, sin[i], 0, cos[i]],
                         ])
        i = +1
        r[i] = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, cos[i], -sin[i]],
                         [0, 0, sin[i], cos[i]],
                         ])
    result_matrix = np.identity(dimensional, dtype=np.float64)
    print("identity matrix", result_matrix)
    for r_i in r:
        result_matrix = np.dot(r_i, result_matrix)
    return result_matrix