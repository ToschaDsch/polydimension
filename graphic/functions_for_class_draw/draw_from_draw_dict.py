from PySide6 import QtGui
from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QColor, QPolygon

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.small_geometry_classes import TypeOfTheObjects, ObjectToDraw, LightLine, LightSurface
from solve.get_results.functions_and_classes_for_result import dict_of_items_for_result, ResultNames
from variables.general_variables import Variables, Geometry


def draw_from_dict(geometry, scale: float, dx_dy: [int], x0y0: [int]):
    """it is general function of the modul.
    the function becomes objects from dict show.
    in the dict all objects are sorted in z direction.
    the function makes parameters and sends the objects to draw"""
    dick_of_draw_objects: [ObjectToDraw] = geometry.dict_of_objects_to_draw
    for key, draw_object in dick_of_draw_objects.items():
        match draw_object.type_of_the_objects:
            case TypeOfTheObjects.point:
                draw_a_point(type_of_point=draw_object.type_of, point=draw_object.self_object, text=draw_object.text)
            case TypeOfTheObjects.text:
                coord_n = draw_object.self_object[0].coord_n
                dx_dy_2 = draw_object.self_object[1]
                x_y = (-coord_n[0] * scale + dx_dy[0] + x0y0[0] + dx_dy_2[0],
                       coord_n[1] * scale + dx_dy[1] + x0y0[1] + dx_dy_2[1])
                draw_a_text(x0_y0=x_y, type_of_point=draw_object.type_of,
                            color=draw_object.color, text=draw_object.text)
            case TypeOfTheObjects.light_line:
                draw_a_light_line(line=draw_object.self_object,
                                  type_of_the_line=draw_object.type_of,
                                  color=draw_object.color, dx_dy=dx_dy, scale=scale, x0y0=x0y0)
            case TypeOfTheObjects.light_surface:
                draw_a_light_surface(surface=draw_object.self_object, type_of_line=draw_object.type_of,
                                     color=draw_object.color, dx_dy=dx_dy, scale=scale, x0y0=x0y0)
            case TypeOfTheObjects.line:
                draw_a_line(line=draw_object.self_object, type_of_line=draw_object.type_of,
                            color=draw_object.color, text=draw_object.text)
            case TypeOfTheObjects.point_load:
                draw_a_point_load(coord_of_lines=draw_object.self_object, color=draw_object.color,
                                  type_of_the_line=draw_object.type_of, text=draw_object.text,
                                  dx_dy=dx_dy, scale=scale, x0y0=x0y0)
            case TypeOfTheObjects.line_load:
                draw_a_line_load(coord_of_lines=draw_object.self_object, color=draw_object.color,
                                 type_of_the_line=draw_object.type_of, text=draw_object.text,
                                 dx_dy=dx_dy, scale=scale, x0y0=x0y0)
            case TypeOfTheObjects.boundary_condition_joint:
                coord = draw_object.self_object[0]
                x1 = int(-coord[0] * scale + dx_dy[0] + x0y0[0])
                y1 = int(coord[1] * scale + dx_dy[1] + x0y0[1])
                draw_an_joint(coordinate=(x1, y1), r=draw_object.self_object[1] * scale,
                              type_of_line=draw_object.type_of)
            case TypeOfTheObjects.boundary_condition_line:
                draw_a_boundary_line(coord_of_lines=draw_object.self_object,
                                     type_of_the_line=draw_object.type_of, dx_dy=dx_dy, scale=scale, x0y0=x0y0)
            case TypeOfTheObjects.boundary_condition_surface:
                draw_a_boundary_surface(coord_of_the_surface=draw_object.self_object,
                                        type_of_the_line=draw_object.type_of, dx_dy=dx_dy, scale=scale, x0y0=x0y0)
            case TypeOfTheObjects.temporary_surface:
                draw_the_temporary_surface(surface=draw_object.self_object, type_of_line=draw_object.type_of,
                                           color=draw_object.color)
            case TypeOfTheObjects.surface:
                draw_a_surface(surface=draw_object.self_object, type_of_line=draw_object.type_of,
                               color=draw_object.color)
            case _:
                print('object is not found')


def draw_a_line_load(coord_of_lines: [], color: QColor, type_of_the_line: str, text: str,
                     scale: float, dx_dy: [int], x0y0: [int]):
    Variables.animation_screen.change_brush(color=color, type_of_line=type_of_the_line)
    polygons_coord = []
    for line in coord_of_lines:
        polygons_coord.append(draw_a_point_load(coord_of_lines=line, color=color, type_of_the_line=type_of_the_line,
                                                text=text, dx_dy=dx_dy, scale=scale, x0y0=x0y0))
    polygon = QPolygon()
    polygon.append(QPoint(polygons_coord[0][0], polygons_coord[0][1]))
    polygon.append(QPoint(polygons_coord[0][2], polygons_coord[0][3]))
    polygon.append(QPoint(polygons_coord[2][2], polygons_coord[2][3]))
    polygon.append(QPoint(polygons_coord[2][0], polygons_coord[2][1]))
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_the_line, color=color)


def draw_a_point_load(coord_of_lines: [], color: QColor, type_of_the_line: str,
                      scale: float, dx_dy: [int], x0y0: [int], text: str = ''):
    x1 = int(-coord_of_lines[0][0] * scale + dx_dy[0] + x0y0[0])
    y1 = int(coord_of_lines[0][1] * scale + dx_dy[1] + x0y0[1])
    x2 = int(-coord_of_lines[1][0] * scale + dx_dy[0] + x0y0[0])
    y2 = int(coord_of_lines[1][1] * scale + dx_dy[1] + x0y0[1])

    if type_of_the_line != 'selected':
        type_of_the_line = TypeOfTheObjects.point_load
    draw_a_line_many_coordinate(type_of_line=type_of_the_line, color=color,
                                x1=x1, y1=y1, x2=x2, y2=y2)
    if dict_of_items_for_result[ResultNames.reaction].show_value and color == Variables.MyColors.reaction:
        text: [] = text.split('|')
        for i, t in enumerate(text):
            draw_a_text(x0_y0=(x1, y1 - 45 + i * 15), type_of_point=type_of_the_line, text=t)
    return x1, y1, x2, y2


def draw_an_joint(coordinate: tuple[int, int], r: float, type_of_line):
    if type_of_line != TypeOfTheObjects.selected:
        type_of_line = TypeOfTheObjects.boundary_condition_joint
    Variables.animation_screen.draw_a_circle(x=coordinate[0], y=coordinate[1], r=r, type_of_line=type_of_line)


def draw_the_temporary_surface(surface: LightSurface, type_of_line: str, color: QColor):
    Variables.animation_screen.change_brush(type_of_line=type_of_line,
                                            color=color)
    polygon = QPolygon()
    for point_i in surface.list_of_points:
        coord = point_i.real_coordinate
        polygon.append(QPoint(coord[0], coord[1]))
    polygon.append(QPoint(Geometry.mouse_position[0], Geometry.mouse_position[1]))
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_line)


def draw_a_surface(surface: Surface, type_of_line: str, color: QColor):
    Variables.animation_screen.change_brush(type_of_line=type_of_line,
                                            color=color)
    polygon = QPolygon()
    for point_i in surface.list_of_points:
        coord = point_i.real_coordinate
        polygon.append(QPoint(coord[0], coord[1]))
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_line)


def draw_a_light_surface(surface: LightSurface, type_of_line: str, color: QColor,
                         scale: float, dx_dy: [int], x0y0: [int]):
    Variables.animation_screen.change_brush(type_of_line=type_of_line,
                                            color=color)
    polygon = QPolygon()
    for point_i in surface.list_of_points:
        x, y = (int(-point_i.coord_n[0] * scale + dx_dy[0] + x0y0[0]),
                int(point_i.coord_n[1] * scale + dx_dy[1] + x0y0[1]))
        polygon.append(QPoint(x, y))

    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_line)


def draw_a_boundary_line(coord_of_lines: [], type_of_the_line: str, scale: float, dx_dy: [int], x0y0: [int]):
    x1 = int(-coord_of_lines[0][0] * scale + dx_dy[0] + x0y0[0])
    y1 = int(coord_of_lines[0][1] * scale + dx_dy[1] + x0y0[1])
    x2 = int(-coord_of_lines[1][0] * scale + dx_dy[0] + x0y0[0])
    y2 = int(coord_of_lines[1][1] * scale + dx_dy[1] + x0y0[1])
    if type_of_the_line != 'selected':
        type_of_the_line = TypeOfTheObjects.boundary_condition_line
    draw_a_line_many_coordinate(type_of_line=type_of_the_line,
                                x1=x1, y1=y1, x2=x2, y2=y2)


def draw_a_light_line(line: LightLine, type_of_the_line: str,
                      scale: float, dx_dy: [int], x0y0: [int], color=QColor(255, 0, 0)):
    Variables.animation_screen.change_brush(type_of_line=type_of_the_line,
                                            color=color)
    x1 = int(-line.point_0.coord_n[0] * scale + dx_dy[0] + x0y0[0])
    y1 = int(line.point_0.coord_n[1] * scale + dx_dy[1] + x0y0[1])
    x2 = int(-line.point_1.coord_n[0] * scale + dx_dy[0] + x0y0[0])
    y2 = int(line.point_1.coord_n[1] * scale + dx_dy[1] + x0y0[1])
    draw_a_line_many_coordinate(type_of_line=type_of_the_line,
                                x1=x1, y1=y1, x2=x2, y2=y2, color=color)


def draw_a_text(x0_y0, text: str, type_of_point: str, color=QColor(0, 255, 0)):
    Variables.animation_screen.draw_a_point_text(text=text, x0_y0=x0_y0, type_of_point=type_of_point, color=color)


def draw_a_boundary_surface(coord_of_the_surface: [], type_of_the_line: str,
                            scale: float, dx_dy: [int], x0y0: [int]):
    if type_of_the_line != 'selected':
        type_of_the_line = TypeOfTheObjects.boundary_condition_surface
    polygon = QPolygon()
    for coord_i in coord_of_the_surface:
        x, y = (int(-coord_i[0] * scale + dx_dy[0] + x0y0[0]),
                int(coord_i[1] * scale + dx_dy[1] + x0y0[1]))
        polygon.append(QPoint(x, y))
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_the_line)


def draw_a_line(line: Line, type_of_line: str, color=None, text: str = None):
    color = Variables.MyColors.lines if color is None else color
    x1 = line.point_0.real_coordinate[0]
    y1 = line.point_0.real_coordinate[1]
    x2 = line.point_1.real_coordinate[0]
    y2 = line.point_1.real_coordinate[1]
    Variables.animation_screen.draw_a_line(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line=type_of_line, color=color)
    if text:
        x0_y0 = .5 * (x1 + x2), .5 * (y1 + y2)
        draw_a_text(x0_y0=x0_y0, text=text, type_of_point=TypeOfTheObjects.color, color=color)


def draw_a_point(point: Point, type_of_point, text: str = None):
    x0_y0 = point.real_coordinate
    Variables.animation_screen.draw_a_point(x=x0_y0[0], y=x0_y0[1], type_of_point=type_of_point)
    if text:
        draw_a_text(x0_y0=x0_y0, text=text, type_of_point=type_of_point)


def draw_a_point_under_cursor(x0_y0):
    x1 = x0_y0[0] - Geometry.point_square_collapse
    y1 = x0_y0[1] - Geometry.point_square_collapse
    #  a frame
    Variables.animation_screen.draw_a_point_under_cursor(x1=x1, y1=y1)


def draw_a_line_many_coordinate(x1: int, y1: int, x2: int, y2: int, type_of_line: str, color=QColor(30, 30, 30)):
    Variables.animation_screen.draw_a_line(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line=type_of_line, color=color)


def draw_line_if_it_under_cursor(line_i: Line):
    match line_i:
        case Geometry.line_with_checked_middle_point:
            draw_a_point_under_cursor(line_i.middle_point_real_coordinate)
        case Geometry.line_with_checked_normal_point:
            draw_a_point_under_cursor(line_i.normal_to_the_point_real_coordinate)
    draw_a_line_under_cursor(line_i)


def draw_a_line_under_cursor(line: Line):
    type_of_line = TypeOfTheObjects.selected
    match Geometry.binding:
        case Geometry.Biding.point_middle:
            draw_a_line_with_middle_point(line=line, type_of_line=type_of_line)
        case Geometry.Biding.point_middle_normal:
            draw_a_line_with_middle_point(line=line, type_of_line=type_of_line)
            if Geometry.stability_point:
                check_and_draw_normal_to_the_line(line=line, type_of_line=type_of_line)
        case _:
            draw_a_triangle(line=line, type_of_line=type_of_line)


def check_and_draw_normal_to_the_line(line, type_of_line: str):
    coord_0 = line.normal_to_the_line_coord_0(point=Geometry.stability_point)
    geometry = Variables.geometry_change_point
    if coord_0:
        real_coordinate = geometry.rotate_coord_0(coord_0)
        line.normal_to_the_point_real_coordinate = real_coordinate
        draw_a_line_with_normal_to_point(line=line,
                                         real_coordinate=real_coordinate,
                                         type_of_line=type_of_line)


def draw_a_triangle(line, type_of_line):
    x1 = line.point_0.real_coordinate[0]
    y1 = line.point_0.real_coordinate[1]
    x2 = line.point_1.real_coordinate[0]
    y2 = line.point_1.real_coordinate[1]
    d = Geometry.size_of_draw_objects
    xm = .5 * (x1 + x2)
    ym = .5 * (y1 + y2)
    dx = x2 - x1
    dy = y2 - y1
    cos = abs(dx / (dy ** 2 + dx ** 2) ** .5)
    sin = 1 - cos ** 2
    delta_sin = d * .5 * sin
    delta_cos = d * .5 * cos
    xa = ya = xb = yb = xd = yd = xc = yc = 0
    if dx > 0 and dy > 0:
        xa = xm + delta_cos
        ya = ym + delta_sin
        xc = xm - delta_cos
        yc = ym - delta_sin
        xb = xc + delta_sin
        yb = yc - delta_cos
        xd = xc - delta_sin
        yd = yc + delta_cos
    elif dx < 0 < dy:
        xa = xm - delta_cos
        ya = ym + delta_sin
        xc = xm + delta_cos
        yc = ym - delta_sin
        xb = xc + delta_sin
        yb = yc + delta_cos
        xd = xc - delta_sin
        yd = yc - delta_cos
    elif dx <= 0 and dy <= 0:
        xa = xm - delta_cos
        ya = ym - delta_sin
        xc = xm + delta_cos
        yc = ym + delta_sin
        xb = xc + delta_sin
        yb = yc - delta_cos
        xd = xc - delta_sin
        yd = yc + delta_cos
    elif dx >= 0 >= dy:
        xa = xm + delta_cos
        ya = ym - delta_sin
        xc = xm - delta_cos
        yc = ym + delta_sin
        xb = xc + delta_sin
        yb = yc + delta_cos
        xd = xc - delta_sin
        yd = yc - delta_cos
    polygon = QtGui.QPolygonF([QPointF(xa, ya), QPointF(xb, yb), QPointF(xc, yc), QPointF(xd, yd)])
    Variables.animation_screen.draw_a_line(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line=type_of_line)
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line="selected")


def draw_a_line_with_middle_point(line, type_of_line):
    x1 = line.point_0.real_coordinate[0]
    y1 = line.point_0.real_coordinate[1]
    x2 = line.point_1.real_coordinate[0]
    y2 = line.point_1.real_coordinate[1]
    d = Geometry.size_of_draw_objects * 1.5
    xm = .5 * (x1 + x2)
    ym = .5 * (y1 + y2)
    dx = x2 - x1
    dy = y2 - y1
    if dy == 0:
        sin = 0
        cos = 1
    else:
        cos = abs(dx / (dy ** 2 + dx ** 2) ** .5)
        sin = 1 - cos ** 2
    delta_sin = d * .5 * sin
    delta_cos = d * .5 * cos
    xa = ya = xb = yb = xd = yd = xc = yc = 0
    if dx > 0 and dy > 0:
        xb = xm + delta_sin
        yb = ym - delta_cos
        xd = xm - delta_sin
        yd = ym + delta_cos
    elif dx < 0 < dy:
        xb = xm + delta_sin
        yb = ym + delta_cos
        xd = xm - delta_sin
        yd = ym - delta_cos
    elif dx <= 0 and dy <= 0:
        xb = xm + delta_sin
        yb = ym - delta_cos
        xd = xm - delta_sin
        yd = ym + delta_cos
    elif dx >= 0 >= dy:
        xb = xm + delta_sin
        yb = ym + delta_cos
        xd = xm - delta_sin
        yd = ym - delta_cos
    polygon = QtGui.QPolygonF([QPointF(xb, yb), QPointF(xd, yd)])
    Variables.animation_screen.draw_a_line(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line=type_of_line)
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_line)


def draw_a_line_with_normal_to_point(line: Line, real_coordinate: (float, float), type_of_line):
    # coordinate of the line
    x1 = line.point_0.real_coordinate[0]
    y1 = line.point_0.real_coordinate[1]
    x2 = line.point_1.real_coordinate[0]
    y2 = line.point_1.real_coordinate[1]
    # coordinate of the normal point
    x_p = real_coordinate[0]
    y_p = real_coordinate[1]
    if Geometry.stability_point is None:
        return None
    point: Point = Geometry.stability_point
    x_0 = point.real_coordinate[0]
    y_0 = point.real_coordinate[1]
    a = Geometry.size_of_draw_objects
    dx = x_0 - x_p
    dy = y_0 - y_p
    dl = (dx ** 2 + dy ** 2) ** .5
    dx2 = x2 - x1
    dy2 = y2 - y1
    dl2 = (dx2 ** 2 + dy2 ** 2) ** .5
    if dl == 0 or dl2 == 0:
        return None
    dx_1 = dx / dl * a
    dy_1 = dy / dl * a
    dx_2 = dx2 / dl2 * a
    dy_2 = dy2 / dl2 * a
    x_1 = x_p + dx_1
    y_1 = y_p + dy_1
    x_2 = x_1 - dx_2
    y_2 = y_1 - dy_2
    x_3 = x_2 - dx_1
    y_3 = y_2 - dy_1

    polygon = QtGui.QPolygonF([QPointF(x_1, y_1), QPointF(x_2, y_2), QPointF(x_3, y_3), QPointF(x_p, y_p)])
    Variables.animation_screen.draw_a_line(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line=type_of_line)
    Variables.animation_screen.draw_a_line(x1=x_0, y1=y_0, x2=x_p, y2=y_p, type_of_line='dotted')
    Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line='dotted')
