import requests
import csv
import re
from io import StringIO
import datetime
from typing import List, Dict

class Remeha:
    _urls = {
        'login_form': 'https://monitoring.remeha.nl/status/accounts/login/?next=/status/dashboard/',
        'login': 'https://monitoring.remeha.nl/status/accounts/login/?next=/status/dashboard/',
        'getdata': 'https://monitoring.remeha.nl/status/srv/handlers/modpython.py'
            }

    _headers = {
            'authority': 'monitoring.remeha.nl',
            'origin': 'https://monitoring.remeha.nl',
            'Content-type': 'application/x-www-form-urlencoded',
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
                }



    def __init__(self, username: str, password: str, ssl_verify: bool = True):
        self._username = username
        self._password = password
        self._ssl_verify = ssl_verify

        self._session = requests.Session()


    def login(self):
        self._get_csrftoken()
        self._do_login()


    def _get_csrftoken(self):
        print(requests.certs.where())
        response = self._session.get(self._urls['login_form'], verify=self._ssl_verify)
        if not response:
            raise(f'failure! {response}')


        if 'csrftoken' in response.cookies:
            self._csrftoken = response.cookies['csrftoken']    

            print(f'csrftoken: {self._csrftoken}')
        self._cookies = response.cookies


    def _do_login(self):


        data = {
                'csrfmiddlewaretoken': self._csrftoken,
                'username': self._username,
                'password': self._password,
                'next': '/status/dashboard/'}

        headers = self._headers
        headers['referer'] = 'https://monitoring.remeha.nl/status/accounts/login/?next=/status/dashboard/'
        response = self._session.post(url=self._urls['login'], 
                data=data,
                headers=headers,
                cookies=self._cookies,
                verify=self._ssl_verify)
        print('logging in')
        if response.status_code != 200:
            print(response)
            print(response.text)
            exit(1)


    def get_data(self, mac_address: str, date_from: datetime = None, date_to: datetime = None) -> List[Dict[str,str]]:

        if not date_to:
            date_to = datetime.datetime.now()
        if not date_from:
            date_from = date_to - datetime.timedelta(days=1)


        db = f'KIT-{mac_address}'
        label = 'data'

        headers = self._headers
        headers['referer'] = 'https://monitoring.remeha.nl/html/graph.html?plot=points'
        headers['x-requested-with'] = 'XMLHttpRequest'
        headers['accept'] = '*/*'

        data = {
                'command': f'<cmd><name>download_points</name><params><table>v2</table><table>v3</table><table>v4</table><table>v5</table><table>v18</table><table>v188</table><table>v192</table><table>v235</table><table>v1</table><table>v252</table><table>v250</table><table>v14</table><table>v32</table><table>v6</table><table>v187</table><table>v241</table><table>v11</table><table>v12</table><table>v186</table><table>v185</table><table>v13</table><table>v184</table><table>v8</table><table>v9</table><table>v10</table><db>{db}</db><label>{label}</label><from>{str(int(date_from.timestamp()))}</from><to>{str(int(date_to.timestamp()))}</to></params></cmd>'}

        response = self._session.post(url=self._urls['getdata'],
                headers=headers,
                data=data,
                verify=self._ssl_verify)

        if response.status_code == 200:
            fields = None
            original_fields = {}
            s = StringIO(response.text)
            reader = csv.reader(s, delimiter='\t')
            if not reader:
                print('Failed reading input')
            result: List[Dict[str, any]] = []
            for row in reader:
                if not fields:
                    fields = []
                    regex = re.compile('[^a-zA-Z_0-9]')

                    for original_field in row:
                        field = original_field.split(',')[0]
                        field = re.sub('\[.*?\]', '', field)
                        field = field.lower().rstrip().replace(' ', '_')
                        field = regex.sub('', field)
                        fields.append(field)
                        original_fields[field] = original_field
                else:
                    result.append({fields[index]: v for index, v in enumerate(row)})
            return result, original_fields

