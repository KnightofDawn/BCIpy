import numpy as np
from Offline.featrue_extractor import feature_extractor
from sklearn.externals import joblib
from keyboard import KEYBOARD

mode = 'smart_stopping'
assert mode in ['smart_stopping', 'fixed_trials'], 'Unsupported mode'


class DataProcessor(object):
    def __init__(self, samplerate, th_p, repeat_time, fserp, chosen_channel, istraining, cut_pos_head, cut_pos_tail):
        self.sampleRate = samplerate
        self._chosen_channel = chosen_channel
        self._cut_pos_head = cut_pos_head
        self._cut_pos_tail = cut_pos_tail
        self.trial_buf_len = round(samplerate * (cut_pos_tail - cut_pos_head))
        self.epoches = np.zeros((12, self.trial_buf_len))
        self.istraining = istraining
        self.repeat_time = repeat_time
        self.th_p = th_p
        self.target_cnt = 0

        # properties going to be implemented by child class
        self.data = None
        self.updatepoints = None

        try:
            self.classification_model = joblib.load('../svm_model.pkl')
        except Exception as err:
            self.classification_model = None
            print(err)
        try:
            self.scaler = joblib.load('../feature_scaler.pkl')
        except Exception as err:
            self.scaler = None
            print(err)
        # 2 class proba
        self.prediction = np.zeros((12,))

        # self.b, self.a = signal.butter(3, fsErp * 2 / self.sampleRate, 'bandpass')
        self.erpband = fserp

        self.onset_cnt = 0
        self.trial_cnt = 1

        self.downsamplingscale = self.sampleRate // 200

    def process_trial(self, onset_index):
        begin = onset_index + round(self._cut_pos_head * self.sampleRate)
        end = onset_index + round(self._cut_pos_tail * self.sampleRate)
        # mean filter
        temp = self.data[begin: end, self._chosen_channel]
        self.epoches[self.onset_cnt] = (self.trial_cnt - 1) / self.trial_cnt * self.epoches[
            self.onset_cnt] + temp / self.trial_cnt
        # filtering, downsampling and normalizing
        filt_data = feature_extractor(self.epoches[self.onset_cnt][None, ::self.downsamplingscale],
                                      samplerate=self.sampleRate,
                                      erp_band=self.erpband,
                                      scaler=self.scaler)
        # return proba of the +1 class
        self.prediction[self.onset_cnt] = self.classification_model.predict_proba(filt_data)[:, 1]

        self.onset_cnt += 1

        if self.onset_cnt >= 12:
            # got whole trial
            self.onset_cnt = 0
            if mode == 'smart_stopping':
                # test
                print(self.prediction)
                # softmax
                p1 = self.prediction[:6] / np.sum(self.prediction[:6])
                p2 = self.prediction[6:] / np.sum(self.prediction[6:])
                pos1 = np.argmax(p1)
                pos2 = np.argmax(p2)
                if p1[pos1] * p2[pos2] > self.th_p:
                    # test
                    print(pos1, pos2)
                    # print(input_char)
                    # clear epoches
                    self.epoches[:, :] = 0
                    self.trial_cnt = 1
                    return KEYBOARD[pos1, pos2]
                else:
                    self.trial_cnt += 1
            elif mode == 'fixed_trials':
                if self.trial_cnt >= self.repeat_time:
                    pos1 = np.argmax(self.prediction[:6])
                    pos2 = np.argmax(self.prediction[6:])
                    return KEYBOARD[pos1, pos2]
                else:
                    self.trial_cnt += 1
        return None

    def training_count(self):
        # no need to predict when training
        # count trial and trigger is enough
        self.onset_cnt += 1
        if self.onset_cnt == 12:
            self.onset_cnt = 0
            if self.trial_cnt == self.repeat_time:
                return True
            else:
                self.trial_cnt += 1
        return False

    def process_data(self):
        # called when get new data
        # check onset
        if self.data.shape[0] < self.trial_buf_len + self.updatepoints:
            return
        check_points = self.data[-self.trial_buf_len - self.updatepoints:-self.trial_buf_len, -1]
        # first trigger is 2
        onset_index = list(np.nonzero(check_points > .5)) if self.onset_cnt else list(
            np.nonzero(check_points > 1.5))
        if onset_index:
            if not self.istraining:
                result = self.process_trial(onset_index[0] - self.trial_buf_len - self.updatepoints)
                if result is not None:
                    self.target_cnt += 1
                    print(result)
                    # self.new_char()
                    # self.screen.process_char(result)
            elif self.training_count():
                # self.screen.process_char(sti_string[self.target_cnt])
                self.target_cnt += 1
                # if self.target_cnt == len(sti_string):
                # finish and close screen
                # self.screen.close()

    def _disconnect(self):
        # super(DataProcessor, self)._disconnect()
        self.onset_cnt = 0
        self.trial_cnt = 1
        self.prediction[:] = 0
        self.epoches[:, :] = 0
        # self.screen.string_buf = []
