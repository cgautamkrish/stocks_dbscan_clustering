import csv
import threading
import time 
import datetime
from operator import itemgetter

files = ["GOOGL.csv", "YHOO2.csv", "ORCL2.csv", "MSFT2.csv"]
dataArray = []
largest_y = 0
smallest_y = 0
setToggle = 1

def dbscan_thread(tempSet):
	print("yoo")
	# eNeighbourhood = 86400
	# minPts = 8
	# for j in tempSet:
	# 		if tempSet[j][3] == '':

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
#print(dataArray)

# k-means start 
#entroids = [[1375372800,smallest_y+8.02],[1438444800,largest_y-13.02],[1122912000,smallest_y+45.02],[1217606400,smallest_y+10.90]]

# Density based clustering start
distPairs = {}
dataArray = sorted(dataArray, key=itemgetter(0))

toggle = 0
tempSet = []
dateToggle = 0
for i in dataArray:
	if dateToggle == 6:
		tempSet.pop()
		# DBSCAN processing
		#while dbscanThread.isAlive() == false:
		print(tempSet)
		dbscanThread = threading.Thread(target=dbscan_thread, args=tempSet)
		dbscanThread.start()		
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
			firstTerm = i[0]
			tempSet.append(i)
			toggle = 1
			dateToggle += 1
