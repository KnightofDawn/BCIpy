import numpy as np
import struct
from scipy import signal


def _preprocess(data, samplerate):
    b1, a1 = signal.butter(3, np.array([48, 51]) / samplerate, 'bandstop')
    b2, a2 = signal.butter(3, np.array([98, 102]) / samplerate, 'bandstop')
    b3, a3 = signal.butter(3, np.array([148, 152]) / samplerate, 'bandstop')
    data = signal.filtfilt(b1, a1, data, axis=0)
    data = signal.filtfilt(b2, a2, data, axis=0)
    data = signal.filtfilt(b3, a3, data, axis=0)
    return data


def bytes2npz(path, nChan, samplerate):
    # dpath = path.join('../data', subjectname)
    # dfile = [f for f in listdir(dpath) if path.isfile(f)]
    with open(path) as f:
        s = bytes(f.read())
    data_length = len(s) // 4  # datatype float
    unpacked = struct.unpack(str(data_length) + 'f', s)
    reshaped = np.reshape(unpacked, (-1, int(nChan)))
    reshaped[:, :-1] = _preprocess(reshaped[:, :-1], samplerate)
    return reshaped
