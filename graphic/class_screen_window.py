from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QIcon, QAction, QPolygonF
from PySide6.QtWidgets import QMenu, QApplication, QLabel

from graphic.functions_for_screen_window import shift, pick_with_frame, rotate, check_collapse, \
    start_shift, start_to_rotate, left_click, left_release, middle_release, start_regime_to_move_node, \
    start_regime_to_move_line, delete_picked_set


class Draw:
    """the window shows the model and graphic"""

    def __init__(self, parent=None):
        self._right_button = False
        self._middle_button = False
        self._ctrl: bool = False  # is ctrl pressed

        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()

        self.canvas = QtGui.QPixmap(Variables.screen_BH[0], Variables.screen_BH[1])
        self.label.setPixmap(self.canvas)
        # self.canvas = self.canvas.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.painter = QtGui.QPainter(self.canvas)
        font = QFont('Century Gothic', 10)
        self.painter.setFont(font)

        pen = QtGui.QPen(QtGui.QBrush(QColor(100, 50, 55)), 5)
        self.pen_points = QtGui.QPen(QtGui.QBrush(Variables.MyColors.points), 5)
        self.pen_lines = QtGui.QPen(QtGui.QBrush(Variables.MyColors.lines), 0)
        self.pen_temporary_surface = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_frame_fill), 1)
        self.brush_temporary_surface = QtGui.QBrush(Variables.MyColors.picked_frame_fill)
        self.selected_pen = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_line), 1)
        self.selected_brush = QtGui.QBrush(Variables.MyColors.picked_frame_fill)
        self.pen_surface = QtGui.QPen(QtGui.QBrush(Variables.MyColors.surfaces), 1)
        self.brush_surface = QtGui.QBrush(Variables.MyColors.surfaces)
        self.pen_axes = QtGui.QPen(QtGui.QBrush(Variables.MyColors.axes), 0)
        self.pen_selected_points = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_points), 5)
        self.pen_selected_lines = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_points), 1)
        self.brush_selected = QtGui.QBrush(QtGui.QBrush(Variables.MyColors.picked_fill))
        self.pen_selected_lines.setBrush(self.brush_selected)
        self.pen_frame_around_a_point = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_points), 0)
        self.brush_frame = QtGui.QBrush(Variables.MyColors.picked_frame_fill)
        self.pen_picked_frame = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_line), 0)
        self.pen_doted = QtGui.QPen(QtGui.QBrush(Variables.MyColors.picked_points), 0)
        self.pen_doted.setStyle(Qt.DashDotLine)
        self.pen_solid = QtGui.QPen(QtGui.QBrush(Variables.MyColors.points), 1)
        self.brush_boundary_condition = QtGui.QBrush(Variables.MyColors.boundary_condition)
        self.pen_boundary_conditions = QtGui.QPen(QtGui.QBrush(Variables.MyColors.boundary_condition_line), 2)
        self.pen_boundary_conditions_surface = QtGui.QPen(QtGui.QBrush(Variables.MyColors.boundary_condition_line), 0)
        self.combine_beam = QtGui.QPen(QtGui.QBrush(Variables.MyColors.black), 1)
        self.combine_beam.setStyle(Qt.DashDotLine)

        self.painter.setPen(pen)
        self.canvas.fill(Variables.MyColors.general_screen)
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)

        # Create the context menu and add some actions
        self.context_menu = QMenu(self)
        self.menu_item_copy = QAction(QIcon('../icons/copy.png'), TextTranslation.copy_shift.text, self)
        self.menu_item_copy.triggered.connect(self.copy_objects)
        self.context_menu.addAction(self.menu_item_copy)

        self.menu_item_rotate = QAction(QIcon('../icons/rotate.png'), TextTranslation.rotate.text, self)
        self.menu_item_rotate.triggered.connect(rotate_points)
        self.context_menu.addAction(self.menu_item_rotate)

        self.menu_item_mirror = QAction(QIcon('../icons/mirror.png'), TextTranslation.mirror.text, self)
        self.menu_item_mirror.triggered.connect(self.mirror_objects)
        self.context_menu.addAction(self.menu_item_mirror)

        self.menu_item_delete = QAction(QIcon('../icons/garbage.png'), TextTranslation.delete.text, self)
        self.menu_item_delete.triggered.connect(delete_points)
        self.context_menu.addAction(self.menu_item_delete)

        self.menu_divide = QAction(QIcon('../icons/part.png'), TextTranslation.divide.text, self)
        self.menu_divide.triggered.connect(Variables.divide_menu.start_lines)
        self.context_menu.addAction(self.menu_divide)

        self.menu_item_info = QAction(QIcon('../icons/info.png'), f'info', self)
        self.menu_item_info.triggered.connect(self.objects_info)
        self.context_menu.addAction(self.menu_item_info)
        self.show()

    def resizeEvent(self, event):
        Variables.screen_BH = (self.width(), self.height())
        canvas = self.canvas.scaled(self.width(), self.height())
        self.label.setPixmap(canvas)
        self.label.resize(self.width(), self.height())



    def draw_a_point(self, x: int = 0, y: int = 0, type_of_point: str = 'normal'):
        match type_of_point:
            case 'normal':
                self.painter.setPen(self.pen_points)
            case 'selected':
                self.painter.setPen(self.pen_selected_points)
        self.painter.drawPoint(x, y)  #

    def draw_a_point_under_cursor(self, x1: int = 0, y1: int = 0):
        """draw a point with a square"""
        w = 2 * Geometry.point_square_collapse
        self.painter.setPen(self.pen_frame_around_a_point)
        self.painter.setBrush(self.brush_frame)
        self.painter.drawRect(x1, y1, w, w)

    def draw_a_point_text(self, x0_y0, text: str, type_of_point, color=QColor(0, 255, 0)):
        match type_of_point:
            case 'normal':
                self.painter.setPen(self.pen_points)
            case 'selected':
                self.painter.setPen(self.pen_selected_points)
            case 'axes':
                self.painter.setPen(self.pen_axes)
            case 'color':
                pen_color = QtGui.QPen(QtGui.QBrush(color), 0)
                self.painter.setPen(pen_color)
            case 'reaction':
                pen_color = QtGui.QPen(QtGui.QBrush(color), 1)
                self.painter.setPen(pen_color)
        self.painter.drawText(x0_y0[0] + 8, x0_y0[1] + 8, text)

    def draw_picked_frame(self):
        self.painter.setPen(self.pen_picked_frame)
        self.painter.setBrush(self.brush_frame)
        x1, y1 = Geometry.picked_frame[0]
        w = Geometry.picked_frame[1][0] - Geometry.picked_frame[0][0]
        h = Geometry.picked_frame[1][1] - Geometry.picked_frame[0][1]
        self.painter.drawRect(x1, y1, w, h)

    def draw_a_line(self, x1: int, y1: int, x2: int, y2: int, type_of_line: str = TypeOfTheObjects.normal,
                    color: QColor = QColor(50, 50, 50)):
        self.change_brush(type_of_line=type_of_line, color=color)
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_a_circle(self, x: int, y: int, r: int, type_of_line: str = TypeOfTheObjects.boundary_condition_joint):
        self.change_brush(type_of_line=type_of_line)
        self.painter.drawEllipse(int(x - r), int(y - r), 2 * r, 2 * r)

    def change_brush(self, color: QColor = QColor(50, 50, 50), type_of_line: str = TypeOfTheObjects.normal):
        match type_of_line:
            case TypeOfTheObjects.axes:
                self.painter.setPen(self.pen_axes)
            case TypeOfTheObjects.normal:
                brush = QtGui.QBrush(color)
                pen = QtGui.QPen(brush, 1)
                self.painter.setBrush(brush)
                self.painter.setPen(pen)
            case TypeOfTheObjects.selected:
                self.painter.setPen(self.selected_pen)
                self.painter.setBrush(self.selected_brush)
            case TypeOfTheObjects.light_surface_of_a_combine_beam:
                brush = QtGui.QBrush(color)
                self.painter.setBrush(brush)
                self.painter.setPen(self.combine_beam)
            case TypeOfTheObjects.dotted:
                self.painter.setPen(self.pen_doted)
            case TypeOfTheObjects.boundary_condition_line:
                self.painter.setBrush(self.brush_boundary_condition)
                self.painter.setPen(self.pen_boundary_conditions)
            case TypeOfTheObjects.boundary_condition_joint | TypeOfTheObjects.boundary_condition_surface:
                self.painter.setBrush(self.brush_boundary_condition)
                self.painter.setPen(self.pen_boundary_conditions_surface)
            case TypeOfTheObjects.light_surface:
                self.pen_solid = QtGui.QPen(QtGui.QBrush(color), 1)
                brush = QtGui.QBrush(color)
                self.painter.setPen(self.pen_solid)
                self.painter.setBrush(brush)
            case TypeOfTheObjects.temporary_surface:
                self.painter.setPen(self.pen_temporary_surface)
                self.painter.setBrush(self.brush_temporary_surface)
            case TypeOfTheObjects.surface:
                self.painter.setPen(self.pen_surface)
                self.painter.setBrush(self.brush_surface)
            case TypeOfTheObjects.light_line:
                pen_line = QtGui.QPen(QtGui.QBrush(color), 1)
                self.painter.setPen(pen_line)
            case TypeOfTheObjects.point_load | TypeOfTheObjects.line_load:
                brush = QtGui.QBrush(color)
                self.painter.setBrush(brush)
                pen_loads = QtGui.QPen(QtGui.QBrush(color), 2)
                self.painter.setPen(pen_loads)
            case TypeOfTheObjects.reaction:
                pen_color = QtGui.QPen(QtGui.QBrush(color), 2)
                self.painter.setPen(pen_color)
            case _:
                brush = QtGui.QBrush(color)
                pen = QtGui.QPen(brush, 1)
                self.painter.setBrush(brush)
                self.painter.setPen(pen)

    def draw_a_polygon(self, polygon: QPolygonF, type_of_line: str, color=QColor(50, 50, 50)):
        if type_of_line == TypeOfTheObjects.color:
            brush = QtGui.QBrush(color)
            self.painter.setBrush(brush)
        self.painter.drawPolygon(polygon)

    def mouseMoveEvent(self, event):
        match str(event.buttons()):
            case 'MouseButton.NoButton':
                #  the function checks collapse by mouse motion
                pass
            case 'MouseButton.RightButton|MiddleButton':
                rotate(x=event.x(), y=event.y())
            case 'MouseButton.LeftButton':
                self.move_left_button(event)
            case 'MouseButton.RightButton':
                pass
            case 'MouseButton.MiddleButton':
                shift(x=event.x(), y=event.y())

        self.draw_all()

    def move_left_button(self, event):
        if Geometry.point_under_cursor and Geometry.regime is None:
            start_regime_to_move_node(event=event)
        if (len(Geometry.picked_lines) > 0 and
                Geometry.binding == Geometry.Biding.point_middle and
                Geometry.point_under_cursor):
            start_regime_to_move_line(event=event, ctrl=self._ctrl)

        match Geometry.regime:
            case Geometry.Regime.edit_with_moved_node | Geometry.Regime.edit_lines_with_moved_node:
                Geometry.Regime.x_y_regime = (event.x(), event.y())
                check_collapse(x=event.x(), y=event.y())
            case _:
                pick_with_frame(x=event.x(), y=event.y(), ctrl=self._ctrl)

    def mousePressEvent(self, event):
        match event.buttons():
            case QtCore.Qt.MouseButton.LeftButton:
                left_click(x=event.x(), y=event.y(), ctrl=self._ctrl)
            case QtCore.Qt.MouseButton.MiddleButton:
                if self._right_button:
                    start_to_rotate(x=event.x(), y=event.y())
                else:
                    start_shift(x=event.x(), y=event.y())
                self._middle_button = True
            case QtCore.Qt.MouseButton.RightButton:
                self._right_button = True
                if self._middle_button:
                    start_to_rotate(x=event.x(), y=event.y())
                else:
                    right_button_event(self, event=event)
        self.draw_all()

    def mouseDoubleClickEvent(self, event):
        match event.buttons():
            case QtCore.Qt.MouseButton.LeftButton:
                self.objects_info()

    def mouseReleaseEvent(self, event):
        match event.button():
            case QtCore.Qt.MouseButton.LeftButton:
                left_release(event=event, ctrl=self._ctrl)
            case QtCore.Qt.MouseButton.MiddleButton:
                middle_release(event, right_button=self._right_button)
                self._middle_button = False
            case QtCore.Qt.MouseButton.RightButton:
                self._right_button = False
                self.end_of_all_operation_and_regime()
        self.draw_all()



    def keyPressEvent(self, event):
        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self._ctrl = True
            case QtCore.Qt.Key.Key_Delete:
                delete_picked_set()
            case QtCore.Qt.Key.Key_Escape | QtCore.Qt.Key.Key_Enter:
                self.end_of_all_operation_and_regime()


    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control:
            self._ctrl = False

    def wheelEvent(self, event):
        """MOUSEWHEEL:"""
        ds = event.angleDelta().y()
        # pos = (event., event.y)
        Variables.animation.scale_change(ds=ds)
        self.draw_all()

    def draw_all(self):
        canvas = self.label.pixmap()
        canvas.fill(Variables.MyColors.general_screen)
        self.painter = QtGui.QPainter(canvas)

        Variables.animation.draw_all(dx_dy=Geometry.dx_dy, df_dj=Geometry.df_dj)
        self.painter.end()
        self.label.setPixmap(canvas)

