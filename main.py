import os
import sys

from PySide6 import QtWidgets, QtGui

from graphic.class_draw import DrawAll
from menus.general_menu import GeneralWindow
from variables.menus import Menus


def load_general_menu():
    basedir = os.path.dirname(__file__)
    #basedir = os.path.join(basedir, 'icons\\icon.png')  # icon for general program

    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon(basedir))
    screen = app.primaryScreen()
    size = screen.size()
    Menus.window_width = size.width()
    Menus.window_height = size.height()
    Menus.general_window = GeneralWindow()
    Menus.general_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    load_general_menu()