# here need a stimulation screen gui
# need a get new char method
# refresh the output string
# show the chosen position
# parameter: test string
from PyQt5.Qt import QDialog
from Online.UI_screen import Ui_Dialog


class Screen(QDialog, Ui_Dialog):
    def __init__(self):
        super(Screen, self).__init__()
        self.string_buf = []

    def process_char(self, new_char):
        pass
