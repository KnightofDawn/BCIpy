import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

'''
1. find trigger
2. reshape & downsampling
3. average
4. plot spectrogram
4. extract Erp features
5. extract Hg
6. concatenate features
7. normalize
'''


def trigger_search(trigger_channel_data, samplerate, plot=True):
    pos = np.nonzero(np.diff(trigger_channel_data) >= .5)
    # next implementing trigger check
    pos_checked = pos
    if plot:
        plt.figure()
        plt.scatter(pos, np.ones_like(pos), c='r')
        plt.scatter(pos_checked, -np.ones_like(pos), c='b')
    return pos_checked


def signal_reshape(data, trigger_pos, samplerate, t_head, t_tail, nChan):
    # reshape to (n_trig, timestep, nchan)
    down_sampling_factor = samplerate // 200
    start = samplerate * t_head
    end = samplerate * t_tail
    length = trigger_pos.shape[0]
    batch_data = np.empty((length, (end - start) // down_sampling_factor, nChan))
    batch_data[range(length)] = data[trigger_pos[range(length)] + start:trigger_pos[range(length)] + end][
                                ::down_sampling_factor]
    return batch_data


def average_signal(data, n_rep_exp, n_rep_train):
    data = np.reshape(data, (-1, n_rep_exp, 12, data.shape[1], data.shape[2]))
    # 5d tensor (n_char, n_rep_exp, 12, timestep, n_channel)
    data_averaged = np.empty((data.shape[0], n_rep_exp // n_rep_train, 12, data.shape[-2], data.shape[-1]))
    for j in range(data.shape[0]):
        exp = data[j]
        for i in range(0, exp.shape[0] - n_rep_train, n_rep_train):
            data_averaged[j, i // n_rep_train] = exp[:, i:i + n_rep_train].mean(axis=0)
    return data_averaged.reshape((-1, data_averaged.shape[-1]))


def spec_plot(data, samplerate):
    pass


def erp_extractor(data, samplerate, erp_band):
    b, a = signal.butter(3, erp_band * 2 / samplerate, 'bandpass')
    data = signal.filtfilt(b, a, data, axis=1)
    return data


def hg_extractor(data, samplerate, hg_band):
    b, a = signal.butter(3, hg_band * 2 / samplerate, 'bandpass')
    data = signal.filtfilt(b, a, data, axis=1)
    feature = np.abs(signal.hilbert(data, axis=1))
    return feature


def feature_extractor(data, samplerate, erp_band, hg_band=None, scaler=None):
    assert len(data.shape) == 2, 'Currently feature extractor only support single channel input!'
    erp = erp_extractor(data, samplerate, erp_band)
    if hg_band is not None:
        hg = hg_extractor(data, samplerate, hg_band)
        # 2d tensor (sample, feature_dims)
        sample = np.concatenate((erp, hg), axis=1)
    else:
        sample = erp
    if scaler is None:
        scaler = StandardScaler()
    scaler.fit(sample)
    # save scaler
    joblib.dump(scaler, '../feature_scaler.pkl')
    return scaler.transform(sample)
