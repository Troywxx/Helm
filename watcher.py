#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import json
import logging.config
import datetime

import click
import requests

from requests.exceptions import ConnectionError
              
from ftplib import FTP
from Timer import Timer
from config import config

__version__ = 'v0.3.0'

path = 'log_dict_config.json'
log_config = json.load(open(path, 'rt'))
logging.config.dictConfig(log_config)

logger_common = logging.getLogger("BasicLog") 
logger_alarm = logging.getLogger("AlarmLog")
logger_text = logging.getLogger("TextLog")
logger_error = logging.getLogger("ErrorLog")

def postdata(url, data):
    try:
        response = requests.post(url, data)
    except ConnectionError:
        logger_error.warn('GET {} 408 Request Timeout'.format(url))

    except Exception as e:
        logger_error.error(e, exc_info=True)

class Product(object):
    """docstring for Product"""
    def __init__(self, product):
        self.prd_type = product['prd_type']
        self.ftp_auth = product['login']
        self.platform = product['platform']
        self.time_offset = product['time_offset']
        self.warn_time = product['warn_time']
        self.now = datetime.datetime.now()
        self.message = product['default_warn_messages']
        self.api = product['write_list_api']

        self.process()

    def process(self):
        try:
            self.login()
            self.listen()
        except Exception as e:
            logger_error.error(e, exc_info=True)


    def login(self, port=21, timeout=30):
        host, user, passwd, path = self.ftp_auth
        files = []
        
        ftp = FTP()
        ftp.connect(host, port, timeout)
        ftp.login(user, passwd)
        ftp.cwd(path)
        ftp.retrlines('LIST', lambda x: files.append(filter(None, x.split(' '))))

        if self.platform == 'win':
            # files_lst = files[0]

            # for file in files:
            #     if files_lst[0] in file and files_lst[1] in file:
            #         latest_file = file 
                    #['05-14-17', '08:54PM', '121286', 'TRBC2054.IPZ']

            self.latest_filename = files[-1][-1]
            # print(self.latest_filename)

            time_radar_struct = Timer(self.prd_type, self.warn_time, self.latest_filename)
            self.latest_file_date = time_radar_struct.get_radar_filetime()
            self.is_warned = time_radar_struct.is_warned()
            # print(self.is_warned)
            logger_common.debug('Radar latest filename %s, created date UTC+8 %s' % (self.latest_filename, self.latest_file_date))

        else:
            self.latest_filename = files[-1][-1] 
            #['-rw-rw-r--', '1', '702', '702', '6879', 'May', '14', '23:09', 'AWOS201705142309.JHK']
            #['-r--r--r--', '1', 'ftp', 'ftp', '814473', 'May', '15', '07:23', 'ISN201705150700.JPG']
            if self.prd_type == "awos":
                time_awos_struct = Timer(self.prd_type, self.warn_time, self.latest_filename)
                self.latest_file_date = time_awos_struct.get_awos_filetime()
                self.is_warned = time_awos_struct.is_warned()
                logger_common.debug('Awos latest filename %s' % (self.latest_file_date))
            elif self.prd_type == "satellite":
                time_sat_struct = Timer(self.prd_type, self.warn_time, self.latest_filename)
                self.latest_file_date = time_sat_struct.get_sat_filetime()
                self.is_warned = time_sat_struct.is_warned()
                logger_common.debug('Satellite latest filename %s' % (self.latest_file_date))
            else:
                time_sat_struct = Timer(self.prd_type, self.warn_time, self.latest_filename)
                self.latest_file_date = time_sat_struct.get_sat_filetime()
                self.is_warned = time_sat_struct.is_warned()
                logger_common.debug('Test latest filename %s' % (self.latest_file_date))

        watchlist = {
            'prd_type' : self.prd_type, 
            'alert' : self.is_warned, 
            'filename' : self.latest_filename, 
            'filetime' : time.mktime(self.latest_file_date.timetuple())
            }


        postdata(self.api, json.dumps(watchlist))
        ftp.quit()

    def is_warned(self):
        return self.is_warned

    def filetime(self):
        return self.latest_file_date

    def get_latest_filename(self):
        return self.latest_filename

    def listen(self):
        if self.is_warned:
            message = self.message
            message = ' '.join([message, 'lost since', self.latest_filename])
            logger_text.info(message)
            logger_alarm.info(message)

            enbale_phone_message = config['enbale_phone_message']
            api = config['api']
            if enbale_phone_message:
                for phone_number in config['contacts']:
                    response = requests.post(api['message_url'], auth=('api', api['token']),data={'mobile': phone_number, 'text': message })
                    response.json()
                    logger_text.info(response.text)
                    logger_text.info(config['contacts'])
                    
                    # time.sleep(30)

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--version', '-v', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def main():
    """ 
    service name: radar awos satellite \n
    run -s [name]                  Start single service \n
    run -s [name] -s [name]        Start multiple services \n
    run -s all                     Start all services \n
    """
    logger_common.debug('Start in DEBUG mode')

@click.command()
@click.option('--service', '-s', type=click.Choice(['radar', 'awos', 'satellite', 'all', 'test']), multiple=True)
def run(service):
    """-s, --service [name] Run watch service."""
    global config

    if 'all' in service:
        service = ('radar', 'awos', 'satellite')
    
    message = None

    while service:
        products = config['products']

        if 'radar' in service:
            prd = Product(products['radar'])
        if 'awos' in service:
            prd = Product(products['awos'])
        if 'satellite' in service:
            prd = Product(products['satellite'])
        if 'test' in service:
            prd = Product(products['test'])

        time.sleep(60)
    else:
        click.echo("Error: please use 'run -s [name]' to start a service")


main.add_command(run)

if __name__ == '__main__':
    main()