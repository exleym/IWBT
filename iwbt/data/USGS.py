# XML Parser Test Script
# Python Code to Parse USGS XML
# This is a simple example script to fetch and parse XML objects
# Will add database connectivity, logging, timing, and support for large batches later
import datetime
import urllib2
import xml.etree.ElementTree as ET
import json


class DataReader(object):

    def __init__(self, rivers, gauge_params=None, ns=None, data_format='json'):
        if gauge_params is None:
            gauge_params = ['00060', '00065']
        self.rivers = rivers
        self.ns = ns
        self.gauges = dict()
        self.params = ''
        self.data_format = data_format
        for p in gauge_params:
            self.params = self.params + p + ','
        self.params = self.params[:-1]
        self.raw_data = None
        if self.ns is None:
            self._set_default_ns()

    def get_flow(self, gauge=None):
        self._get_flow_data()
        self._parse_raw_data()
        if gauge is None:
            return self.gauges
        else:
            return self.gauges[gauge]

    def _parse_raw_data(self):
        if self.data_format == 'json':
            self._parse_json()
        elif self.data_format == 'waterml,2.0':
            self._parse_xml()
        else:
            print "Use an approved data format (json or waterml,2.0)"

    def _get_flow_data(self):
        usgs_url = "http://waterservices.usgs.gov/nwis/iv/?format=" + self.data_format + "&sites="
        for r in self.rivers.keys():
            usgs_url += self.rivers[r] + ','
        usgs_url = usgs_url[:-1] + "&parameterCd=" + self.params
        print usgs_url
        url_file = urllib2.urlopen(usgs_url)
        ret_data = url_file.read()
        url_file.close()
        self.raw_data = ret_data

    def _parse_xml(self):
        root = ET.fromstring(self.raw_data)
        for river in root.findall('gml:featureMember', self.ns):
            x = river[0].find('wml:observationMember', self.ns)
            rid = river[0].find('gml:name', self.ns).text
            c = river[0].attrib
            gauge = [c[v] for v in c.keys()][0].split('.')[2]
            y = x.find('om:OM_Observation', self.ns)
            z = y.find('om:result', self.ns)
            flow = dict()
            for i in z[0][2][0]:
                flow[i.tag.split("}")[1]] = i.text
            self.gauges[gauge] = flow

    def _parse_json(self):
        j = json.loads(self.raw_data)
        print j
        params = j['value']['queryInfo']['criteria']['variableParam'].replace('[','').replace(']','').split(',')
        param_ix = {x.strip(): params.index(x) for x in params}
        for x in j['value']['timeSeries']:
            location = x['sourceInfo']['siteName']
            gauge_id = x['sourceInfo']['siteCode'][0]['value']
            variable_name = x['variable']['variableName']
            variable_id = x['variable']['variableCode'][0]['value']
            value = x['values'][0]['value'][0]['value']
            self.gauges[gauge_id] = {'location': location, 'gauge_id': gauge_id, 'variable_name': variable_name, 'variable_id': variable_id,
                   'value': value, 'timestamp': x['values'][0]['value'][0]['dateTime']}

        #print j['value']['timeSeries'][3]['sourceInfo']['siteName']
        #print j['value']['timeSeries'][3]['values'][0]['value'][0]['value']

    def _set_default_ns(self):
        self.ns = {'gml': 'http://www.opengis.net/gml/3.2',
                   'wml': 'http://www.opengis.net/waterml/2.0',
                   'om': 'http://www.opengis.net/om/2.0'}


if __name__ == '__main__':
    river_dict = {'chattooga_bridge': '02177000', 'chattooga_burrells': '02176930', 'gallatin': '06043500'}
    dr = DataReader(rivers=river_dict) #, data_format='waterml,2.0')
    print dr.get_flow(river_dict['chattooga_bridge'])
    print dr.get_flow(river_dict['chattooga_burrells'])
    print dr.get_flow(river_dict['gallatin'])



