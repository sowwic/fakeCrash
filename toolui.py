import pymel.core as pm
import time
import os
from maya import OpenMayaUI as omui
from maya import OpenMaya as om
from shiboken2 import wrapInstance
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


GIF_PATH = "D:/Repos/UsefulTool/helper.ico"


class QHelperWidget(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(QHelperWidget, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        fileData = None
        with open(GIF_PATH, "rb") as helperFile:
            fileData = helperFile.read()
        self.gifByteArray = QtCore.QByteArray(fileData)
        self.gifBuffer = QtCore.QBuffer(self.gifByteArray)
        self.movie = QtGui.QMovie()
        self.movie.setFormat("GIF")
        self.movie.setDevice(self.gifBuffer)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.setMovie(self.movie)
        self.movie.jumpToFrame(0)
        self.movie.start()
        self.movie.setScaledSize(self.size())


class DialogUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DialogUI, self).__init__(parent)
        self.setWindowTitle("PRANKED")
        self.setMinimumSize(1000, 1000)
        self.showMaximized()
        helper = QHelperWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addWidget(helper)


def mayaMainWindow():
    """
    Get maya main window as QWidget

    :return: Maya main window as QWidget
    :rtype: PySide2.QtWidgets.QWidget
    """
    mainWindowPtr = omui.MQtUtil.mainWindow()
    if mainWindowPtr:
        return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)
    else:
        mayaMainWindow()


def showMessageDialog():
    fileName = time.strftime("%Y%m%d.%H%M") + ".ma"
    filePath = os.path.join(pm.internalVar(utd=1), fileName)
    pm.confirmDialog(icon="warning", m="Fatal Error. Attempting to save in {0}".format(filePath), t="maya", button=["OK"], ma="left")
    time.sleep(3)


def ui(*args):
    showMessageDialog()
    newUI = DialogUI(parent=mayaMainWindow())
    newUI.exec_()


def addSaveCallback():
    om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, ui, None)


if __name__ == "__main__":
    ui()
