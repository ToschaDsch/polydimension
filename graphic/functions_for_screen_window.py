from geometry.class_point import Point


def get_scale(list_of_point: list[Point],
              screen_width: int,
              screen_height: int) -> float:
    point_0: Point = list_of_point[0]
    x_max = point_0.coord_n[0]
    y_max = point_0.coord_n[1]
    x_min = point_0.coord_n[0]
    y_min = point_0.coord_n[1]
    for point in list_of_point:
        if point.coord_n[0] > x_max:
            x_max = point.coord_n[0]
        elif point.coord_n[0] < x_min:
            x_min = point.coord_n[0]
        if point.coord_n[1] > y_max:
            y_max = point.coord_n[1]
        elif point.coord_n[1] < y_min:
            y_min = point.coord_n[1]
    max_value_x = max(abs(x_max), abs(x_min))
    max_value_y = max(abs(y_max), abs(y_min))
    if max_value_x == 0:
        scale_x = 1
    else:
        scale_x = (screen_width - 10) / max_value_x * 0.3
    if max_value_y == 0:
        scale_y = 1
    else:
        scale_y = (screen_height - 10) / max_value_y * 0.3
    return min(scale_x, scale_y)