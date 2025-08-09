class Point:
    def __init__(self, coordinates: list[float] = None):
        self._coordinates = coordinates if coordinates is not None else [0.0, 0.0, 0.0, 0.0]
        self.coord_n = self._coordinates

    @property
    def coord_0(self) -> list[float]:
        return self._coordinates

    @coord_0.setter
    def coord_0(self, coordinates: list[float]):
        self._coordinates = coordinates