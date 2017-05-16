import requests
import json
from config import Config


state = 'SC'
town = 'CLEMSON'

class Wunderground(object):
    def __init__(self):
        self.key = Config.WUNDERGROUND_API_KEY

    def get_url(self, state, town):
        return 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(self.key, state, town)

    def get_json(self, state, town):
        return requests.get(self.get_url(state, town)).json()

# f = urllib2.urlopen()
# json_string = f.read()
# parsed_json = json.loads(json_string)
# location = parsed_json['location']['city']
# temp_f = parsed_json['current_observation']['temp_f']
# print(parsed_json)
# #print "Current temperature in %s is: %s" % (location, temp_f)
# f.close()

if __name__ == '__main__':
    w = Wunderground()
    print(w.get_url('SC', 'CLEMSON'))
    print(w.get_json('SC', 'CLEMSON'))