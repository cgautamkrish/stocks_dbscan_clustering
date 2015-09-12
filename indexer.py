import csv
import threading
import time 
import datetime
from operator import itemgetter

import scipy
from scipy.spatial import distance
import numpy as np
import matplotlib.pyplot as plt

files = ["GOOGL.csv", "YHOO2.csv", "ORCL2.csv", "MSFT2.csv"]
dataArray = []
largest_y = 0
smallest_y = 0
setToggle = 1
fileName = 'corepoint_'
globalVar = 0
allCorePoints = []

# DBSCAN constants
radiusDistance = 100000
minPoints = 10

def dbscan(tempSet):
	#print(set)
	individualSet = []
	allPoints = []
	dataValue = tempSet
	for i in dataValue:
		for j in i:
			coordinates = (j[0], j[2])
			#print(coordinates)
			individualSet.append(coordinates)
			allPoints.append(j)

	dist = scipy.spatial.distance.cdist(individualSet,individualSet,'euclidean')
	for d in range(0, len(dist)):
		borderPoint = 0
		borderPoints = []
		for h in range(0, len(dist[d])):
			if dist[d][h] < radiusDistance:
				print(dist[d][h])
				borderPoint += 1
				borderPoints.append(allPoints[h])
		if borderPoint >= minPoints:
			print("core point!")
			allCorePoints.append(borderPoints)

def findRanges(change):
	global largest_y
	global smallest_y
	if change > largest_y:
		largest_y = change
	elif change < smallest_y:
		smallest_y = change

pairIndex = 0 
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
			obj = [time2, company, change, '', pairIndex]
			dataArray.append(obj)
		toggle += 1

# Density based clustering start
distPairs = {}
dataArray = sorted(dataArray, key=itemgetter(0))

toggle = 0
tempSet = []
dailyData = []
dateToggle = 0
for i in dataArray:
	if toggle == 0:
		#print(i)
		firstTerm = i[0]
		tempSet.append(i)
		toggle = 1
		dateToggle += 1
	else:
		if i[0] == firstTerm:
			tempSet.append(i)
		else:
			dailyData.append(tempSet)
			tempSet = []
			firstTerm = i[0]
			tempSet.append(i)
			toggle = 1
			dateToggle += 1

packet = 1
weeklySet = []
for j in range(0, len(dailyData)):
	if j%5 == 0 and j != 0:
		dbscan(weeklySet)
		weeklySet = []
		weeklySet.append(dailyData[j])
	else:
		weeklySet.append(dailyData[j])

#print((allCorePoints))
print(len(allCorePoints))
