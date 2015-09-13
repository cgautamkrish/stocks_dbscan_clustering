import csv
import threading
import time 
import datetime
import scipy
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from scipy.spatial import distance

files = ["data/GOOGL.csv", "data/YHOO2.csv", "data/ORCL2.csv", "data/MSFT2.csv"]
dataArray = []
largest_y = 0
smallest_y = 0
setToggle = 1
allCorePoints = []

# DBSCAN constants
# Chosen after several trial and errors
radiusDistance = 40
minPoints = 10

# DBSCAN clustering function of 20 points
# Identifies cores points based on number of border points it has
# Disregard border points and noise points
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

	# Euclidean distance. Generates a distance matric for each point in set ie. 20
	dist = scipy.spatial.distance.cdist(individualSet,individualSet,'euclidean')
	for d in range(0, len(dist)):
		borderPoint = 0
		borderPoints = []
		for h in range(0, len(dist[d])):
			if dist[d][h] < radiusDistance:
				#print(dist[d][h])
				borderPoint += 1
				borderPoints.append(allPoints[h])
		if borderPoint >= minPoints:
			#print("core point!")
			allCorePoints.append(borderPoints)

# To keep track of maximum and minimum delta change. Non-essential
def findRanges(change):
	global largest_y
	global smallest_y
	if change > largest_y:
		largest_y = change
	elif change < smallest_y:
		smallest_y = change

pairIndex = 0
print('-------')
print('Clustering start..') 
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
			obj = [time2/1000000, company, change*100, '', pairIndex]
			dataArray.append(obj)
		toggle += 1
	print('File read..')

distPairs = {}
dataArray = sorted(dataArray, key=itemgetter(0))

toggle = 0
tempSet = []
dailyData = []
dateToggle = 0

# Loop through to find sets of 5 dates to send for DBSCAN
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

weeklySet = []
for j in range(0, len(dailyData)):
	if j%5 == 0 and j != 0:
		print('DBSCAN processing weekly set..')
		dbscan(weeklySet)
		weeklySet = []
		weeklySet.append(dailyData[j])
	else:
		weeklySet.append(dailyData[j])

print('Clustering done..')
datesDict = {}

# Variables for scatter plot generation
x = []
y = []

# Get the unique dates and store in dict with company value*
for i in allCorePoints:
	for j in i:
		date = datetime.datetime.fromtimestamp(int(j[0]*1000000)).strftime('%Y-%m-%d')
		x.append(j[0]*1000000)
		y.append(j[2]/100)
		datesDict[date] = j[1]

print('Number of dates with dense clusters - ' + str(len(datesDict)))
print('Writing dates to csv..')
writer = csv.writer(open('dates.csv', 'w', newline=''))
for key, value in datesDict.items():
	writer.writerow([key, value])

# Uncomment the follwing to view the scatter plot of the density clusters
# Same as image in images/dense_clusters.png
print('Plotting dense clusters..')	
s = np.pi * (1 * 2)**2
plt.scatter(x, y, s=s, c=x, alpha=0.5)
plt.show()