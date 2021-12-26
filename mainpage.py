
from PyQt5 import QtCore, QtGui, QtWidgets
import Oyun


class Ui_Form(object):

    def botakarsi(self):
        Oyun.main(1)
        app.exit(app.exec())
        

    def ikioyunculu(self):
        Oyun.main(2)
        app.exit(app.exec())
        


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)
        Form.setMinimumSize(QtCore.QSize(1000, 600))
        Form.setMaximumSize(QtCore.QSize(1000, 600))
        Form.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(110, 270, 291, 161))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ikioyunculu)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(340, 80, 321, 131))
        font = QtGui.QFont()
        font.setFamily("MS PGothic")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 270, 291, 161))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.botakarsi)
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "2 Oyunculu oyun"))
        self.label.setText(_translate("Form", "Satranç Delux"))
        self.pushButton_2.setText(_translate("Form", "Bota karşı oyna"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
