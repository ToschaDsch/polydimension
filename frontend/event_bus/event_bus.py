# event_bus.py

from collections import defaultdict
import inspect


class EventBus:

    def __init__(self):
        self._subscribers = defaultdict(list)

    def publish(self, event):

        for handler in self._subscribers[type(event)]:
            handler(event)

    def register(self, obj):

        for _, method in inspect.getmembers(obj, inspect.ismethod):

            if not getattr(method, "_subscribe", False):
                continue

            sig = inspect.signature(method)

            params = list(sig.parameters.values())

            if len(params) != 1:
                raise ValueError("Handler must have exactly one parameter")

            event_type = params[0].annotation

            self._subscribers[event_type].append(method)