import os
import sys
import json
import csv
import math

skeletonFolderPath = sys.argv[1]
#csvFileName = sys.argv[2]

allFiles = os.listdir(skeletonFolderPath)
allFiles.sort()
csvFileName = ''
if len(allFiles[0].split('_')) > 3:
	for i in range(len(allFiles[0].split('_'))-2):
		if i == 0:
			csvFileName = allFiles[0].split('_')[i]
		else:
			csvFileName = csvFileName + '_' + allFiles[0].split('_')[i]
else:
	csvFileName = allFiles[0].split('_')[0]

# Open a csv file to write
currentFilePath = os.path.dirname(os.path.abspath(__file__))
csvFile = open(currentFilePath + '/' + csvFileName + '.csv', 'w')

# change directory
os.chdir(skeletonFolderPath)

# 17 pairs
skeletonPairs = [[1, 8], [1, 11], [8, 9], [9, 10], [11, 12], [12, 13], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 0], [0, 14], [14, 16], [0, 15], [15, 17]]

frameCnt = 0
for jsonFileID in range(0, len(allFiles) - 1):
	if jsonFileID < 10:
		#skeletonFileName = allFiles[0].split('_')[0] + '_' +  '00000000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
		skeletonFileName = csvFileName+ '_' +  '00000000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
	elif jsonFileID < 100:	
		#skeletonFileName = allFiles[0].split('_')[0] + '_' +  '0000000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
		skeletonFileName = csvFileName + '_' +  '0000000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
	elif jsonFileID < 1000:
		#skeletonFileName = allFiles[0].split('_')[0] + '_' +  '000000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
		skeletonFileName = csvFileName+ '_' +  '000000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
	elif jsonFileID < 10000:
		#skeletonFileName = allFiles[0].split('_')[0] + '_' +  '00000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
		skeletonFileName = csvFileName+ '_' +  '00000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
	elif jsonFileID < 100000:
		#skeletonFileName = allFiles[0].split('_')[0] + '_' +  '0000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
		skeletonFileName = csvFileName+ '_' +  '0000000' + str(jsonFileID) + '_' + allFiles[0].split('_')[-1]
	print("File name : " +skeletonFileName)
	frameCnt += 1
	skeletonParsed = json.load(open(skeletonFileName))
	peopleData = skeletonParsed['people']

	# Create csv writer object
	csvWriter = csv.writer(csvFile)
	count = 0
	skeletonJointNumber = 18

	# Record which pair need to be compare
	comparePairID = 0

	# Comparison for these players
	filterThreshold = -9.99
	filterYValueThreshold = 0

	# Which player ID is right and need to be recorded
	rightPlayerID = 0
	#csvFile.write("%d\n" % jsonFileID)
	
	# filtering correct detection
	# Check threshold
	# First check pairs exist in these player
	# filter out null or false detection (5 skeleton joints is 0)
	# print(peopleData[0])
	peopleNum = len(peopleData)
	if peopleNum > 1:
		for index, pair in enumerate(skeletonPairs):
			
			# if players all has this pair, then we will use this pair to find which player is needed to be recorded
			# so pairConfirmFlag is used to count how many players have this pair, if == peopleNum, that means this pair can be used. If not, continue finding
			pairConfirmFlag = 0
			for player in peopleData:
				header = player.keys()
						
				# Ref:https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python
				poseDataID = header.index("pose_keypoints")
	
				# check player valid or not (filter out if 5 skeleton joints are (0, 0)
				zeroCount = 0
				
				# check all joints in this player
				for jointID in range(0, skeletonJointNumber):
					if player.values()[poseDataID][jointID*3] == 0 and player.values()[poseDataID][jointID*3 + 1] == 0:
						zeroCount = zeroCount + 1

				if zeroCount > 6:
					peopleNum = peopleNum - 1
					continue
				
				if player.values()[poseDataID][pair[0]*3] != 0 and player.values()[poseDataID][pair[1]*3] != 0:
					#print(player.values()[poseDataID][pair[0]*3])
					#print(player.values()[poseDataID][pair[1]*3])
					pairConfirmFlag = pairConfirmFlag + 1
			
			# record which pair we are to comapre
			if pairConfirmFlag == peopleNum:
				#print(comparePairID)
				comparePairID = index
				break

		
		#print(comparePairID)
		# When find the pair we can compare, find the correct player to record
		for index, player in enumerate(peopleData):
			header = player.keys()
			poseDataID = header.index("pose_keypoints")
			
			# Also need to check player is valid or not			
			zeroCount = 0
			# check all joints in this player
			for jointID in range(0, skeletonJointNumber):
				if player.values()[poseDataID][jointID*3] == 0 and player.values()[poseDataID][jointID*3 + 1] == 0:
					zeroCount = zeroCount + 1
			
			if zeroCount > 6:
				continue

			# Find max value of pair, that is our expected player values
			x1 = player.values()[poseDataID][(skeletonPairs[comparePairID][0])*3]
			y1 = player.values()[poseDataID][(skeletonPairs[comparePairID][0])*3 + 1] 
			x2 = player.values()[poseDataID][(skeletonPairs[comparePairID][1])*3]
			y2 = player.values()[poseDataID][(skeletonPairs[comparePairID][1])*3 + 1]
		
			# MaxYValue means the y value of eye (Left index 46, right index 43) and y value of ankle (Left index 40, right index 31) in this player
			# MaxYValue means his height
			if player.values()[poseDataID][43] != 0 and player.values()[poseDataID][31] != 0:
				maxYValue = abs(player.values()[poseDataID][43] - player.values()[poseDataID][31])
			elif player.values()[poseDataID][46] != 0 and player.values()[poseDataID][40] != 0:
				maxYValue = abs(player.values()[poseDataID][46] - player.values()[poseDataID][40])
			else:
				maxYValue = 1
			pairDistance = abs((x1 - x2)**2 + (y1 - y2)**2)
			#print(player.values()[poseDataID][0])
			#print(skeletonPairs[comparePairID][1]*3)
			if maxYValue != 1:
				if filterThreshold < pairDistance and filterYValueThreshold < maxYValue:
					rightPlayerID = index
					filterThreshold = pairDistance
					filterYValueThreshold = maxYValue
			else:
				if filterThreshold < pairDistance:
                                        rightPlayerID = index
                                        filterThreshold = pairDistance		
	# Have found the maximum pair distance, which means our recorded player ID is found
	if not peopleData:
		continue
	header = peopleData[rightPlayerID].keys()
	poseDataID = header.index("pose_keypoints")
	#print(rightPlayerID)
	if poseDataID:
		csvFile.write("%d\n" % jsonFileID)
		#print player.values()[poseDataID][0]
		for jointID in range(0, skeletonJointNumber):
			csvFile.write("%s, %s, %s\n" % (str(peopleData[rightPlayerID].values()[poseDataID][jointID*3]), str(peopleData[rightPlayerID].values()[poseDataID][jointID*3 + 1]), str(peopleData[rightPlayerID].values()[poseDataID][jointID*3 + 2])))
	

		
csvFile.close()
print("Frame count:{}".format(frameCnt))
