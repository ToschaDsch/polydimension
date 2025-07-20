from boundary_condition.class_boundary_graph import BoundaryGraph
from geometry.class_combine_beams import CombineBeams
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.joint_draw import GeneralJoint
from load.class_point_load import PointLoad
from menus.tab_menus.menu_boundary_conditions.tab_menu_boundary_conditions import \
    delete_a_point_from_boundary_conditions
from menus.tab_menus.tab_menu_elements.tab_menu_joint import delete_joints
from menus.tab_menus.tab_menu_elements.tab_menu_section import delete_sections
from menus.tab_menus.tab_menu_geometry.functions_to_work_with_menu_lines import delete_lines
from menus.tab_menus.tab_menu_geometry.tab_menu_lines import merge_the_line_with_point
from menus.tab_menus.tab_menu_geometry.tab_menu_points import merge_points
from menus.tab_menus.tab_menu_geometry.functions_to_work_with_menu_points import add_points, delete_points
from menus.tab_menus.tab_menu_geometry.tab_menu_surfaces import delete_surfaces
from menus.tab_menus.tab_menu_loads.tab_menu_loads_line_loads import delete_line_loads
from menus.tab_menus.tab_menu_loads.tab_menu_loads_point_loads import delete_point_loads
from functions.universal_functions import i_am_back_with_points, edit_lines_and_points_button_enabled, correct_binding
from menus.small_menus.small_menus_copy import i_am_back_with_a_point, copy_to, shift_to
from variables.general_variables import Geometry, Variables


def check_collapse(x: int, y: int):
    """the function checks - is the object under the cursor or not"""
    if Variables.current_tab == Variables.tabs[0]:
        # points and lines, surfaces
        check_collapse_tab_geometry(x=x, y=y)
    elif Variables.current_tab == Variables.tabs[1]:  # sections or joints or combine beams
        check_collapse_tab_elements(x=x, y=y)
    elif Variables.current_tab == Variables.tabs[2]:  # boundary conditions
        check_collapse_boundary_conditions(x=x, y=y)
    elif Variables.current_tab == Variables.tabs[3]:  # loads
        check_collapse_loads(x=x, y=y)


def check_collapse_tab_geometry(x: int, y: int):
    match Geometry.binding:
        case Geometry.Biding.points:  # points
            check_collapse_points(x=x, y=y)
        case Geometry.Biding.lines:  # lines
            check_collapse_lines(x=x, y=y)
        case Geometry.Biding.point_middle | Geometry.Biding.point_middle_normal | Geometry.Biding.points_and_lines:
            check_collapse_points(x=x, y=y)
            check_collapse_lines(x=x, y=y)
        case Geometry.Biding.surfaces:
            check_collapse_surfaces(x=x, y=y)


def check_collapse_surfaces(x: int, y: int):
    if Geometry.Regime.grab_a_point:
        check_collapse_points(x=x, y=y)


def check_collapse_tab_elements(x: int, y: int):
    if Variables.current_tab_element == Variables.tabs_element[0]:  # section
        check_collapse_lines(x=x, y=y)
    elif Variables.current_tab_element == Variables.tabs_element[1]:  # joint
        match Geometry.regime:
            case Geometry.Regime.grab_lines_for_joint:
                check_collapse_lines(x=x, y=y)
            case _:
                check_collapse_joints(x=x, y=y)
    elif Variables.current_tab_element == Variables.tabs_element[2]:    # combine
        match Geometry.regime:
            case Geometry.Regime.grab_elements:
                check_collapse_elements(x=x, y=y)
            case Geometry.Regime.grab_beams:    # combine beams
                check_collapse_combine_beams(x=x, y=y)


def check_collapse_boundary_conditions(x: int, y: int):
    if (Geometry.regime == Geometry.Regime.grab_points_for_boundary_condition_general_menu or
            Geometry.regime == Geometry.Regime.grab_points_for_boundary_condition_info_menu):
        check_collapse_points(x=x, y=y)
    elif (Geometry.regime == Geometry.Regime.grab_lines_for_boundary_condition_general_menu or
          Geometry.regime == Geometry.Regime.grab_lines_for_boundary_condition_info_menu):
        check_collapse_lines(x=x, y=y)
    else:
        check_collapse_points_lines_boundary_conditions(x=x, y=y)


def check_collapse_loads(x: int, y: int):
    if Variables.current_tab_loads == Variables.tabs_loads[0]:  # self-wight loads
        match Geometry.regime:
            case Geometry.Regime.grab_lines_for_loads \
                 | Geometry.Regime.grab_lines_for_loads_info_menu | Geometry.Regime.grab_lines_for_dead_load:
                check_collapse_lines(x=x, y=y)
            case _:
                check_collapse_line_loads(x=x, y=y)
    if Variables.current_tab_loads == Variables.tabs_loads[1]:  # point loads
        match Geometry.regime:
            case Geometry.Regime.grab_points_for_loads | Geometry.Regime.grab_points_for_loads_info_menu:
                check_collapse_points(x=x, y=y)
            case _:
                check_collapse_point_loads(x=x, y=y)
    elif Variables.current_tab_loads == Variables.tabs_loads[2]:  # line loads
        match Geometry.regime:
            case Geometry.Regime.grab_lines_for_loads \
                 | Geometry.Regime.grab_lines_for_loads_info_menu | Geometry.Regime.grab_lines_for_dead_load:
                check_collapse_lines(x=x, y=y)
            case _:
                check_collapse_line_loads(x=x, y=y)
    elif Variables.current_tab_loads == Variables.tabs_loads[3]:  # influence lines
        match Geometry.regime:
            case Geometry.Regime.grab_lines_for_influence_line:
                check_collapse_lines(x=x, y=y)
            case _:
                check_collapse_line_loads(x=x, y=y)


def check_collapse_points(x: int, y: int):
    """the function checks is a point under the cursor,
        when yes - it make the point 'under cursor' """
    for key, point_i in Geometry.points.items():
        if point_i.moved_node:
            continue
        x0 = point_i.real_coordinate[0] - Geometry.delta_collapse
        x1 = x0 + 2 * Geometry.delta_collapse
        y0 = point_i.real_coordinate[1] - Geometry.delta_collapse
        y1 = y0 + 2 * Geometry.delta_collapse
        if x0 < x < x1 and y0 < y < y1:
            point_i.under_cursor = True
            Geometry.point_under_cursor = point_i
            return None
        else:
            point_i.under_cursor = False
    Geometry.point_under_cursor = None


def check_collapse_points_lines_boundary_conditions(x: int, y: int):
    """the function checks is a point - .5 m under the cursor,
        when yes - it make the boundary 'under cursor' """
    for key, boundary in Geometry.boundary_conditions.items():
        if boundary.point:
            point_i = boundary.point
            x0 = point_i.real_coordinate[0] - Geometry.delta_collapse
            x1 = x0 + 2 * Geometry.delta_collapse
            y0 = point_i.real_coordinate[1] - 2 * Geometry.delta_collapse
            y1 = y0 + 2 * Geometry.delta_collapse + 30
            if x0 < x < x1 and y0 < y < y1:
                boundary.under_cursor = True
                Geometry.boundary_under_cursor = boundary
                return None
            else:
                boundary.under_cursor = False
        elif boundary.line:
            line_i = boundary.line
            if collapse_a_line(line_i=line_i, x=x, y=y):
                boundary.under_cursor = True
                Geometry.boundary_under_cursor = boundary
                return None
            else:
                boundary.under_cursor = False
    Geometry.boundary_under_cursor = None


def check_collapse_point_loads(x: int, y: int):
    """the function checks is a point + .5 m under the cursor,
        when yes - it make the point load 'under cursor' """
    for key, point_load in Geometry.point_loads.items():
        for point_i in point_load.objects:
            x0 = point_i.real_coordinate[0] - Geometry.delta_collapse
            x1 = x0 + 2 * Geometry.delta_collapse
            y0 = point_i.real_coordinate[1] - 50
            y1 = y0 + 2 * Geometry.delta_collapse + 50
            if x0 < x < x1 and y0 < y < y1:
                point_load.under_cursor = True
                Geometry.point_load_under_cursor = point_load
                return None
            else:
                point_load.under_cursor = False
    Geometry.point_load_under_cursor = None


def check_collapse_line_loads(x: int, y: int):
    """the function checks is a line of a line load under the cursor,
        when yes - it make the line load 'under cursor' """
    space: int = 30
    for key, line_load in Geometry.line_loads.items():
        for line_i in line_load.objects:
            x0 = line_i.point_0.real_coordinate[0]
            x1 = line_i.point_1.real_coordinate[0]
            y0 = line_i.point_0.real_coordinate[1]
            y1 = line_i.point_1.real_coordinate[1]

            if abs(x1 - x0) > abs(y1 - y0):
                collapse = check_horizontal(x0=x0, y0=y0, x1=x1, y1=y1, x=x, y=y, space=space)
            else:
                collapse = check_vertical(x0=x0, y0=y0, x1=x1, y1=y1, x=x, y=y, space=space)

            if collapse:
                line_load.under_cursor = True
                Geometry.line_load_under_cursor = line_load
                return None
            else:
                line_load.under_cursor = False


def check_collapse_joints(x: int, y: int):
    """the function checks is a joint under the cursor,
    when yes - it make the joint 'under cursor' """
    for key, joint in Geometry.joints.items():
        for point_i, line_i in joint.points_and_lines:
            x0 = point_i.real_coordinate[0] - Geometry.delta_collapse
            x1 = x0 + 2 * Geometry.delta_collapse
            y0 = point_i.real_coordinate[1] - 50
            y1 = y0 + 2 * Geometry.delta_collapse + 50
            if x0 < x < x1 and y0 < y < y1:
                joint.under_cursor = True
                Geometry.joint_under_cursor = joint
                return None
            else:
                joint.under_cursor = False
    Geometry.joint_under_cursor = None


def collapse_a_line(x: int, y: int, line_i: Line) -> bool:
    """the function checks is a line under the cursor,
        when yes - it returns True else False """
    x0 = line_i.point_0.real_coordinate[0]
    x1 = line_i.point_1.real_coordinate[0]
    y0 = line_i.point_0.real_coordinate[1]
    y1 = line_i.point_1.real_coordinate[1]

    # space is make for regime with lines and points simultaneously
    # it make space around points
    space: int = 10 if Geometry.binding in (Geometry.Biding.point_middle, Geometry.Biding.point_middle_normal) \
        else 0

    if abs(x1 - x0) > abs(y1 - y0):
        return check_horizontal(x0=x0, y0=y0, x1=x1, y1=y1, x=x, y=y, space=space)
    else:
        return check_vertical(x0=x0, y0=y0, x1=x1, y1=y1, x=x, y=y, space=space)


def collapse_a_beam(x: int, y: int, beam: CombineBeams) -> bool:
    """the function checks is a combine beam under the cursor,
            when yes - it returns True else False """
    if len(beam.paar_of_points) == 0 or len(beam.objects) == 0:
        return False
    point_0: Point = beam.paar_of_points[0]
    point_1: Point = beam.paar_of_points[1]
    x0 = point_0.real_coordinate[0]
    x1 = point_1.real_coordinate[0]
    y0 = point_0.real_coordinate[1]
    y1 = point_1.real_coordinate[1]

    # space is made for regime with lines and points simultaneously
    # it make space around points
    space: int = 10

    if abs(x1 - x0) > abs(y1 - y0):
        return check_horizontal(x0=x0, y0=y0, x1=x1, y1=y1, x=x, y=y, space=space)
    else:
        return check_vertical(x0=x0, y0=y0, x1=x1, y1=y1, x=x, y=y, space=space)


def check_collapse_elements(x: int, y: int):
    """the function checks is a line under the cursor, and it has a section,
    when yes - it make the line 'under cursor' """
    if len(Geometry.lines) == 0 or len(Geometry.sections) == 0:
        return None
    for key, line_i in Geometry.lines.items():
        if collapse_a_line(line_i=line_i, x=x, y=y):
            if line_i.section is None:
                continue
            line_i.under_cursor = True
            Geometry.line_under_cursor = line_i
            return None
        else:
            line_i.under_cursor = False
    Geometry.line_under_cursor = None


def check_collapse_combine_beams(x: int, y: int):
    """the function checks is a combine beam under cursor,
        when yes - it make the beam 'under cursor' """
    if len(Geometry.beams) == 0 or len(Geometry.sections) == 0 or len(Geometry.lines) == 0:
        return None
    for key, beam_i in Geometry.beams.items():
        if collapse_a_beam(beam=beam_i, x=x, y=y):
            beam_i.under_cursor = True
            Geometry.beam_under_cursor = beam_i
            return None
        else:
            beam_i.under_cursor = False
    Geometry.beam_under_cursor = None


def check_collapse_lines(x: int, y: int):
    """the function checks is a line under the cursor,
    when yes - it make the line 'under cursor' """
    if len(Geometry.lines) == 0:
        return None
    for key, line_i in Geometry.lines.items():
        if collapse_a_line(line_i=line_i, x=x, y=y):
            line_i.under_cursor = True
            Geometry.line_under_cursor = line_i
            if Variables.current_tab == Variables.tabs[1]:  # only for lines
                match Geometry.binding:
                    case Geometry.Biding.point_middle:
                        check_middle_point_collapse(line_i=line_i, x=x, y=y)
                    case Geometry.Biding.point_middle_normal:
                        check_middle_point_collapse(line_i=line_i, x=x, y=y)
                        check_normal_to_line_collapse(line_i=line_i, x=x, y=y)
            if Variables.current_tab == Variables.tabs[0]:  # for points
                check_middle_point_collapse(line_i=line_i, x=x, y=y)
            return None
        else:
            line_i.under_cursor = False
    Geometry.line_under_cursor = None


def check_middle_point_collapse(line_i: Line, x: int, y: int):
    d = Geometry.delta_collapse
    x_min = line_i.middle_point_real_coordinate[0] - d
    x_max = line_i.middle_point_real_coordinate[0] + d
    y_min = line_i.middle_point_real_coordinate[1] - d
    y_max = line_i.middle_point_real_coordinate[1] + d
    if x_min < x < x_max and y_min < y < y_max:
        Geometry.line_with_checked_middle_point = line_i
    else:
        Geometry.line_with_checked_middle_point = None


def check_normal_to_line_collapse(line_i: Line, x: int, y: int):
    d = Geometry.delta_collapse

    if line_i.normal_to_the_point_real_coordinate is None:
        return None
    x_min = line_i.normal_to_the_point_real_coordinate[0] - d
    x_max = line_i.normal_to_the_point_real_coordinate[0] + d
    y_min = line_i.normal_to_the_point_real_coordinate[1] - d
    y_max = line_i.normal_to_the_point_real_coordinate[1] + d
    if x_min < x < x_max and y_min < y < y_max:
        Geometry.line_with_checked_normal_point = line_i
    else:
        Geometry.line_with_checked_normal_point = None


def check_horizontal(x0: float, y0: float, x1: float, y1: float, x: float, y: float, space: int = 0) -> bool:
    """check a quasi horizontal line is it under cursor or not"""

    def f_line() -> tuple[float, float]:
        d = (y1 - y0) / (x1 - x0) * (x - x0) + y0
        return d - Geometry.delta_collapse, d + Geometry.delta_collapse

    dy_min, dy_max = f_line()
    if min(x0, x1) + space < x < max(x0, x1) - space and dy_min < y < dy_max:
        return True
    return False


def check_vertical(x0: float, y0: float, x1: float, y1: float, x: float, y: float, space: int = 0) -> None | bool:
    """check a quasi vertical line is it under cursor or not"""

    def f_line() -> tuple[float, float] | bool:
        if y1 - y0 == 0:
            return False, False
        d = (x1 - x0) / (y1 - y0) * (y - y0) + x0
        return d - Geometry.delta_collapse, d + Geometry.delta_collapse

    dx_min, dx_max = f_line()
    if dx_min is False:
        return False
    if min(y0, y1) + space < y < max(y0, y1) - space and dx_min < x < dx_max:
        return True
    return False


def check_collapse_for_objects(ctrl: bool, object_self):
    my_set: set[Point] | set[Line] = set()
    my_object: Point | Line | None = None
    match object_self:
        case Geometry.Biding.joints:
            my_set: set[GeneralJoint] = Geometry.picked_joints
            my_object: BoundaryGraph = Geometry.joint_under_cursor
        case Geometry.Biding.point_load:
            my_set: set[PointLoad] = Geometry.picked_point_loads
            my_object: BoundaryGraph = Geometry.point_load_under_cursor
        case Geometry.Biding.line_load:
            my_set: set[PointLoad] = Geometry.picked_line_loads
            my_object: BoundaryGraph = Geometry.line_load_under_cursor
        case Geometry.Biding.points_boundary:
            my_set: set[BoundaryGraph] = Geometry.picked_boundary
            my_object: BoundaryGraph = Geometry.boundary_under_cursor
        case Geometry.Biding.points:
            my_set: set[Point] = Geometry.picked_points
            my_object: Point = Geometry.point_under_cursor
        case Geometry.Biding.lines | Geometry.Biding.beams | Geometry.Biding.elements:
            my_set: set[Line] = Geometry.picked_lines
            my_object: Line = Geometry.line_under_cursor

    if ctrl is False and Geometry.picked_frame[0] == Geometry.picked_frame[1]:  # side click
        for object_i in my_set:
            object_i.is_got = False
        my_set = set()
    if my_object:  # point click
        if my_object.is_got:
            if my_object in my_set:
                my_set.remove(my_object)
            my_object.is_got = False
        else:
            my_set.add(my_object)
            my_object.is_got = True

    match object_self:
        case Geometry.Biding.joints:
            Geometry.picked_joints = my_set
        case Geometry.Biding.point_load:
            Geometry.picked_point_loads = my_set
        case Geometry.Biding.line_load:
            Geometry.picked_line_loads = my_set
        case Geometry.Biding.points:
            Geometry.picked_points = my_set
        case Geometry.Biding.lines | Geometry.Biding.beams | Geometry.Biding.elements:
            Geometry.picked_lines = my_set
        case Geometry.Biding.points_boundary:
            Geometry.picked_boundary = my_set
    edit_lines_and_points_button_enabled()


def left_click(x: int, y: int, ctrl: bool):
    Geometry.picked_frame = [(x, y), (x, y)]
    if Geometry.regime:
        geometry_regime_points_lines()  # grab points at cetera
        return None


def geometry_regime_points_lines():
    match Geometry.regime:
        case None:
            return None
        case Geometry.Regime.grab_a_point | Geometry.Regime.change_line_one_point:
            regime_grab_a_point()
        case Geometry.Regime.grab_two_points | Geometry.Regime.new_line_with_mouse | Geometry.Regime.new_polyline_with_mouse:
            regime_grab_two_points()


def regime_grab_two_points():
    """Geometry.Regime.grab_two_points |
    Geometry.Regime.new_line_with_mouse |
    Geometry.Regime.new_polyline_with_mouse:"""

    if Geometry.point_under_cursor:
        regime_for_point_under_cursor(new_point=Geometry.point_under_cursor)
    elif Geometry.line_with_checked_middle_point is not None or Geometry.line_with_checked_normal_point is not None:
        regime_for_line_under_cursor()


def regime_for_line_under_cursor():
    new_coord: [float, float, float] = [0, 0, 0]
    if Geometry.line_with_checked_normal_point:
        new_coord = Geometry.line_with_checked_normal_point.normal_to_the_line_coord_0(
            point=Geometry.stability_point)
    elif Geometry.line_with_checked_middle_point:
        new_coord = Geometry.line_with_checked_middle_point.middle_point_coord_0

    new_point: Point = add_points(list_of_coord_0=[new_coord])[0]
    # now you have the real point under cursor and you can use regim for it
    regime_for_point_under_cursor(new_point=new_point)


def regime_grab_a_point():
    """Geometry.Regime.grab_a_point | Geometry.Regime.change_line_one_point"""
    if Geometry.point_under_cursor:
        point = Geometry.point_under_cursor
        i_am_back_with_a_point(point)
        if Geometry.back_to_menu_with_a_point == 'menu_surface':
            return None
        Geometry.regime = None


def regime_for_point_under_cursor(new_point: Point):
    if Geometry.stability_point is None:
        Geometry.stability_point = new_point
        Geometry.binding = Geometry.Biding.point_middle_normal  # for point two
    elif (Geometry.stability_point is not None and
          Geometry.grabbed_point_1 is None and
          Geometry.stability_point != new_point):
        point_from = Geometry.stability_point
        point_to = new_point
        Geometry.stability_point = None
        i_am_back_with_points(point_from=point_from, point_to=point_to)


def start_shift(x: int, y: int):
    """first click of the mousewheel or right button"""
    Geometry.x0y0 = (x, y)


def start_to_rotate(x: int, y: int):
    """first click of the mousewheel or right button"""
    Geometry.x0y0 = (x, y)


def left_release(event, ctrl: bool = False):
    if (Geometry.regime == Geometry.Regime.edit_with_moved_node or
            Geometry.regime == Geometry.Regime.edit_lines_with_moved_node):
        release_moved_node(ctrl=ctrl)
        return None
    match Geometry.binding:
        case Geometry.Biding.points:  # only points available
            check_collapse_for_objects(ctrl=ctrl, object_self=Geometry.Biding.points)
            if ctrl is False:
                geometry_regime_points_lines()  # grab points at cetera
        case Geometry.Biding.lines | Geometry.Biding.beams | Geometry.Biding.elements:  # only lines available
            check_collapse_for_objects(ctrl=ctrl, object_self=Geometry.Biding.lines)
        case Geometry.Biding.point_middle | Geometry.Biding.point_middle_normal | Geometry.Biding.points_and_lines:
            check_collapse_for_objects(ctrl=ctrl, object_self=Geometry.Biding.points)
            check_collapse_for_objects(ctrl=ctrl, object_self=Geometry.Biding.lines)
        case Geometry.Biding.points_boundary | Geometry.Biding.point_load | Geometry.Biding.line_load | \
             Geometry.Biding.joints:
            check_collapse_for_objects(ctrl=ctrl, object_self=Geometry.binding)
    Geometry.picked_frame = [(0, 0), (0, 0)]

    #correct_binding()


def release_moved_node(ctrl: bool = False):
    Geometry.regime = None
    if Geometry.moved_node is None:
        return None
    Geometry.moved_node.moved_node = False
    new_point_coord_0 = None
    if Geometry.point_under_cursor:  # merge the nodes (under cursor and moved node)
        new_point_coord_0: [float] = Geometry.point_under_cursor.coord_0
    elif Geometry.line_with_checked_middle_point:  # merge the nodes with middle of the line
        new_point_coord_0: [float] = Geometry.line_with_checked_middle_point.middle_point_coord_0
    elif Geometry.line_with_checked_normal_point:  # merge the nodes with middle of the line
        new_point_coord_0: [float] = Geometry.line_with_checked_middle_point.middle_point_coord_0

    if new_point_coord_0 is not None:
        copy_or_shift_objects_with_moved_node(old_point_coord_0=Geometry.moved_node.coord_0,
                                              new_point_coord_0=new_point_coord_0,
                                              ctrl=ctrl)
    set_none_to_old_objects()
    merge_points()

    correct_binding()


def set_none_to_old_objects():
    if Geometry.line_with_checked_normal_point:
        dict_to_change = {Geometry.line_with_checked_normal_point.hash_id: [Geometry.moved_node]}
        merge_the_line_with_point(dict_to_change=dict_to_change)
        Geometry.line_with_checked_normal_point.is_got = False
        Geometry.line_with_checked_normal_point = None
    if Geometry.line_with_checked_middle_point:
        dict_to_change = {Geometry.line_with_checked_middle_point.hash_id: [Geometry.moved_node]}
        merge_the_line_with_point(dict_to_change=dict_to_change)
        Geometry.line_with_checked_middle_point.is_got = False
        Geometry.line_with_checked_middle_point = None
    Geometry.moved_node.is_got = False
    Geometry.moved_node.moved_node = False
    Geometry.moved_node = None


def copy_or_shift_objects_with_moved_node(new_point_coord_0: [float],
                                          old_point_coord_0: [float],
                                          ctrl: bool = False):
    dx, dy, dz = (new_point_coord_0[0] - old_point_coord_0[0],
                  new_point_coord_0[1] - old_point_coord_0[1],
                  new_point_coord_0[2] - old_point_coord_0[2])
    objects_to_copy: set = set()
    if Variables.current_tab == Variables.tabs[0]:
        objects_to_copy = Geometry.picked_points
        objects_to_copy.add(Geometry.moved_node)
    elif Variables.current_tab == Variables.tabs[1]:
        objects_to_copy = Geometry.picked_lines

    if ctrl:
        copy_to(x=dx, y=dy, z=dz, objects_to_copy=objects_to_copy)
    else:
        shift_to(x=dx, y=dy, z=dz, objects_to_copy=objects_to_copy)


def middle_release(event, right_button: bool):
    Variables.animation.end_of_shift()
    if right_button:
        Geometry.df_dj = (0, 0)
    else:
        Geometry.dx_dy = (0, 0)


def pick_with_frame(x: int, y: int, ctrl: bool):
    """check - are the points picked by frame? """
    if ctrl is False:
        for point in Geometry.picked_points:
            point.is_got = False
        for line in Geometry.picked_lines:
            line.is_got = False
        Geometry.picked_points = set()
        Geometry.picked_lines = set()
    Geometry.picked_frame[1] = (x, y)
    x_min = min(Geometry.picked_frame[0][0], Geometry.picked_frame[1][0])
    x_max = max(Geometry.picked_frame[0][0], Geometry.picked_frame[1][0])
    y_min = min(Geometry.picked_frame[0][1], Geometry.picked_frame[1][1])
    y_max = max(Geometry.picked_frame[0][1], Geometry.picked_frame[1][1])

    match Geometry.binding:
        case Geometry.Biding.points:  # only points available
            Geometry.picked_points.update(picked_frame_for_points(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max))
            for key, point_i in Geometry.points.items():
                if point_i in Geometry.picked_points:
                    point_i.is_got = True
                else:
                    point_i.is_got = False
        case Geometry.Biding.lines | Geometry.Biding.points_and_lines:  # only lines available
            Geometry.picked_lines.update(picked_frame_for_lines(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max))
            for key, line_i in Geometry.lines.items():
                if line_i in Geometry.picked_lines:
                    line_i.is_got = True
                else:
                    line_i.is_got = False
    edit_lines_and_points_button_enabled()
    #correct_binding()


def picked_frame_for_points(x_min: float, x_max: float, y_min: float, y_max: float) -> set[Point]:
    new_picked_set = set()
    for key, point_i in Geometry.points.items():
        if x_min < point_i.real_coordinate[0] < x_max and y_min < point_i.real_coordinate[1] < y_max:
            new_picked_set.add(point_i)
    return new_picked_set


def picked_frame_for_lines(x_min: float, x_max: float, y_min: float, y_max: float) -> set[Line]:
    delta = Geometry.picked_frame[1][0] - Geometry.picked_frame[0][0]
    from_left_to_right = True if delta > 0 else False
    if from_left_to_right:
        return pick_up_lines_with_frame_from_left_to_right(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    else:
        return pick_up_lines_with_frame_from_right_to_left(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)


def pick_up_lines_with_frame_from_left_to_right(x_min: float, x_max: float, y_min: float, y_max: float) -> set[Line]:
    new_set_of_lines = set()
    for key, line_i in Geometry.lines.items():
        line_x_min = min(line_i.point_0.real_coordinate[0], line_i.point_1.real_coordinate[0])
        line_x_max = max(line_i.point_0.real_coordinate[0], line_i.point_1.real_coordinate[0])
        line_y_min = min(line_i.point_0.real_coordinate[1], line_i.point_1.real_coordinate[1])
        line_y_max = max(line_i.point_0.real_coordinate[1], line_i.point_1.real_coordinate[1])
        if x_min < line_x_min and line_x_max < x_max and y_min < line_y_min and line_y_max < y_max:
            line_i.is_got = True
            new_set_of_lines.add(line_i)
    return new_set_of_lines


def pick_up_lines_with_frame_from_right_to_left(x_min: float, x_max: float, y_min: float, y_max: float) -> set[Line]:
    set_of_lines = set()
    for key, point_i in Geometry.points.items():
        if x_min < point_i.real_coordinate[0] < x_max and y_min < point_i.real_coordinate[1] < y_max:
            set_of_lines.update(point_i.get_my_lines())

    new_set_of_lines = set()
    for hash_line_i in set_of_lines:
        line_i: Line = Geometry.lines[hash_line_i]
        new_set_of_lines.add(line_i)
    return new_set_of_lines


def shift(x: int, y: int):
    Geometry.dx_dy = (Geometry.dx_dy[0] + x - Geometry.x0y0[0],
                      Geometry.dx_dy[1] + y - Geometry.x0y0[1])
    Geometry.x0y0 = x, y


def rotate(x: int, y: int):
    Geometry.df_dj = (Geometry.df_dj[0] + (x - Geometry.x0y0[0]) * 0.01,
                      Geometry.df_dj[1] - (y - Geometry.x0y0[1]) * 0.01)
    Geometry.x0y0 = x, y


def start_regime_to_move_node(event):
    Geometry.moved_node = Geometry.point_under_cursor
    Geometry.moved_node.moved_node = True
    Geometry.regime = Geometry.Regime.edit_with_moved_node
    Geometry.binding = Geometry.Biding.point_middle_normal


def start_regime_to_move_line(event, ctrl: bool):
    Geometry.moved_node = Geometry.point_under_cursor
    Geometry.moved_node.moved_node = True
    Geometry.regime = Geometry.Regime.edit_lines_with_moved_node
    Geometry.binding = Geometry.Biding.point_middle_normal


def delete_picked_set():
    """the function works by key 'del'"""
    if Variables.current_tab == Variables.tabs[0]:  # geometry
        if Variables.current_tab_geometry == Variables.tabs_geometry[0]:  # only points available
            delete_points(set_to_delete=Geometry.picked_points)
        elif Variables.current_tab_geometry == Variables.tabs_geometry[1]:  # lines
            delete_lines(set_to_delete=Geometry.picked_lines)
        elif Variables.current_tab_geometry == Variables.tabs_geometry[2]:  # surfaces
            delete_surfaces(set_to_delete=Geometry.picked_surfaces)
    elif Variables.current_tab == Variables.tabs[1]:  # only lines elements
        if Variables.current_tab_element == Variables.tabs_element[0]:  # sections
            delete_sections(set_to_delete=Geometry.picked_sections)
        elif Variables.current_tab_element == Variables.tabs_element[1]:  # joint
            delete_joints(set_to_delete=Geometry.picked_joints)
    elif Variables.current_tab == Variables.tabs[2]:  # only points boundary conditions
        delete_a_point_from_boundary_conditions(set_to_delete=Geometry.picked_boundary)
    elif Variables.current_tab == Variables.tabs[3]:  # loads
        if Variables.current_tab_loads == Variables.tabs_loads[0]:  # point loads
            delete_point_loads(set_to_delete=Geometry.picked_point_loads)
        elif Variables.current_tab_loads == Variables.tabs_loads[1]:  # line loads
            delete_line_loads(set_to_delete=Geometry.picked_line_loads)
        elif Variables.current_tab_loads == Variables.tabs_loads[2]:  # influence line
            pass
