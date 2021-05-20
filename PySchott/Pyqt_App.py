from .Pyqt_Widget import LightWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import sys

from .PySchott import MCLS_Light     
def LightControl(port=None):
    """
    basic control of the the light source and its intensity

    Parameters
    ----------
    port : string
        port used to establish the serial communication with the light source
    """

    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    light = MCLS_Light(port)
    a = LightWidget(light)
    a.show()
    app.exec_()
    
