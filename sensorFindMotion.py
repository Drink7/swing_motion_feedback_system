import os
import sys
import csv
import math
import numpy as np
from datetime import datetime
from datetime import timedelta

# This sensor segmentation only for experienced players
# Impact Time will happen when the gyro x value turn to negative value
# So we can also use variation of gyro x
csvFilePath = sys.argv[1]
localMinNum = int(sys.argv[2])
motionNum = int(sys.argv[3]) - 1
videoStartTime = sys.argv[4]
videoImpactTime = sys.argv[5]
videoEndTime = sys.argv[6]

# Open the csvFile (Raw csv)
currentFilePath = os.path.dirname(os.path.abspath(__file__))
csvFileOrigin = open(csvFilePath, 'r')

# find the column number of csvfile
tmpCSVFile = open(csvFilePath, 'r')
tmpCSVReader = csv.reader(tmpCSVFile)
numCol = len(next(tmpCSVReader))
tmpCSVFile.close()
jointNum = 18

# Read csv and save data
# record the row number of csvfile
numRow = 0
data = np.empty((0, numCol), float)
reader = csv.reader(csvFileOrigin)
for row in reader:
	data = np.vstack((data, row))
	numRow += 1

csvFileOrigin.close()

# sensor data
accX = (data[:, 1].astype(np.float))
accY = (data[:, 2].astype(np.float))
accZ = (data[:, 3].astype(np.float))
gyroX = (data[:, 4].astype(np.float))
gyroY = (data[:, 5].astype(np.float))
gyroZ = (data[:, 6].astype(np.float))

# impact point index list
impactList=[]

# motion index list
motionIdList = []
	
def sensorSegMotion():
	# Sensor start, impact, end time
	v_startTime = videoStartTime.split(':')
	v_startHour = int(v_startTime[0])
	v_startMin = int(v_startTime[1])
	v_startSec = int(v_startTime[2])
	v_startMicroSec = int(v_startTime[3]) * 1000

	v_impactTime = videoImpactTime.split(':')
	v_impactHour = int(v_impactTime[0])
	v_impactMin = int(v_impactTime[1])
	v_impactSec = int(v_impactTime[2])
	v_impactMicroSec = int(v_impactTime[3]) * 1000

	v_endTime = videoEndTime.split(':')
	v_endHour = int(v_endTime[0])
	v_endMin = int(v_endTime[1])
	v_endSec = int(v_endTime[2])
	v_endMicroSec = int(v_endTime[3]) * 1000
	
	# construct a for loop to find the impact time
	# Find the offset of video impact and the sensor impact point 	
	s_impactTime = data[impactList[motionNum]][0].split(':')
	s_impactHour = int(s_impactTime[0])
	s_impactMin = int(s_impactTime[1])
	s_impactSec = int(s_impactTime[2])
	s_impactMicroSec = int(s_impactTime[3])

	################################################################################################################	
	# There is no 999990 value in sensor data
	# Offset count
	# Use math.ceil or round
	tmpDiv = int(round(float(v_impactMicroSec) / 33333.0))
		
	if tmpDiv > 29:
		v_impactMilliSec = 0
		v_impactSec += 1
		if v_impactSec > 59:
			v_impactSec = 0
			v_impactMin += 1
			if v_impactMin > 59:
				v_impactMin = 0
				v_impactHour += 1
	else:
	
		v_impactMicroSec = 33333 * tmpDiv
	
	# https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings/3097001#3097001	
	# https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
	# https://docs.python.org/2/library/datetime.html#timedelta-objects
	# When used with the strptime() method, the %f directive accepts from one to six digits and zero pads on the right. !!!
	if v_impactMicroSec < 133332:	
		v_impactTime = str(v_impactHour) + ':' + str(v_impactMin) + ':'+str(v_impactSec) + ':0' + str(v_impactMicroSec)
	else:
		v_impactTime = str(v_impactHour) + ':' + str(v_impactMin) + ':'+str(v_impactSec) + ':' + str(v_impactMicroSec)
	if s_impactMicroSec < 133332:
		s_impactTime = str(s_impactHour) + ':' + str(s_impactMin) + ':'+str(s_impactSec) + ':0' + str(s_impactMicroSec)
	else:
		s_impactTime = str(s_impactHour) + ':' + str(s_impactMin) + ':'+str(s_impactSec) + ':' + str(s_impactMicroSec)
	
	timeFormat="%H:%M:%S:%f"
	tdelta = datetime.strptime(s_impactTime, timeFormat)-datetime.strptime(v_impactTime, timeFormat)
	#tdelta = datetime.strptime(v_impactTime, timeFormat)-datetime.strptime(s_impactTime, timeFormat)
	if tdelta.days < 0:
		tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)	
	print(tdelta)
	# Now delta is the time interval between sensor impact time and video impact time
	shiftOffset = int(tdelta.seconds) * 30 + int(tdelta.microseconds) / 33333
	print("Shift Offset:{}".format(shiftOffset))
	
	################################################################################################################	
	# Find Start index
	tmpDiv = int(round(float(v_startMicroSec) / 33333.0))
	if tmpDiv > 29:
		v_startMilliSec = 0
		v_startSec += 1
		if v_startSec > 59:
			v_startSec = 0
			v_startMin += 1
			if v_startMin > 59:
				v_startMin = 0
				v_startHour += 1
	else:
		v_startMicroSec = 33333 * tmpDiv
	
	# Handle strptime() method 
	if v_startMicroSec < 133332:	
		v_startTime = str(v_startHour) + ':' + str(v_startMin) + ':' + str(v_startSec) + ':0' + str(v_startMicroSec)
	else:	
		v_startTime = str(v_startHour) + ':' + str(v_startMin) + ':' + str(v_startSec) + ':' + str(v_startMicroSec)

	# Add shift offset!
	# Bug 0421 : origin code will show '14:58:59:033323'
	# Need to handle 999990
	# some modification of handling 999990 + 33333 ... situation
	s_startTime = (datetime.strptime(v_startTime, timeFormat) + tdelta).strftime("%H:%M:%S:%f")
	s_startTimeSplit = s_startTime.split(':')
	if int(s_startTimeSplit[-1]) % 33333 != 0:
		s_startTimeSplit[-1] = int(math.ceil(float(s_startTimeSplit[-1]) / 33333.0) * 33333)
	if int(s_startTimeSplit[3]) == 999990:
		s_startTimeSplit[3] = 0
		s_startTimeSplit[2] = int(s_startTimeSplit[2]) + 1
                if int(s_startTimeSplit[2]) > 59:
                        s_startTimeSplit[2] = 0
                        s_startTimeSplit[1] = int(s_startTimeSplit[1]) + 1
                        if int(s_startTimeSplit[1]) > 59:
                        	s_startTimeSplit[1] = 0
                        	s_startTimeSplit[0] = int(s_startTimeSplit[0]) + 1
	
	# Get start index in sensor data
	for i in range(numRow):
		
		# check where the expected sensor data map the actual sensor data
		# hour, min, sec and microsecond are the same
		realData = data[i, 0].split(':')
		if int(realData[0]) == int(s_startTimeSplit[0]) and int(realData[1]) == int(s_startTimeSplit[1]) and int(realData[2]) == int(s_startTimeSplit[2]) and int(realData[3]) == int(s_startTimeSplit[3]):
			motionIdList.append(i)
			break
	
	# Add impact index to motion index list
	motionIdList.append(impactList[motionNum])
		
	################################################################################################################	
	# Find End index
	tmpDiv = int(round(float(v_endMicroSec) / 33333.0))
	
	if tmpDiv > 29:
		v_endMicroSec = 0
		v_endSec += 1
		if v_endSec > 59:
			v_endSec = 0
			v_endMin += 1
			if v_endMin > 59:
				v_endMin = 0
				v_endHour += 1
	else:
	
		v_endMicroSec = int(33333 * tmpDiv)

	# Handle strptime() method 
	if v_endMicroSec < 133332:	
	        v_endTime = str(v_endHour) + ':' + str(v_endMin) + ':' + str(v_endSec) + ':0' + str(v_endMicroSec)
        else:
	        v_endTime = str(v_endHour) + ':' + str(v_endMin) + ':' + str(v_endSec) + ':' + str(v_endMicroSec)
	
	#print('v_endTime:{}'.format(v_endTime))
	# Add shift offset!
        s_endTime = (datetime.strptime(v_endTime, timeFormat) + tdelta).strftime("%H:%M:%S:%f")
	s_endTimeSplit = s_endTime.split(':')
	if int(s_endTimeSplit[-1]) % 33333 != 0:
                s_endTimeSplit[-1] = int(math.ceil(float(s_endTimeSplit[-1]) / 33333.0) * 33333)

	if int(s_endTimeSplit[3]) == 999990:
		s_endTimeSplit[3] = 0
		s_endTimeSplit[2] = int(s_endTimeSplit[2]) + 1
		if int(s_endTimeSplit[2]) > 59:
			s_endTimeSplit[2] = 0
			s_endTimeSplit[1] = int(s_endTimeSplit[1]) + 1
			if int(s_endTimeSplit[1]) > 59:
				s_endTimeSplit[1] = 0
				s_endTimeSplit[0] = int(s_endTimeSplit[0]) + 1

	# Get end index in sensor data
        for i in range(numRow):

		# check where the expected sensor data map the actual sensor data
		# hour, min, sec and microsecond are the same
		realData = data[i, 0].split(':')
		if int(realData[0]) == int(s_endTimeSplit[0]) and int(realData[1]) == int(s_endTimeSplit[1]) and int(realData[2]) == int(s_endTimeSplit[2]) and int(realData[3]) == int(s_endTimeSplit[3]):
			motionIdList.append(i)
			break		  
	print(v_startTime)
	print(v_impactTime)
	print(v_endTime)
	print(s_startTime)
	print(s_impactTime)
	print(s_endTime)
	
	print('Motion ID :{}'.format(motionIdList))
	print('Motion ID (start from 1):{}'.format([x+1 for x in(motionIdList)]))
	return motionIdList
	
def sensorFindImpact():

	# First find gyroX max, then find the (accX)^2 + (gyroX) maximum value in near 30 frames
	sorted_gyroX = sorted(gyroX)
	sorted_gyroX_ID = sorted(range(len(gyroX)), key=lambda k: gyroX[k], reverse=True)

	# Impact metric IM = (accX)^2 + (gyroX)^2

	impactTimeList=[]
	localMinCnt = 0
	for ID in sorted_gyroX_ID:

		# Impact point: gyroX is local maximum, accX is local minimum(<0)
		if gyroX[ID] > 0 and accX[ID] < 0:
			#print('---'+str(gyroX[ID])+'---')
			IM = (accX[ID]**2) + (gyroX[ID]**2)
			isIM = 1
	
			# Check the local minimum of accX and local maximum of gyroX before and after 15 frames 
			for i in range(ID-15, ID+15):
				if gyroX[i] > 0 and accX[i] < 0:
					tmp = (accX[i]**2) + (gyroX[i]**2)
					if tmp > IM:
						isIM = 0
						break

			# if the local minimum and local maximum is right, then record it
			if isIM == 1:
				
				# Find the actual impact id
				# The actual impact time happens just before the gyroX value turns to negative value
				for IDOffset in range(1, 5):
					if gyroX[ID + IDOffset] < 0:
						ID = ID + (IDOffset-1)
						break
				impactTimeList.append(ID)
				localMinCnt += 1
				if localMinCnt >= localMinNum:
					break
	
	# Save to global impact list
	global impactList
	impactList = sorted(impactTimeList)
	#print('Index start from 0: {}'.format(sorted(impactTimeList)))
	#print('Index start from 1: {}'.format([x+1 for x in sorted(impactTimeList)]))
	#print('Index start from 0: {}'.format(impactList[motionNum]))
	#print('Index start from 1: {}'.format(impactList[motionNum]+1))

def sensorSegAndSave(frameStart, frameImpact, frameEnd):

	frameStart = int(frameStart)
	frameImpact = int(frameImpact)
	frameEnd = int(frameEnd)
	# motionNum start from 0
	outputFile = (csvFilePath.split('/')[-1]).split('.')[0] + "_" + str(motionNum+1) + ".csv"
	outputAfterFile = (csvFilePath.split('/')[-1]).split('.')[0] + "_A_" + str(motionNum+1) + ".csv"
	outputBeforeFile = (csvFilePath.split('/')[-1]).split('.')[0] + "_B_" + str(motionNum+1) + ".csv"

	inputFP = open(csvFilePath, 'r')
	outputFP = open(outputFile, 'w')
	outputFPA = open(outputAfterFile, 'w')
	outputFPB = open(outputBeforeFile, 'w')
	csvWriter = csv.writer(outputFP)
	csvWriterA = csv.writer(outputFPA)
	csvWriterB = csv.writer(outputFPB)
	
	# Start segment data and save
	frameCnt = 0
	for row in csv.reader(inputFP):
		if frameCnt >= frameStart and frameCnt <= frameImpact:
			csvWriterB.writerow(row)
	
		if frameCnt > frameImpact and frameCnt <= frameEnd:
			csvWriterA.writerow(row)
		
		if frameCnt >= frameStart and frameCnt <= frameEnd:
			csvWriter.writerow(row)
		frameCnt += 1


	print("Finish segmentation!")

if __name__ == "__main__":
	sensorFindImpact()
	motionIdList = sensorSegMotion()
	sensorSegAndSave(motionIdList[0], motionIdList[1], motionIdList[2])
