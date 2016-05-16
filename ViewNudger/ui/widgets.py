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


class ButtonWidget(QtGui.QPushButton):
    '''
    :class:`QPushButton` deals with building a QPushButton.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, parent=None):

        super(ButtonWidget, self).__init__(parent)

        # self.setText(name)
        self.setObjectName("{0}_btn".format(name))

        # Font.
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 0))


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


class TreeWidget(QtGui.QTreeWidget):
    '''
    :class:`QTreeWidget` deals with building a QTreeWidget.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, headerName=None, parent=None):

        super(TreeWidget, self).__init__(parent)

        self.setObjectName("{0}_treeWidget".format(name))
        self.headerItem().setText(0, headerName)
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


class TextWidget(QtGui.QTextEdit):
    '''
    :class:`QTextEdit` deals with building a QTextEdit.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    text_changed = QtCore.Signal(str)

    def __init__(self, name, headerName=None, parent=None):

        super(TextWidget, self).__init__(parent)

        self.setObjectName("{0}_textEdit".format(name))

        # Font.
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)


class ComboBox(QtGui.QComboBox):
    '''
    :class:`ComboBox` deals with building a ComboBox.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, parent=None):

        super(ComboBox, self).__init__(parent)
        self.setObjectName(name)


class LineEdit(QtGui.QLineEdit):
    '''
    :class:`LineEdit` deals with building a LineEdit.

    :raises: None

    :return: None
    :rtype: NoneType
    '''
    def __init__(self, name, parent=None):

        super(LineEdit, self).__init__(parent)
        self.setObjectName(name)

        # Size.
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        self.setSizePolicy(sizePolicy)
