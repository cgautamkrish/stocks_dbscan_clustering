import csv
import threading
import time 
import datetime
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt

files = ["GOOGL.csv", "YHOO2.csv", "ORCL2.csv", "MSFT2.csv"]
dataArray = []
largest_y = 0
smallest_y = 0
setToggle = 1

def findRanges(change):
	global largest_y
	global smallest_y
	if change > largest_y:
		largest_y = change
	elif change < smallest_y:
		smallest_y = change

pairIndex = 0 
x = []
y = []

for f in files:
	company = f.split('.')[0]
	cr = csv.reader(open(f,"rt"))
	toggle = 0
	for row in cr:
		if toggle != 0:
			#print(company)
			pairIndex += 1
			change = ((float(row[4]) - float(row[1]))/float(row[1]))*100
			if setToggle == 1:
				smallest_y = change
				largest_y = change
				setToggle = 0
			findRanges(change)
			time2 = time.mktime(datetime.datetime.strptime(row[0], "%Y-%m-%d").timetuple())
			x.append(time2)
			y.append(change)
			obj = [time2, company, change, '', pairIndex]
			dataArray.append(obj)
		toggle += 1

s = np.pi * (1 * 2)**2
plt.scatter(x, y, s=s, c=x, alpha=0.5)
plt.show()