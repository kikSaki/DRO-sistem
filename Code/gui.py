import sys
import serial
from time import sleep

from PyQt5.QtCore import QSize, Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QMainWindow, QButtonGroup
from PyQt5.QtGui import QFont

class UpdateX(QObject):
    progress = pyqtSignal(str)

    arduinoX = serial.Serial(port='COM3', baudrate=115200)

    def setX_os(self):

        while(True):
            #if(self.arduinoX.readline()):
            poz = self.arduinoX.readline().decode('UTF-8').rstrip()
            #print(poz.rjust(5, "0"))

            self.progress.emit(poz.zfill(6))
            #print(poz.zfill(6))

            #print(type(poz))
            #print(self.arduinoX.readline())
    
    def setX(self, value):
        self.arduinoX.write(value.encode())


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Demo - Merilne letve")
        self.setFixedSize(QSize(800, 420))

        widget = QWidget()
        self.setCentralWidget(widget)
        
        layout = QGridLayout()

        widget.setLayout(layout)

        

        self.xOs = QLineEdit("000000")
        self.xOs.setFixedSize(410, 100)
        self.xOs.setFont(QFont('Arial', 60))
        self.xOs.setReadOnly(True)
        self.yOs = QLineEdit("000000")
        self.yOs.setFixedSize(410, 100)
        self.yOs.setFont(QFont('Arial', 60))
        self.yOs.setReadOnly(True)
        self.zOs = QLineEdit("000000")
        self.zOs.setFixedSize(410, 100)
        self.zOs.setFont(QFont('Arial', 60))
        self.zOs.setReadOnly(True)

        self.xButton = QPushButton("X")
        self.xButton.setFixedSize(60, 60)
        self.xButton.setFont(QFont('Arial', 20))
        self.xButtonRes = QPushButton("RES")
        self.xButtonRes.setFixedSize(60, 60)
        self.xButtonRes.setFont(QFont('Arial', 15))
        self.xButtonRes.setObjectName("resX")

        self.yButton = QPushButton("Y")
        self.yButton.setFixedSize(60, 60)
        self.yButton.setFont(QFont('Arial', 20))
        self.yButtonRes = QPushButton("RES")
        self.yButtonRes.setFixedSize(60, 60)
        self.yButtonRes.setFont(QFont('Arial', 15))
        self.yButtonRes.setObjectName("resY")

        self.zButton = QPushButton("Z")
        self.zButton.setFixedSize(60, 60)
        self.zButton.setFont(QFont('Arial', 15))
        self.zButtonRes = QPushButton("RES")
        self.zButtonRes.setFixedSize(60, 60)
        self.zButtonRes.setFont(QFont('Arial', 15))
        self.zButtonRes.setObjectName("resZ")



        self.ena = QPushButton("1")
        self.ena.setFixedSize(60, 60)
        self.ena.setObjectName("1")
        self.dva = QPushButton("2")
        self.dva.setFixedSize(60, 60)
        self.dva.setObjectName("2")
        self.tri = QPushButton("3")
        self.tri.setFixedSize(60, 60)
        self.tri.setObjectName("3")
        self.štiri = QPushButton("4")
        self.štiri.setFixedSize(60, 60)
        self.štiri.setObjectName("4")
        self.pet = QPushButton("5")
        self.pet.setFixedSize(60, 60)
        self.pet.setObjectName("5")
        self.šest = QPushButton("6")
        self.šest.setFixedSize(60, 60)
        self.šest.setObjectName("6")
        self.sedem = QPushButton("7")
        self.sedem.setFixedSize(60, 60)
        self.sedem.setObjectName("7")
        self.osem = QPushButton("8")
        self.osem.setFixedSize(60, 60)
        self.osem.setObjectName("8")
        self.devet = QPushButton("9")
        self.devet.setFixedSize(60, 60)
        self.devet.setObjectName("9")
        self.nič = QPushButton("0")
        self.nič.setFixedSize(60, 60)
        self.nič.setObjectName("0")
        self.clear = QPushButton("Clear")
        self.clear.setFixedSize(60, 60)
        self.clear.setObjectName("Clear")
        self.enter = QPushButton("Enter")
        self.enter.setFixedSize(60, 60)
        self.enter.setObjectName("Enter")
        self.ena.setEnabled(False)
        self.dva.setEnabled(False)
        self.tri.setEnabled(False)
        self.štiri.setEnabled(False)
        self.pet.setEnabled(False)
        self.šest.setEnabled(False)
        self.sedem.setEnabled(False)
        self.osem.setEnabled(False)
        self.devet.setEnabled(False)
        self.nič.setEnabled(False)
        self.clear.setEnabled(False)
        self.enter.setEnabled(False)

    
        

        layout.addWidget(self.xOs, 0, 0, 2, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.yOs, 2, 0, 2, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zOs, 4, 0, 2, 1, Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.xButton, 0, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.xButtonRes, 1, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.yButton, 2, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.yButtonRes, 3, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zButton, 4, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zButtonRes, 5, 1, Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.ena, 1, 2, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.dva, 1, 3, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.tri, 1, 4, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.štiri, 2, 2, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.pet, 2, 3, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.šest, 2, 4, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.sedem, 3, 2, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.osem, 3, 3, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.devet, 3, 4, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.nič, 4, 3, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.clear, 4, 4, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.enter, 4, 2, Qt.AlignmentFlag.AlignLeft)
       



        self.btn_grpReset = QButtonGroup()
        self.btn_grpReset.setExclusive(True)
        self.btn_grpReset.addButton(self.xButtonRes)
        self.btn_grpReset.addButton(self.yButtonRes)
        self.btn_grpReset.addButton(self.zButtonRes)
        self.btn_grpReset.buttonClicked.connect(self.resetButton)


        self.btn_numbers = QButtonGroup()
        self.btn_numbers.setExclusive(True)
        self.btn_numbers.addButton(self.ena)
        self.btn_numbers.addButton(self.dva)
        self.btn_numbers.addButton(self.tri)
        self.btn_numbers.addButton(self.štiri)
        self.btn_numbers.addButton(self.pet)
        self.btn_numbers.addButton(self.šest)
        self.btn_numbers.addButton(self.sedem)
        self.btn_numbers.addButton(self.osem)
        self.btn_numbers.addButton(self.devet)
        self.btn_numbers.addButton(self.nič)
        self.btn_numbers.addButton(self.clear)
        self.btn_numbers.addButton(self.enter)
        self.btn_numbers.buttonClicked.connect(self.numberButton)

        self.xButton.clicked.connect(self.numbersXos)


        self.updateX = UpdateX()
        self.xThread = QThread()

        self.updateX.progress.connect(self.setX)

        self.updateX.moveToThread(self.xThread)
        self.xThread.started.connect(self.updateX.setX_os)
        self.xThread.start()



        self.show()

        
    def setX(self, v):
        self.xOs.setText(v)
    



    def numbersXos(self):
        #self.xButton.setEnabled(False)

        #print(self.xOs.text())

        self.xOs.setText("")
        self.ena.setEnabled(True)
        self.dva.setEnabled(True)
        self.tri.setEnabled(True)
        self.štiri.setEnabled(True)
        self.pet.setEnabled(True)
        self.šest.setEnabled(True)
        self.sedem.setEnabled(True)
        self.osem.setEnabled(True)
        self.devet.setEnabled(True)
        self.nič.setEnabled(True)
        self.clear.setEnabled(True)
        self.enter.setEnabled(True)
        
        #self.btn_numbers.buttonClicked.connect(self.numberButton)

    def numberButton(self, a):
        #print(a)
        #self.xOs.setText("000000")
        text = self.xOs.text()

        if a.objectName() == "1":
            text = text + "1"
            self.xOs.setText(text)
        elif a.objectName() == "2":
            text = text + "2"
            self.xOs.setText(text)
        elif a.objectName() == "3":
            text = text + "3"
            self.xOs.setText(text)
        elif a.objectName() == "4":
            text = text + "4"
            self.xOs.setText(text)
        elif a.objectName() == "5":
            text = text + "5"
            self.xOs.setText(text)
        elif a.objectName() == "6":
            text = text + "6"
            self.xOs.setText(text)
        elif a.objectName() == "7":
            text = text + "7"
            self.xOs.setText(text)
        elif a.objectName() == "8":
            text = text + "8"
            self.xOs.setText(text)
        elif a.objectName() == "9":
            text = text + "9"
            self.xOs.setText(text)
        elif a.objectName() == "0":
            text = text + "0"
            self.xOs.setText(text)

        elif a.objectName() == "Clear":
            text = ""
            self.xOs.setText(text)

        elif a.objectName() == "Enter":
            self.updateX.setX(text)

            self.ena.setEnabled(False)
            self.dva.setEnabled(False)
            self.tri.setEnabled(False)
            self.štiri.setEnabled(False)
            self.pet.setEnabled(False)
            self.šest.setEnabled(False)
            self.sedem.setEnabled(False)
            self.osem.setEnabled(False)
            self.devet.setEnabled(False)
            self.nič.setEnabled(False)
            self.clear.setEnabled(False)
            self.enter.setEnabled(False)
            #self.xButton.setEnabled(True)


    def resetButton(self, b):

        if b.objectName() == "resX":
            self.xOs.setText("000000")
            UpdateX.arduinoX.setDTR(False)
            sleep(0.22)
            UpdateX.arduinoX.setDTR(True)
        elif b.objectName() == "resY":
            self.yOs.setText("000000")
        else:
            self.zOs.setText("000000")



    



app = QApplication(sys.argv)
window = MainWindow()

app.exec()
