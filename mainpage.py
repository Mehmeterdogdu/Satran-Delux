
from PyQt5 import QtCore, QtGui, QtWidgets
import Oyun 
import kayıtlıoyunlar

class Ui_Form(object):

    def botakarsisiyah(self):
        Oyun.main(1,2,0,0,0)
        sys.exit(app.exec_())
    def botakarsibeyaz(self):
        Oyun.main(1,1,0,0,0)
        sys.exit(app.exec_())
    def ikioyunculu(self):
        Oyun.main(2,0,0,0,0)
        sys.exit(app.exec_())
    def oyunyukle(self):
        self.mainwindow = QtWidgets.QMainWindow()
        self.ui = kayıtlıoyunlar.secondform()
        self.ui.setupUi(self.mainwindow)
        self.mainwindow.show()
        

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 700)
        Form.setMinimumSize(QtCore.QSize(1000, 700))
        Form.setMaximumSize(QtCore.QSize(1000, 700))
        Form.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(110, 230, 291, 161))
        self.pushButton.setMinimumSize(QtCore.QSize(401, 141))
        self.pushButton.setMaximumSize(QtCore.QSize(401, 141))
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
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 370, 401, 141))
        self.pushButton_3.setMinimumSize(QtCore.QSize(401, 141))
        self.pushButton_3.setMaximumSize(QtCore.QSize(401, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.botakarsisiyah)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 230, 401, 141))
        self.pushButton_2.setMinimumSize(QtCore.QSize(401, 141))
        self.pushButton_2.setMaximumSize(QtCore.QSize(400, 1000))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.botakarsibeyaz)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(110, 370, 401, 141))
        self.pushButton_4.setMinimumSize(QtCore.QSize(401, 141))
        self.pushButton_4.setMaximumSize(QtCore.QSize(401, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.pushButton_4.setObjectName("pushButton_3")
        self.pushButton_4.clicked.connect(self.oyunyukle)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "2 Oyunculu oyun"))
        self.label.setText(_translate("Form", "Satranç Delux"))
        self.pushButton_3.setText(_translate("Form", "Siyah bota karşı oyna"))
        self.pushButton_2.setText(_translate("Form", "Beyaz bota karşı oyna"))
        self.pushButton_4.setText(_translate("Form", "Oyun yükle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
