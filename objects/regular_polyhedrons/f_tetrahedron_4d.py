import numpy as np

from frontend.event_bus.event_bus import EventBus
from geometry.class_line import Line
from geometry.class_point import Point
from objects.class_draw_interface import NDimensionalObject
from objects.regular_polyhedrons.e_tetrahedron_3d import Tetrahedron3d
from variables.class_state import MyState


class Tetrahedron4d(NDimensionalObject):

    def __init__(self, state: MyState, bus: EventBus, dimensions: int=4, dz: float=0,
                 colorful: bool = False, size: float=2.0,
                 init_point: list[int]=None):
        self._init_points = init_point if init_point else [0, 1, 2]
        super().__init__(dimensions=dimensions, dz=dz,
                         colorful=colorful, size=size, bus=bus, state=state)
        self.name_of_the_object = "16Cell 4d"
        print(self)
        print(len(self._my_surfaces))

    def make_points(self):
        w, h = self.dimensions, self.dimensions
        init_coordinate = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(0, self.dimensions):
            init_coordinate[i][i] = self.size

        point_0 = np.array([0 for _ in range(self.dimensions)], dtype=np.float64)
        self._my_points.append(Point(coordinates=point_0, bus=self.bus,state=self.state))
        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(coord_i, dtype=np.float64), bus=self.bus, state=self.state))
        self.points_to_show = self._my_points.copy()


    def make_lines(self):
        for i in range(len(self._my_points)):
            for j in range(i + 1, len(self._my_points)):
                self._my_lines.append(Line(point_0=self._my_points[i],
                                           point_1=self._my_points[j], width=2, bus=self.bus))

    def make_surfaces(self):
        pass        # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make an octahedron in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        init_spaces = ([1, 2, 3],
                       [0, 1, 3],
                       [0, 2, 3],
                       [0, 1, 2])
        for list_of_init_spaces in init_spaces:
            octa_i = Tetrahedron3d(dimensions=4, init_point=list_of_init_spaces, bus=self.bus, state=self.state)
            volume_i = self._get_a_volume_surfaces_and_points_form_another_object(obj=octa_i)
            self._my_volumes.append(volume_i)

