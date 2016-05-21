#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from PySide import QtGui, QtCore
except:
    pass


class IconButton(QtGui.QLabel):
    '''
    Icon button.

    :raises: None

    :return: Maya's main window.
    :rtype: QtGui.QLabel
    '''
    clicked = QtCore.Signal()
    cache = {}

    def __init__(self, icon, icon_hover, *args, **kwargs):
        super(IconButton, self).__init__(*args, **kwargs)

        if icon not in self.cache:
            self.cache[icon] = QtGui.QPixmap(QtGui.QImage(icon))
        if icon_hover not in self.cache:
            self.cache[icon_hover] = QtGui.QPixmap(QtGui.QImage(icon_hover))

        self.normal = self.cache[icon]
        self.hover = self.cache[icon_hover]
        self.hovering = False
        self.setPixmap(self.normal)

    def mousePressEvent(self, event):

        self.setPixmap(self.normal)
        super(IconButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.hovering:
            self.setPixmap(self.hover)
        else:
            self.setPixmap(self.normal)

        super(IconButton, self).mouseReleaseEvent(event)
        if self.hovering:
            self.clicked.emit()

    def enterEvent(self, event):

        self.setPixmap(self.hover)
        self.hovering = True
        super(IconButton, self).enterEvent(event)

    def leaveEvent(self, event):

        self.setPixmap(self.normal)
        self.hovering = False
        super(IconButton, self).leaveEvent(event)


class LineWidget(QtGui.QFrame):
    '''
    :class:`QFrame` deals with building a QPushButton.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, parent=None):

        super(LineWidget, self).__init__(parent)
        self.setObjectName(name)
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class LabelWidget(QtGui.QLabel):
    '''
    :class:`labelWidget` deals with building a QLabel.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, parent=None):

        super(LabelWidget, self).__init__(parent)

        self.setText(name)
        self.setObjectName("{0}_lbl".format(name))

        # Size.
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        self.setSizePolicy(sizePolicy)

        # Font.
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)


class CheckBox(QtGui.QCheckBox):
    '''
    :class:`CheckBox` deals with building a QCheckBox.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, checked, parent=None):

        super(CheckBox, self).__init__(parent)
        self.setObjectName(name + "_CHKBOX")
        self.setChecked(checked)
        self.setAutoExclusive(False)


class DoubleSpinBox(QtGui.QDoubleSpinBox):
    '''
    :class:`DoubleSpinBox` deals with building a QCheckBox.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, value, parent=None):
        super(DoubleSpinBox, self).__init__(parent)
        self.setObjectName(name)
        self.setMaximum(100000)
        self.setMinimum(0.0)
        self.setValue(value)
