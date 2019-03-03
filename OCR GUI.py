# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Starparivaaar.ui'
#
# Created by: PyQt5 UI code generator 5.11
#
# WARNING! All changes made in this file will be lost!
import OCR
import os
from pdf2image import convert_from_path

from PyQt5 import QtCore, QtGui, QtWidgets
import sys,PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMainWindow, QLabel, QAction
from PyQt5.QtGui import QIcon

class variables:
    choice=0
    str1 = []
    str2=[]
    list1=[]
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(964, 670)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.frame_3 = QtWidgets.QFrame(self.frame_5)
        self.frame_3.setGeometry(QtCore.QRect(120, 10, 721, 91))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(100, 10, 571, 61))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setIndent(38)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.frame_5)
        self.frame.setGeometry(QtCore.QRect(40, 140, 131, 411))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.convert_b = QtWidgets.QPushButton(self.frame)
        self.convert_b.setGeometry(QtCore.QRect(0, 210, 131, 61))
        self.convert_b.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/iConvert-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.convert_b.setIcon(icon)
        self.convert_b.setIconSize(QtCore.QSize(53, 53))
        self.convert_b.setDefault(True)
        self.convert_b.setObjectName("convert_b")
        self.clear_b = QtWidgets.QPushButton(self.frame)
        self.clear_b.setGeometry(QtCore.QRect(0, 310, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clear_b.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_b.setIcon(icon1)
        self.clear_b.setIconSize(QtCore.QSize(53, 53))
        self.clear_b.setObjectName("clear_b")
        self.image_open_b = QtWidgets.QPushButton(self.frame)
        self.image_open_b.setGeometry(QtCore.QRect(0, 10, 131, 61))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.image_open_b.setIcon(icon2)
        self.image_open_b.setIconSize(QtCore.QSize(53, 53))
        self.image_open_b.setObjectName("image_open_b")
        self.pdf_open_b = QtWidgets.QPushButton(self.frame)
        self.pdf_open_b.setGeometry(QtCore.QRect(0, 110, 131, 61))
        self.pdf_open_b.setIcon(icon2)
        self.pdf_open_b.setIconSize(QtCore.QSize(53, 53))
        self.pdf_open_b.setObjectName("pdf_open_b")
        self.frame_4 = QtWidgets.QFrame(self.frame_5)
        self.frame_4.setGeometry(QtCore.QRect(350, 190, 511, 371))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.textEdit = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 461, 321))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setGeometry(QtCore.QRect(230, 130, 651, 51))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.frame_5, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 964, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
        def selectFile():
            variables.str2 = variables.str2+QFileDialog.getOpenFileNames()[0]
            
            for i in range(len(variables.str2)):
                print(variables.str2[i])
                os.mkdir("%s" % variables.str2[i][:-4])
                pages=convert_from_path(variables.str2[i],500)
                count=1
                for page in pages:
                    page.save("%s/%d.jpg" % (variables.str2[i][:-4],count),'JPEG')
                    variables.list1.append("%s/%d.jpg" % (variables.str2[i][:-4],count))
                    count=count+1
                variables.choice=1
                #variables.list1 = [variables.list1]
                self.label_2.setText("Selcted File : " + ''.join(variables.list1))
                print(variables.list1)

        def selectImage():
            variables.str1 = variables.str1+QFileDialog.getOpenFileNames()[0]
            variables.choice=0
            self.label_2.setText("Selcted File : " + ''.join(variables.str1[0]) )
            print(variables.str1)
        #dlg.locationBtn.clicked.connect(selectFile)

        self.image_open_b.clicked.connect(selectImage)#for openting images
        self.pdf_open_b.clicked.connect(selectFile)#for opening pdf
        self.convert_b.clicked.connect(self.convert_open)#for converting files and begin process
        self.clear_b.clicked.connect(self.clear_open)#to clear the content

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Medical Prescription OCR"))
        self.convert_b.setText(_translate("MainWindow", "Convert"))
        self.clear_b.setText(_translate("MainWindow", "Clear"))
        self.image_open_b.setText(_translate("MainWindow", "Open Image"))
        self.pdf_open_b.setText(_translate("MainWindow", "Open PDF"))
        self.label_2.setText(_translate("MainWindow", "Selcted File :"))

        #def selectFile():
        #lineEdit.setText(QFileDialog.getOpenFileName())
    def image_open(self):
        print('hello')

#pushButton.clicked.connect(selectFile)
        
    def convert_open(self):
        OCR.fun(variables.list1) if variables.choice == 1 else OCR.fun(variables.str1)
        f=open('outputgsmain.txt','r')
        output= f.read()
        self.textEdit.setText(output)
    def pdf_open(self):
        print('hello')
    def clear_open(self):
        variables.str1=[]
        variables.str2=[]
        variables.list1=[]
        self.label_2.setText("Selcted File : ")
        self.textEdit.setText(' ')
#import LOGOS_rc    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
