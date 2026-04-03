import numpy as np

from frontend.event_bus.event_bus import EventBus
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points
from objects.class_draw_interface import NDimensionalObject
from variables.graphics import Transparency


class Tetrahedron3d(NDimensionalObject):

    def __init__(self,bus: EventBus, dimensions: int=4, dz: float = 0,
                 colorful: bool = False, size: float = 2,
                 init_point: list[int]=None,
                 transparent: Transparency=Transparency.transparent):
        self._init_points: list[int] = init_point if init_point else [0, 1, 2]
        super().__init__(dimensions=dimensions, dz=dz,
                         colorful=colorful, size=size, transparent=transparent, bus=bus)
        self.name_of_the_object = "Tetrahedron 3d"
        print(self)

    def make_points(self):
        w, h = self.dimensions, 3
        init_coordinate = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(0, 3):
            init_coordinate[i][self._init_points[i]] = self.size

        point_0 = np.array([0 for _ in range(self.dimensions)], dtype=np.float64)
        self._my_points.append(Point(coordinates=point_0, bus=self.bus))
        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(coord_i, dtype=np.float64), bus=self.bus))
        self.points_to_show = self._my_points.copy()


    def make_lines(self):
        for i in range(len(self._my_points)):
            for j in range(i + 1, len(self._my_points)):
                self._my_lines.append(Line(point_0=self._my_points[i],
                                           point_1=self._my_points[j], width=2, bus=self.bus))

    def make_surfaces(self):
        center = Point(coordinates=get_center_from_list_of_points(self._my_points), bus=self.bus)
        list_of_points = [[0, 1, 2],
                          [0, 2, 3],
                          [0, 3, 1],
                          [1, 2, 3]]
        for list_i in list_of_points:
            list_of_point = [self._my_points[i] for i in list_i]
            self._my_surfaces.append(Surface(list_of_points=list_of_point,
                                         init_center_of_the_volume=center, bus=self.bus))

    def make_volumes(self):
        pass



