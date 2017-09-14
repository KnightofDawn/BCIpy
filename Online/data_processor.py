import numpy as np
from Offline.featrue_extractor import feature_extractor
from Online.Client import DataClient
from sklearn.externals import joblib
import sys
from PyQt5.Qt import QApplication
from keyboard import KEYBOARD
from Offline.config import load_config

# load config
config = load_config()
nChan = int(config['nChan'])
# currently only support single channel
chosen_channel = int(config['nChan'])
sampleRate = int(config['samplerate'])
repeat_time = int(config['n_rep_train'])
fsErp = np.array([float(config['erp_band_low']), float(config['erp_band_high'])])
cut_pos_head = float(config['t_head'])
cut_pos_tail = float(config['t_tail'])
# in seconds
updateInterval = 0.04
ipAddress = 'localhost'
serverPort = 8712
# in seconds
bufferSize = 0.5
# prediction probability threshold
th_p = 0.7
mode = 'smart_stopping'
assert mode in ['smart_stopping', 'fixed_trials'], 'Unsupported mode'


class DataProcessor(DataClient):
    def __init__(self, fserp, chosen_channel, istraining=False, cut_pos_head=0., cut_pos_tail=.5, **kwargs):
        super(DataProcessor, self).__init__(**kwargs)
        self._chosen_channel = chosen_channel
        self._cut_pos_head = cut_pos_head
        self._cut_pos_tail = cut_pos_tail
        trial_buf_len = round(self.sampleRate * (cut_pos_tail - cut_pos_head))
        self.epoches = np.zeros((12, trial_buf_len, len(chosen_channel)))
        self.training_flag = istraining
        try:
            self.classification_model = joblib.load('../svm_model.pkl')
            self.scaler = joblib.load('../feature_scaler.pkl')
        except Exception as err:
            self.classification_model = None
            self.scaler = None
            print(err)
        self.prediction = np.zeros((12,))

        # self.b, self.a = signal.butter(3, fsErp * 2 / self.sampleRate, 'bandpass')
        self.erpband = fserp

        self.onset_cnt = 0
        self.trial_cnt = 1

        self.downsamplingscale = self.sampleRate // 200

        # 6x6 keyboard
        self.keyboard_book = KEYBOARD

    def process_trial(self, onset_index):
        begin = onset_index + round(self._cut_pos_head * self.sampleRate)
        end = onset_index + round(self._cut_pos_tail * self.sampleRate)
        # average
        temp = self.data[begin: end, self._chosen_channel]
        self.epoches[self.onset_cnt] = (self.trial_cnt - 1) / self.trial_cnt * self.epoches[
            self.onset_cnt] + temp / self.trial_cnt
        # filtering, downsampling and normalizing
        filt_data = feature_extractor(self.epoches[self.onset_cnt][None, ::self.downsamplingscale],
                                      samplerate=self.sampleRate,
                                      erp_band=self.erpband,
                                      scaler=self.scaler)

        self.prediction[self.onset_cnt] = self.classification_model.predict(filt_data)

        self.onset_cnt += 1

        if self.onset_cnt >= 12:
            # got whole trial
            self.onset_cnt = 0
            if mode == 'smart_stopping':
                # softmax
                p1 = np.exp(self.prediction[:6])
                p1 /= np.sum(p1)
                p2 = np.exp(self.prediction[6:])
                p2 /= np.sum(p2)
                pos1 = np.argmax(p1)
                pos2 = np.argmax(p2)
                input_char = self.keyboard_book[pos1, pos2]
                if p1[pos1] * p2[pos2] > th_p:
                    # print(input_char)
                    # clear epoches
                    self.epoches[:, :, :] = 0
                    self.trial_cnt = 1
                    return input_char
                else:
                    self.trial_cnt += 1
            elif mode == 'fixed_trials':
                if self.trial_cnt >= repeat_time:
                    pos1 = np.argmax(self.prediction[:6])
                    pos2 = np.argmax(self.prediction[6:])
                    return self.keyboard_book[pos1, pos2]
                else:
                    self.trial_cnt += 1
        return None

    def get_data(self):
        super(DataProcessor, self).get_data()
        self.process_data()

    def process_data(self):
        # check onset
        data_buffer_len = round(self.sampleRate * self.timestep)
        check_points = self.data[-data_buffer_len - self.updatepoints, -1]
        onset_index = np.nonzero(np.diff(check_points) > .5)
        if onset_index:
            result = self.process_trial(onset_index[0] - data_buffer_len - self.updatepoints)
            if result is not None:
                # get a new char
                # call screen refresh method
                self.screen.process_char(result)

    def _disconnect(self):
        super(DataProcessor, self)._disconnect()
        self.onset_cnt = 0
        self.trial_cnt = 1
        self.prediction[:] = 0
        self.epoches[:, :, :] = 0
        self.screen.string_buf = []


if __name__ == "__main__":
    # create qt object to run Qtimer
    app = QApplication(sys.argv)
    # connect
    window = DataProcessor(chosen_channel=chosen_channel,
                           istraining=False,
                           cut_pos_head=cut_pos_head,
                           cut_pos_tail=cut_pos_tail,
                           updateInterval=updateInterval,
                           ipAddress=ipAddress,
                           serverPort=serverPort,
                           nChan=nChan,
                           sampleRate=sampleRate,
                           bufferSize=bufferSize)
    window.show()

    exit(app.exec_())
