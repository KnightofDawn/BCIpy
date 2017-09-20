import pyqtgraph as pg
from PyQt5.Qt import QApplication, QTimer, QMainWindow
from Online.UI_main import Ui_MainWindow
from Online.Amplifiers import AmplifierNeuracle, Amplifier301
from config import load_config
import numpy as np
import sys

# load config
config = load_config()
nChan = int(config['nChan'])
sampleRate = int(config['samplerate'])
# currently only support single channel
chosen_channel = int(config['nChan'])
repeat_time = int(config['n_rep_train'])

fsErp = np.array([float(config['erp_band_low']), float(config['erp_band_high'])])
cut_pos_head = float(config['t_head'])
cut_pos_tail = float(config['t_tail'])

sti_string = config['sti_string']
# in seconds
updateInterval = 0.04
ipAddress = 'localhost'
serverPort = 8712
# in seconds
bufferSize = 1.

# prediction probability threshold
th_p = 0.7
istraining = False


class APP(QMainWindow, Ui_MainWindow):
    def __init__(self, dataclient):
        # gui settings
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.DataClient = dataclient
        super(APP, self).__init__()
        self.setupUi(self)
        # self.screen = visulScreen()
        self.actionConnect.triggered.connect(self.DataClient._connect)
        self.actionDisconnect.triggered.connect(self.DataClient._disconnect)
        self.actionStart.triggered.connect(self.start_recording)
        self.actionStop.triggered.connect(self.DataClient.end_recording)
        # self.pushButton.clicked.connect(self.sti_screen)
        # self.pushButton_2.clicked.connect(self.screen.run_experiment)
        self.graph.plotItem.showGrid(True, True, 0.7)

        # data receiver clock
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.DataClient.process_data)
        # plotting clock
        self.plotting_timer = QTimer()
        self.plotting_timer.timeout.connect(self.update_frame)

    def update_frame(self):
        print('update_frame is running')
        x = np.linspace(0, self.DataClient.data.shape[0] // self.DataClient.sampleRate,
                        self.DataClient.data.shape[0]) + self.DataClient.cumtime
        self.graph.plot(x, self.DataClient.data[:, :-1])
        self.graph_2.plot(x, self.DataClient.data[:, -1])
        QApplication.processEvents()

    def _connect(self):
        if self.DataClient._connect():
            # start timer
            self.data_timer.start(self.DataClient.updateInterval)
            self.plotting_timer.start(self.DataClient.updateInterval)

    def _disconnect(self):
        self.DataClient._disconnect()
        self.data_timer.stop()
        self.plotting_timer.stop()

    def start_recording(self):
        self.DataClient.get_filecursor(self.textEdit.toPlainText())


if __name__ == "__main__":
    # create qt object to run Qtimer
    app = QApplication(sys.argv)
    # connect
    amplifier = AmplifierNeuracle(fserp=fsErp,
                           th_p=th_p,
                           repeat_time=repeat_time,
                           chosen_channel=chosen_channel,
                           istraining=istraining,
                           cut_pos_head=cut_pos_head,
                           cut_pos_tail=cut_pos_tail,
                           updateInterval=updateInterval,
                           ipAddress=ipAddress,
                           serverPort=serverPort,
                           nChan=nChan,
                           sampleRate=sampleRate,
                           bufferSize=bufferSize,
                           sti_string=sti_string)
    window = APP(amplifier)
    window.show()

    exit(app.exec_())
