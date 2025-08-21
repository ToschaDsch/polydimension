from geometry.class_geometry_change_point import GeometryChangePoint
from variables.graphics import ObjectToDraw


def add_all_draw_objects_to_the_dict(list_of_all_objects: list[ObjectToDraw],
                                     geometry: GeometryChangePoint):
    for draw_object in list_of_all_objects:
        geometry.add_the_draw_element_to_sorted_dict(draw_object=draw_object)