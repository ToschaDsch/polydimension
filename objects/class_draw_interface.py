import functools
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from geometry.geometry_functions import get_center_from_list_of_points
from menus.single_functions import open_and_read_a_file, parce_html_with_arrays
from variables.geometry_var import CoordinatesScreen
from variables.graphics import Transparency, MyColors, default_palette
from variables.menus import Menus


@dataclass
class JSONData:
    points: list[float|int] = None
    lines: list[list[int]] = None
    surfaces: list[list[int]] = None
    volumes: list[int] = None

class NDimensionalObject(ABC):
    def __init__(self, dimensions: int = 4,
                 size: float = CoordinatesScreen.init_size_of_the_object,
                 line_color: QColor=None, colorful: bool = False, raw_data_path: str = None):
        self.dimensions = dimensions
        self.draw_with_normal = False            # normal on/ off
        self.points_to_show: list[Point] = []
        self._my_points: list[Point] = []
        self._my_lines: list[Line] = []
        self._my_surfaces: list[Surface] = []
        self._my_volumes: list[Volume] = []
        self._solid: bool = True
        self._transparent: bool = True
        self.line_color: QColor = line_color if line_color else QColor(*MyColors.default_line_color)
        self.size: float = size
        self.name_of_the_object: str = "Noname"
        self.json_data = dict()
        if raw_data_path is None:
            self.make_geometry()    # name the property self
        else:
            self.load_from_json(raw_data_path)  # load property form file
        self.change_color(colorful=colorful)
        self.z_min = self.get_z_min()
        self._send_normals_from_surfaces()

    def load_from_json(self, raw_data_path: str):
        path = Menus.raw_data_path + "//" + raw_data_path
        raw_data = open_and_read_a_file(path=path)
        typ_of_file = path.split(".")[-1]
        details_of_the_objects = dict()
        if typ_of_file == "txt":
            details_of_the_objects = json.loads(raw_data)
        elif typ_of_file == "html":
            print("html")
            result = parce_html_with_arrays(raw_str=path)
            self.json_data = JSONData(points=[],
                                      lines=result["lines_600_cell"],
                                      surfaces=result["surfaces_600_cell"],
                                      volumes=[], )
            return None
        else:
            print("cant read the file")
        self.json_data = JSONData(points=details_of_the_objects["points"],
                                  lines=details_of_the_objects["edges"],
                                  surfaces=details_of_the_objects["surfaces"],
                                  volumes=details_of_the_objects["volumes"],)
        for coord in self.json_data.points:
            self._my_points.append(Point(coordinates=self.size*np.array(coord)))
        self.points_to_show = self._my_points.copy()
        center = get_center_from_list_of_points(list_of_points=self._my_points)
        for i, j in self.json_data.lines:
            self._my_lines.append(Line(point_0=self._my_points[i], point_1=self._my_points[j]))
        for list_of_points_i in self.json_data.surfaces:
            list_of_points_i = [self._my_points[i] for i in list_of_points_i]
            self._my_surfaces.append(Surface(list_of_points=list_of_points_i, init_center_of_the_volume=center))

    def get_surfaces(self) -> list[Surface]:
        return self._my_surfaces

    def get_z_min(self):
        return functools.reduce(lambda x, y: min(x.coord_0[2] if isinstance(x, Point) else x, y.coord_0[2]), self._my_points, 0)

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._transparent = value
        for surface in self._my_surfaces:
            surface.transparent = value

    def make_geometry(self):
        self.make_points()
        self.make_lines()
        self.make_surfaces()
        self.make_volumes()

    def _send_normals_from_surfaces(self):
        for surface in self._my_surfaces:
            if self.draw_with_normal:
                self._my_lines.append(surface.normal_line)
                self._my_points.append(surface.normal_line.point_0)
                self._my_points.append(surface.normal_line.point_1)
            self._my_points.append(surface.normal)
            self._my_points.append(surface.center)

    @abstractmethod
    def make_points(self):
        pass

    @abstractmethod
    def make_lines(self):
        pass

    @abstractmethod
    def make_surfaces(self):
        pass
    @abstractmethod
    def make_volumes(self):
        pass

    def change_color(self, colorful: bool=True):
        if colorful:
            list_of_colors = default_palette
        else:
            list_of_colors = 100*[MyColors.default_surface_color]

        if len(self._my_volumes):
            color_elements = self._my_volumes
        elif len(self._my_surfaces):
            color_elements = self._my_surfaces
        else:
            color_elements = []

        for i, color_element in enumerate(color_elements):
            if i > len(list_of_colors) - 1:
                #  random color
                number = np.random.choice(range(256), size=3)
                color = QColor(*number)
            else:
                color = QColor(*list_of_colors[i])
            color_element.color = color

    def init_geometry(self) -> None:
        pass

    @property
    def solid(self)->bool:
        return self._solid

    @solid.setter
    def solid(self, solid: bool):
        self._solid = solid

    def get_geometric_objects(self, transparency: int = Transparency.transparent) \
            -> list[Line] | list[Surface] | list[Volume] | None:
        if not self._solid:
            return self._my_lines

        objects_with_area = self._my_volumes if len(self._my_volumes) else self._my_surfaces

        match transparency:
            case Transparency.full:
                return objects_with_area
            case Transparency.sceleton:
                return self._my_lines
            case Transparency.transparent:
                return objects_with_area + self._my_lines
            case _:
                print("there is no case for transparency")
                return None


    def __str__(self):
        list_of_points: list[str] = [str(x) for x in self._my_points]
        list_of_lines: list[str] = [str(x) for x in self._my_lines]
        list_of_surfaces: list[str] = [str(x) for x in self._my_surfaces]
        return (f"i'm {self.name_of_the_object}, \n"
                f"I have {self.dimensions} dimensions\n"
                f"my points: {len(list_of_points)} {list_of_points}\n"
                f"my lines: {len(list_of_lines)} {list_of_lines}\n"
                f"my surfaces: {list_of_surfaces}\n"
                f"my volumes: {self._my_volumes}\n")

    def update_lighting_for_all_surfaces(self):
        for surface in self._my_surfaces:
            surface.change_coordinate()

    def _get_a_volume_surfaces_and_points_form_another_object(self, obj) -> Volume:
        """the function get an NDimensionalObject object,
        take all surfaces of it, send all important points to self._my_points"""
        list_of_surfaces = obj.get_surfaces()
        for surface in list_of_surfaces:
            for point_i in surface.list_of_points:
                if point_i in self._my_points:
                    continue
                for point_j in self._my_points:
                    if np.array_equal(point_i.coord_0, point_j.coord_0):
                        index = surface.list_of_points.index(point_i)
                        surface.list_of_points[index] = point_j
                        continue
        return Volume(list_of_points=None, list_of_lines=None, list_of_surfaces=list_of_surfaces)
