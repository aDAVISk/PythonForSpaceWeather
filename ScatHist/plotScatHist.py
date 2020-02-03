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
	     saveName=None, # file name for saving
	     showing=False, # set True to display the figure on the screen
	     fontsize=16, # font size
	     ylabelOff=0.07 # ajust the position of y-axis title
	    ):
	
	# Parameter checks
	x = np.array(x)
	y = np.array(y)
	if xticks is None:
		xticks = np.arange(np.floor(np.min(x)*(1-0.1*np.sign(np.min(x)))), np.ceil(np.max(x)*(1+0.1*np.sign(np.max(x)))))
	if yticks is None:
		yticks = np.arange(np.floor(np.min(y)*(1-0.1*np.sign(np.min(y)))), np.ceil(np.max(y)*(1+0.1*np.sign(np.max(y)))))
	if xlim is None:
		xlim = np.array([xticks[0]*(1-0.1*np.sign(xticks[0])),xticks[-1]*(1+0.1*np.sign(xticks[0]))])
	if ylim is None:
		ylim = np.array([yticks[0]*(1-0.1*np.sign(yticks[0])),yticks[-1]*(1+0.1*np.sign(yticks[0]))])
	if bins is None:
		bins = np.linspace(np.min([xlim[0],ylim[0]]),np.max([xlim[1],ylim[1]]),10)

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
	axScatter.plot(xlim,ylim,":", color="grey")
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
	axScatter.text(xlim[0]+0.2,ylim[1]-0.5,"coefficient = {0:5.2f}".format(reg.coef_[0][0]))#,fontsize=fontsize)
	axScatter.yaxis.set_label_coords(-ylabelOff, 0.5)

	# Adjestment for histgram of x
	axHistX.hist(x, bins=bins,color="lightgrey",edgecolor='black',linewidth=1.2)
	axHistX.grid(axis="x")
	axHistX.set_ylabel("counts")
	axHistX.set_xlim(axScatter.get_xlim())
	axHistX.yaxis.set_label_coords(-ylabelOff, 0.5)

	# Adjestment for histgram of y
	axHistY.hist(y, bins=bins,color="lightgrey",edgecolor='black',linewidth=1.2,orientation="horizontal")
	axHistY.set_xlabel("counts")
	axHistY.grid(axis="y")
	axHistY.set_ylim(axScatter.get_ylim())
  
	# Saving
	if saveName is not None:
		plt.savefig(saveName)
		print("plotScatHist: save to {0}".format(saveName))
	if showing:
		plt.show()
	else:
		plt.close()
# end of plotScatHist
