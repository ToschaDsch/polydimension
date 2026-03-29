from sortedcontainers import SortedDict

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawAllPrimitives
from variables.graphics import Transparency


def draw_from_dict(
        bus: EventBus, dick_of_draw_objects: SortedDict,
                    transparency: Transparency = Transparency.transparent):
    """it is general function of the module.
    the function becomes objects from dict show.
    in the dict all objects are sorted in z direction.
    the function makes parameters and sends the objects to draw"""
    for key, draw_object in dick_of_draw_objects.items():
        draw_object.draw_me()
    bus.publish(DrawAllPrimitives())
