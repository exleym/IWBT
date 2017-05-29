from iwbt.data.readers import USGSDataReader
import requests

API_BASE = 'http://localhost:5000/api/v1.0'


def main():
    gauges_url = API_BASE + '/gauges/'
    gauges = requests.get(gauges_url)

    reader = USGSDataReader()

    for g in gauges.json():
        gdata = reader.get_data(g['usgs_id'])
        package = {"gauge_id": g['id'],
                   "timestamp": gdata['timestamp'],
                   "level": gdata['level'],
                   "flow_cfs": gdata['flow_cfs']}
        requests.post(API_BASE + '/gauge_data/', json=package)

if __name__ == '__main__':
    main()

