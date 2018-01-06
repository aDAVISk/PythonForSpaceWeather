#########################################################################
# ReadGoesXrsReport.py
# Author: Akito D. Kawamura (aDAVISk)
# Goes Xrs Report
# https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/
#########################################################################
import astropy.time as Time

#__all__ = ['ReadGoesXrsReport']

FlareClassFluxSI = { # Watt/m**2
	"A": 1.0e-8,
	"B": 1.0e-7,
	"C": 1.0e-6,
	"M": 1.0e-5,
	"X": 1.0e-4
}

def calcFlux(clss, mag):
	return FlareClassFluxSI[clss]*float(mag)

class FlareEvent:
	# start : astropy.Time object - start time
	# end   : astropy.Time object - end time
	# max   : astropy.Time object - max time
	# clss  : char (one-length string) - class of the flare
	# mag   : float - magnitude within the class of the flare
	# flux  : float - GOES flux in Watt/m**2
	# lat   : int - latitude of the flare (North = + direction)
	# cmd   : int - central meridian distance of the flare (East = + direction)
	__defFormat="isot"
	def __init__(self,start=None,end=None, max=None, clss=None, mag=None,location=None):
		self.setStart(start)  
		self.setEnd(end)
		self.setMax(max)
		self.setClssMag(clss,mag)
		self.setLocation(location)

	def __del__(self):
		pass

	def setStart(self,startTime, format=__defFormat):
		#print("{0}".format(startTime))
		self.start = Time.Time(startTime, format=format) if startTime is not None else None

	def setEnd(self,endTime, format=__defFormat):
		#print("{0}".format(endTime))
		if endTime is not None:
			hh = int(endTime[11:13])
			if hh >= 24:
				endTime=endTime[:11]+"{0:02d}".format(hh-24)+endTime[13:]
				self.end = Time.Time(endTime, format=format)+Time.TimeDelta(1.0,format="jd")
			else:
				self.end = Time.Time(endTime, format=format)
		else:
			self.end = None

	def setMax(self, maxTime, format=__defFormat):
		#print("{0}".format(maxTime))
		if maxTime is not None:
			hh = int(maxTime[11:13])
			if hh >= 24:
				maxTime=maxTime[:11]+"{0:02d}".format(hh-24)+maxTime[13:]
				self.max = Time.Time(maxTime, format=format)+Time.TimeDelta(1.0,format="jd")
			else:
				self.max = Time.Time(maxTime, format=format) 
		else:
			self.max = None

	def setClssMag(self,clss, mag):
		self.clss = clss if clss is not None else None
		self.mag  = int(mag)*0.1 if mag is not None else None
		#print("{0}, {1}".format(mag, self.mag))
		self.flux = calcFlux(self.clss,self.mag) if (clss is not None) and (mag is not None) else None

	def setLocation(self,location):
		#print("{0}".format(location))
		if location is not None:
			if((location[0]!="N") and (location[0]!="S")) or ((location[3]!="E") and (location[3]!="W")):
				self.lat = None
				self.cmd = None
			else:
				self.lat = int(location[1:3]) if location[0] == "N" else -1*int(location[1:3])
				self.cmd = int(location[4:6]) if location[3] == "E" else -1*int(location[4:6])
		else:
			self.lat = None
			self.cmd = None
# end of class FlareEvent

def ReadOneGoesXrsReport(istr):
	#print(istr)
	date = "19" if int(istr[5:7]) >= 70 else "20"
	date += istr[5:7]+"-"+istr[7:9]+"-"
	start = date+istr[9:11]+"T"+istr[13:15]+":"+istr[15:17]
	end = date+istr[9:11]+"T"+istr[18:20]+":"+istr[20:22]
	max = date+istr[9:11]+"T"+istr[23:25]+":"+istr[25:27] if istr[23:25] != "  " else None
	return FlareEvent(start=start,end=end,max=max,location=istr[28:34],clss=istr[59], mag=istr[60:63])

def ReadGoesXrsReport(file):
	ifile = open(file, "r")
	data = ifile.readlines()
	ifile.close()
	flares = []
	for line in data:
		if len(line) >= 63:
			#print("{0}".format(len(line)))
			flares.append(ReadOneGoesXrsReport(line))
	return flares