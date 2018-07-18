#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import re

from config import config

standard = config["radar_check"]["standard"]
shift = config["radar_check"]["shift"]

pattern = re.compile(r'\d', re.S)

class Timer(object):

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
            for i in standard:
                time_hour = datetime.datetime.strptime(i, "%H%M")
                time_standard = datetime.datetime.combine(datetime.datetime.utcnow(), time_hour.time())
                start_time = time_standard - datetime.timedelta(minutes=shift)
                if start_time < self.utcnow < time_standard:
                    diff_time = time_standard - self.get_time_struct()
                    check_time = datetime.timedelta(minutes=int(self.warn_time))
                    if diff_time < check_time:
                        return False
                    else:
                        return True
        elif self.prd_type == 'satellite':
            return self.now - self.get_time_struct() > datetime.timedelta(minutes=self.warn_time)
        else:
            return self.utcnow - self.get_time_struct() > datetime.timedelta(minutes=self.warn_time)


if __name__ == '__main__':
    config1 = {
        'radar':'201807190046400.10P.100.2.jpg',
        'awos':'AWOS201807181703.JHK',
        'satellite':'ISN201705150700.JPG',
        'radar_166': '2018-07-18 16:17(UTC)',
        'awos_166': '2018-07-18 17:16(UTC)'
    }

    test = Timer('radar', 3, config1['radar'])
    print test.is_warned()