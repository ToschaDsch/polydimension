from objects.class_draw_interface import NDimensionalObject


class Cell24Snub4d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None):
        raw_data_path = "cell_24_snub.txt"
        super().__init__(dimensions=dimensions, colorful=colorful, size=size, raw_data_path=raw_data_path)
        self.name_of_the_object = "cell 24 snub 4d"


    def make_points(self):
        pass


    def make_lines(self):
        pass


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass