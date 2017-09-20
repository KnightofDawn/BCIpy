import socket
import struct
from os.path import isfile, join
from os import mkdir
import datetime
import numpy as np
from Online.Data_processor_base import DataProcessor
import parallel


class AmplifierNeuracle(DataProcessor):
    # Neuracle Amplifier
    def __init__(self,
                 updateInterval,
                 ipAddress,
                 serverPort,
                 nChan,
                 sampleRate,
                 bufferSize,
                 **kwargs):
        # initial parameters
        super(AmplifierNeuracle, self).__init__(samplerate=sampleRate, **kwargs)
        self.updateInterval = updateInterval
        self.serverPort = serverPort
        self.ipAddress = ipAddress
        self.nChan = nChan
        self.sampleRate = sampleRate

        self.data = np.empty((0, nChan))
        # self.TCPIP = None
        self.dataclient = None
        self.bufsize = round(bufferSize * sampleRate)
        if round(sampleRate * updateInterval) > 1:
            self.updatepoints = round(sampleRate * updateInterval)
        else:
            self.updatepoints = sampleRate
        self.BytesCnt = 4 * nChan * self.updatepoints
        # x index used to plot data
        self.cumtime = 0
        self.filecursor = None

    def _connect(self):
        self.cumtime = 0.
        # connect tcpip socket
        self.TCPIP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.dataclient = parallel.Parallel(port=port_address)
        try:
            self.TCPIP.connect((self.ipAddress, self.serverPort))
        except Exception as err:
            print(err)
            return False
        print('Succesfully connected.')
        return True

    def get_filecursor(self, string):
        # create save path
        username = string
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

    def process_data(self):
        print('get_data is running')
        print(self.cumtime)
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

        # call data processor to check stimulations and process data
        super(AmplifierNeuracle, self).process_data()

    def end_recording(self):
        self.filecursor.close()
        self.filecursor = None
        print('End recording.')

    def _disconnect(self):
        if self.filecursor is not None:
            self.filecursor.close()
            self.filecursor = None
        self.cumtime = 0
        self.TCPIP.close()
        print('Disconnected.')


class Amplifier301(DataProcessor):
    def __init__(self, samplerate, **kwargs):
        super(Amplifier301, self).__init__(samplerate=samplerate, **kwargs)
        # parallel port
