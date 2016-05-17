#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
from . import utils
from . import widgets
from functools import partial

try:
    from PySide import QtGui, QtCore
except:
    pass

from .. import api
reload(api)

this_package = os.path.abspath(os.path.dirname(__file__))
icon_path = partial(os.path.join, this_package)

log = logging.getLogger("ViewNudger")


class UI(QtGui.QDialog):
    """
    :class:`UI` deals with building our UI.
    """
    def __init__(self, parent=utils.get_maya_window()):

        super(UI, self).__init__(parent)

        self.parent = parent

        self.setWindowTitle("View Nudger")
        self.resize(200, 200)
        self.setObjectName("viewNudger")
        self.setWindowFlags(QtCore.Qt.Window)

        with open(icon_path("style.css")) as f:
            self.setStyleSheet(f.read())

        # Center to frame.
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Our main layout
        self.central_boxLayout = QtGui.QVBoxLayout()
        self.central_boxLayout.setSpacing(2)
        self.central_boxLayout.setContentsMargins(10, 10, 10, 10)

        self.create_layout()
        self.create_connections()
        self.create_tooltips()

        self.setLayout(self.central_boxLayout)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def create_layout(self):
        """
        Creates layout for publishing camera.

        :raises: None

        :return: None
        :rtype: NoneType
        """
        self.button_layout = QtGui.QGridLayout()

        self.nudgeUp_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeUp_normal.png"),
            icon_hover=icon_path("icons", "nudgeUp_hover.png"),
        )
        self.nudgeDown_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeDown_normal.png"),
            icon_hover=icon_path("icons", "nudgeDown_hover.png"),
        )
        self.nudgeLeft_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeLeft_normal.png"),
            icon_hover=icon_path("icons", "nudgeLeft_hover.png"),
        )
        self.nudgeRight_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeRight_normal.png"),
            icon_hover=icon_path("icons", "nudgeRight_hover.png"),
        )
        self.nudgeUpLeft_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeUpLeft_normal.png"),
            icon_hover=icon_path("icons", "nudgeUpLeft_hover.png"),
        )
        self.nudgeUpRight_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeUpRight_normal.png"),
            icon_hover=icon_path("icons", "nudgeUpRight_hover.png"),
        )
        self.nudgeDownLeft_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeDownLeft_normal.png"),
            icon_hover=icon_path("icons", "nudgeDownLeft_hover.png"),
        )
        self.nudgeDownRight_Btn = widgets.IconButton(
            icon=icon_path("icons", "nudgeDownRight_normal.png"),
            icon_hover=icon_path("icons", "nudgeDownRight_hover.png"),
        )

        self.button_separator = widgets.LineWidget("main_seperator")

        self.bottom_layout = QtGui.QHBoxLayout()

        self.rotateView_LBL = widgets.LabelWidget("Rotate View : ")
        self.rotateView_CHKBOX = widgets.CheckBox("rotateView", False)

        self.moveObject_LBL = widgets.LabelWidget("Move Object : ")
        self.moveObject_CHKBOX = widgets.CheckBox("moveObject", False)

        self.nudgeValue_SPNBOX = widgets.DoubleSpinBox("nudgeValue", 1.0)

        self.bottom_layout.addWidget(self.rotateView_LBL)
        self.bottom_layout.addWidget(self.rotateView_CHKBOX)
        self.bottom_layout.addWidget(self.moveObject_LBL)
        self.bottom_layout.addWidget(self.moveObject_CHKBOX)
        self.bottom_layout.addWidget(self.nudgeValue_SPNBOX)

        self.button_layout.addWidget(self.nudgeUpLeft_Btn, 0, 0)
        self.button_layout.addWidget(self.nudgeUp_Btn, 0, 1)
        self.button_layout.addWidget(self.nudgeUpRight_Btn, 0, 2)
        self.button_layout.addWidget(self.nudgeLeft_Btn, 1, 0)
        self.button_layout.addWidget(self.nudgeRight_Btn, 1, 2)
        self.button_layout.addWidget(self.nudgeDownLeft_Btn, 2, 0)
        self.button_layout.addWidget(self.nudgeDown_Btn, 2, 1)
        self.button_layout.addWidget(self.nudgeDownRight_Btn, 2, 2)

        self.button_layout.setVerticalSpacing(0)
        self.button_layout.setHorizontalSpacing(3)

        self.central_boxLayout.addLayout(self.button_layout)
        self.central_boxLayout.addWidget(self.button_separator)
        self.central_boxLayout.addLayout(self.bottom_layout)

    def create_connections(self):
        """
        Creates connections to buttons.

        :raises: None

        :return: None
        :rtype: NoneType
        """
        self.nudgeUp_Btn.clicked.connect(
            partial(self.nudge, [0.0, 1.0]))
        self.nudgeDown_Btn.clicked.connect(
            partial(self.nudge, [0.0, -1.0]))
        self.nudgeLeft_Btn.clicked.connect(
            partial(self.nudge, [-1.0, 0.0]))
        self.nudgeRight_Btn.clicked.connect(
            partial(self.nudge, [1.0, 0.0]))
        self.nudgeUpLeft_Btn.clicked.connect(
            partial(self.nudge, [-1.0, 1.0]))
        self.nudgeUpRight_Btn.clicked.connect(
            partial(self.nudge, [1.0, 1.0]))
        self.nudgeDownLeft_Btn.clicked.connect(
            partial(self.nudge, [-1.0, -1.0]))
        self.nudgeDownRight_Btn.clicked.connect(
            partial(self.nudge, [1.0, -1.0]))

    def nudge(self, vector):
        """
        Does the nudge!

        :param vector: 2d vector representing direction.
        :type vector: list of 2 floats

        :raises: None

        :return: None
        :rtype: NoneType
        """
        pixelMove = self.nudgeValue_SPNBOX.value()
        moveObject = self.moveObject_CHKBOX.isChecked()
        rotateView = self.rotateView_CHKBOX.isChecked()

        transform = api.getSelection()

        pixelAmount = [pixelMove * i for i in vector]

        api.nudge(
            transform,
            pixelAmount=pixelAmount,
            moveObject=moveObject,
            rotateView=rotateView)

    def create_tooltips(self):
        """
        Creates tool tips for various widgets.

        :raises: None

        :return: None
        :rtype: NoneType
        """
        pass

    def close_dialog(self):
        """
        Closes the dialog.

        :raises: None

        :return: None
        :rtype: NoneType
        """
        self.close()

    def create(self):
        """
        Shows the window.

        :raises: None

        :return: None
        :rtype: NoneType
        """
        self.show()
        self.activateWindow()
        self.raise_()

if __name__ == "__main__":
    app = UI()
    app.create()
