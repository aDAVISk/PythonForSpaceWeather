from ReadGoesXrsReport import *
from time import sleep

#flares = ReadGoesXrsReport("./goes-xrs-report_1983.txt")
flares = ReadGoesXrsReport("./goes-xrs-report_2003.txt")

ss = len(flares)

for ii in range(ss):
	curr = flares[ii]
	print("{0} ~ {1} ({2}): [{3}{4:>4.1f}]={5:7.1e} at {6} ({7}, {8})".format(curr.start.iso, curr.end.iso,\
	                 curr.max.iso, curr.clss, curr.mag, curr.flux, curr.noaa, curr.lat, curr.cmd))
	sleep(0.2)