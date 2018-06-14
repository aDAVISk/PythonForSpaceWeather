# BitGraphics.py
# This code is under Creative Commons BY: Akito D. Kawamura
# Transform a given 2D numpy boolean numpy array into the stripes of binary stream.
# The first bit (highest order) is set to 1 as a header
import numpy as np

class BitGraphicsHR:
	def __init__(self, idata=None, padding=0):
		self.shape = (0,0)
		self.data = []
		if idata is not None:
			self.set(idata,padding)
	#end of __init__()
	def __repr__(self):
		return "["+"]\n[".join([str(bin(v)) for v in self.data])+"]"
	#end of __repr__
	def set(self, idata, padding=0):
		# jth bit of odata[i] is idata[i,j]
		try:
			if type(idata) != np.ndarray or idata.dtype != 'bool':
				raise TypeError("BitGraphicsHR: input data must be numpy.bool_")
		except AttributeError:
			raise TypeError("BitGraphicsHR: input data must be numpy.bool_")

		nraw, ncol = idata.shape
		odata = []
		initial = 1 << 63|1 # do not say 1 << 62 or error would be returned
		msk = 2 **(2*padding+ncol+1)-1
		for rr in idata:
			tmp = initial
			for ii,cc in enumerate(rr):
				tmp = tmp <<1 | cc
			odata.append((tmp<<padding)&msk)
		self.data = odata
		self.shape = (nraw+2*padding, ncol+2*padding)
	#end of set()
	def graph(self):
		print("\n".join([str(bin(v))[3:].replace("1","#").replace("0"," ") for v in self.data]))
	#end of graph
#end of BitGraphicHR
