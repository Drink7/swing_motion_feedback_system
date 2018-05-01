import os
import sys
import csv
from subprocess import call

date = sys.argv[1]
#skelScalingFolder = sys.argv[2]
#senBeforeImpactFolder = sys.argv[3]

# example 
# senBeforeImpactFolder : ~/HMMModelTrace/TrainSamples/PaperData/sensor_BeforeImpact/0416
# skelScalingFolder : ~/PaperSkelDatabase/Batting0416_SkelCSV/CoordinatePreprocess
senBeforeImpactFolder = "/home/drink7/HMMModelTrace/TrainSamples/PaperData/sensor_BeforeImpact/" + date
skelScalingFolder = "/home/drink7/PaperSkelDatabase/Batting" + date + "_SkelCSV/CoordinatePreprocess"
cmd = "python spaceScaling.py {}".format(skelScalingFolder)
call(cmd, shell=True)

# scaled data are in "Scaled" folder
# whole data are in "Scaled" folder
if not os.path.exists("AfterImpact"):
	os.makedirs("AfterImpact")
if not os.path.exists("BeforeImpact"):
	os.makedirs("BeforeImpact")

# change directory
# save current path first
curPath = os.getcwd()
os.chdir(senBeforeImpactFolder)
allFiles = os.listdir(senBeforeImpactFolder)
allFiles.sort()
numRow = 0

# go through all sensor csv file
for CSVFile in allFiles:
	if CSVFile.endswith(".csv"):	
		csvFileOrigin = open(CSVFile, 'r')
		numRow = 0
		with open(CSVFile, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				numRow += 1
		# Ex : filename = 0416_56_5_B_5.csv
		# split with .
		fileName = CSVFile.split('.')[0]
		# split with _
	
		date = fileName.split('_')[0]
		who = fileName.split('_')[1]
		roundNum = fileName.split('_')[2]
		motionNum = fileName.split('_')[4]
		
		# numRow means the number before impact

		os.chdir(curPath)

		cmd = "python movieSegmentImpact.py Scaled/S_P_T_{}_{}_{}_{}.csv {}".format(date, who, roundNum, motionNum, str(numRow))
		call(cmd, shell=True)
		print(cmd)

		os.chdir(senBeforeImpactFolder)

