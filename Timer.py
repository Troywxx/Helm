#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("radar_check_config.cfg")
clock_items = config.items("check_clock")
shift_items = config.items("check_shift")

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
			filetime = datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.timetuple(self.get_radar_filetime())))
			# print filetime
			for i in clock_items:
				time_hour = datetime.datetime.strptime(i[0], "%H")
				time_standard = datetime.datetime.combine(datetime.datetime.utcnow(), time_hour.time())
				if self.utcnow.hour == time_standard.hour:
					check_start = time_standard - datetime.timedelta(minutes=int(shift_items[0][1]))
					check_end = time_standard + datetime.timedelta(minutes=int(shift_items[1][1]))
					# print filetime
					m = filetime > check_start
					n = check_end > filetime
					# print filetime
					# print check_start,check_end
					# print m,n
					if m and n and i[1]=="False":
						# print i[1]
						config.set("check_clock", i[0], "True")
						config.write(open("radar_check_config.cfg","w"))
						# print i[1]
						return False
					else:
						return True
				elif self.utcnow.hour - time_standard.hour == 1:
					config.set("check_clock", i[0], "False")
					config.write(open("radar_check_config.cfg","w"))
		elif self.prd_type == 'awos':
			filetime = self.get_awos_filetime()
			return self.utcnow - filetime > datetime.timedelta(minutes=self.warn_time)
		elif self.prd_type == 'satellite':
			filetime = self.get_sat_filetime()
			return self.now - filetime > datetime.timedelta(minutes=self.warn_time)
		else:
			filetime = self.get_sat_filetime()
			return self.now - filetime > datetime.timedelta(minutes=self.warn_time)


if __name__ == '__main__':
	config1 = {
		'radar':['09-12-17', '03:05PM', '121286', 'TRBC1505.IPZ'],
		'awos':['-rw-rw-r--', '1', '702', '702', '6879', 'May', '14', '23:09', 'AWOS201705142309.JHK'],
		'satellite':['-r--r--r--', '1', 'ftp', 'ftp', '814473', 'May', '15', '07:23', 'ISN201705150700.JPG']
	}

	test = Timer('radar', 180, config1['radar'])
	print test.is_warned()