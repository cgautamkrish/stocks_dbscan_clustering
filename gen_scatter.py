import csv
import threading
import time 
import datetime
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt

files = ["data/GOOGL.csv", "data/YHOO2.csv", "data/ORCL2.csv", "data/MSFT2.csv"]
dataArray = []
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
			time2 = time.mktime(datetime.datetime.strptime(row[0], "%Y-%m-%d").timetuple())
			x.append(time2)
			y.append(change)
			obj = [time2, company, change, '', pairIndex]
			dataArray.append(obj)
		toggle += 1

# Generate scatter plot of dataset
# Same as image in images/initial_scatter_plot.png
s = np.pi * (1 * 2)**2
plt.scatter(x, y, s=s, c=x, alpha=0.5)
plt.show()