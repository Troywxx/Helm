#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime

class Timer(object):

	def __init__(self, prd_type, warn_time, files):
		self.prd_type= prd_type
		self.warn_time = warn_time
		self.files = files
		self.now = datetime.datetime.now()
		self.utcnow = datetime.datetime.utcnow()


	def get_radar_filetime(self):

		date = self.files[0]
		time = self.files[1]

		year = '20' + date[6:]
		month = date[0:2]
		day = date[3:5]
		hour_12 = time[0:2]
		minute = time[3:5]
		half_12 = time[5:]
		time_string = year + ' ' + month + ' ' + day + ' ' + hour_12 + ' ' + minute + ' ' + half_12
		time_radar_struct = datetime.datetime.strptime(time_string, "%Y %m %d %I %M %p")
		return time_radar_struct

	def get_awos_filetime(self):

		filename = self.files

		year = filename[4:8]
		month = filename[8:10]
		day = filename[10:12]
		hour_24 = filename[12:14]
		minute = filename[14:16]
		time_string = year + ' ' + month + ' ' + day + ' ' + hour_24 + ' ' + minute
		time_awos_struct = datetime.datetime.strptime(time_string, "%Y %m %d %H %M")
		return time_awos_struct

	def get_sat_filetime(self):

		filename = self.files

		year = filename[3:7]
		month = filename[7:9]
		day = filename[9:11]
		hour_24 = filename[11:13]
		minute = filename[13:15]
		time_string = year + ' ' + month + ' ' + day + ' ' + hour_24 + ' ' + minute
		time_sat_struct = datetime.datetime.strptime(time_string, "%Y %m %d %H %M")
		return time_sat_struct

	def is_warned(self):
		if self.prd_type == 'radar':
			filetime = self.get_radar_filetime()
			return self.now - filetime > datetime.timedelta(minutes=self.warn_time)
		elif self.prd_type == 'awos':
			filetime = self.get_awos_filetime()
			return self.utcnow - filetime > datetime.timedelta(minutes=self.warn_time)
		elif self.prd_type == 'satellite':
			filetime = self.get_sat_filetime()
			return self.now - filetime > datetime.timedelta(minutes=self.warn_time)


# if __name__ == '__main__':
# 	config = {
# 		'radar':['05-14-17', '08:54PM', '121286', 'TRBC2054.IPZ'],
# 		'awos':['-rw-rw-r--', '1', '702', '702', '6879', 'May', '14', '23:09', 'AWOS201705142309.JHK'],
# 		'satellite':['-r--r--r--', '1', 'ftp', 'ftp', '814473', 'May', '15', '07:23', 'ISN201705150700.JPG']
# 	}

# 	test = Timer('radar',config['radar'])
# 	print test.is_warned()