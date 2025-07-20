import numpy as np
from PySide6.QtGui import QColor

from boundary_condition.class_boundary_graph import BoundaryGraph
from geometry.class_combine_beams import CombineBeams
from geometry.class_geometry_change_point import GeometryChangePoint
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_section import Section
from geometry.class_surface import Surface
from geometry.small_geometry_classes import ObjectToDraw, TypeOfTheObjects, LightSurface, LightPoint, LightLine
from graphic.functions_for_class_draw.draw_from_draw_dict import draw_a_line_many_coordinate, \
    draw_line_if_it_under_cursor, draw_a_point_under_cursor
from graphic.functions_for_class_draw.send_results_to_dict import send_result
from load.class_dead_load import DeadLoad
from load.class_influence_load import InfluenceLoad
from functions.universal_functions import get_lines_0_2_for_line_load, get_set_of_load
from variables.general_variables import Geometry, dict_to_show, Finite, Variables
from variables.variables_for_loads import SetOfLoads


def shift_and_draw_on_the_canvas(geometry: GeometryChangePoint, line_axes,
                                 scale: float, dx_dy: [int], x0y0: [int]):
    if dict_to_show['global_axes'].showed:
        draw_axes(line_axes=line_axes, geometry=geometry)
    if dict_to_show['lines'].showed:
        send_to_dict_show_lines(geometry=geometry)  # lines and sections
    if dict_to_show['points'].showed:
        send_points_to_dict(geometry=geometry)
    if dict_to_show['surfaces'].showed:
        send_surfaces(geometry=geometry)
    if dict_to_show['joints'].showed:
        send_to_dict_joints(geometry=geometry)
    if Finite.show_result is False:
        if Variables.current_tab in (Variables.tabs[3], Variables.tabs[4], Variables.tabs[5]):
            # only draw by tabs loads, group, solve
            if Variables.current_tab_loads == Variables.tabs_loads[3]:  # tab 'influence lines'
                if dict_to_show['line_loads'].showed:
                    send_to_dict_show_influence_lines(geometry=geometry)
            else:
                if dict_to_show['point_loads'].showed:
                    send_to_dict_show_point_loads(geometry=geometry)
                if dict_to_show['line_loads'].showed:
                    send_to_dict_show_line_loads(geometry=geometry)
    if Variables.current_tab == Variables.tabs[1] and Variables.current_tab_element == Variables.tabs_element[
        2] and Variables.draw_arc_to_beams is True:  # draw arc to beams
        draw_arcs_of_beam(geometry=geometry)
    if dict_to_show['boundary_conditions'].showed:
        draw_boundary_conditions(geometry=geometry)
    # draw results
    if Finite.show_result:
        if Finite.current_group_result is None:
            Finite.show_result = False
        else:
            send_result(geometry=geometry, scale=scale, dx_dy=dx_dy, x0y0=x0y0)


def draw_arcs_of_beam(geometry):
    for key, beam_i in Geometry.beams.items():
        draw_a_arc_of_beam(beam_i=beam_i, geometry=geometry)


def draw_a_arc_of_beam(beam_i: CombineBeams, geometry):
    type_of_line = TypeOfTheObjects.normal
    # draw y-arc
    draw_a_list_of_lines(lines=beam_i.graphic_y.lines_for_graph, type_of_line=type_of_line,
                         color=Variables.MyColors.arc_of_beam_y, geometry=geometry)
    # draw z-arc
    draw_a_list_of_lines(lines=beam_i.graphic_z.lines_for_graph, type_of_line=type_of_line,
                         color=Variables.MyColors.arc_of_beam_z, geometry=geometry)


def draw_a_list_of_lines(lines: [], type_of_line: str, color: QColor, geometry):
    for line_i in lines:
        draw_object = ObjectToDraw(self_object=line_i, type_of=type_of_line,
                                   type_of_the_objects=TypeOfTheObjects.light_line, color=color)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def draw_boundary_conditions(geometry):
    for key, boundary in Geometry.boundary_conditions.items():
        draw_a_boundary_conditions(boundary=boundary, geometry=geometry)


def draw_a_boundary_conditions(boundary: BoundaryGraph, geometry):
    list_of_line = boundary.draw_elements.lines
    list_of_joint: [LightPoint, float] = boundary.draw_elements.joint
    list_of_surface = boundary.draw_elements.surfaces
    type_of_line = TypeOfTheObjects.selected if boundary.is_got or boundary.under_cursor else TypeOfTheObjects.boundary_condition_line
    send_to_dict_show_joints(list_of_joint=list_of_joint, type_of_line=type_of_line, geometry=geometry)
    send_to_dict_show_boundary_lines(list_of_line=list_of_line, type_of_line=type_of_line, geometry=geometry)
    send_to_dict_show_boundary_surfaces(list_of_surfaces=list_of_surface, type_of=type_of_line, geometry=geometry)


def send_to_dict_show_joints(list_of_joint: [LightPoint, float], type_of_line: str, geometry):
    """the function sends joints to show dict"""
    for joint in list_of_joint:
        coord_0: np.array = np.array(joint[0].coord_n)
        radius: float = joint[1]
        draw_object = ObjectToDraw(self_object=[coord_0, radius], type_of=type_of_line,
                                   type_of_the_objects=TypeOfTheObjects.boundary_condition_joint)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_show_boundary_lines(list_of_line: [LightLine], type_of_line: str, geometry):
    """the function sends boundary lines to show dict"""
    if type_of_line != TypeOfTheObjects.selected:
        type_of_line = TypeOfTheObjects.boundary_condition_line
    for line in list_of_line:
        send_to_dict_a_light_line(line=line, type_of_line=type_of_line, geometry=geometry)


def send_to_dict_a_light_line(geometry, line: LightLine, type_of_line: str = TypeOfTheObjects.normal):
    draw_object = ObjectToDraw(self_object=line, type_of=type_of_line,
                               type_of_the_objects=TypeOfTheObjects.light_line)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_show_boundary_surfaces(geometry, list_of_surfaces: [LightSurface], type_of: str):
    """the function boundary surfaces displacement to show dict"""
    if type_of != TypeOfTheObjects.selected:
        type_of = TypeOfTheObjects.boundary_condition_surface
    for surface in list_of_surfaces:
        draw_object = ObjectToDraw(self_object=surface, type_of=type_of,
                                   type_of_the_objects=TypeOfTheObjects.light_surface)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_show_line_loads(geometry):
    """the function sends line loads to show dict"""
    send_dead_load(geometry)
    send_other_line_load(geometry)


def send_dead_load(geometry):
    # dead load
    dead_load: DeadLoad = Variables.dead_load
    if dead_load.show is False:
        return None
    type_of_the_objects = TypeOfTheObjects.line_load
    color0 = SetOfLoads.dead_load[1]
    color = QColor(*color0)
    for value in dead_load.list_of_line_point_point:
        point_1 = value.line.point_0
        point_2 = value.line.point_1
        point_2a = value.point_2
        point_1a = value.point_1
        draw_object = ObjectToDraw(self_object=LightSurface([point_1, point_2, point_2a, point_1a]),
                                   type_of=type_of_the_objects,
                                   type_of_the_objects=TypeOfTheObjects.light_surface,
                                   text='dead_load',
                                   color=color)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_other_line_load(geometry):
    for key, line_load in Geometry.line_loads.items():
        if line_load.show is False:
            continue
        type_of_the_objects = 'selected' \
            if line_load.is_got is True or line_load.under_cursor is True else TypeOfTheObjects.line_load
        color0 = get_set_of_load(line_load.group)[1]
        color = QColor(*color0)
        for value in line_load.list_of_line_point_point:
            point_1 = value.line.point_0
            point_2 = value.line.point_1
            point_2a = value.point_2
            point_1a = value.point_1
            draw_object = ObjectToDraw(self_object=LightSurface([point_1, point_2, point_2a, point_1a]),
                                       type_of=type_of_the_objects,
                                       type_of_the_objects=TypeOfTheObjects.light_surface,
                                       text=line_load.name,
                                       color=color)
            geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_show_point_loads(geometry):
    """the function sends point loads to show dict"""
    for key, point_load in Geometry.point_loads.items():
        if point_load.show is False:
            continue
        type_of_the_objects = 'normal' if point_load.is_got or point_load.under_cursor is False else 'selected'
        color0 = get_set_of_load(point_load.group)[1]
        color = QColor(color0[0], color0[1], color0[2])
        rx: str = 'Px = ' + "%.2f" % point_load.x + '|' if point_load.x != 0 else ''
        ry: str = 'Py = ' + "%.2f" % point_load.y + '|' if point_load.y != 0 else ''
        rz: str = 'Pz = ' + "%.2f" % point_load.z + '|' if point_load.z != 0 else ''
        text = rx + ry + rz
        for line in point_load.lines:
            coord_load_0 = np.array(line.point_0.coord_n)
            coord_load_1 = np.array(line.point_1.coord_n)
            for point in point_load.objects:
                coord_point_0 = np.array(point.coord_n)
                new_line = [coord_point_0 + coord_load_0, coord_point_0 + coord_load_1]
                draw_object = ObjectToDraw(self_object=new_line, type_of_the_objects=TypeOfTheObjects.point_load,
                                           text=text, type_of=type_of_the_objects, color=color)
                geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_show_influence_lines(geometry):
    """the function sends influence lines to show dict"""
    line_load: InfluenceLoad = Variables.influence_load
    coord_load_0 = np.array(line_load.point_1.coord_n)
    coord_load_1 = np.array(line_load.point_2.coord_n)
    coord_load_0_1 = .5 * (coord_load_0 + coord_load_1)

    type_of_the_objects = TypeOfTheObjects.line_load

    color0 = (0, 50, 200)
    color = QColor(*color0)
    for line_i in line_load.lines:
        coord_point_0, coord_point_1, coord_point_2 = get_lines_0_2_for_line_load(line_i=line_i)
        new_line_0 = [coord_point_0, coord_point_0 + coord_load_0]
        new_line_1 = [coord_point_1, coord_point_1 + coord_load_0_1]
        new_line_2 = [coord_point_2, coord_point_2 + coord_load_1]
        draw_object = ObjectToDraw(self_object=[new_line_0, new_line_1, new_line_2],
                                   type_of_the_objects=TypeOfTheObjects.line_load,
                                   text='influence_line', type_of=type_of_the_objects, color=color)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_joints(geometry):
    joint_color = Variables.MyColors.joint
    for key, joint in Geometry.joints.items():
        if joint.is_got is True or joint.under_cursor is True:
            type_of_line = TypeOfTheObjects.selected
        else:
            type_of_line = TypeOfTheObjects.light_line

        for line in joint.lines_to_draw:
            draw_object = ObjectToDraw(self_object=line, type_of=type_of_line, color=joint_color,
                                       type_of_the_objects=TypeOfTheObjects.light_line)
            geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_surfaces(geometry):
    if len(Geometry.temporary_surface.list_of_points):
        send_the_temporary_surface(geometry=geometry)
    for key, surface in Geometry.surfaces.items():
        send_a_surface_from_geometry(surface=surface, geometry=geometry)


def send_a_surface_from_geometry(geometry, surface: Surface):
    type_of_line = TypeOfTheObjects.selected if surface.is_got else TypeOfTheObjects.surface
    draw_surface = ObjectToDraw(self_object=surface,
                                type_of_the_objects=TypeOfTheObjects.surface,
                                color=Variables.MyColors.surfaces,
                                type_of=type_of_line)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_surface)


def send_the_temporary_surface(geometry):
    type_of_line = TypeOfTheObjects.selected
    surface = Geometry.temporary_surface
    draw_surface = ObjectToDraw(self_object=surface,
                                type_of_the_objects=TypeOfTheObjects.temporary_surface,
                                color=Variables.MyColors.picked_frame_fill,
                                type_of=type_of_line)
    geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_surface)


def send_to_dict_show_lines(geometry):
    """the function sends lines to show dict"""
    send_general_lines(geometry)
    send_temporary_lines()


def send_general_lines(geometry):
    for key, line_i in Geometry.lines.items():
        if line_i.draw_it is False:
            continue
        type_of_line, color = get_type_and_color_of_a_line(line_i=line_i)
        text = get_text_for_the_line(line_i=line_i)
        draw_object = ObjectToDraw(self_object=line_i, type_of=type_of_line, text=text,
                                   type_of_the_objects=TypeOfTheObjects.line, color=color)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)
        if line_i.under_cursor:
            draw_line_if_it_under_cursor(line_i=line_i)
        # section of the element
        if dict_to_show['section'].showed is True and line_i.section is not None:
            draw_section_for_a_line(line_i=line_i, type_of_line=type_of_line, geometry=geometry)


def send_temporary_lines():
    if (Geometry.regime in (Geometry.Regime.change_line_one_point, Geometry.Regime.grab_two_points,
                            Geometry.Regime.new_line_with_mouse, Geometry.Regime.new_polyline_with_mouse)
            and Geometry.stability_point is not None):
        point: Point = Geometry.stability_point
        x1, y1 = point.real_coordinate[0], point.real_coordinate[1]
        x2, y2 = Geometry.mouse_position
        draw_a_line_many_coordinate(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line='dotted')


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


def get_type_and_color_of_a_line(line_i) -> (str, QColor):
    """for all type of lines"""
    if line_i.is_got:
        type_of_line = TypeOfTheObjects.selected
    else:
        type_of_line = TypeOfTheObjects.normal
    if line_i.section:
        color = QColor(*line_i.section.color)
    else:
        color = Variables.MyColors.lines
    return type_of_line, color


def get_text_for_the_line(line_i: Line) -> str | None:
    if (dict_to_show['line_id'].showed or
            dict_to_show['line_comment'].showed or
            dict_to_show['id_for_section'].showed):
        if dict_to_show['line_id'].showed:
            text = str(line_i.hash_id)
            if dict_to_show['point_comment'].showed:
                text += f'\n {line_i.comment}'
        elif dict_to_show['id_for_section'].showed is True and line_i.section is not None:
            section: Section = line_i.section
            text = f'{section.hash_id}'
        else:
            text = str(line_i.comment)
        return text
    return None


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


def draw_section_for_a_line(geometry, line_i: Line, type_of_line: str):
    color = line_i.section.color if dict_to_show['sections_with_colors'].showed \
        else (100, 100, 100, Variables.MyColors.transparency)
    for surface in line_i.solid:
        if type_of_line != TypeOfTheObjects.selected:
            if line_i.combine_beam:
                type_of_line = TypeOfTheObjects.light_surface_of_a_combine_beam
            else:
                type_of_line = TypeOfTheObjects.light_surface
        draw_surface = ObjectToDraw(self_object=surface,
                                    type_of_the_objects=TypeOfTheObjects.light_surface,
                                    color=QColor(*color),
                                    type_of=type_of_line)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_surface)
