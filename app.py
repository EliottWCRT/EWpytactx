import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("login.ui", self)
    def onTextChanged(self, text):
        print("Text changed", text)
    def onPushButton(self):
        print("Bouton cliqué")
    


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()