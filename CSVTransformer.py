import os
import sys
import csv
import math
import numpy as np

csvFilePath = sys.argv[1]
# 0 means no filter, 1 means mean average filter, 2 means median average filter
filterType = int(sys.argv[2])
csvFileName = csvFilePath.split('/')[-1]

# Open a csv file to write
currentFilePath = os.path.dirname(os.path.abspath(__file__))
csvFileOrigin = open(csvFilePath, 'r')
csvFileTemp = open(currentFilePath + '/T_' + csvFileName, 'w')
csvWriter = csv.writer(csvFileTemp)
timestampCnt = 0
jointCnt = 1
numCol = 55
numJoint = 18

for row in csv.reader(csvFileOrigin):
	
	# 1st row is timestamp
	if timestampCnt == 0:
		timestampCnt = 1
		data = []
		jointCnt = 0
		data = data + row
	else:
		# records 18 skeleton joint data
		jointCnt += 1
		
		# remove space in list
		# https://stackoverflow.com/questions/3232953/python-removing-spaces-from-list-objects
		removed = []
		
		# colCnt is to point out the y value
		colCnt = 0
		for i in row:
			real = i.replace(' ', '')
			colCnt += 1
			if colCnt == 2:
				
				# Reverse y axis
				real = abs(1 - float(real))
				#print(real)
			removed.append(real)
		data = data + removed
		if jointCnt > 17:
			timestampCnt = 0
			csvWriter.writerow(data)
csvFileOrigin.close()
csvFileTemp.close()

if filterType != 0:
	# filter parameter is 7
	filterParam = 7
	data = np.empty((0, numCol), float)
	csvFileTransform = open(currentFilePath + '/FT_' + csvFileName, 'w')
	csvWriter = csv.writer(csvFileTransform)
	with open(currentFilePath + '/T_' + csvFileName, 'r') as csvFileTemp:
		reader = csv.reader(csvFileTemp)
		for row in reader:
			data = np.vstack((data, row))
	new_data = np.copy(data)
	startIdx = int(math.floor(filterParam / 2.0))

	
	# moving filter processing
	# https://dsp.stackexchange.com/questions/27349/moving-average-vs-moving-median
	for rowIdx in range(startIdx, data.shape[0] - startIdx):	
		
		# for each joint
		for jointId in range(numJoint):
			colIdx = jointId*3 + 1
			colIdy = jointId*3 + 2
			
			if filterType == 1:
				# moving filter (average)
			
				filterSumX = 0.0
				filterSumY = 0.0
				for filterId in range(rowIdx - startIdx, rowIdx + startIdx + 1):
					filterSumX = filterSumX + float(data[filterId, colIdx])
					filterSumY = filterSumY + float(data[filterId, colIdy])
			
				new_data[rowIdx, colIdx] = (filterSumX / filterParam)
				new_data[rowIdx, colIdy] = (filterSumY / filterParam)
			
			if filterType == 2:
				# moving filter (median)
				filterListX = []
				filterListY = []
				for filterId in range(rowIdx - startIdx, rowIdx + startIdx + 1):
					filterListX.append(float(data[filterId, colIdx]))
					filterListY.append(float(data[filterId, colIdy]))
		
				#break
				# calculate the list length
			
				filterListX = sorted(filterListX)
				filterListY = sorted(filterListY)
				size = len(filterListX)
		
				# if even
				if size % 2 == 0:
					medianX = (filterListX[size//2]+filterListX[size//2-1]) / 2
					medianY = (filterListY[size//2]+filterListY[size//2-1]) / 2
				# if odd			
				if size % 2 == 1:
					medianX = filterListX[size//2-1]
					medianY = filterListY[size//2-1]
			
				new_data[rowIdx, colIdx] = medianX
				new_data[rowIdx, colIdy] = medianY
	
	for rowIdx in range(new_data.shape[0]):
		csvWriter.writerow(new_data[rowIdx, :])
	
	csvFileTransform.close()
	
	# Todo
	# interpolation modified
	# linear interpolation
	# indice : 1, 2, 4, 5, ......	  

# CoordinateTransformer: camera view to body view
csvFileTransformed = open(currentFilePath + '/T_' + csvFileName, 'r')
csvFileTemp = open(currentFilePath + '/P_T_' + csvFileName, 'w')
csvWriter = csv.writer(csvFileTemp)
# Transform camera coordinate system to body coordinate system
# Origin of our coordinate system is the point 1

for row in csv.reader(csvFileTransformed):
	origin_offsetX = 0.0
        origin_offsetY = 0.0

	# set point 1 to the origin point
	origin_offsetX = float(row[1*3+1])
	origin_offsetY = float(row[1*3+2])

	# Transform 18 skeleton joints
	for k in range(int(numJoint)):
		if float(row[k*3+1]) == 0 and float(row[k*3+2]) == 1:
			continue
		row[k*3+1] = float(row[k*3+1]) - origin_offsetX
		row[k*3+2] = float(row[k*3+2]) - origin_offsetY
	csvWriter.writerow(row)

csvFileTransformed.close()
csvFileTemp.close()

