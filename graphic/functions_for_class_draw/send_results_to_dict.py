import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor

from geometry.small_geometry_classes import TypeOfTheObjects, ObjectToDraw, LightPoint
from graphic.functions_for_class_draw.draw_from_draw_dict import draw_a_text
from solve.classes_for_finite import ResultGraph
from solve.get_results.functions_and_classes_for_result import CurrentShowValues, ResultNames, get_min_max_for_all_results, \
    dict_of_items_for_result
from solve.get_results.get_color_palette import palette
from variables.general_variables import Finite, Variables


def send_result(geometry, scale: float, dx_dy: [int], x0y0: [int]):
    """it is the general function of the modul
    send graph of results to dict to show all objects"""
    current_group = Finite.current_group_result
    draw_palette_with_values()
    # send displacement
    if dict_of_items_for_result[ResultNames.displacement].show_graphic:  # displacement
        send_to_dict_show_result_displacement(current_group=current_group, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.reaction].show_graphic:  # reaction
        send_to_dict_show_result_reaction(current_group=current_group, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.reaction_moment].show_graphic:
        send_to_dict_show_result_reaction_moment(current_group=current_group, geometry=geometry,
                                                 scale=scale, dx_dy=dx_dy, x0y0=x0y0)
    elif dict_of_items_for_result[ResultNames.normal_forge].show_graphic:  # forges
        send_forges_with_two_parameters(results=Finite.result_normal_forge[current_group],
                                        name_of_the_forge=ResultNames.normal_forge, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.shear_forge_y].show_graphic:
        send_forges_with_two_parameters(results=Finite.result_shear_forge_y[current_group],
                                        name_of_the_forge=ResultNames.shear_forge_y, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.shear_forge_z].show_graphic:
        if Finite.result_shear_forge_z:
            send_forges_with_two_parameters(results=Finite.result_shear_forge_z[current_group],
                                            name_of_the_forge=ResultNames.shear_forge_z, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.torsion].show_graphic:
        if Finite.result_torsion:
            send_forges_with_two_parameters(results=Finite.result_torsion[current_group],
                                            name_of_the_forge=ResultNames.torsion, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.moment_y].show_graphic:
        if Finite.result_moment_forge_y:
            send_forges_with_two_parameters(results=Finite.result_moment_forge_y[current_group],
                                            name_of_the_forge=ResultNames.moment_y, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.moment_z].show_graphic:
        send_forges_with_two_parameters(results=Finite.result_moment_forge_z[current_group],
                                        name_of_the_forge=ResultNames.moment_z, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.local_axes].show_graphic:
        send_local_axes(geometry=geometry)
    elif dict_of_items_for_result[ResultNames.stress_max].show_graphic:  # stress
        stress_result = ResultNames.stress_max
        send_forges_with_two_parameters(results=Finite.result_stress[stress_result][current_group],
                                        name_of_the_forge=stress_result, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.stress_min].show_graphic:
        stress_result = ResultNames.stress_min
        send_forges_with_two_parameters(results=Finite.result_stress[stress_result][current_group],
                                        name_of_the_forge=stress_result, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.stress_abs_max].show_graphic:
        stress_result = ResultNames.stress_abs_max
        send_forges_with_two_parameters(results=Finite.result_stress[stress_result][current_group],
                                        name_of_the_forge=stress_result, geometry=geometry)
    elif dict_of_items_for_result[ResultNames.stress_s_fd].show_graphic:
        stress_result = ResultNames.stress_s_fd
        send_forges_with_two_parameters(results=Finite.result_stress[stress_result][current_group],
                                        name_of_the_forge=stress_result, geometry=geometry)


def send_local_axes(geometry):
    type_of_line = TypeOfTheObjects.light_line
    for key, element in Finite.elements.items():
        line_color = ((element.local_axes.axis_x, QColor(255, 0, 0)),
                      (element.local_axes.axis_y, QColor(0, 255, 0)),
                      (element.local_axes.axis_z, QColor(0, 0, 255)))
        for line_i, color in line_color:
            draw_object = ObjectToDraw(self_object=line_i, type_of=type_of_line, color=color,
                                       type_of_the_objects=TypeOfTheObjects.light_line)
            geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_forges_with_two_parameters(geometry, results: ResultGraph, name_of_the_forge: str):
    """the function sends results of the forge to show dict"""
    type_of_line = TypeOfTheObjects.light_surface
    # send curve
    send_curve_for_forge_with_two_parameters(dict_with_forge=results.dict_of_surfaces,
                                             type_of_line=type_of_line, geometry=geometry)
    # send value
    if dict_of_items_for_result[name_of_the_forge].show_value:
        send_values_for_forge_with_two_parameters(results=results, geometry=geometry)


def send_curve_for_forge_with_two_parameters(dict_with_forge: {}, type_of_line: str, geometry):
    for key, surface_value in dict_with_forge.items():
        surfaces = surface_value.surfaces
        for surface in surfaces:
            if Variables.colorful_result:
                color = surface.color
            else:
                color = Variables.MyColors.result_curve
            draw_object = ObjectToDraw(self_object=surface,
                                       type_of=type_of_line,
                                       type_of_the_objects=TypeOfTheObjects.light_surface,
                                       color=color)
            geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_values_for_forge_with_two_parameters(geometry, results: ResultGraph):
    type_of_line = TypeOfTheObjects.normal
    for key, value_begin in results.dict_point_value_begin.items():
        # send text with value at the beginning
        point_begin, number_begin = value_begin
        text_begin = "%.2f" % number_begin if number_begin != 0 else ''
        dx = 0
        dy = 0
        draw_object_begin = ObjectToDraw(self_object=[point_begin, (dx, dy)],
                                         type_of=type_of_line, text=text_begin,
                                         type_of_the_objects=TypeOfTheObjects.text, color=QColor(200, 200, 200))
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object_begin)
        # send text with value at the end
        value_end: [float, float] = results.dict_point_value_end[key]
        point_end, number_end = value_end
        text_end = "%.2f" % number_end if number_end != 0 else ''
        dx = 0
        dy = 0
        draw_object_end = ObjectToDraw(self_object=[point_end, (dx, dy)],
                                       type_of=type_of_line, text=text_end,
                                       type_of_the_objects=TypeOfTheObjects.text, color=QColor(200, 200, 200))
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object_end)


def send_to_dict_show_result_reaction_moment(geometry, current_group: str,
                                             scale: float, dx_dy: [int], x0y0: [int]):
    """the function sends reaction_moments to show dict"""
    for key, reaction in Finite.result_reaction_moment[current_group].items():
        type_of_the_objects = 'reaction'
        color = Variables.MyColors.reaction

        for moment_i in (reaction.graph_moment_x, reaction.graph_moment_y, reaction.graph_moment_z):
            if moment_i is None:
                continue
            for line in moment_i.lines_for_graph:
                draw_object = ObjectToDraw(self_object=line, type_of_the_objects=TypeOfTheObjects.light_line,
                                           type_of=type_of_the_objects, color=color)
                geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)

            if dict_of_items_for_result[ResultNames.reaction_moment].show_value is False:  # draw text
                continue
            rx: str = '0' if reaction.graph_moment_x is None else "%.2f" % reaction.graph_moment_x.value
            ry: str = '0' if reaction.graph_moment_y is None else "%.2f" % reaction.graph_moment_y.value
            rz: str = '0' if reaction.graph_moment_z is None else "%.2f" % reaction.graph_moment_z.value
            text = (f'Mx = {rx}', f'My = {ry}', f'Mz = {rz}')
            if reaction.graph_moment_x is not None:
                point: LightPoint = reaction.graph_moment_x.point
            elif reaction.graph_moment_y is not None:
                point: LightPoint = reaction.graph_moment_y.point
            elif reaction.graph_moment_z is not None:
                point: LightPoint = reaction.graph_moment_z.point
            else:
                continue
            x1 = int(-point.coord_n[0] * scale + dx_dy[0] + x0y0[0])
            y1 = int(point.coord_n[1] * scale + dx_dy[1] + x0y0[1])
            for i, t in enumerate(text):
                draw_a_text(x0_y0=(x1, y1 - 45 + i * 15), type_of_point=type_of_the_objects, text=t)


def send_to_dict_show_result_reaction(geometry, current_group: str):
    """the function sends reaction to show dict,
    I use here the same element as point_load, but with only one point"""
    for key, reaction in Finite.result_reaction[current_group].items():
        type_of_the_objects = 'reaction'
        color = Variables.MyColors.reaction
        point = list(reaction.objects)[0]
        coord_point_0 = np.array(point.coord_n)
        for i, line in enumerate(reaction.lines):
            coord_load_0 = np.array(line.point_0.coord_n)
            coord_load_1 = np.array(line.point_1.coord_n)
            if i == 0:
                if dict_of_items_for_result[ResultNames.reaction].show_value:  # draw text
                    rx: str = "Rx = %.2f|" % reaction.x if reaction.x != 0 else ''
                    ry: str = "Ry = %.2f|" % reaction.y if reaction.y != 0 else ''
                    rz: str = "Rz = %.2f|" % reaction.z if reaction.z != 0 else ''
                    text = rx + ry + rz
                else:
                    text = ''
            else:
                text = ''
            new_line = [coord_point_0 + coord_load_0, coord_point_0 + coord_load_1]
            draw_object = ObjectToDraw(self_object=new_line, type_of_the_objects=TypeOfTheObjects.point_load,
                                       text=text, type_of=type_of_the_objects, color=color)
            geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def send_to_dict_show_result_displacement(geometry, current_group: str):
    """the function sends displacement to show dict"""
    type_of_line = TypeOfTheObjects.selected
    dict_with_lines = Finite.result_displacement[current_group].dict_of_lines
    color = Variables.MyColors.displacement
    for key, line in dict_with_lines.items():
        draw_object = ObjectToDraw(self_object=line,
                                   type_of=type_of_line,
                                   type_of_the_objects=TypeOfTheObjects.light_line, color=color)
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)
    # send value

    if dict_of_items_for_result[ResultNames.displacement].show_value:
        dict_with_values = Finite.result_displacement[current_group].dict_point_value
        for key, value in dict_with_values.items():
            point, numbers = value
            for i, t in enumerate(numbers):
                text = "%.5f" % t
                dx = 0
                dy = 45 - 15 * i
                draw_object = ObjectToDraw(self_object=[point, (dx, dy)],
                                           type_of=type_of_line, text=text,
                                           type_of_the_objects=TypeOfTheObjects.text, color=color)
                geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)


def draw_palette_with_values():
    write_values()
    if Variables.colorful_result:
        draw_color_palette()


def draw_color_palette():
    if CurrentShowValues.name in (ResultNames.displacement, ResultNames.reaction,
                                  ResultNames.reaction_moment, ResultNames.local_axes):
        return None
    value_min, value_max = get_min_max_for_all_results(name_of_the_result=CurrentShowValues.name)
    if value_max - value_min == 0:
        return None
    text = []
    for x in range(len(palette) + 1):
        value_i = x * (value_max - value_min) / len(palette) + value_min
        text.append("%.2f" % value_i)
    type_of_point = TypeOfTheObjects.color
    color_text = Variables.MyColors.annotation
    h = 15
    b = 30
    x_0 = 20
    y_0 = 65
    x_i_1 = x_0 + b
    y_i = y_0
    y_i_1 = y_0 + h
    # draw palette
    draw_a_text(x0_y0=(x_i_1 + 1, y_i - 5), type_of_point=type_of_point, text=str(text[0]), color=color_text)
    for i, color in enumerate(palette):
        polygon = QtGui.QPolygonF([QPointF(x_0, y_i), QPointF(x_0, y_i_1),
                                   QPointF(x_i_1, y_i_1), QPointF(x_i_1, y_i)])
        Variables.animation_screen.draw_a_polygon(polygon=polygon, type_of_line=type_of_point, color=color)
        y_i = y_i_1
        y_i_1 += h
        # draw values
        draw_a_text(x0_y0=(x_i_1 + 1, y_i - 5), type_of_point=type_of_point, text=str(text[i + 1]),
                    color=color_text)


def write_values():
    type_of_point = TypeOfTheObjects.color
    color = Variables.MyColors.annotation
    x_0 = 10
    y_0 = 15
    for i, text_i in enumerate([CurrentShowValues.name,
                                f"max = {"%.2f" % CurrentShowValues.max}",
                                f"min = {"%.2f" % CurrentShowValues.min}"]):
        draw_a_text(x0_y0=(x_0, y_0 * (1 + i)), type_of_point=type_of_point, text=text_i, color=color)
