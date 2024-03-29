from config import load_config, write_config
from Offline.bytes2npz import bytes2npz
from Offline.featrue_extractor import *
from Offline.classifier_training import *

if __name__ == '__main__':
    config_path = '../Config.csv'
    config = load_config()
    nChan = int(config['nChan'])
    samplerate = int(config['samplerate'])
    subjname = config['subjname']
    n_rep = config['n_rep']
    n_rep_train = config['n_rep_train']
    print(config)
    file_path = '../data/'
    data = bytes2npz(path=file_path, samplerate=samplerate, nChan=nChan)
    np.savez_compressed(file_path + '.npz', data=data)
    # search trigger signal
    tri_pos = trigger_search(trigger_channel_data=data[:, -1], samplerate=samplerate, plot=False)
    # extract trigger potential return 2d signal
    data_tri = signal_reshape(data, trigger_pos=tri_pos, t_head=0, t_tail=.5, samplerate=samplerate, nChan=nChan)
    # average
    data_for_training = average_signal(data_tri, n_rep_exp=n_rep, n_rep_train=n_rep_train)
    # plot spectrogram
    # wait for implementing
    # input erp_band and t start t end
    erp_band_low = input('input Erp band low:')
    erp_band_high = input('input Erp band high:')
    t_head = input('input t start:')
    t_tail = input('input t end:')
    best_channel = input('input best channel:')
    # refresh Config.csv
    config['erp_band_low'] = erp_band_low
    config['erp_band_high'] = erp_band_high
    config['t_head'] = t_head
    config['t_tail'] = t_tail
    config['best_channel'] = best_channel
    write_config(config, mode='w')
    # extract features
    features = feature_extractor(data_for_training[:, best_channel], samplerate, erp_band=np.array([erp_band_low, erp_band_high]))
    # load sti_order file
    sti_order_path = ''
    sti_order = np.load(sti_order_path)['sti_order']
    # get target
    sti_string = ['A', 'H', 'O', 'V', '2', '9']
    target = get_target(sti_order=sti_order, sti_string=sti_string, n_rep_exp=n_rep, n_rep_train=n_rep_train)
    # train and save SVM model
    scores = train_svm(feature=features, target=target, save_model=True)
    print(scores.mean())
