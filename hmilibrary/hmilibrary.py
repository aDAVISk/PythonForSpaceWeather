# -*- coding: utf-8 -*-
"""
 !!! This hmilibrary.py is beta version. Please use this under your responsibility. !!!
 Creative Commons BY: Akito D. Kawamura
 
 Provides preparation routine for data captured by the HMI instrument on SDO.
 This program is a modification of 
 	http://docs.sunpy.org/en/stable/_modules/sunpy/instr/aia.html#aiaprep
 	(retrieved at 2017.12.26)
 ---update log---
	2017.12.27 : release beta version tested with HMI.M & HMI.C
"""
import numpy as np
import astropy.units as u
import sunpy.map
from sunpy.map.sources.sdo import HMIMap

__all__ = ['hmiprep']


def hmiprep(hmimap,missing=0.0):
	"""
	Input
		hmimap: input map for preparation
		issing: value to replace NaNs, default=0.0
	Output
		newmap: an instance of sunpy.map.GenericMap
	"""
	if not isinstance(hmimap, HMIMap):
		raise ValueError("Input must be an HMIMap")

	print("[hmiprep] NaNs and values at out of the solar radius will be replaced with {0}.".format(missing))
	tempmap = sunpy.map.Map(hmimap.data,hmimap.meta)
	tempmap.data[np.where(tempmap.data != tempmap.data)]=missing

	if (tempmap.scale[0] / 0.6).round() != 1.0 * u.arcsec and tempmap.data.shape != (4096, 4096):
		scale = (tempmap.scale[0] / 0.6).round() * 0.6 * u.arcsec
	else:
		scale = 0.6*u.arcsec
	scale_factor = tempmap.scale[0] / scale

	tempmap2 = tempmap.rotate(angle=180*u.degree, scale=scale_factor.value, 
		                        recenter=True,missing=missing)

	cx = np.floor(tempmap2.meta['crpix1'])
	cy = np.floor(tempmap2.meta['crpix2'])
	range_x = (cx + np.array([-1, 1]) * tempmap.data.shape[0] / 2) * u.pix
	range_y = (cy + np.array([-1, 1]) * tempmap.data.shape[1] / 2) * u.pix
	newmap = tempmap2.submap(u.Quantity([range_x[0], range_y[0]]),
								u.Quantity([range_x[1], range_y[1]]))

	# Setting missing value for R > Rsun: this portion maybe needs more improvement.
	ss = newmap.data.shape
	r2_sun = (newmap.meta['rsun_obs'] / newmap.meta['cdelt1'])**2
	cx = newmap.meta['crpix1']
	cy = newmap.meta['crpix2']
	r2 = np.reshape((np.arange(ss[0],dtype='float64')-cx)**2,(ss[0],-1))\
			+(np.arange(ss[1],dtype='float64')-cy)**2
	newmap.data[np.where(r2>r2_sun)] = missing	
	###

	newmap.meta['r_sun'] = newmap.meta['rsun_obs'] / newmap.meta['cdelt1']
	newmap.meta['lvl_num'] = 1.5

	return newmap
#End of hmiprep
