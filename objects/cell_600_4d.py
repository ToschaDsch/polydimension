from objects.class_draw_interface import NDimensionalObject


class Cell6004d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None):
        raw_data_path = "arrays_600_cell.html"
        super().__init__(dimensions=dimensions, colorful=colorful, size=size, raw_data_path=raw_data_path)
        self.name_of_the_object = "cell 600 4d"


    def make_points(self):
        """{
        /** the function makes all vertex coordinates for the object
         *
         */
        val symbols = arrayOf(0.5f * a * c, 0.5f * a, 0.5f * a / c, 0f)
        var icosians = onlyEvenPermutations(symbols = symbols)
        for (i in 0..3) {
            icosians = mirrorIt(oldList = icosians, axis = i)
        }
        val coordinate2 = addTetrahedron(icosians)
        val coordinate3 = add16coordinates(coordinate2)
        verticesOf600Cell = makeItWithPoint(
            correctHeightOfCoordinates(coordinate3)
        )
        currentVerticesCoordinate =
            Array(verticesOf600Cell.size) { Array(howDimensionWeHave) { 0f } }
        currentVerticesCoordinate2D = Array(verticesOf600Cell.size) { floatArrayOf(0f, 0f) }
    }
"""


    def make_lines(self):
        pass


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass