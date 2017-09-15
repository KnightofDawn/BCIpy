# here need a stimulation screen gui
# need a get new char method
# refresh the output string
# show the chosen position
# parameter: test string
from PyQt5.Qt import QDialog
from PyQt5 import QtGui
from Online.UI_screen import Ui_Dialog
from PyQt5.Qt import QParallelAnimationGroup, QPropertyAnimation

class Screen(QDialog, Ui_Dialog):
    def __init__(self, istraining):
        super(Screen, self).__init__()
        # set background color
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setPalette(pal)
        self.string_buf = []
        self.istraining = istraining

    def process_char(self, new_char):
        pass

    def run_experiment(self):
        self.setWindowFlags(QDialog)
        self.showFullScreen()
        print('run')
