from PyQt5 import QtCore, QtGui, QtWidgets
from os import system
from pathlib import Path


class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(390, 386)
        window.setStyleSheet("background-color:rgb(170, 255, 255)")
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.s_path = QtWidgets.QPushButton(self.centralwidget)
        self.s_path.setGeometry(QtCore.QRect(10, 60, 151, 51))
        self.s_path.setStyleSheet("background-color:rgb(212, 212, 212)")
        self.s_path.setObjectName("s_path")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(140, 10, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 80, 211, 31))
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet("background-color:white")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 150, 211, 31))
        self.lineEdit_2.setStyleSheet("background-color:white")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.d_path = QtWidgets.QPushButton(self.centralwidget)
        self.d_path.setGeometry(QtCore.QRect(10, 130, 151, 51))
        self.d_path.setStyleSheet("background-color:rgb(212, 212, 212)")
        self.d_path.setObjectName("d_path")
        self.success = QtWidgets.QLabel(self.centralwidget)
        self.success.setGeometry(QtCore.QRect(10, 350, 211, 31))
        self.success.setText("")
        self.success.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.success.setObjectName("success")
        self.convert = QtWidgets.QPushButton(self.centralwidget)
        self.convert.setGeometry(QtCore.QRect(50, 270, 301, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.convert.setFont(font)
        self.convert.setStyleSheet("background-color:rgb(212, 212, 212)")
        self.convert.setObjectName("convert")
        self.new_name_line = QtWidgets.QLineEdit(self.centralwidget)
        self.new_name_line.setGeometry(QtCore.QRect(170, 220, 211, 31))
        self.new_name_line.setStyleSheet("background-color:white")
        self.new_name_line.setObjectName("new_name_line")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(10, 220, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_label.setFont(font)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setObjectName("name_label")
        window.setCentralWidget(self.centralwidget)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.s_path.clicked.connect(self.get_spath)
        self.d_path.clicked.connect(self.get_dpath)
        self.convert.clicked.connect(self.convert_press)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Pie2Ui"))
        self.s_path.setText(_translate("window", "Browse for .ui"))
        self.title.setText(_translate("window", "UI to PY"))
        self.d_path.setText(_translate("window", "Destination Folder"))
        self.convert.setText(_translate("window", "CONVERT!"))
        self.name_label.setText(_translate("window", "Name File (.py):"))

    def get_spath(self):
        self.source, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open UI File', r"C:\\Users\\llcze\\Desktop\\ui_files\\", "Designer UI Files (*.ui)")
        self.lineEdit.setText(self.source)

    def get_dpath(self):
        self.dest = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        self.lineEdit_2.setText(self.dest)
        
    def convert_press(self):
        pyuic = r"C:\Users\llcze\AppData\Local\Programs\Python\Python38-32\Scripts\pyuic5"
        destination = Path(self.dest) / self.new_name_line.text()
        system('cmd /c "{} -x {} -o {}'.format(pyuic, self.source, destination))
        self.success.setText("Success")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
