from geometry.class_geometry_change_point import GeometryChangePoint
from objects.class_draw_interface import DrawObject


def add_all_draw_objects_to_the_dict(list_of_all_objects: list[DrawObject],
                                     geometry: GeometryChangePoint):
    for draw_object in list_of_all_objects:
        for element in draw_object.get_geometric_objects():
            geometry.add_the_draw_element_to_sorted_dict(draw_object=element)