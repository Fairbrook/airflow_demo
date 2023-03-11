import logging
from typing import Dict
from airflow.decorators import dag, task
import requests
import pendulum
from bs4 import BeautifulSoup
import pdfkit


@dag(schedule=None, catchup=False, dag_id='siiau_schedule_to_pdf', start_date=pendulum.datetime(2023, 3, 10, tz='UTC'))
def myDAG(code: str, password: str):
    @task()
    def signIn(code: str, password: str):
        res = requests.post('http://siiauescolar.siiau.udg.mx/wus/gupprincipal.valida_inicio',
                            data={'p_codigo_c': code, 'p_clave_c': password})
        print(res.status_code)
        if res.status_code == 404:
            raise Exception("Unauthorized")
        if res.status_code != 200:
            raise Exception("Error at login")
        return res.headers['set-cookie']

    @task()
    def fetch_schedule(recived_cookies: str):
        print(recived_cookies)
        cookies = [cookie.replace(';path=/', '').split('=')
                   for cookie in recived_cookies.split(',')]
        print(cookies)
        pidmp = ''
        for item in cookies:
            if 'SIIAUUDG' in item[0]:
                pidmp = item[1]
        print('pidmp', pidmp)
        cookies_dict = dict()
        for cookie in cookies:
            cookies_dict[cookie[0]] = cookie[1]
        print('cookies dict', cookies)
        res = requests.get(
            f'http://siiauescolar.siiau.udg.mx/wal/sgpregi.horario?pidmp={pidmp}&majrp=INCO', cookies=cookies_dict)
        return res.text

    @task()
    def clean_table(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all('table')[1].prettify()

    @task()
    def table_to_pdf(table):
        pdfkit.from_string(table, 'out.pdf')
    cookies = signIn(code, password)
    print(cookies)
    html = fetch_schedule(cookies)
    table_html = clean_table(html)
    table_to_pdf(table_html)


dag = myDAG('219294382', '040499cran')
