from remeha import Remeha
import json
import datetime
from time import sleep
import configparser, psycopg2, psycopg2.extras as extras
import os
from datetime import date

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/config.ini')

database = config['database']
username = database['username']
password = database['password']
hostname = database['hostname']
dbname = database['database']

dsn = f"dbname='{dbname}' user='{username}' host='{hostname}' password='{password}'"

try:
    conn = psycopg2.connect(dsn, cursor_factory=extras.DictCursor)
except Exception as e:
    print(f'db is b0rken {e}')
    exit(1)
cur = conn.cursor()



dates = []
date_to = datetime.datetime.now()
# change the range to fetch date for more days (use with care)
for i in range(0, 1):
    dates.append(date_to - datetime.timedelta(days=i))

r = Remeha(config['remeha']['username'], config['remeha']['password'], ssl_verify=False);
r.login()

date_to_str = os.environ.get('DATE_TO', None)
if date_to_str:
    date_to = datetime.datetime.strptime(f'{date_to_str}T23:59:59', '%Y-%m-%dT%H:%M:%S')
    print(date_to)
else:
    date_to = None



"""
Fields
{
    'time': '\ufeffTIME', 
    'tvi': 'Tvi, sensor bron WP/verdamper IN [°C*10]', 
    'tvu': 'Tvu, sensor bron WP/verdamper UIT [°C*10]', 
    'tci': 'Tci, sensor CV WP/condensor IN [°C*10]', 
    'tcu': 'Tcu, sensor CV condensor UIT [°C*10]', 
    'tbu': 'Tbu, sensor buitentemperatuur [°C*10]', 
    'ttw': 'Ttw, sensor tapwater [°C*10]', 
    'actuele_regelwaardesetpoint': 'Actuele regelwaarde/setpoint [°C*10]', 
    'monitor_state': 'Monitor State', 
    'error': 'Error', 
    'kwh1': 'kWh1 [PV]', 
    'kwh2': 'kWh2 [woning]', 
    'kwhwp_actieve_koeling': 'kWhWP Actieve koeling [kWh]', 
    'lockout_error': 'Lockout error', 
    'tau': 'Tau, sensor CV WP UIT [°C*10]', 
    'tbi': 'Tbi, sensor binnentemperatuur [°C*10]', 
    'tzc': 'Tzc, sensor zonnecollector [°C*10]', 
    'verbruik_cv_compressor': 'Verbruik CV compressor [kWh]', 
    'verbruik_cv_cpr_en_ee': 'Verbruik CV CPR en EE [kWh]', 
    'verbruik_noodbedrijf_cv': 'Verbruik Noodbedrijf CV [kWh]', 
    'verbruik_noodbedrijf_tapwater': 'Verbruik Noodbedrijf tapwater', 
    'verbruik_passief_koelen': 'Verbruik Passief koelen [kWh]', 
    'verbruik_regeneratie': 'Verbruik Regeneratie [kWh]', 
    'verbruik_standby': 'Verbruik Stand-by [kWh]', 
    'ver:/bruik_tapwater_compressor': 
    'Verbruik Tapwater compressor [kWh]', 
    'verbruik_tapwater_cpree': 'Verbruik tapwater CPR+EE'
}

"""
count = 0
for date_to in dates:
    data, fields = r.get_data(mac_address=config['remeha']['mac_address'], date_to=date_to)
    db_fields = [k for k in fields.keys()]
    db_fields[0] = 'sample'


    ## prepare query
    cols = ','.join(db_fields)
    placeholders = ','.join(['%s' for m in db_fields])
    query = f'INSERT INTO remeha ({cols}) VALUES ({placeholders}) ON CONFLICT (sample) DO NOTHING'
    for row in data:
        values = []
        for key, value in row.items():
            if key == 'time':
                values.append(row[key])
            else:
                if len(row[key]) > 0:
                    values.append(int(row[key].split(',')[0]))
                else:
                    values.append(None)

        cur.execute(query, values)
        count += 1
    print(f'Inserted {len(data)} rows for {date_to.strftime("%Y-%m-%d")}')
    sleep(1)
conn.commit()

print(f'inserted {count}')
