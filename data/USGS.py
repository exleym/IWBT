# XML Parser Test Script
# Python Code to Parse USGS XML
# This is a simple example script to fetch and parse XML objects
# Will add database connectivity, logging, timing, and support for large batches later

import urllib2
import xml.etree.ElementTree as ET
import datetime
import pandas as pd

class DataReader(object):

    def __init__(self, rivers, gauge_params=['00060'], ns=None):
        self.rivers = rivers
        self.ns = ns
        self.gauges = dict()
        self.params = ''
        for p in gauge_params:
            self.params = self.params + p + ','
        self.params = self.params[:-1]
        self.current_xml = None
        if self.ns is None:
            self._set_default_ns()

    def get_flow(self, gauge=None):
        self._get_flow_xml()
        self._parse_flow_xml()
        if gauge is None:
            return self.gauges
        else:
            return self.gauges[gauge]

    def _get_flow_xml(self):
        usgs_url = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,2.0&sites="
        for r in self.rivers.keys():
            usgs_url += self.rivers[r] + ','
        usgs_url = usgs_url[:-1] + "&parameterCd=" + self.params
        url_file = urllib2.urlopen(usgs_url)
        xml_data = url_file.read()
        url_file.close()
        self.current_xml = xml_data

    def _parse_flow_xml(self):
        root = ET.fromstring(self.current_xml)
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
            flow['time'] = pd.to_datetime(flow['time'])
            flow['time'].tz_localize('UTC').tz_convert('US/Pacific')
            self.gauges[gauge] = flow

    def _set_default_ns(self):
        self.ns = {'gml': 'http://www.opengis.net/gml/3.2',
                   'wml': 'http://www.opengis.net/waterml/2.0',
                   'om': 'http://www.opengis.net/om/2.0'}


river_dict = {'chattooga_bridge': '02177000', 'chattooga_burrells': '02176930', 'gallatin': '06043500'}
dr = DataReader(rivers=river_dict)
print dr.get_flow(river_dict['chattooga_bridge'])


"""
print gauges
ch1 = gauges['02176930']['time']
ch2 = gauges['02177000']['time']
ga1 = gauges['06043500']['time']

print pd.to_datetime(ch1)
print pd.to_datetime(ch2)
print pd.to_datetime(ga1)
"""