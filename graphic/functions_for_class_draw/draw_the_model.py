"""test regime"""
from PySide6.QtGui import QColor

from geometry.small_geometry_classes import TypeOfTheObjects
from graphic.functions_for_class_draw.draw_from_draw_dict import draw_a_text, draw_a_line_many_coordinate
from solve.class_node import Node
from variables.geometry_var import Finite, Variables, Hinge


def show_the_model(scale: float, dx_dy: [int], x0y0: [int], key=None):
    show_nodes(scale=scale, dx_dy=dx_dy, x0y0=x0y0)
    show_elements(scale=scale, dx_dy=dx_dy, x0y0=x0y0)


def show_nodes(scale: float, dx_dy: [int], x0y0: [int], key=None):
    for key, node in Finite.nodes.items():
        type_of_point = TypeOfTheObjects.normal
        x, y = (-node.coordinate.coord_n[0] * scale + dx_dy[0] + x0y0[0],
                node.coordinate.coord_n[1] * scale + dx_dy[1] + x0y0[1])
        Variables.animation_screen.draw_a_point(x=x, y=y, type_of_point=type_of_point)
        if Finite.dict_to_show_finite['nodes']:
            type_of_point = TypeOfTheObjects.normal
            text = str(key)
            color = QColor(255, 0, 0)
            draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['boundary']:
            if node.boundaries is not None:
                text = str(node.boundaries)
                if node.boundaries.ux[1] > 0:
                    text = text + f', s_ux_ = {node.boundaries.ux[1]}'
                if node.boundaries.uy[1] > 0:
                    text = text + f', s_uy_ = {node.boundaries.uy[1]}'
                if node.boundaries.uz[1] > 0:
                    text = text + f', s_uz_ = {node.boundaries.uz[1]}'
                if node.boundaries.mx[1] > 0:
                    text = text + f', s_mx_ = {node.boundaries.mx[1]}'
                if node.boundaries.my[1] > 0:
                    text = text + f', s_my_ = {node.boundaries.my[1]}'
                if node.boundaries.mz[1] > 0:
                    text = text + f', s_mz_ = {node.boundaries.mz[1]}'
                type_of_point = TypeOfTheObjects.color
                color = QColor(0, 255, 0)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['load_x']:
            if node.loads[key][0] != 0:
                text = str("%.2f" % node.loads[key][0])
                type_of_point = TypeOfTheObjects.color
                color = QColor(0, 0, 255)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['load_y']:
            if node.loads[key][1] != 0:
                text = str("%.2f" % node.loads[key][1])
                type_of_point = TypeOfTheObjects.color
                color = QColor(0, 0, 255)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['load_z']:
            if node.loads[key][2] != 0:
                text = str("%.2f" % node.loads[key][2])
                type_of_point = TypeOfTheObjects.color
                color = QColor(0, 0, 255)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['displacement']:
            if node.result.displacement[key] != [0, 0, 0]:
                text = ', '.join("%.5f" % x for x in node.result.displacement[key])
                type_of_point = TypeOfTheObjects.color
                color = QColor(255, 0, 255)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['reaction']:
            if node.result.reaction[key] is not None:
                text = ','.join("%.2f" % x for x in node.result.reaction[key])
                type_of_point = TypeOfTheObjects.color
                color = QColor(0, 255, 200)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['reaction_moment']:
            if node.result.reaction_moment[key] is not None:
                text = ','.join("%.2f" % x for x in node.result.reaction_moment[key])
                type_of_point = TypeOfTheObjects.color
                color = QColor(0, 255, 200)
                draw_a_text(x0_y0=(x, y), text=text, type_of_point=type_of_point, color=color)


def show_elements(scale: float, dx_dy: [int], x0y0: [int], key=None):
    for key, element in Finite.elements.items():
        node_0: Node = element.node_0
        node_1: Node = element.node_1
        x1, y1 = (int(-node_0.coordinate.coord_n[0] * scale + dx_dy[0] + x0y0[0]),
                  int(node_0.coordinate.coord_n[1] * scale + dx_dy[1] + x0y0[1]))
        x2, y2 = (int(-node_1.coordinate.coord_n[0] * scale + dx_dy[0] + x0y0[0]),
                  int(node_1.coordinate.coord_n[1] * scale + dx_dy[1] + x0y0[1]))
        draw_a_line_many_coordinate(x1=x1, y1=y1, x2=x2, y2=y2, type_of_line='selected')
        if Finite.dict_to_show_finite['elements']:
            type_of_point = TypeOfTheObjects.color
            color = QColor(140, 140, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=str(key),
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['normal_forge']:
            type_of_point = TypeOfTheObjects.color
            text = "%.2f" % element.result.normal_forge
            color = QColor(140, 250, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['shear_forge_y']:
            type_of_point = TypeOfTheObjects.color
            text = "%.2f" % element.result.shear_forge_y[0]
            color = QColor(140, 250, 140)
            draw_a_text(x0_y0=(x1 + 10, y1 + 10), text=text,
                        type_of_point=type_of_point, color=color)
            text = "%.2f" % element.result.shear_forge_y[1]
            draw_a_text(x0_y0=(x2 - 10, y2 - 10), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['moment_z']:
            type_of_point = TypeOfTheObjects.color
            text = "%.2f" % element.result.moment_z[0]
            color = QColor(140, 250, 140)
            draw_a_text(x0_y0=(x1 + 10, y1 + 10), text=text,
                        type_of_point=type_of_point, color=color)
            text = "%.2f" % element.result.moment_z[1]
            draw_a_text(x0_y0=(x2 - 10, y2 - 10), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['elements_loads_x']:
            type_of_point = TypeOfTheObjects.color
            text = ','.join("%.2f" % x for x in element.loads_x)
            color = QColor(140, 0, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['elements_loads_y']:
            type_of_point = TypeOfTheObjects.color
            text = ','.join("%.2f" % x for x in element.loads_y)
            color = QColor(140, 0, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['elements_loads_z']:
            type_of_point = TypeOfTheObjects.color
            text = ','.join("%.2f" % x for x in element.loads_z)
            color = QColor(140, 0, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['local_axes']:
            type_of_point = TypeOfTheObjects.color
            text = str(element.local_axes)
            color = QColor(50, 80, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=text,
                        type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['hinges']:
            type_of_point = TypeOfTheObjects.color
            hinge: Hinge | None = None
            x, y = 0, 0
            number_of_node = 0
            if element.hinge_at_beginning:
                x, y = x1, y1
                hinge: Hinge = element.hinge_at_beginning
                number_of_node = element.node_0.number
            if element.hinge_at_the_end:
                x, y = x2, y2
                hinge: Hinge = element.hinge_at_the_end
                number_of_node = element.node_1.number
            if hinge is not None:
                text_0 = f'element Nr {element.number}'
                text_1 = f'node Nr {number_of_node}'
                text_2 = ''
                if hinge.hinge_y:
                    text_2 += 'y'
                if hinge.hinge_z:
                    text_2 += 'z'
                color = QColor(250, 180, 140)
                draw_a_text(x0_y0=(x, y), text=text_0,
                            type_of_point=type_of_point, color=color)
                draw_a_text(x0_y0=(x, y + 15), text=text_1,
                            type_of_point=type_of_point, color=color)
                draw_a_text(x0_y0=(x, y + 30), text=text_2,
                            type_of_point=type_of_point, color=color)
        if Finite.dict_to_show_finite['l_ef']:
            type_of_point = TypeOfTheObjects.color
            text = ','.join("%.2f" % x for x in element.l_ef)
            color = QColor(140, 0, 140)
            draw_a_text(x0_y0=(.5 * (x1 + x2), .5 * (y1 + y2)), text=text,
                        type_of_point=type_of_point, color=color)
