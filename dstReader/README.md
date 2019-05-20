# DstReader
License: Creative Commons BY: Akito D. Kawamura (@aDAVISK)<br>
<br>
This program is for reading Dst-index in "WDC-like Dst format." <br>
For Dst-index, please check World Data Center for Geomagnetism, Kyoto (http://wdc.kugi.kyoto-u.ac.jp/).

### How to use
1) Get your DST file in WDC-like format via http://wdc.kugi.kyoto-u.ac.jp/dstae/index.html
2) Use constructor `dstReader("datafile")` or method `readData("datafile")` to initialize.
3) Call methods `getDstDate(date)`, `getDst24h(date)`, or `getDstRange(start,end)` to get Dst value(s) of the date, 24 hours from the date, or the range of date from start till end (excluded).  The arguments must be `datetime.datetime` object, which values of minutes or less are ignored. 

Additional tips;
- The data is stored in `dstReader.dstData` as a 1D Numpy array.
- You can use method `findDate(int)` to find the date of the given index of `dstData`. 
