from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QPolygon

from variables import geometry_var
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from variables.graphics import ObjectToDraw, TypeOfTheObjects


def draw_from_dict(geometry, scale: float, dx_dy: list[int], x0y0: list[int]):
    """it is general function of the modul.
    the function becomes objects from dict show.
    in the dict all objects are sorted in z direction.
    the function makes parameters and sends the objects to draw"""
    dick_of_draw_objects: list[ObjectToDraw] = geometry.dict_of_objects_to_draw
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
            case TypeOfTheObjects.surface:
                draw_a_surface(surface=draw_object.self_object, type_of_line=draw_object.type_of,
                               color=draw_object.color)
            case _:
                print('object is not found')


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


def draw_a_line(line: Line, type_of_line: str, color=None, text: str = None):
    color = variables.graphics.MyColors.lines if color is None else color
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


def draw_a_line_many_coordinate(x1: int, y1: int, x2: int, y2: int, type_of_line: str, color=QColor(30, 30, 30)):
    Variables.animation_screen.draw_a_line(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line=type_of_line, color=color)

