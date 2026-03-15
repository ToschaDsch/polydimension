from PySide6 import QtGui, QtCore
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from frontend.event_bus.decorators import subscribe
from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawPoint, DrawPointText, DrawLine, DrawCircle, DrawPolygon, \
    DrawAllPrimitives
from graphic.functions_for_screen_window import rotate_the_object, shift_the_object, left_release, right_release, \
    start_shift, start_to_rotate
from variables.geometry_var import CoordinatesScreen
from variables.menus import Menus


def change_brush_and_pen(painter: QPainter=None, brush: QtGui.QBrush=None, pen: QtGui.QPen=None):
    if brush and pen:
        painter.setBrush(brush)
        painter.setPen(pen)


class ScreenWindow(QWidget):
    """the window shows the model and graphic"""

    def __init__(self, bus: EventBus):
        super().__init__()
        self._right_button = False
        self._middle_button = False
        self._ctrl: bool = False  # is ctrl pressed
        self.setMouseTracking(True)
        self.shapes = []
        bus.register(self)

    def resizeEvent(self, event):
        #Menus.screen_width, Menus.screen_height = self.geometry()
        return
        canvas = self.scaled(Menus.window_width, Menus.window_height)
        self.setPixmap(canvas)
        self.draw_all()

    @subscribe
    def draw_a_point(self, event: DrawPoint):
        self.shapes.append(event)

    @subscribe
    def draw_a_point_text(self, event: DrawPointText):
        self.shapes.append(event)

    @subscribe
    def draw_a_line(self, event: DrawLine):
        self.shapes.append(event)

    @subscribe
    def draw_a_circle(self, event: DrawCircle):
        self.shapes.append(event)

    @subscribe
    def draw_a_polygon(self, event: DrawPolygon):
        self.shapes.append(event)

    def mouseMoveEvent(self, event):
        match event.buttons():
            case QtCore.Qt.MouseButton.NoButton:
                #  the function checks collapse by mouse motion
                pass
            case QtCore.Qt.MouseButton.RightButton|QtCore.Qt.MouseButton.MiddleButton:
                rotate_the_object(x=event.x(), y=event.y())
                self.draw_all()
            case QtCore.Qt.MouseButton.LeftButton:
                shift_the_object(x=event.x(), y=event.y())
                self.draw_all()
            case QtCore.Qt.MouseButton.RightButton:
                pass
            case QtCore.Qt.MouseButton.MiddleButton:
                pass

    def mouseDoubleClickEvent(self, event):
        print("mause_double_click")

    def mouseReleaseEvent(self, event):
        match event.button():
            case QtCore.Qt.MouseButton.LeftButton:
                left_release(x=event.x(), y=event.y())
            case QtCore.Qt.MouseButton.MiddleButton:
                pass
                #middle_release(event, right_button=self._right_button)
                self._middle_button = False
            case QtCore.Qt.MouseButton.RightButton:
                right_release(x=event.x(), y=event.y())

    def mousePressEvent(self, event):
        match event.buttons():
            case QtCore.Qt.MouseButton.LeftButton:
                start_shift(x=event.x(), y=event.y())
            case QtCore.Qt.MouseButton.MiddleButton:
                pass
            case QtCore.Qt.MouseButton.RightButton:
                start_to_rotate(x=event.x(), y=event.y())

    def keyPressEvent(self, event):
        match event.key():
            case QtCore.Qt.Key.Key_Control:
                pass
            case QtCore.Qt.Key.Key_Delete:
                pass
            case QtCore.Qt.Key.Key_Escape | QtCore.Qt.Key.Key_Enter:
                pass


    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control:
            self._ctrl = False

    def wheelEvent(self, event):
        """MOUSEWHEEL:"""
        ds = int(event.angleDelta().y())
        CoordinatesScreen.scale +=0.05*ds
        self.draw_all(scale=CoordinatesScreen.scale)

    @subscribe
    def draw_all(self, event: DrawAllPrimitives):
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)

        for shape in self.shapes:
            if isinstance(shape, DrawPoint):
                change_brush_and_pen(pen=shape.pen, brush=shape.brush, painter=painter)
                if shape.radius == 0:
                    painter.drawEllipse((shape.x, shape.y))
                else:
                    painter.drawEllipse(int(shape.x - shape.radius),
                                             int(shape.y - shape.radius),
                                             2 * shape.radius, 2 * shape.radius)
            elif isinstance(shape, DrawPointText):
                painter.drawText(shape.x0_y0[0] + 8, shape.x0_y0[1] + 8, shape.text)
            elif isinstance(shape, DrawLine):
                change_brush_and_pen(pen=shape.pen, brush=shape.brush, painter=painter)
                painter.drawLine(shape.x1, shape.y1, shape.x2, shape.y2)
            elif isinstance(shape, DrawCircle):
                painter.drawEllipse(int(shape.x - shape.r), int(shape.y - shape.r), 2 * shape.r, 2 * shape.r)
            elif isinstance(shape, DrawPolygon):
                change_brush_and_pen(pen=shape.pen, brush=shape.brush, painter=painter)
                painter.drawPolygon(shape.polygon)
        self.shapes = []


