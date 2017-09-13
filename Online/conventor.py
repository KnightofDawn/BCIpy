from PyQt5 import uic
fin = open('dialog.ui','r')
fout = open('UI_screen.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()
