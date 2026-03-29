from dataclasses import dataclass

from PySide6.QtGui import QColor

from variables.graphics import InitLight


@dataclass
class SourceOfLight:
    coordinate: tuple = InitLight.coordinate
    intensity: float = InitLight.intensity
    color: QColor = InitLight.color