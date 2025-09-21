from geometry.class_geometry_change_point import GeometryChangePoint
from objects.class_draw_interface import NDimensionalObject
from variables.graphics import Transparency


def add_all_draw_objects_to_the_dict(list_of_all_objects: list[NDimensionalObject],
                                     geometry: GeometryChangePoint, transparency: int = Transparency.transparent):
    for draw_object in list_of_all_objects:
        for element in draw_object.get_geometric_objects(transparency=transparency):
            geometry.add_the_draw_element_to_sorted_dict(draw_object=element)