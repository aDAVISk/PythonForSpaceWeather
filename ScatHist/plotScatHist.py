# plotScatHist.py
# CC-BY Akito D. Kawamura (@aDAVISk) 
#
# This program plots the scatter plot of height & width equal to scatHeight times of histgram height
# as described as following. 
#   =============================    
#   |         margin_tr         |   <- Parameter description on a figure
#   |  x------------x           |   * Scatter plot would be square if the figure is square.
#   |m : histgram X :         m |   * "histgram height" is the length of "x---x" for histY or "x:x" for histgram X. 
#   |a x------------x         a |   * "spacing" and "margin_??" are in the unit of figure size as 1.
#   |r    spacing             r |
#   |g x------------x s x---x g |
#   |i :  scatter   : p : h : i |
#   |n :   plot     : a : i : n |
#   |_ :            : c : s : _ |
#   |l :            : i : t : t |
#   |b : scatHeight : n : Y : r |
#   |  x------------x g x---x   |
#   |         margin_lb         |
#   =============================

import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression

def plotScatHist(x,y, # data for plotting
	     xticks=None,yticks=None, #  ticks for x or y axis
	     xlim=None,ylim=None, # plotting limits for x or y axis
	     bins=None, # bins for histgram
	     figsize=(8.0,8.0), # size of figure
	     margin_lb = 0.1, margin_tr = 0.05, # margin on left&bottom (lb) or top&right (tp) in the unit of figure size
	     spacing = 0.02, # space in between the scatter plot and histgrams in the unit of figure size 
	     scatHeight=5, # size of figure in the unit of the height of histgram graphic
	     scatMark="k.", # format of scattering marks
	     xTitle=" ",yTitle=" ", # Titles of x or y axis
	     axStrFormat = "%.1f", # tick format for scatter plot 
	     saveName=None, # file name for saving
	     showing=False, # set True to display the figure on the screen
	     fontsize=16, # font size
	     ylabelOff=0.07 # ajust the position of y-axis title
	    ):
	
	# Parameter checks
	logFloor = lambda xx: np.sign(xx)*(np.floor(np.abs(xx)/10**np.floor(np.log10(np.abs(xx))))+0.5*(1-np.sign(xx)))\
			*10**np.floor(np.log10(np.abs(xx)))
	logCeil  = lambda xx: np.sign(xx)*(np.ceil(np.abs(xx)/10**np.floor(np.log10(np.abs(xx))))-0.5*(1-np.sign(xx)))\
			*10**np.floor(np.log10(np.abs(xx)))
	x = np.array(x)
	y = np.array(y)
	if xticks is None:
		if yticks is None:
			xticks = np.linspace(logFloor(np.min([x,y])), logCeil(np.max([x,y])),binNum+1)
		else:
			xticks = yticks
	if yticks is None:
		yticks = xticks
	if xlim is None:
		axMargin = 0.1*np.min([np.abs(logFloor(xticks[0])),np.abs(logFloor(xticks[-1]))])
		xlim = np.array([logFloor(xticks[0])-axMargin,logCeil(xticks[-1])+axMargin])
	if ylim is None:
		axMargin = 0.1*np.min([np.abs(logFloor(yticks[0])),np.abs(logFloor(yticks[-1]))])
		ylim = np.array([logFloor(yticks[0])-axMargin,logCeil(yticks[-1])+axMargin])
	if bins is None:
		bins = np.linspace(np.min([xticks[0],yticks[0]]),np.max([xticks[-1],yticks[-1]]),binNum+1)
	
	# calculate the linear regression
	lin_x = x.reshape(-1,1)
	lin_y = y.reshape(-1,1)
	reg = LinearRegression().fit(lin_x,lin_y)

	print("Linear Regression:")
	print("   score = {0}".format(reg.score(lin_x, lin_y)))
	print("   coeff = {0}".format(reg.coef_[0][0]))
	print("   intcp = {0}".format(reg.intercept_[0]))

	# calculate the positions of plots
	histHeight = (1.0-spacing-margin_lb-margin_tr)/(1+scatHeight)
	scatLen = histHeight * scatHeight
	rect_scatter = [margin_lb, margin_lb, scatLen, scatLen]
	rect_histx = [margin_lb, margin_lb + scatLen + spacing, scatLen, histHeight]
	rect_histy = [margin_lb + scatLen + spacing, margin_lb, histHeight, scatLen]


	# Basic setup of the figure
	fig = plt.figure(figsize=figsize)
	plt.rcParams["font.size"] = fontsize
	axScatter = plt.axes(rect_scatter)
	axScatter.tick_params(direction='in', top=True, right=True)
	axHistX = plt.axes(rect_histx)
	axHistX.tick_params(direction='in', labelbottom=False)
	axHistY = plt.axes(rect_histy)
	axHistY.tick_params(direction='in', labelleft=False)
  
	# Plots
	axScatter.plot(xlim,[ylim[0],xlim[1]/float(xlim[0])*ylim[0]],":", color="grey")
	axScatter.plot(x,y,scatMark,ms=10)
	axScatter.plot(xlim,reg.predict(xlim.reshape(-1,1)),color='black', linestyle='dashed')
  
	# Adjestment for the scatter plot
	axScatter.set_xticks(xticks)
	axScatter.set_yticks(yticks)
	axScatter.set_xlim(xlim)
	axScatter.set_ylim(ylim)
	axScatter.set_aspect(1.)
	axScatter.grid()
	axScatter.set_xlabel(xTitle)
	axScatter.set_ylabel(yTitle)
	if axStrFormat is not None:
		axScatter.xaxis.set_major_formatter(FormatStrFormatter(axStrFormat))
		axScatter.yaxis.set_major_formatter(FormatStrFormatter(axStrFormat))
	axScatter.text(xlim[0]+0.01*(xlim[1]-xlim[0]),ylim[1]-0.05*(ylim[1]-ylim[0]),\
		"coefficient = {0:5.2f}".format(reg.coef_[0][0]))
	axScatter.yaxis.set_label_coords(-ylabelOff, 0.5)

	# Adjestment for histgram of x
	axHistX.hist(x, bins=bins,color="lightgrey",edgecolor='black',linewidth=1.2)
	axHistX.grid(axis="x")
	axHistX.set_ylabel("counts")
	axHistX.set_xlim(axScatter.get_xlim())
	axHistX.set_xticks(axScatter.get_xticks())
	if axStrFormat is not None:
		axHistX.yaxis.set_major_formatter(FormatStrFormatter("%{0}d".format(len(format(yticks[-1],axStrFormat[1:])))))
	axHistX.yaxis.set_label_coords(-ylabelOff, 0.5)

	# Adjestment for histgram of y
	axHistY.hist(y, bins=bins,color="lightgrey",edgecolor='black',linewidth=1.2,orientation="horizontal")
	axHistY.set_xlabel("counts")
	axHistY.grid(axis="y")
	axHistY.set_ylim(axScatter.get_ylim())
	axHistY.set_yticks(axScatter.get_yticks())
	if axStrFormat is not None:
		axHistY.xaxis.set_major_formatter(FormatStrFormatter("%{0}d".format(len(format(xticks[-1],axStrFormat[1:])))))
  
	# Saving
	if saveName is not None:
		plt.savefig(saveName)
		print("plotScatHist: save to {0}".format(saveName))
	if showing:
		plt.show()
	else:
		plt.close()
# end of plotScatHist
