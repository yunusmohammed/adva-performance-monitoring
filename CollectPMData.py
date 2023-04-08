"""
CollectPMData.py - monitor ADVA optical power, BER and
                      SNR levels and send a status email
"""

from datetime import datetime
import requests
import json
import urllib3
from models.PMData import PMData
from models.InstantaneousPMData import InstantaneousPMData
from models.FifteenMinuteBinnedPMData import FifteenMinuteBinnedPMData
from models.FifteenMinuteBinnedProperty import FifteenMinuteBinnedProperty
from pathlib import Path

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


def obj_dict(obj):
    return obj.__dict__


def get_pmdata(host, port_id, port_speed) -> PMData:
    och_syntax = {"100": "ot100/otu4",
                  "150": "ol150/otlc1p5a", "200": "ot200/otuc2pa"}
    # Make a REST connection to the chassis
    rest_uri = 'https://{}/auth'.format(host)
    headers = {'Accept': 'application/json;ext=nn',
               'Content-Type': 'application/json;ext=nn',
               'AOS-API-Version': '1.0'}

    # First, authenticate and obtain the token
    payload = {'in': {'un': 'poller', 'pswd': 'LAbp3rFmOn$'}}
    req = requests.post(rest_uri, headers=headers, json=payload,
                        params={'actn': 'lgin'}, verify=False)
    # TODO: add error handling
    if 'X-Auth-Token' in req.headers:
        headers['X-Auth-Token'] = req.headers['X-Auth-Token']
    else:
        raise Exception(
            'Did not receive X-Auth-Token, {} response status{}'.format(host, req.status_code))

    # GET the optical level for the port
    [shelf, slot, port_name] = port_id.split('/')
    port = port_name[1:]
    port_uri = 'https://{}/mit/me/1/eqh/shelf,{}/eqh/slot,{}/eq/card/ptp/nw,{}/opt/pm/crnt'.format(
        host, shelf, slot, port)
    req = requests.get(port_uri, headers=headers, verify=False)
    myresult = json.loads(req.text)
    powerlevel: float = None
    powerlevel_15: FifteenMinuteBinnedProperty = None
    for res in myresult['result']:
        if res['bintv'] == "nint":
            powerlevel = res['pmdata']['opr']
        elif res['bintv'] == "m15":
            powerlevel_15 = FifteenMinuteBinnedProperty(
                res['pmdata']['oprl'], res['pmdata']['oprm'], res['pmdata']['oprh'])

    # GET the BER for the port
    port_uri = 'https://{}/mit/me/1/eqh/shelf,{}/eqh/slot,{}/eq/card/ptp/nw,{}/ctp/{}/pm/crnt'.format(
        host, shelf, slot, port, och_syntax[port_speed])
    req = requests.get(port_uri, headers=headers, verify=False)
    myresult = json.loads(req.text)
    ber: float = None
    ber_15: FifteenMinuteBinnedProperty = None
    for res in myresult['result']:
        if res['bintv'] == "nint":
            ber = res['pmdata']['fecber']
        elif res['bintv'] == "m15" and res["name"] == "FEC":
            ber_15 = FifteenMinuteBinnedProperty(
                None, res['pmdata']['fecberm'], None)

    # GET the SNR, Q-factor, dispersion, offset and DGD for the port
    port_uri = 'https://{}/mit/me/1/eqh/shelf,{}/eqh/slot,{}/eq/card/ptp/nw,{}/ctp/ot{}/och/pm/crnt'.format(
        host, shelf, slot, port, port_speed)
    req = requests.get(port_uri, headers=headers, verify=False)
    myresult = json.loads(req.text)
    snr: float = None
    snr_15: FifteenMinuteBinnedProperty = None
    dgd: float = None
    dgd_15: FifteenMinuteBinnedProperty = None
    qfactor: float = None
    qfactor_15: FifteenMinuteBinnedProperty = None
    chrom_disp: float = None
    chrom_disp_15: FifteenMinuteBinnedProperty = None
    carrier_offset: float = None
    carrier_offset_15: FifteenMinuteBinnedProperty = None
    for res in myresult['result']:
        if res['bintv'] == "nint":
            if res['name'].startswith("ImpQF"):
                snr = res['pmdata']['snr']
                dgd = res['pmdata']['dgd']
            elif res['name'] == "RxQuality":
                qfactor = res['pmdata']['qfact']
            elif res['name'].startswith("RxQF"):
                chrom_disp = res['pmdata']['cdc']
                carrier_offset = res['pmdata']['cfot']
        elif res['bintv'] == "m15":
            if res['name'] == "Impairments":
                snr_15 = FifteenMinuteBinnedProperty(
                    res['pmdata']['snrl'], res['pmdata']['snrm'], res['pmdata']['snrh'])
                dgd_15 = FifteenMinuteBinnedProperty(
                    res['pmdata']['dgdl'], res['pmdata']['dgdm'], res['pmdata']['dgdh'])
            elif res['name'] == "RxQuality":
                qfactor_15 = FifteenMinuteBinnedProperty(
                    res['pmdata']['qfactl'], res['pmdata']['qfactm'], res['pmdata']['qfacth'])
            elif res['name'] == "Receiver":
                chrom_disp_15 = FifteenMinuteBinnedProperty(
                    res['pmdata']['cdcl'], res['pmdata']['cdcm'], res['pmdata']['cdch'])
                carrier_offset_15 = FifteenMinuteBinnedProperty(
                    res['pmdata']['cfotl'], res['pmdata']['cfotm'], res['pmdata']['cfoth'])

    # Last, log out of the session
    # TODO: make all the GET calls for ports in a shelf in one session rather than logging out and back in
    requests.post(rest_uri, headers=headers, params={
                  'actn': 'lgout'}, verify=False)

    instantaneous_data = InstantaneousPMData(
        powerlevel, ber, snr, dgd, qfactor, chrom_disp, carrier_offset)
    binned_data = FifteenMinuteBinnedPMData(
        powerlevel_15, ber_15, snr_15, dgd_15, qfactor_15, chrom_disp_15, carrier_offset_15)
    return PMData(instantaneous_data, binned_data)


# Entry point
current_utc_time = datetime.utcnow()
script_dir = Path(__file__).resolve().parent

output_file: Path = script_dir / \
    Path('output/' + str(current_utc_time.date()) + '.json')
config_file: Path = script_dir / Path('config/ADVA_powerlevels.json')
time_stamp: str = str(current_utc_time.timestamp())

# Turn off warnings for unvalidated HTTPS connections
urllib3.disable_warnings()

# TODO: make this an argument rather than hardcoded
with open(config_file, 'r') as configfile:
    config = json.load(configfile)
    configfile.close()

devices = []
for device in config:
    chassis_hostname = config[device]['hostname']
    portlist = config[device]['ports']
    portsPMData = []
    for port in portlist:
        # print(device, port)
        description = port['description']
        port_id: str = port['portID']
        port_speed = port['speed']
        connection_index = port['index']
        pmdata: PMData = get_pmdata(chassis_hostname, port_id, port_speed)
        portsPMData.append({port_id: pmdata})
    devices.append({device: portsPMData})

new_entry = {time_stamp: devices}
jsonEntry = json.loads(json.dumps(new_entry, default=obj_dict))

file_data = {}
if output_file.is_file():
    with open(output_file.absolute(), 'r+') as file:
        file_data = json.load(file)

file_data.update(jsonEntry)

with open(output_file, 'w+') as file:
    file.seek(0)
    json.dump(file_data, file)
