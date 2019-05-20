##############################################
# File: test_dstReader.py
# License: Creative Commons BY: Akito D. Kawamura (@aDAVISK)
#
# This is a test program for dstReader.py
##############################################

from dstReader import dstReader
from astropy.time import Time
from datetime import datetime

dstFile = "../DST/DST_1976-2000.txt"
myDst = dstReader(dstFile)
myDate = datetime(2000,1,1)
print("---Checking I/O & Warning---")
print("{0}: {1}".format(myDate.strftime("%Y-%m-%d"), myDst.getDstDate(myDate)))
print("{0}: {1}".format("2000-01-01", myDst.getDstDate("2000-01-01")))
print("---Checking 24H, Range---")
print("{0}: {1}".format(myDate.strftime("%Y-%m-%d"), myDst.getDst24h(myDate)))
print("{0} - {1}: {2}".format(myDate.isoformat()[0:13], datetime(2000,1,1,2).isoformat()[0:13], myDst.getDstRange(myDate,datetime(2000,1,1,3))))
print("---Checking Date---")
print("{0}".format(myDst.findDate(26)))
