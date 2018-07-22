#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import json
import logging.config
import time
import datetime
import re

import click
import requests

from requests.exceptions import ConnectionError
              
from ftplib import FTP
from config import config
from bs4 import BeautifulSoup

__version__ = 'v0.4.0'

path = 'log_dict_config.json'
log_config = json.load(open(path, 'rt'))
logging.config.dictConfig(log_config)

logger_common = logging.getLogger("BasicLog") 
logger_alarm = logging.getLogger("AlarmLog")
logger_text = logging.getLogger("TextLog")
logger_error = logging.getLogger("ErrorLog")

standard = config["radar_check"]["standard"]
shift = config["radar_check"]["shift"]

pattern = re.compile(r'\d', re.S)

class Timestruct(object):
    #Get standard UTC time and compare it with checktime to tell if it should be warned

    def __init__(self, prd_type, warn_time, files):
        self.prd_type= prd_type
        self.warn_time = warn_time
        self.files = "".join(re.findall(pattern, files))
        self.now = datetime.datetime.now()
        self.utcnow = datetime.datetime.utcnow()

    def get_time_struct(self):
        year = self.files[0:4]
        month = self.files[4:6]
        day = self.files[6:8]
        hour = self.files[8:10]
        minute = self.files[10:12]
        time_string = year + ' ' + month + ' ' + day + ' ' + hour + ' ' + minute
        time_struct = datetime.datetime.strptime(time_string, "%Y %m %d %H %M")
        
        if self.prd_type == 'radar':
            time_struct = datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.timetuple(time_struct)))

        return time_struct

    def is_warned(self):
        if 'radar' in self.prd_type:
            warning = False
            for i in standard:
                time_hour = datetime.datetime.strptime(i, "%H%M")
                time_standard = datetime.datetime.combine(datetime.datetime.utcnow(), time_hour.time())
                start_time = time_standard - datetime.timedelta(minutes=shift)
                if start_time < self.utcnow < time_standard:
                    diff_time = time_standard - self.get_time_struct()
                    check_time = datetime.timedelta(minutes=int(self.warn_time))
                    if diff_time < check_time:
                        warning = False
                    else:
                        warning = True
            return warning
        elif self.prd_type == 'satellite':
            return self.now - self.get_time_struct() > datetime.timedelta(minutes=self.warn_time)
        else:
            return self.utcnow - self.get_time_struct() > datetime.timedelta(minutes=self.warn_time)

def postdata(url, data):
    #post json data to Flask-api
    try:
        response = requests.post(url, data)
    except ConnectionError:
        logger_error.warn('GET {} 408 Request Timeout'.format(url))

    except Exception as e:
        logger_error.error(e, exc_info=True)

def listen(is_warned, message, filetime):
    if is_warned:
        message = ' '.join([message, 'lost since', filetime])
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

def product166(product166):
    #Get filetime from 166

    url = product166['url_166']
    prd_type = product166['prd_type']
    api = product166['write_list_api']
    warn_time = product166['warn_time']
    message = product166['default_warn_messages']

    cookies = config['cookie166']
    
    pattern = re.compile(r'[[](.*?)[]]', re.S)  #最小匹配

    response = requests.get(url, cookies=cookies, timeout=30)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    if prd_type == 'radar_166':
        result = soup.find(id="ListBox_Time").option.string #2018-07-18 08:17(UTC)
    elif prd_type == 'awos_166':
        result = re.findall(pattern, soup.find(id="Repeater_RWYNO_ctl00_Label_RWYName").string)[0] #2018-07-18 08:36(UTC)

    timestruct = Timestruct(prd_type, warn_time, result)
    is_warned = timestruct.is_warned()
    filetime = time.mktime(datetime.datetime.timetuple(timestruct.get_time_struct()))
    logger_common.debug('%s latest filetime %s' % (prd_type, timestruct.get_time_struct())) 

    watchlist = {
            'prd_type' : prd_type, 
            'alert' : is_warned, 
            'filename' : None, 
            'filetime' : filetime
            }
    postdata(api, json.dumps(watchlist))
    listen(is_warned, message, timestruct)

class Productlocal(object):
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
            #['05-14-17', '08:54PM', '121286', 'TRBC2054.IPZ']

            self.latest_filename = files[-1][-1]

            time_radar_struct = Timestruct(self.prd_type, self.warn_time, self.latest_filename)
            self.latest_file_date = time_radar_struct.get_time_struct()
            self.is_warned = time_radar_struct.is_warned()
            logger_common.debug('%s latest filename %s, created date UTC+8 %s' % (self.prd_type, self.latest_filename, self.latest_file_date))

        else:
            self.latest_filename = files[-1][-1] 
            #['-rw-rw-r--', '1', '702', '702', '6879', 'May', '14', '23:09', 'AWOS201705142309.JHK']
            #['-r--r--r--', '1', 'ftp', 'ftp', '814473', 'May', '15', '07:23', 'ISN201705150700.JPG']
            time_awos_struct = Timestruct(self.prd_type, self.warn_time, self.latest_filename)
            self.latest_file_date = time_awos_struct.get_time_struct()
            self.is_warned = time_awos_struct.is_warned()
            logger_common.debug(self.prd_type + ' latest filename %s' % (self.latest_file_date))

        watchlist = {
            'prd_type' : self.prd_type, 
            'alert' : self.is_warned, 
            'filename' : self.latest_filename, 
            'filetime' : time.mktime(datetime.datetime.timetuple(self.latest_file_date))
            }
        postdata(self.api, json.dumps(watchlist))
        listen(self.is_warned, self.message, self.latest_file_date)
        ftp.quit()

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
@click.option('--service', '-s', type=click.Choice(['radar', 'awos', 'satellite', 'radar_166', 'awos_166', 'all']), multiple=True)
def run(service):
    """-s, --service [name] Run watch service."""
    global config

    if 'all' in service:
        service = ('radar', 'awos', 'satellite', 'radar_166', 'awos_166')
    
    message = None

    while service:
        products = config['products']

        if 'radar' in service:
            prd = Productlocal(products['radar'])
        if 'awos' in service:
            prd = Productlocal(products['awos'])
        if 'satellite' in service:
            prd = Productlocal(products['satellite'])
        if 'radar_166' in service:
            prd = product166(products['radar_166'])
        if 'awos_166' in service:
            prd = product166(products['awos_166'])

        time.sleep(60)
    else:
        click.echo("Error: please use 'run -s [name]' to start a service")


main.add_command(run)

if __name__ == '__main__':
    main()