import os
import logging
from . import widgets

try:
    from PySide import QtGui, QtCore
except:
    pass

from .. import api
reload(api)

DIR = os.path.dirname(__file__)
log = logging.getLogger('ViewNudger')


class UI(QtGui.QDialog):
    '''
    :class:`UI` deals with building our UI.
    '''
    def __init__(self, parent=widgets.maya_main_window()):

        super(UI, self).__init__(parent)

        self.parent = parent

        self.setWindowTitle("View Nudger")
        self.resize(400, 400)
        self.setObjectName("viewNudger")
        self.setWindowFlags(QtCore.Qt.Window)

        with open(os.path.join(DIR, "style.css")) as f:
            self.setStyleSheet(f.read())

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
        '''
        Creates layout for publishing camera.

        :raises: None

        :return: None
        :rtype: NoneType
        '''
        pass

    def create_connections(self):
        '''
        Creates connections to buttons.

        :raises: None

        :return: None
        :rtype: NoneType
        '''
        pass

    def create_tooltips(self):
        '''
        Creates tool tips for various widgets.

        :raises: None

        :return: None
        :rtype: NoneType
        '''
        pass

    def close_dialog(self):
        '''
        Closes the dialog.

        :raises: None

        :return: None
        :rtype: NoneType
        '''
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

if __name__ == '__main__':
    app = UI()
    app.create()
