from datetime import datetime
from iwbt.models.rivers import Gauge, GaugeData
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+pymysql://iwbt_admin:wetoodeep42@localhost:3306/iwbt'
API_BASE = 'http://localhost:5000/api/v1.0'
USGS_CODE_FLOW = '00060'
USGS_CODE_LEVEL = '00065'
DATA_FORMAT = 'json'
USGS_URL_BASE = "http://waterservices.usgs.gov/nwis/iv/?format={}&sites={}&parameterCd={}"

CHATTOOGA_BRIDGE_CODE = '02177000'


def main():
    con = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=con)

    session = Session()
    gauges = session.query(Gauge).all()

    for g in gauges:
        usgs_code = '0' * (8 - len(str(g.usgs_id))) + str(g.usgs_id)
        params = USGS_CODE_LEVEL + ',' + USGS_CODE_FLOW
        usgs_url = USGS_URL_BASE.format(DATA_FORMAT, usgs_code, params)
        result = requests.get(usgs_url).json()
        data = result["value"]["timeSeries"]
        output = {x["variable"]["variableCode"][0]["value"] :x["values"][0]["value"][0] for x in data}
        flow, level = None, None
        if "00060" in output.keys():
            flow = output["00060"]["value"]
        if "00065" in output.keys():
            level = output["00065"]["value"]
        package = {"gauge_id": g.id,
                   "timestamp": datetime.strptime(output["00065"]["dateTime"][:18], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                   "level": level,
                   "flow_cfs": flow}
        #print(package)
        requests.post(API_BASE + '/gauge_data/', json=package)

if __name__ == '__main__':
    main()

