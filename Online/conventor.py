from PyQt5 import uic
fin = open('BCI.ui','r')
fout = open('UI_main.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()
