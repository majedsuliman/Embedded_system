from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QGraphicsView, QWizard, QMainWindow, QLabel,QDialog, QFileDialog,QMessageBox

from PyQt5 import QtGui
from PyQt5 import uic
import sys
import qdarkstyle
from pictoplot.new import *



Filename = ''
class UI(QMainWindow):

   
    def __init__(self):
        super(UI,self).__init__()
        # load UI
        uic.loadUi("Printer.ui",self)

        # Initialize widgets from UI
        self.lbl1 = self.findChild(QLabel,"label")
        self.lbl2 = self.findChild(QLabel,"label_2")
        self.img1 = self.findChild(QLabel,"label_3")
        self.img2 = self.findChild(QLabel,"label_4")
        self.btn1 = self.findChild(QPushButton,"pushButton")
        self.btn2 = self.findChild(QPushButton,"pushButton_2")

        # Initialize Button
        self.btn1.clicked.connect(self.BrowseImage)
        self.btn2.clicked.connect(self.Draw)
        self.img1.setStyleSheet("border: 1px solid black;")
        self.img2.setStyleSheet("border: 1px solid black;")
        self.show()

    def BrowseImage(self):
        fname = QFileDialog.getOpenFileName(self,'Open File', 'c:\\', 'Image files (*.jpg *png)')
        global Filename
        imagepth = fname[0]
        x = imagepth.split('/')
        filename = x[5].split('.')
        print(imagepth)
        pixmap = QtGui.QPixmap(imagepth)
        self.img1.setPixmap(QtGui.QPixmap(imagepth))
        img2bmp(imagepth,filename)
        CovertToPBM(0.3,filename)
      
        pixmap1 = QtGui.QPixmap('./PBM images/'+filename[0]+'.pbm')
        self.img2.setPixmap(pixmap1)
        Filename = filename[0]
    
       

    def Draw(self):
        
        if self.img1.pixmap()== None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Choose image first')
            msg.setWindowTitle("Error")
    
            x= msg.exec_()
        else:
            global Filename
            ConvertToSVG(Filename)
            FixSvgHeader(Filename)
            ConvertToGCode(Filename)
         


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet())
UImain = UI()
app.exec_()