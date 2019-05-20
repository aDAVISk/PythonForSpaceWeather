##############################################
# File: dstReader.py
# License: Creative Commons BY: Akito D. Kawamura (@aDAVISK)
#
# This program is for reading Dst-index in "WDC-like Dst format"
# For Dst-index, please check
# World Data Center for Geomagnetism, Kyoto (http://wdc.kugi.kyoto-u.ac.jp/)
##############################################

import numpy as np
from datetime import datetime, timedelta
import warnings 

class dstReader:
	dstData = np.array([])
	dstIdxLst = {}
	def __init__(self,dataFile=None):
		self.readData(dataFile)
	def readData(self,dataFile=None):
		if dataFile is None:
			print("<DSTreader> Warning: no data is set.")
			return self
		ifile = open(dataFile,"r") 
		ifline = ifile.readline().rstrip('\r\n')
		while ifline:
			date_s = ifline[14:16] + ifline[3:7]+ifline[8:10]
			baseV = int(ifline[16:20])
			vals = np.array([ifline[i: i+4] for i in range(20, len(ifline)-4, 4)],dtype=float) + baseV
			vals[np.where(vals == 9999)] = np.nan
			self.dstIdxLst["{0}-{1}-{2}".format(date_s[0:4],date_s[4:6],date_s[6:8])] = np.size(self.dstData)
			self.dstData = np.hstack((self.dstData,vals))
			ifline = ifile.readline().rstrip('\r\n')
		ifile.close()

	def getDstDate(self, date):
		return self.dstData[self.__getIdx(date)]

	def getDst24h(self, date):
		idx = self.__getIdx(date)
		return self.dstData[idx:idx+24]

	def getDstRange(self, startDate, endDate):
		return self.dstData[self.__getIdx(startDate):self.__getIdx(endDate)]

	def __getIdx(self,date):
		if type(date) is datetime:
			isoDate = date.strftime("%Y-%m-%d")
			hour = date.hour
		else:
			if type(date) is str:
				warnings.warn("<dstReader: _getIdx> date is prefered to be datetime.datetime object.", UserWarning)
				isoDate = date
				hour = 0
			else:
				raise TypeError("<dstReader: _getIdx> date must be datetime.datetime object.")
		return self.dstIdxLst[isoDate]+hour

	def findDate(self,idx):
		dates = [dd for dd, vv in self.dstIdxLst.items() if vv >= idx]
		if dates:
			return datetime.strptime(dates[0], "%Y-%m-%d") + timedelta(hours = idx - self.dstIdxLst[dates[0]])
		return None
# End of class dstReader
