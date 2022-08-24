from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QShortcut
from PIL import ImageGrab
import cv2
import numpy
import SnippingMenu


class SnippingWindow(QtWidgets.QWidget):
    # setup variables
    isSnipping = False
    background = True

    def __init__(SnippingWindow):
        super().__init__()
        SnippingWindow.initUI()

    # setup
    def initUI(SnippingWindow):
        screen = QApplication.primaryScreen()
        screensize = screen.size()
        SnippingWindow.setGeometry(
            0, 0, screensize.width(), screensize.height())
        SnippingWindow.setWindowOpacity(0)

        SnippingWindow.begin = QtCore.QPoint()
        SnippingWindow.end = QtCore.QPoint()

        #shortcut for quitting
        SnippingWindow.quit_snipWin = QShortcut(QKeySequence("Q"), SnippingWindow)
        SnippingWindow.quit_snipWin.activated.connect(SnippingWindow.QuitEvent)

    # start snipping function
    def startSnipping(SnippingWindow):
        SnippingWindow.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        SnippingWindow.isSnipping = True
        SnippingWindow.background = False
        SnippingWindow.setWindowOpacity(0.3)
        SnippingWindow.show()

    # paintEvent, mousePressEvent, mouseMoveEvent, mouseReleaseEvent are predefiened function.
    # we use them to paint a rect on when mouse is pressed and capture paintet rect on screen when mouse is released.
    # After captured image is sent back to SnippingWindow
    def paintEvent(SnippingWindow, event):
        if SnippingWindow.isSnipping:
            fillColor = (77, 107, 255)
            penThicness = 2
            windowOpacity = 0.3
        else:
            fillColor = (0, 0, 0)
            penThicness = 0
            windowOpacity = 0
            SnippingWindow.begin = QtCore.QPoint()
            windowOpacity = 0
            SnippingWindow.end = QtCore.QPoint()

        SnippingWindow.setWindowOpacity(windowOpacity)
        qp = QtGui.QPainter(SnippingWindow)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), penThicness))
        qp.setBrush(QtGui.QColor(*fillColor))
        rect = QtCore.QRectF(SnippingWindow.begin, SnippingWindow.end)
        qp.drawRect(rect)

    def mousePressEvent(SnippingWindow, event):
        SnippingWindow.begin = event.pos()
        SnippingWindow.end = SnippingWindow.begin
        SnippingWindow.update()

    def mouseMoveEvent(SnippingWindow, event):
        SnippingWindow.end = event.pos()
        SnippingWindow.update()
        if event.button() == QtCore.Qt.LeftButton:
            SnippingWindow.dragPosition = event.globalPos(
            ) - SnippingWindow.frameGeometry().topLeft()
            event.accept()

    def mouseReleaseEvent(SnippingWindow, event):
        SnippingWindow.end = event.pos()
        SnippingWindow.update()
        SnippingWindow.repaint()
        if event.buttons() == QtCore.Qt.LeftButton:
            SnippingWindow.move(event.globalPos() -
                                SnippingWindow.dragPosition)
            event.accept()

        if SnippingWindow.end:
            xStart = min(SnippingWindow.begin.x(), SnippingWindow.end.x())
            xEnd = max(SnippingWindow.begin.x(), SnippingWindow.end.x())
            yStart = min(SnippingWindow.begin.y(), SnippingWindow.end.y())
            yEnd = max(SnippingWindow.begin.y(), SnippingWindow.end.y())
        SnippingWindow.isSnipping = False

        QtWidgets.QApplication.processEvents()
        SnippingWindow.background = True
        SnippingWindow.update()

        SnippingWindow.close()
        img = ImageGrab.grab(bbox=(xStart, yStart, xEnd, yEnd))
        img = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)
        SnippingWindow.snippingMenu = SnippingMenu.MainWindow(img)
        QtWidgets.QApplication.processEvents()

    def QuitEvent(SnippingWindow):
        SnippingWindow.background = True
        SnippingWindow.update()

        SnippingWindow.close()
        img = None
        SnippingWindow.snippingMenu = SnippingMenu.MainWindow(img)
        QtWidgets.QApplication.processEvents()
