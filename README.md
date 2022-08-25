# py-remeha
scraper to get some metrics from Remeha heatpump portal


# how to use it


Example:
```python

from remeha import Remeha

r = Remeha(username=username, password=password, ssl_verify=False);
r.login()
data = r.get_data(mac_address=mac_address)

```

This should get you all available data of the past 24 hours.

# storage
the script `doit.py` contains an example of how to store the data in a postgres db.


# what does it mean?
```
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

```

# monitoring codes:
```
1    Stand-by
2    Passief tapwater
4    Tapwaterbedrijf voordraaitijd
8    Passief CV
16   Centraal verwarmingsbedrijf voordraaitijd
32   Passief koelbedrijf actief
128  Regenereren
256  Noodbedrijf tapwaterbedrijf actief
1028 Tapwaterbedrijf actief (compressor draait)
1040 Centraal verwarmingsactief (compressor draait)
2048 Elektrisch element actief
3088 Centraal verwarmingsactief (compressor + elektrisch element aan)

```

