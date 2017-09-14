import socket
import struct
from os.path import isfile, join
from os import mkdir
import datetime
import numpy as np
import pyqtgraph as pg
from PyQt5.Qt import QApplication, QTimer, QMainWindow
from Online.UI_main import Ui_MainWindow
from Online.screen import Screen


# Tcp/Ip client and main GUI class
class DataClient(QMainWindow, Ui_MainWindow):
    def __init__(self,
                 updateInterval,
                 ipAddress,
                 serverPort,
                 nChan,
                 sampleRate,
                 bufferSize):
        # initial parameters
        self.updateInterval = updateInterval
        self.serverPort = serverPort
        self.ipAddress = ipAddress
        self.nChan = nChan
        self.sampleRate = sampleRate

        self.data = np.empty((0, nChan))
        self.TCPIP = None
        self.bufsize = round(bufferSize * sampleRate)
        if round(sampleRate * updateInterval) > 1:
            self.updatepoints = round(sampleRate * updateInterval)
        else:
            self.updatepoints = sampleRate
        self.BytesCnt = 4 * nChan * self.updatepoints
        self.cumtime = None
        self.filecursor = None

        # gui settings
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        super(DataClient, self).__init__()
        self.screen = Screen()
        self.setupUi(self)
        self.actionConnect.triggered.connect(self._connect)
        self.actionDisconnect.triggered.connect(self._disconnect)
        self.actionStart.triggered.connect(self.start_recording)
        self.actionStop.triggered.connect(self.end_recording)
        self.pushButton.clicked.connect(self.sti_screen)
        self.graph.plotItem.showGrid(True, True, 0.7)

        # data receiver clock
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.get_data)
        # plotting clock
        self.plotting_timer = QTimer()
        self.plotting_timer.timeout.connect(self.update_frame)

    def _connect(self):
        self.cumtime = 0.
        # connect tcpip socket
        self.TCPIP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.TCPIP.connect((self.ipAddress, self.serverPort))
        except Exception as err:
            print(err)
            return
        print('Succesfully connected.')
        # start timer
        self.data_timer.start(self.updateInterval)
        self.plotting_timer.start(self.updateInterval)

    def start_recording(self):
        # create save path
        username = self.textEdit.toPlainText()
        try:
            mkdir(join('../data', username))
        except:
            pass
        time = datetime.date.today().strftime('%m-%d-%y')
        filename = join('../data', username, time)

        index = 0
        while isfile(filename + '_%d' % index):
            index += 1
        self.filecursor = open(filename + '_%d' % index, 'a')
        print('Start recording data, file name: %s' % (filename + '_%d' % index))

    def get_data(self):
        self.cumtime += self.updateInterval
        # receive raw bytes
        raw_data = ''
        while len(raw_data) < self.BytesCnt:
            raw_data += self.TCPIP.recv(self.BytesCnt - len(raw_data))
        if self.filecursor is not None:
            self.filecursor.write(raw_data)
        # reshape and interp as float
        length_rawdata = len(raw_data)
        num_rawdata = length_rawdata // 4
        data_interpreted = struct.unpack(str(num_rawdata) + 'f', raw_data)
        data_channel = np.reshape(data_interpreted, (-1, self.nChan))

        # cut if too long
        userdatalength = self.data.shape[0] + data_channel.shape[0]
        if userdatalength > self.bufsize:
            cut_length = userdatalength - self.bufsize
            self.data = np.row_stack((self.data[cut_length:], data_channel))
        else:
            self.data = np.row_stack((self.data, data_channel))

    def update_frame(self):
        x = np.linspace(0, self.data.shape[0] // self.sampleRate, self.data.shape[0]) + self.cumtime
        self.graph.plot(x, self.data[:, :-1])
        self.graph_2.plot(x, self.data[:, -1])
        QApplication.processEvents()

    def end_recording(self):
        self.filecursor.close()
        self.filecursor = None
        print('End recording.')

    def _disconnect(self):
        self.cumtime = 0
        self.TCPIP.close()
        self.data_timer.stop()
        self.plotting_timer.stop()
        print('Disconnected.')

    def sti_screen(self):
        # open a dialog window
        self.screen.show()
