"""
 !!! This FilterHMI.py is beta version. Please use this under your responsibility. !!!
 Creative Commons BY: Akito D. Kawamura
 
 Special requirements:
 	hmilibrary.py

 This program will try to extract polarity inversion lines from HMI.M by filtering technique.

 This program is using Sunpy (http://docs.sunpy.org/)

 ---update log---
  2018.04.03 : Beta version released

"""
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u

import sunpy.map

from hmilibrary import hmiprep

idata = sunpy.map.Map('./hmi.M_45s.20141024_210215_TAI.2.magnetogram.fits')

mdata = hmiprep(idata)

ss = mdata.data.shape
dtype = mdata.data.dtype

ff = 5 # unit size of filter
hff = 2 #int(np.floor(ff/2)) # margin of 
flt_limit = 100*ff*(ff+2*hff+1)
flt_cutoff = 1.0 # minimum absolute value for filtering polarity inversion lines 

"""
filter notation flt_abcd associated with a current cell noted as *
      ff hff
    <----x->
    |---------------| ^
    |....|.| |.|....| | b ff
    |---------------| x
    |....|.| |.|....| |   hff
 L  |---------------| v
 A  |....|.|*|.|....| 
 T  |---------------| ^
    |....|.| |.|....| |   hff
    |---------------| x
    |....|.| |.|....| | a ff
    |---------------| v
    <---->     <---->
      c         d       (. = aribital number of pixels)
           LON
 where latitude and longitude increase as going to up and right of this diagram.
"""

flt_abs = np.zeros((ss[0],ss[1]),dtype=dtype)
flt_p000 = np.zeros((ss[0],ss[1]),dtype=dtype)
flt_0p00 = np.zeros((ss[0],ss[1]),dtype=dtype)
flt_00p0 = np.zeros((ss[0],ss[1]),dtype=dtype)
flt_000p = np.zeros((ss[0],ss[1]),dtype=dtype)

msk_p000 = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_n000 = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_0p00 = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_0n00 = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_00p0 = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_00n0 = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_000p = np.zeros((ss[0],ss[1]),dtype=dtype)
msk_000n = np.zeros((ss[0],ss[1]),dtype=dtype)

yy1 = ff+hff
yy2 = ss[0]-ff-hff-1
xx1 = ff+hff
xx2 = ss[1]-ff-hff-1

print("")

for ii in range(hff+1,hff+ff):
	for jj in range(-hff-ff,hff+ff):
		flt_p000[yy1:yy2,xx1:xx2] += mdata.data[yy1-ii:yy2-ii,xx1+jj:xx2+jj]
		flt_0p00[yy1:yy2,xx1:xx2] += mdata.data[yy1+ii:yy2+ii,xx1+jj:xx2+jj]
		flt_00p0[yy1:yy2,xx1:xx2] += mdata.data[yy1+jj:yy2+jj,xx1-ii:xx2-ii]
		flt_000p[yy1:yy2,xx1:xx2] += mdata.data[yy1+jj:yy2+jj,xx1+ii:xx2+ii]
		print("{0},".format(jj),end="")
	print("-- {0}/{1}".format(ii,hff+ff))

msk_p000[np.where(flt_p000 > flt_limit)] = 1.0
msk_0p00[np.where(flt_0p00 > flt_limit)] = 1.0
msk_00p0[np.where(flt_00p0 > flt_limit)] = 1.0
msk_000p[np.where(flt_000p > flt_limit)] = 1.0

msk_n000[np.where(flt_p000 < -flt_limit)] = 1.0
msk_0n00[np.where(flt_0p00 < -flt_limit)] = 1.0
msk_00n0[np.where(flt_00p0 < -flt_limit)] = 1.0
msk_000n[np.where(flt_000p < -flt_limit)] = 1.0

""" #Checking pixel # satisfying each conditions
print("{0}".format(np.sum(msk_p000)))
print("{0}".format(np.sum(msk_n000)))
print("{0}".format(np.sum(msk_0p00)))
print("{0}".format(np.sum(msk_0n00)))
print("{0}".format(np.sum(msk_00p0)))
print("{0}".format(np.sum(msk_00n0)))
print("{0}".format(np.sum(msk_000p)))
print("{0}".format(np.sum(msk_000n)))
"""

flt_pn00 = (  flt_p000 - flt_0p00)*msk_p000*msk_0n00
flt_np00 = (- flt_p000 + flt_0p00)*msk_n000*msk_0p00
flt_00pn = (  flt_00p0 - flt_000p)*msk_00p0*msk_000n
flt_00np = (- flt_00p0 + flt_000p)*msk_00n0*msk_000p

flt_x = flt_00np - flt_00pn # for longitudal gradient
flt_y = flt_np00 - flt_pn00 # for latitudal gradient
flt_abs = np.sqrt(flt_x**2 + flt_y**2) # for total gradient

flt_data = flt_abs # here you can choose what kind of polarity inversion line to detect (flt_x, flt_y, flt_abs)

msk_flt = np.ma.masked_less_equal(np.absolute(flt_data),flt_cutoff) 
#print("{0}: {1}".format(np.sum(np.absolute(msk_flt)),np.nanmax(flt_data)))

fdata = sunpy.map.Map(flt_data,mdata.meta,mask=msk_flt.mask)
#mdata.plot_settings['cmap'] = 'hmimag'
fdata.plot_settings['cmap'] = 'bwr'

magmax = 1000.0
flt_absmax = 100.0

fig = plt.figure(figsize=(12, 9), dpi=100)
axes = plt.subplot()
magplt = mdata.plot(vmin=-magmax,vmax=magmax)
plt.colorbar()
csplt = fdata.plot(vmin=-flt_absmax,vmax=flt_absmax)
fdata.draw_limb()
#fdata.draw_grid(grid_spacing=30*u.deg) #draw the Heliographic Stonyhurst Coordinate
#plt.colorbar()
plt.show()

# showing close-up utilized for the sample data
cut_min = [2175,1250]*u.pixel
cut_max = [2775,1750]*u.pixel

cmdata = mdata.submap(cut_min,cut_max)
cfdata = fdata.submap(cut_min,cut_max)

fig = plt.figure(figsize=(12, 9), dpi=100)
axes = plt.subplot()
magplt = cmdata.plot(vmin=-magmax,vmax=magmax)
plt.colorbar()
csplt = cfdata.plot(vmax=flt_absmax, vmin=-flt_absmax)
#cmdata.draw_limb()
#cmdata.draw_grid(grid_spacing=5*u.deg)
plt.show()
