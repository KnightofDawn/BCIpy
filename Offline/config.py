import csv


def load_config(config_path):
    # if csv has name conflict, program would choose the last input for the conflict parameter
    config = {}
    with open(config_path) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            config[row[0]] = config[row[1]]
    return config


def write_config(config_path, config, mode='w'):
    # mode = 'a' append; 'w' overwrite old config
    with open(config_path, mode) as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for key, item in enumerate(config):
            spamwriter.writerow([key, item])
