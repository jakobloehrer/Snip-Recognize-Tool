#from re import M
#from typing import final
#from cv2 import  resize
#from PIL import Image
import time
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QShortcut#, QComboBox,  QGridLayout, QPushButton, QTextEdit, QLabel, QStatusBar
import cv2
import SnippingWidget
import easyocr

# Features to add:
# • Make Appllication never quit --> impossible actions
# • only inclue necessary libaries
# • start Recongnition after Taking Image
# • accuracy label
# • box capture image display (by button)
# • add characters to easyocr char_set for better accuracy
# • automatic size adjustment
# • freeze screen when taking screenshot
# • different dedection algorithm
# • working for moltible screens


class MainWindow(QMainWindow):

    def __init__(MainWindow, numpy_image=None):
        super().__init__()
        MainWindow.initUi(numpy_image)

    def initUi(MainWindow, numpy_image):

        # Window Setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(830, 628)
        MainWindow.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.centralwidget.setObjectName("centralwidget")

        # Default Delay & Language
        MainWindow.delay = 0
        MainWindow.language = ["en"]

        # connect to snippingWidget
        MainWindow.snippingWidget = SnippingWidget.SnippingWindow()

        # Grid Layout Setup
        MainWindow.gridLayout_2 = QtWidgets.QGridLayout(
            MainWindow.centralwidget)
        MainWindow.gridLayout_2.setObjectName("gridLayout_2")
        MainWindow.gridLayout = QtWidgets.QGridLayout()
        MainWindow.gridLayout.setHorizontalSpacing(10)
        MainWindow.gridLayout.setObjectName("gridLayout")

        # TextEdit Result
        MainWindow.te_textResult = QtWidgets.QTextEdit(
            MainWindow.centralwidget)
        MainWindow.te_textResult.setObjectName("te_textResult")
        MainWindow.gridLayout.addWidget(MainWindow.te_textResult, 1, 0, 1, 5)

        # Label Display Screenshot
        MainWindow.lbl_screenshot = QtWidgets.QLabel(MainWindow.centralwidget)
        MainWindow.lbl_screenshot.setFrameShape(QtWidgets.QFrame.Box)
        MainWindow.lbl_screenshot.setFrameShadow(QtWidgets.QFrame.Sunken)
        MainWindow.lbl_screenshot.setText("")
        MainWindow.lbl_screenshot.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        MainWindow.lbl_screenshot.setObjectName("lbl_screenshot")
        MainWindow.gridLayout.addWidget(MainWindow.lbl_screenshot, 1, 6, 1, 5)

        # Display Screenshot
        if numpy_image is not None:
            MainWindow.conv_img = numpy_image
            MainWindow.snip_img = numpy_image
            MainWindow.save_img = numpy_image

            MainWindow.snip_img = QtGui.QImage(
                MainWindow.snip_img.data, MainWindow.snip_img.shape[1], MainWindow.snip_img.shape[0], MainWindow.snip_img.strides[0], QtGui.QImage.Format_BGR888)
            MainWindow.lbl_screenshot.setPixmap(
                QtGui.QPixmap.fromImage(MainWindow.snip_img))

        # https://stackoverflow.com/questions/57204782/show-an-opencv-image-with-pyqt5

        # Button Recognize Text
        MainWindow.btn_recTxt = QtWidgets.QPushButton(MainWindow.centralwidget)
        MainWindow.btn_recTxt.setObjectName("btn_recTxt")
        MainWindow.gridLayout.addWidget(MainWindow.btn_recTxt, 0, 0, 1, 1)
        MainWindow.btn_recTxt.clicked.connect(MainWindow.convertSnip)

        # Button Save Screenshot
        MainWindow.btn_saveImg = QtWidgets.QPushButton(
            MainWindow.centralwidget)
        MainWindow.btn_saveImg.setObjectName("btn_saveImg")
        MainWindow.gridLayout.addWidget(MainWindow.btn_saveImg, 0, 9, 1, 1)
        MainWindow.btn_saveImg.clicked.connect(MainWindow.saveFile)
        MainWindow.btn_saveImg.clicked.connect(
            lambda: MainWindow.saveFile("imgBox"))

        # Button copy Text
        MainWindow.btn_copyTxt = QtWidgets.QPushButton(
            MainWindow.centralwidget)
        MainWindow.btn_copyTxt.setObjectName("btn_copyTxt")
        MainWindow.gridLayout.addWidget(MainWindow.btn_copyTxt, 0, 2, 1, 1)
        MainWindow.btn_copyTxt.clicked.connect(
            lambda: MainWindow.copyToClipboard("txtBox"))

        # Button copy Image
        MainWindow.btn_copyImg = QtWidgets.QPushButton(
            MainWindow.centralwidget)
        MainWindow.btn_copyImg.setObjectName("btn_copyImg")
        MainWindow.gridLayout.addWidget(MainWindow.btn_copyImg, 0, 8, 1, 1)
        MainWindow.btn_copyImg.clicked.connect(
            lambda: MainWindow.copyToClipboard("imgBox"))

        # ComboBox Delay
        MainWindow.cb_delay = QtWidgets.QComboBox(MainWindow.centralwidget)
        MainWindow.cb_delay.setObjectName("cb_delay")
        MainWindow.cb_delay.addItem("")
        MainWindow.cb_delay.addItem("")
        MainWindow.cb_delay.addItem("")
        MainWindow.cb_delay.addItem("")
        MainWindow.cb_delay.addItem("")
        MainWindow.cb_delay.addItem("")
        MainWindow.gridLayout.addWidget(MainWindow.cb_delay, 0, 7, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        MainWindow.gridLayout.addItem(spacerItem, 0, 10, 1, 1)
        MainWindow.cb_delay.activated[str].connect(
            MainWindow.cb_delayActivated)

        # Button save Text
        MainWindow.btn_saveTxt = QtWidgets.QPushButton(
            MainWindow.centralwidget)
        MainWindow.btn_saveTxt.setObjectName("btn_saveTxt")
        MainWindow.gridLayout.addWidget(MainWindow.btn_saveTxt, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        MainWindow.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        MainWindow.btn_saveTxt.clicked.connect(
            lambda: MainWindow.saveFile("txtBox"))

        # ComboBox Text Language
        MainWindow.cb_recLanguage = QtWidgets.QComboBox(
            MainWindow.centralwidget)
        MainWindow.cb_recLanguage.setObjectName("cb_recLanguage")
        MainWindow.cb_recLanguage.addItem("")
        MainWindow.cb_recLanguage.addItem("")
        MainWindow.cb_recLanguage.addItem("")
        MainWindow.gridLayout.addWidget(MainWindow.cb_recLanguage, 0, 1, 1, 1)
        MainWindow.cb_recLanguage.activated[str].connect(
            MainWindow.cb_languageActivated)

        # Button newSnip
        MainWindow.btn_newSnip = QtWidgets.QPushButton(
            MainWindow.centralwidget)
        MainWindow.btn_newSnip.setObjectName("btn_newSnip")
        MainWindow.gridLayout.addWidget(MainWindow.btn_newSnip, 0, 6, 1, 1)
        MainWindow.btn_newSnip.clicked.connect(MainWindow.newSnip)

        # Label Instructions
        MainWindow.label = QtWidgets.QLabel(MainWindow.centralwidget)
        MainWindow.label.setAlignment(QtCore.Qt.AlignLeading |
                                      QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        MainWindow.label.setObjectName("label")
        MainWindow.gridLayout.addWidget(MainWindow.label, 1, 5, 1, 1)

        # Status Bar
        MainWindow.gridLayout_2.addLayout(MainWindow.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(MainWindow.centralwidget)
        MainWindow.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(MainWindow.statusbar)

        # Shortcuts:
        # Save Img
        MainWindow.shortcut_saveImage = QShortcut(
            QKeySequence("Ctrl+S"), MainWindow)
        MainWindow.shortcut_saveImage.activated.connect(
            lambda: MainWindow.saveFile("imgBox"))

        # Save Text
        MainWindow.shortcut_saveImage = QShortcut(
            QKeySequence("Ctrl+Shift+S"), MainWindow)
        MainWindow.shortcut_saveImage.activated.connect(
            lambda: MainWindow.saveFile("txtBox"))

        # Recognize Text
        MainWindow.shortcut_recText = QShortcut(
            QKeySequence("Ctrl+R"), MainWindow)
        MainWindow.shortcut_recText.activated.connect(MainWindow.convertSnip)

        # Copy Text
        MainWindow.shortcut_cpTxt = QShortcut(
            QKeySequence("Ctrl+Shift+C"), MainWindow)
        MainWindow.shortcut_cpTxt.activated.connect(
            lambda: MainWindow.copyToClipboard("txtBox"))

        # Copy Image --> ctrl+c is reserved by python --> had no motivation programming it:)
        MainWindow.shortcut_cpImg = QShortcut(
            QKeySequence("Ctrl+Shift+I"), MainWindow)
        MainWindow.shortcut_cpImg.activated.connect(
            lambda: MainWindow.copyToClipboard("imgBox"))

        # New Snip
        MainWindow.shortcut_newSnip = QShortcut(
            QKeySequence("Ctrl+N"), MainWindow)
        MainWindow.shortcut_newSnip.activated.connect(MainWindow.newSnip)

        MainWindow.show()
        MainWindow.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Add Text and Stuff
    def retranslateUi(MainWindow, self):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.btn_recTxt.setText(
            _translate("MainWindow", "Recognize Text"))
        MainWindow.te_textResult.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        MainWindow.btn_saveImg.setText(_translate("MainWindow", "Save Image"))
        MainWindow.btn_copyTxt.setText(_translate("MainWindow", "Copy Text"))
        MainWindow.btn_copyImg.setText(_translate("MainWindow", "Copy Image"))
        MainWindow.cb_delay.setItemText(
            0, _translate("MainWindow", "No Delay"))
        MainWindow.cb_delay.setItemText(
            1, _translate("MainWindow", "1 Second"))
        MainWindow.cb_delay.setItemText(
            2, _translate("MainWindow", "3 Seconds"))
        MainWindow.cb_delay.setItemText(
            3, _translate("MainWindow", "5 Seconds"))
        MainWindow.cb_delay.setItemText(
            4, _translate("MainWindow", "10 Seconds"))
        MainWindow.cb_delay.setItemText(
            5, _translate("MainWindow", "30 Seconds"))
        MainWindow.btn_saveTxt.setText(_translate("MainWindow", "Save Text"))
        MainWindow.cb_recLanguage.setItemText(
            0, _translate("MainWindow", "EN"))
        MainWindow.cb_recLanguage.setItemText(
            1, _translate("MainWindow", "DE"))
        MainWindow.cb_recLanguage.setItemText(
            2, _translate("MainWindow", "FR"))
        MainWindow.btn_newSnip.setText(_translate("MainWindow", "New"))
        MainWindow.label.setText(_translate("MainWindow", "\"Ctrl+N\" = New Screenshot\n"
                                            "\"Ctrl+Shift+I\" = Copy Screenshot\n"
                                            "\"Ctrl+S\" = Save Screenshot\n"
                                            "\"Ctrl+R\" = Recocnize Text\n"
                                            "\"Ctrl+Shift+C\" = Copy Text\n"
                                            "\"Ctrl+Shift+S\" = Save Text\n"
                                            "\"Q\" = Quit Snipping Window"))

    # NewSnip Function --> Opens SnippingWidget
    def newSnip(MainWindow):
        MainWindow.hide()
        time.sleep(MainWindow.delay)
        MainWindow.snippingWidget.startSnipping()
        if not MainWindow.snippingWidget.background:
            MainWindow.close()

    # ConvertSnip Function --> Recognize text and format it
    # EasyOcr Documentation: https://www.jaided.ai/easyocr/documentation/ --> Libary used for Text Recongnition
    def convertSnip(MainWindow):

        # EacyOcr Setup and Recognize
        reader = easyocr.Reader(MainWindow.language)
        result = reader.readtext(MainWindow.conv_img, min_size=1,
                                 height_ths=20, low_text=0.5, width_ths=1, ycenter_ths=1)

        # gnerate Variables for formating
        previousRightX = 0
        perviousMiddleY = 0

        minLeftX = 1000
        for detection in result:
            topLeft = tuple(detection[0][0])
            if minLeftX > topLeft[0]:
                minLeftX = topLeft[0]

        # format and Display Result
        for detection in result:
            # setup variables
            topLeft = tuple(detection[0][0])
            bottomLeft = tuple(detection[0][3])
            topRight = tuple(detection[0][1])
            topY = topLeft[1]
            bottomY = bottomLeft[1]
            leftX = topLeft[0]

            # FontSize & Space Size
            # --> Cortinates begin in Left Corner

            fontsize = bottomY - topY
            spaceSize = fontsize / 2
            spaces = 0

            # Display Text in Found Text Size --> looks shitty
            #stringFontSize = "\"font-size:"  + str(fontsize) + "px; white-space: pre; \""
            stringFontSize = "\"font-size: 13px; white-space: pre; \""

            # Format Text --> made for Code recognition

            # aline on one line if necessary
            # if detection on same line continue
            if (perviousMiddleY - 5 < bottomY - fontsize/2 < perviousMiddleY + 5):
                distanceToMinX = leftX - previousRightX
                while (distanceToMinX > 0):
                    spaces + 1
                    distanceToMinX -= spaceSize
                spacing = spaces * " "

            # if its first detection do nothing (but spaces if necessary)
            elif perviousMiddleY == 0 & previousRightX == 0:
                distanceToMinX = leftX - minLeftX
                while (distanceToMinX > 0):
                    spaces += 1
                    distanceToMinX -= spaceSize
                spacing = spaces * " "

            # if its a new line break
            else:
                distanceToMinX = leftX - minLeftX
                paragraph = "<br>"
                while (distanceToMinX > 0):
                    spaces += 1
                    distanceToMinX -= spaceSize
                spacing = paragraph + spaces * " "

            # Put Result in Html Form and in textEditBox
            html = (f"<p style={stringFontSize}>{spacing}{detection[1]} </p>")
            MainWindow.te_textResult.insertHtml(html)

            # Print Detectet Boxes to Image --> usefull for debugging
            #top_left = tuple(detection[0][0])
            #bottom_right = tuple(detection[0][2])
            #text = detection[1]
            #MainWindow.conv_img = cv2.rectangle(
            #    MainWindow.conv_img, top_left, bottom_right, (0, 255, 0), 1)
            #cv2.imwrite('F:\image.png', MainWindow.conv_img)

            # Assign Variables for next iteration
            perviousMiddleY = bottomY - fontsize/2  # Y-Middlde of dedection Box
            previousRightX = topRight[0]

    # copyToClipboard Function --> depends on pushed button
    def copyToClipboard(MainWindow, source):
        # decide what to copy then copy
        print("copy to clipboard" + source)

        # copy text
        if source == "txtBox":
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(MainWindow.te_textResult.toPlainText(),
                       mode=cb.Clipboard)

        # copy image
        elif source == "imgBox":
            print("right source")
            try:
                print("working")
                cb = QApplication.clipboard()
                cb.clear(mode=cb.Clipboard)
                cb.setImage(MainWindow.snip_img, mode=cb.Clipboard)
            except:
                print("img exeption")
                pass
        else:
            print("else")
            pass

    # saveFile Function --> depends on pushed button
    def saveFile(MainWindow, source):
        # decide what to savve then save

        # save Disalog
        path_desktop_img = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop/NewScreenshot')
        path_desktop_txt = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop/NewTextFile')

        # save text
        if source == "txtBox":
            filePath, _ = QFileDialog.getSaveFileName(MainWindow, "Save Text", path_desktop_txt,
                                                      "TXT(*.txt);;All Files(*.*) ")
            with open(filePath, 'w') as f:
                f.write(MainWindow.te_textResult.toPlainText())

        # save image
        elif source == "imgBox":
            try:
                doesExist = MainWindow.snip_img
                filePath, _ = QFileDialog.getSaveFileName(MainWindow, "Save Screenshot", path_desktop_img,
                                                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
                MainWindow.snip_img.save(filePath)
            except:
                pass

        else:
            pass

    # combobox delay setup
    def cb_delayActivated(MainWindow, selected):
        if selected == "1 Second":
            MainWindow.delay = 1
        elif selected == "3 Seconds":
            MainWindow.delay = 3
        elif selected == "5 Seconds":
            MainWindow.delay = 5
        elif selected == "10 Seconds":
            MainWindow.delay = 10
        elif selected == "30 Seconds":
            MainWindow.delay = 30
        elif selected == "No Delay":
            MainWindow.delay = 0
        else:
            pass

    # combobox languages setup
    def cb_languageActivated(MainWindow, selected):
        if selected == "DE":
            MainWindow.language = ['de']
        elif selected == "FR":
            MainWindow.language = ['fr']
        elif selected == "EN":
            MainWindow.language = ['en']
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainWindow()
    sys.exit(app.exec_())
