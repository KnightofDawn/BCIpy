from PyQt5.Qt import QDialog, QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtOpenGL
from Online.UI_screen import Ui_Dialog
from keyboard import KEYBOARD
from PyQt5.Qt import QParallelAnimationGroup

sti_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (160, 82, 45), (100, 120, 100)]

class Screen(QDialog, Ui_Dialog):
    def __init__(self, sti_string):
        super(Screen, self).__init__()
        self.setupUi(self)
        # set background color
        #pal = QtGui.QPalette()
        #pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        #self.setPalette(pal)
        self.textBrowser.setFontPointSize(30)
        self.textBrowser.setText(' '.join(sti_string))

        self.string_buf = []
        self.sti_string = sti_string

    def draw_rect(self):
        w, h = self.frameGeometry().width(), self.frameGeometry().height()
        L_squL = 0.9 * min(w, h)
        w_offset = (w - L_squL) // 2
        h_offset = (h - L_squL) // 2 + 100
        L_squS = L_squL // 18
        for i in range(6):
            for j in range(6):
                col_s = w_offset + L_squS + 3 * i * L_squS
                row_s = h_offset + L_squS + 3 * j * L_squS

    def process_char(self, result):
        self.string_buf.append(result)
        self.textBrowser_2.setFontPointSize(30)
        self.textBrowser_2.setText(self.string_buf)
        pass

    def run_experiment(self):
        print('run experiment')
