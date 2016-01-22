
import ConfigParser

class MyIni:
    def __init__(self, conf_path='my_ini.conf'):
        self.conf_path = conf_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(conf_path)

    def get_hbc(self):
        conf = {}
        section = 'HBC'
        conf['hbc_img_path'] = self.cf.get(section, 'hbc_img_path').decode('gbk')
        conf['wz_img_path'] = self.cf.get(section, 'wz_img_path').decode('gbk')
        return conf

if __name__ == '__main__':
    ini = MyIni()
    hbc = ini.get_hbc()
    print hbc
