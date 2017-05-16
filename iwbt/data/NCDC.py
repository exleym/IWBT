from config import Config

class NCDCWeatherReader(object):
    def __init__(self):
        self.key = Config.NCDC_TOKEN
        self.header = {'header': self.key}