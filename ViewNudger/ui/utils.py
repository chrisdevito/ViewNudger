import time
import shiboken
from PySide import QtGui
from maya.OpenMayaUI import MQtUtil


def get_maya_window():
    """
    Get Maya MainWindow as a QWidget.

    :raises: None

    :return: Maya's main window.
    :rtype: QtGui.QMainWindow
    """
    ptr = long(MQtUtil.mainWindow())
    return shiboken.wrapInstance(ptr, QtGui.QMainWindow)


def wait(delay=1):
    """
    Delay python execution for a specified amount of time

    :raises: None

    :return: None
    :rtype: NoneType
    """
    s = time.clock()

    while True:
        if time.clock() - s >= delay:
            return
        QtGui.qApp.processEvents()
