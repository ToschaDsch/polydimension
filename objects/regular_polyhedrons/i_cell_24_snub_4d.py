from frontend.event_bus.event_bus import EventBus
from objects.class_draw_interface import NDimensionalObject
from variables.graphics import Transparency


class Cell24Snub4d(NDimensionalObject):

    def __init__(self, bus: EventBus, dimensions: int = 4, dz: float = 0,
                 colorful: bool = False, size: float=1.0, raw_data: str = None,
                 transparent: Transparency=Transparency.transparent):
        raw_data_path = "cell_24_snub.txt"
        super().__init__(dimensions=dimensions, dz=dz,
                         colorful=colorful, size=size, raw_data_path=raw_data_path, bus=bus)
        self.name_of_the_object = "cell 24 snub 4d"
        print(self)

    def make_points(self):
        pass


    def make_lines(self):
        pass


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass