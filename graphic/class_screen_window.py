from PySide6 import QtGui, QtCore
from PySide6.QtGui import QColor, QFont, QPolygonF, QPixmap, QPen
from PySide6.QtWidgets import QLabel

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
        self.canvas = canvas
        self.label = QLabel(self)
        print("label", self)
        self.setPixmap(self.canvas)
        self.painter = QtGui.QPainter(self.canvas)
        font = QFont('Century Gothic', 10)
        self.painter.setFont(font)

        pen = QPen()
        self.painter.setPen(pen)
        self.canvas.fill(QColor(*MyColors.general_screen))
        self.setPixmap(self.canvas)
        self.setMouseTracking(True)

    def resizeEvent(self, event):
        #Menus.screen_width, Menus.screen_height = self.geometry()
        canvas = self.canvas.scaled(Menus.screen_width, Menus.screen_height)
        self.setPixmap(canvas)

    def draw_a_point(self, x: int = 0, y: int = 0, radius: int=2):
        if radius == 0:
            self.painter.drawEllipse((x, y))
        else:
            self.painter.drawEllipse(int(x - radius), int(y - radius), 2 * radius, 2 * radius)


    def draw_a_point_text(self, x0_y0, text: str):
        self.painter.drawText(x0_y0[0] + 8, x0_y0[1] + 8, text)


    def draw_a_line(self, x1: int, y1: int, x2: int, y2: int):
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_a_circle(self, x: int, y: int, r: int, type_of_line: str = None):
        self.painter.drawEllipse(int(x - r), int(y - r), 2 * r, 2 * r)

    def draw_a_polygon(self, polygon: QPolygonF, type_of_line: str, color=QColor(50, 50, 50)):
        self.painter.drawPolygon(polygon)

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent", event.buttons)
        match str(event.buttons()):
            case 'MouseButton.NoButton':
                #  the function checks collapse by mouse motion

                pass
            case 'MouseButton.RightButton|MiddleButton':
                #rotate(x=event.x(), y=event.y())
                pass
            case 'MouseButton.LeftButton':
                self.move_left_button(event)
            case 'MouseButton.RightButton':
                pass
            case 'MouseButton.MiddleButton':
                pass
                #shift(x=event.x(), y=event.y())

        self.draw_all()

    def move_left_button(self, event):
        print(event.x(), event.y())
        self.draw_all()

    def mousePressEvent(self, event):
        print(event.x(), event.y())
        self.draw_all()

    def mouseDoubleClickEvent(self, event):
        print("mause_double_click")

    def mouseReleaseEvent(self, event):
        match event.button():
            case QtCore.Qt.MouseButton.LeftButton:
                pass
                #left_release(event=event, ctrl=self._ctrl)
            case QtCore.Qt.MouseButton.MiddleButton:
                pass
                #middle_release(event, right_button=self._right_button)
                self._middle_button = False
            case QtCore.Qt.MouseButton.RightButton:
                self._right_button = False
        self.draw_all()



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
        ds = event.angleDelta()
        print(ds)
        self.draw_all()

    def draw_all(self):
        canvas = self.pixmap()
        canvas.fill(QColor(*MyColors.general_screen))
        self.painter = QtGui.QPainter(canvas)
        #Menus.animation.draw_all(dx_dy=CoordinatesScreen.dx_dy, df_dj=CoordinatesScreen.df_dj)
        self.painter.end()
        self.setPixmap(canvas)




