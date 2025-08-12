import numpy as np
from PySide6.QtGui import QColor


from variables import geometry_var
from geometry.class_geometry_change_point import GeometryChangePoint
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from variables.graphics import ObjectToDraw, TypeOfTheObjects


def draw_a_list_of_lines(lines: [], type_of_line: str, color: QColor, geometry):
    for line_i in lines:
        draw_object = ObjectToDraw(self_object=line_i, type_of=type_of_line,
                                   type_of_the_objects=TypeOfTheObjects.light_line, color=color)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_a_light_line(geometry, line: LightLine, type_of_line: str = TypeOfTheObjects.normal):
    draw_object = ObjectToDraw(self_object=line, type_of=type_of_line,
                               type_of_the_objects=TypeOfTheObjects.light_line)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)




def send_a_surface_from_geometry(geometry, surface: Surface):
    type_of_line = TypeOfTheObjects.selected if surface.is_got else TypeOfTheObjects.surface
    draw_surface = ObjectToDraw(self_object=surface,
                                type_of_the_objects=TypeOfTheObjects.surface,
                                color=QColor(0, 255, 0),
                                type_of=type_of_line)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_surface)


def send_to_dict_show_lines(geometry):
    """the function sends lines to show dict"""
    send_general_lines(geometry)



def draw_axes(geometry: GeometryChangePoint, line_axes: []):
    type_of_line = TypeOfTheObjects.normal
    color = QColor(80, 80, 80)
    send_a_line_to_dict(line_i=line_axes[0], text='x', color=color,
                        geometry=geometry, type_of_line=type_of_line)
    send_a_line_to_dict(line_i=line_axes[1], text='y', color=color,
                        geometry=geometry, type_of_line=type_of_line)
    send_a_line_to_dict(line_i=line_axes[2], text='z', color=color,
                        geometry=geometry, type_of_line=type_of_line)


def send_a_line_to_dict(line_i: Line, geometry: GeometryChangePoint, type_of_line: str = None, color: QColor = None,
                        text: str = None):
    if type_of_line is None or color is None:
        type_of_line, color = get_type_and_color_of_a_line(line_i=line_i)
    text = get_text_for_the_line(line_i=line_i) if text is None else text
    draw_object = ObjectToDraw(self_object=line_i, type_of=type_of_line, text=text,
                               type_of_the_objects=TypeOfTheObjects.line, color=color)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)




def send_points_to_dict(geometry):
    for key, point_i in Geometry.points.items():
        type_of_point = TypeOfTheObjects.selected if point_i.is_got else TypeOfTheObjects.normal
        text = get_text_for_a_point(point_i=point_i)
        send_a_point_to_dict(point=point_i, type_of_point=type_of_point, text=text, geometry=geometry)
        if point_i.under_cursor:
            x0_y0 = point_i.real_coordinate
            draw_a_point_under_cursor(x0_y0)


def get_text_for_a_point(point_i: Point) -> str | None:
    if dict_to_show['point_id'].showed or dict_to_show['point_comment'].showed:
        if dict_to_show['point_id'].showed:
            text = str(point_i.hash_id)
            if dict_to_show['point_comment'].showed:
                text += f'\n {point_i.comment}'
            return text
        else:
            return str(point_i.comment)
    else:
        return None


def send_a_point_to_dict(point: Point, type_of_point: str, text: str | None, geometry):
    draw_object = ObjectToDraw(self_object=point, type_of=type_of_point, text=text,
                               type_of_the_objects=TypeOfTheObjects.point)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)
