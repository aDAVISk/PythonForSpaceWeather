# load_dscovr_sw.py
# CC-BY: Akito D. Kawamura (@aDAVISk)
# last update: 2021.Aug.31
# This program reads DSCOVR data file availabe at
# https://www.ngdc.noaa.gov/dscovr/portal/index.html#/download/
# and manages datasets with sorting sortedData(), multiplying
# two variables calcMultiple(), and evaluating one-variable
# use-defined function evalFunc().
#
#--- Sample Useage ---
# from load_dscovr_sw import DSCOVRdata
# swData = DSCOVRdata()
# swData.load("oe_m1m.nc",["bx_gsm","by_gsm","bz_gsm"],["bx","by",bz"])
# swData.load("oe_f1m.nc.gz","proton_vx_gsm","vx")
# print(swDta.attributes["bx"]) # check the attribute of Bx
# swData.calcMultiple("MagFlux","bz","vx",const=10**-3, attr={"unit":"mV/m"})
# dataSortedByTime = swData.sortedData()
# ----

import netCDF4
import re
import math
import warnings
from datetime import datetime, timedelta
import gzip

class DSCOVRdata:
    def __init__(self):
        self.data = {}
        self.attributes = {}
    def printFileVariableKeys(self,filename):
        with netCDF4.Dataset(ifile_m_name) as nc:
            print(nc.variables.keys()) # Check variable keys of the dataset

    def load(self,filename, keys, savekeys=None):
        if not isinstance(keys,list): keys = [keys]
        if savekeys is None: savekeys = keys
        if not isinstance(savekeys,list): savekeys = [savekeys]
        mem = None
        if filename[-3:] == ".gz":
            with gzip.open(filename,"rb") as gz:
                mem = gz.read()
        with netCDF4.Dataset(filename,"r",memory=mem) as nc:
            time = nc.variables["time"]
            epoch = datetime.fromisoformat(re.search('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',time.units).group(0))
            myTime = [epoch + timedelta(milliseconds=float(tt)) for tt in time]
            if "time" not in self.attributes:
                self.attributes["time"] = time.__dict__
            for kk, sk in zip(keys, savekeys):
                var = [float(vv) for vv in nc.variables[kk]]
                if sk not in self.attributes:
                    self.attributes[sk] = nc.variables[kk].__dict__
                for tt, vv in zip(myTime, var):
                    kt = tt.isoformat()
                    if kt not in self.data: self.data[kt] = {'time':tt}
                    if math.isnan(vv):
                        warnings.warn("DSCOVRdata: {0} is skipped for nan at {1}".format(sk,kt))
                    else:
                        self.data[kt][sk] = vv

    def calcMultiple(self,savekey,key1,key2,const=1,attr={}):
        self.attributes[savekey] = attr
        for dd in self.data.values():
            if key1 in dd and key2 in dd:
                dd[savekey] = dd[key1] * dd[key2] * const

    def evalFunc(self,savekey,key,func=lambda x:x,attr={}):
        self.attributes[savekey] = attr
        for dd in self.data.values():
            if key in dd:
                dd[savekey] = func(dd[key])

    def sortedData(self):
        return sorted(self.data.values(), key=lambda x:x["time"])
# End of class ESCOVRdata
