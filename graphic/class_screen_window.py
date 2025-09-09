from PySide6 import QtGui, QtCore
from PySide6.QtGui import QColor, QFont, QPolygonF, QPixmap, QPen, QBrush
from PySide6.QtWidgets import QLabel

from graphic.functions_for_screen_window import rotate_the_object, shift_the_object, left_release, right_release, \
    start_shift, start_to_rotate
from variables.geometry_var import CoordinatesScreen
from variables.graphics import MyColors
from variables.menus import Menus


class ScreenWindow(QLabel):
    """the window shows the model and graphic"""

    def __init__(self, canvas: QPixmap, parent=None):
        super().__init__(parent)
        self._right_button = False
        self._middle_button = False
        self._ctrl: bool = False  # is ctrl pressed
        # make parent a label + self
        self.canvas = QtGui.QPixmap(Menus.display_width, Menus.display_height)
        self.setPixmap(self.canvas)
        self.my_size = self.canvas.size()
        self.painter = QtGui.QPainter(self.canvas)
        font = QFont('Century Gothic', 10)
        self.painter.setFont(font)

        self.pen = QPen()
        self.brush = QBrush()
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)
        self.canvas.fill(QColor(*MyColors.general_screen))
        self.setMouseTracking(True)

    def resizeEvent(self, event):
        #Menus.screen_width, Menus.screen_height = self.geometry()
        canvas = self.canvas.scaled(Menus.window_width, Menus.window_height)
        self.setPixmap(canvas)
        self.draw_all()

    def draw_a_point(self, x: int = 0, y: int = 0, radius: int=2):
        if radius == 0:
            self.painter.drawEllipse((x, y))
        else:
            self.painter.drawEllipse(int(x - radius), int(y - radius), 2 * radius, 2 * radius)


    def draw_a_point_text(self, x0_y0, text: str):
        self.painter.drawText(x0_y0[0] + 8, x0_y0[1] + 8, text)


    def draw_a_line(self, x1: int, y1: int, x2: int, y2: int, color=None):
        """if color:
            self.brush.setColor(color)
            self.pen.setColor(color)
            self.pen.setWidth(3)
            self.pen.setBrush(self.brush)
            self.painter.setPen(self.pen)
            self.painter.setBrush(self.brush)"""
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_a_circle(self, x: int, y: int, r: int, type_of_line: str = None):
        self.painter.drawEllipse(int(x - r), int(y - r), 2 * r, 2 * r)

    def draw_a_polygon(self, polygon: QPolygonF):
        self.painter.drawPolygon(polygon)

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
        ds = int(event.angleDelta())
        CoordinatesScreen.scale =+0.1*ds
        self.draw_all()

    def draw_all(self):
        canvas = QtGui.QPixmap(self.my_size)
        canvas.fill(QColor(*MyColors.general_screen))
        self.painter = QtGui.QPainter(canvas)
        Menus.animation.draw_all()
        self.painter.end()
        self.setPixmap(canvas)




