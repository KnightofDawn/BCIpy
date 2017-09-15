import csv

# 路径需要回退一级，因为调用这个函数的function都在下一级菜单中
def load_config():
    # if encounter parameter name conflict, program would choose the last input
    config = {}
    with open('../Config.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            config[row[0]] = row[1]
    return config


def write_config(config, mode='w'):
    # mode = 'a' append; 'w' overwrite old config
    with open('../Config.csv', mode) as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for key, item in enumerate(config):
            spamwriter.writerow([key, item])
