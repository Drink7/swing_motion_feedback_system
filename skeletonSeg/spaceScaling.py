from __future__ import print_function

import datetime
import numpy as np
import pylab as pl
from matplotlib import cm, pyplot as plt
from sklearn.externals import joblib
import csv
import sys
import os
import math
import pickle

# ignore deprecation warnings
#https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
###############################################################################
trainingDataFolder = sys.argv[1]
allFiles = os.listdir(trainingDataFolder)
allFiles.sort()
print(allFiles)

# training sample numbers
#print('Training sample numbers is {}.'.format(trainingSampleNum))
inputType = 2
#inputType = int(sys.argv[2])

# change directory
# save current path first
curPath = os.getcwd()
os.chdir(trainingDataFolder)

# data array structure setup
# http://tw.gitbook.net/python/file_next.html
numCol = 0
for CSVFile in allFiles:
	if CSVFile.endswith(".csv"):
		tmpCSVFile = open(CSVFile)
		tmpCSVReader = csv.reader(tmpCSVFile)
		numCol = len(next(tmpCSVReader))
		tmpCSVFile.close()	
		break

###############################################################################
#### Raw data from all CSV File
#### Read all skeleton joints or sensor data from all CSV
#### Only save 18 joints with XY value or save accX ~ GyroZ(6 values)
firstCSVFile = 0
numJoint = 18

X_TrainingList = []
lengths = []
# Traverse the training samples to build multi-sequence samples for HMM
for CSVFile in allFiles:

	# Initial structure for each sequence (CSV file)
	X_Sequence = []
	data = np.empty((0, numCol), float)
	if CSVFile.endswith(".csv"):
		numRow = 0
		with open(CSVFile, 'r') as csvfile:
		#with open('T_1214001_Bat4.csv', 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				data = np.vstack((data, row))
				numRow += 1
			 
		# Data type
		# 1 is wearable data
		# 2 is body skeleton data
		# https://stackoverflow.com/questions/28393103/typeerror-cannot-perform-reduce-with-flexible-type
		if inputType == 1: 
			# will give up the last timestep data (ex: 1785 -> 1784) 
			for i in range(numRow):
				accX = (data[:, 1].astype(np.float))
				accY = (data[:, 2].astype(np.float))
				accZ = (data[:, 3].astype(np.float))
				gyroX =(data[:, 4].astype(np.float))
				gyroY =(data[:, 5].astype(np.float))
				gyroZ =(data[:, 6].astype(np.float))
		
				# sequence stack
				X_Sequence.append([accX, accY, accZ, gyroX, gyroY, gyroZ])
				#X_Sequence = np.column_stack([accX, accY, accZ, gyroX, gyroY, gyroZ])

		elif inputType == 2:
			for i in range(numRow):
				x0 = data[i, 1].astype(np.float)
				x1 = data[i, 4].astype(np.float)
				x2 = data[i, 7].astype(np.float)
				x3 = data[i, 10].astype(np.float)
				x4 = data[i, 13].astype(np.float)
				x5 = data[i, 16].astype(np.float)
				x6 = data[i, 19].astype(np.float)
				x7 = data[i, 22].astype(np.float)
				x8 = data[i, 25].astype(np.float)
				x9 = data[i, 28].astype(np.float)
				x10 = data[i, 31].astype(np.float)
				x11 = data[i, 34].astype(np.float)
				x12 = data[i, 37].astype(np.float)
				x13 = data[i, 40].astype(np.float)
				x14 = data[i, 43].astype(np.float)
				x15 = data[i, 46 ].astype(np.float)
				x16 = data[i, 49].astype(np.float)
				x17 = data[i, 52].astype(np.float)
		
				y0 = data[i, 2].astype(np.float)
				y1 = data[i, 5].astype(np.float)
				y2 = data[i, 8].astype(np.float)
				y3 = data[i, 11].astype(np.float)
				y4 = data[i, 14].astype(np.float)
				y5 = data[i, 17].astype(np.float)
				y6 = data[i, 20].astype(np.float)
				y7 = data[i, 23].astype(np.float)
				y8 = data[i, 26].astype(np.float)
				y9 = data[i, 29].astype(np.float)
				y10 = data[i, 32].astype(np.float)
				y11 = data[i, 35].astype(np.float)
				y12 = data[i, 38].astype(np.float)
				y13 = data[i, 41].astype(np.float)
				y14 = data[i, 44].astype(np.float)
				y15 = data[i, 47].astype(np.float)
				y16 = data[i, 50].astype(np.float)
				y17 = data[i, 53].astype(np.float)

				# sequence stack
				X_Sequence.append([x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, x11, y11, x12, y12, x13, y13, x14, y14, x15, y15, x16, y16, x17, y17])
			#X_Sequence = np.column_stack([x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, x11, y11, x12, y12, x13, y13, x14, y14, x15, y15, x16, y16, x17, y17])
		'''
		if firstCSVFile == 0:
			X_TrainingList.append(X_Sequence)
			lengths = [len(X_Sequence)]
			firstCSVFile = 1
		else:
		'''
			#X_TrainingList = np.concatenate([X_TrainingList, X_Sequence])
		X_TrainingList.append(X_Sequence)
		lengths.append(len(X_Sequence))

###############################################################################
# PreprocessData(For skeleton data)
# Time-space scaling, First do time scaling

# Space Scaling, propotional scaling, using shoulder width
# Use first 1 ~ 2 frames of every segmented video to do space scaling
# Use joint1 and joint 8 as scaling metric
# Record every 1 ~ 2 frames from each sample video
joint18DistanceList = []

# shape function can only use in np.array
X_TrainingListNum = np.array(X_TrainingList).shape[0]

# Before scaling
#print(X_TrainingList[0][0][0])

# Find maximum value of all scaling distance
for sampleId in range(X_TrainingListNum):
	
	# calculate joint1 and joint8 distance of frame 0
	joint1_X = X_TrainingList[sampleId][0][2]
	joint1_Y = X_TrainingList[sampleId][0][3]
	joint8_X = X_TrainingList[sampleId][0][16]
	joint8_Y = X_TrainingList[sampleId][0][17]

	dist = math.sqrt((joint8_X - joint1_X)**2 + (joint8_Y - joint1_Y)**2)
	joint18DistanceList.append(dist)

# maximum of scale list
# Make all sample height and width consistent 
scalingMax = max(joint18DistanceList)

# scale all samples' frames
for sampleId in range(X_TrainingListNum):

	# calculate joint1 and joint8 distance of frame 0
	joint1_X = X_TrainingList[sampleId][0][2]
	joint1_Y = X_TrainingList[sampleId][0][3]
	joint8_X = X_TrainingList[sampleId][0][16]
	joint8_Y = X_TrainingList[sampleId][0][17]

	dist = math.sqrt((joint8_X - joint1_X)**2 + (joint8_Y - joint1_Y)**2)
	scalingProp = scalingMax / dist
	#print(scalingProp)	
	# Has known the scaling propotional value, now modify all the frames of this sample with scaling propotional value
	# Propotional increase or decrease
	sampleLen = lengths[sampleId]
	for i in range(sampleLen):
		for j in range(numJoint):

			# X value scaling
			X_TrainingList[sampleId][i][j*2] = X_TrainingList[sampleId][i][j*2] * scalingProp
			
			# Y value scaling
			X_TrainingList[sampleId][i][j*2+1] = X_TrainingList[sampleId][i][j*2+1] * scalingProp
		
		
#	videoStartId = videoStartId + sampleNum

# After scaling
#print(X_TrainingList[0][0][0])

# Save data
sampleId = 0
for CSVFile in allFiles:
	if CSVFile.endswith(".csv"):
		numRow = 0
		tmpData = np.empty((0, numCol), float)
		with open(CSVFile, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				tmpData = np.vstack((tmpData, row))
				numRow += 1
		#print(tmpData.shape)

		# space scaling value revised version
		# write revised space scaling value to csv file
		if not os.path.exists(curPath + "/Scaled"):
			os.makedirs(curPath + "/Scaled")
		with open(curPath + "/Scaled/S_" + CSVFile, 'w') as csvfile:
			csvWriter = csv.writer(csvfile)
			for nRow in range(tmpData.shape[0]):
				for nJoint in range(numJoint):
					
					# Store revised X 
					tmpData[nRow][nJoint*3+1] = X_TrainingList[sampleId][nRow][nJoint*2]
					
					# Store revised Y
					tmpData[nRow][nJoint*3+2] = X_TrainingList[sampleId][nRow][nJoint*2+1]
				csvWriter.writerow(tmpData[nRow])
		sampleId += 1
