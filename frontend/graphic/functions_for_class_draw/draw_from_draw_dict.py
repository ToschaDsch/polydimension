from PySide6.QtCore import QPoint
from PySide6.QtGui import QPolygon
from sortedcontainers import SortedDict

import geometry.class_point
from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawAllPrimitives, DrawPolygon, DrawPointText, DrawLine, DrawPoint
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_text import TextDraw
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from variables.graphics import Transparency


def draw_from_dict(
        bus: EventBus, dick_of_draw_objects: SortedDict,
                    transparency: Transparency = Transparency.transparent):
    """it is general function of the module.
    the function becomes objects from dict show.
    in the dict all objects are sorted in z direction.
    the function makes parameters and sends the objects to draw"""
    for key, draw_object in dick_of_draw_objects.items():
        match type(draw_object):
            case geometry.class_point.Point:
                draw_a_point(point=draw_object, radius=draw_object.radius, bus=bus)
            case geometry.class_text.TextDraw:
                coord_n = draw_object.self_object[0].coord_n
                x_y = (-coord_n[0],
                       coord_n[1])
                draw_a_text(x0_y0=x_y, text=draw_object, bus=bus)
            case geometry.class_line.Line:
                draw_a_line(line=draw_object, bus=bus)
            case geometry.class_surface.Surface:
                if transparency == Transparency.full and draw_object.visible is False:
                    continue
                draw_a_surface(surface=draw_object, bus=bus)
            case geometry.class_volume.Volume:
                draw_a_volume(volume=draw_object, bus=bus)
            case _:
                print('object is not found')
    bus.publish(DrawAllPrimitives())


def draw_a_volume(volume: Volume, bus: EventBus):
    for surface in volume.list_of_surfaces:
        draw_a_surface(surface=surface, bus=bus)


def draw_a_surface(surface: Surface, bus: EventBus):
    polygon = QPolygon()
    for point_i in surface.list_of_points:
        coord = point_i.coord_n
        polygon.append(QPoint(int(coord[0]), int(coord[1])))
    bus.publish(DrawPolygon(brush=surface.brush,
                          polygon=polygon,
                          pen=surface.pen))


def draw_a_text(x0_y0, text: str, bus: EventBus):
    bus.publish(DrawPointText(x0_y0=x0_y0, text=text))


def draw_a_line(line: Line, bus: EventBus):
    x1 = int(line.point_0.coord_n[0])
    y1 = int(line.point_0.coord_n[1])
    x2 = int(line.point_1.coord_n[0])
    y2 = int(line.point_1.coord_n[1])
    bus.publish(DrawLine(x1=x1, y1=y1, x2=x2, y2=y2,
                         brush=line.brush, pen=line.pen))


def draw_a_point(bus: EventBus, point: Point, radius: int=2):
    x0_y0 = point.coord_n
    bus.publish(DrawPoint(x=int(x0_y0[0]), y=int(x0_y0[1]), radius=radius,
                                     brush=point.brush, pen=point.pen))



