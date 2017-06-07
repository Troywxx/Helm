#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import logging
import datetime
import click
import requests
from ftplib import FTP
from Timer import Timer
from config import config

__version__ = 'v0.3.0'


def setup_log(debug=False):
    log_level = logging.DEBUG if debug else logging.INFO

    _format = '[%(asctime)s] %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(_format)

    # set stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # set log file
    fh = logging.FileHandler('watch.log')
    fh.setLevel(log_level)
    fh.setFormatter(formatter)

    # log
    log = logging.getLogger(__name__)
    log.setLevel(log_level)
    log.addHandler(ch)
    log.addHandler(fh)

    return log

log = setup_log(debug=config['debug'])


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
        
    def login(self, port=21, timeout=30):
        host, user, passwd, path = self.ftp_auth

        ftp = FTP()
        ftp.connect(host, port, timeout)
        ftp.login(user, passwd)
        ftp.cwd(path)
        files = []
        ftp.retrlines('LIST', lambda x: files.append(filter(None, x.split(' '))))

        if self.platform == 'win':
            files_lst = files[0]

            for file in files:
                if files_lst[0] in file and files_lst[1] in file:
                    latest_file = file 
                    #['05-14-17', '08:54PM', '121286', 'TRBC2054.IPZ']

            self.latest_filename = latest_file[-1]

            time_radar_struct = Timer(self.prd_type, self.warn_time, latest_file)
            self.latest_file_date = time_radar_struct.get_radar_filetime()
            self.is_warned = time_radar_struct.is_warned()
            log.debug('Radar latest filename %s, created date UTC+8 %s' % (self.latest_filename, self.latest_file_date))

        else:
            self.latest_filename = files[-1][-1] 
            #['-rw-rw-r--', '1', '702', '702', '6879', 'May', '14', '23:09', 'AWOS201705142309.JHK']
            #['-r--r--r--', '1', 'ftp', 'ftp', '814473', 'May', '15', '07:23', 'ISN201705150700.JPG']
            if self.prd_type == "awos":
                time_awos_struct = Timer(self.prd_type, self.warn_time, self.latest_filename)
                self.latest_file_date = time_awos_struct.get_awos_filetime()
                self.is_warned = time_awos_struct.is_warned()
                log.debug('Awos latest filename %s' % (self.latest_file_date))
            elif self.prd_type == "satellite":
                time_sat_struct = Timer(self.prd_type, self.warn_time, self.latest_filename)
                self.latest_file_date = time_sat_struct.get_sat_filetime()
                self.is_warned = time_sat_struct.is_warned()
                log.debug('Satellite latest filename %s' % (self.latest_file_date))

        # inserttime = self.now.strftime("%Y%m%d %H:%M:%S")
        # filetime = time.strftime("%Y%m%d %H:%M:%S", self.latest_file_date)
        
        watchlist = [self.is_warned, self.latest_filename, self.latest_file_date]
        return watchlist

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
            log.info(message)

            enbale_phone_message = config['enbale_phone_message']
            api = config['api']
            if enbale_phone_message:
                for phone_number in config['contacts']:
                    response = requests.post(api['message_url'], data={'token': api['token'], 'phone_number': phone_number, 'message': message })
                    log.info(response.text)
                    return response.json()
                    time.sleep(30)

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
    log.debug('Start in DEBUG mode')

@click.command()
@click.option('--service', '-s', type=click.Choice(['radar', 'awos', 'satellite', 'all']), multiple=True)
def run(service):
    """-s, --service [name] Run watch service."""
    global config

    if 'all' in service:
        service = ('radar', 'awos', 'satellite')
    
    message = None

    while service:
        config = load_config()
        products = config['products']

        if 'radar' in service:
            listen(products['radar'], message)
        if 'awos' in service:
            listen(products['awos'], message)
        if 'satellite' in service:
            listen(products['satellite'], message)
        time.sleep(300)
    else:
        click.echo("Error: please use 'run -s [name]' to start a service")


main.add_command(run)

if __name__ == '__main__':
    # main()
    products = config['products']
    x = Product(products['test-s'])
    y = Product(products['test-a'])
    z = Product(products['test-r'])