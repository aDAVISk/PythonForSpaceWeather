# retrieveDSCOVRdata.py
# CC-BY: Akito D. Kawamura (@aDAVISk)
# last update: 2021.Aug.31
# This program downloads DSCOVR data files which URLs are saved
# in a file, e.g."filelist.txt," seperated with a space ' '.
# Plese check https://www.ngdc.noaa.gov/dscovr/portal/index.html#/download/
# to claim the URL list of the data files.
#
# !!! NOTICE !!!
# This program will access the NOAA server for more than 3 hours
# if all data is requested. To reduce the traffic on the NOAA server,
# share downloaded data with your mates if possible.

import re
import urllib.request
import os
import time

ifilename = "filelist.txt"
savepath = "./"

with open(ifilename,"r") as ifile:
    files = re.split(r' +',ifile.read().replace('\n',''))

#print(files)

for ff in files:
    print(ff,end="")
    year,month,filename = ff.split('/')[-3:]
    #print("{0}/{1}/{2}".format(year,month,filename))
    if not os.path.isdir("{0}{1}".format(savepath,year)):
        os.mkdir("{0}".format(year))
    if not os.path.isdir("{0}{1}/{2}".format(savepath,year,month)):
        os.mkdir("{0}/{1}".format(year,month))
    if not os.path.isfile("{0}{1}/{2}/{3}".format(savepath,year,month,filename)):
        urllib.request.urlretrieve(ff,"{0}{1}/{2}/{3}".format(savepath,year,month,filename))
        print("--retrieved",end="")
        time.sleep(1)
    print("")
