""" DataReader code lives here. All DataReader classes should extend DataReader 
    and implement the following methods:
    - help()
    - get_data()
"""
from datetime import datetime
import requests


class DataReader(object):
    """ Class-level constants that can be defined in code until we get around 
    to putting them into a database table """
    TARGET_URL = None
    DATA_TYPE = None
    RETURN_FORMAT = None  # This is a help-feature for help() method

    def __init__(self):
        pass

    def help(self):
        return self.RETURN_FORMAT


class USGSDataReader(DataReader):

    TARGET_URL = "http://waterservices.usgs.gov/nwis/iv/?format={}&sites={}&parameterCd={}"
    DATA_TYPE = "json"
    USGS_CODE_FLOW = '00060'
    USGS_CODE_LEVEL = '00065'

    def __init__(self):
        super(USGSDataReader, self).__init__()
        pass


    def get_data(self, uri):
        """ Hit USGS API and retrieve JSON object. Return GaugeData JSON object. 
        :param uri: USGS id of the gauge being queried
        :returns: <GaugeData>: updated values in the form of a JSON object
        """
        usgs_code = '0' * (8 - len(str(uri))) + str(uri)
        params = self.USGS_CODE_LEVEL + ',' + self.USGS_CODE_FLOW
        usgs_url = self.TARGET_URL.format(self.DATA_TYPE, usgs_code, params)
        result = requests.get(usgs_url).json()
        data = result["value"]["timeSeries"]
        output = { x["variable"]["variableCode"][0]["value"]: x["values"][0]["value"][0] for x in data }
        flow, level = None, None
        if "00060" in output.keys():
            flow = output["00060"]["value"]
        if "00065" in output.keys():
            level = output["00065"]["value"]
        package = {"gauge_id": uri,
                   "timestamp": datetime.strptime(
                       output["00065"]["dateTime"][:18],
                       "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                   "level": level,
                   "flow_cfs": flow}
        return package


class WundergroundReader(DataReader):

    TARGET_URL = "http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json"

    def __init__(self):
        super(WundergroundReader, self).__init__()
        pass

    def get_data(self, uri):
        """ Hit Wunderground API and retrieve JSON object. Return GaugeData object. 
        :param uri : this is the gauge being queried
        :returns: <GaugeData>: updated values in the form of a GaugeData object
        """
