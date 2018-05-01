import numpy as np
import sys
import os
import csv

def segmentation():
	inputFile = sys.argv[1] 
	#fileNum = sys.argv[2]
	#frameStart = int(sys.argv[2])

	# real world start from 1st frame, but in data need to shift offset by -1
	impactTime = int(sys.argv[2])
	#frameEnd = int(sys.argv[4])
	#outputFile = inputFile.split('.')[0] + "_" + fileNum + ".csv"
	outputAfterFile = (inputFile.split('/')[-1]).split('.')[0] + "_A.csv"
	outputBeforeFile = (inputFile.split('/')[-1]).split('.')[0] + "_B.csv"
	#outputFile = sys.argv[5]
	inputFP = open(inputFile, 'r')
	#outputFP = open(outputFile, 'w')
	
	if not os.path.exists("AfterImpact"):
		os.makedirs("AfterImpact")
	if not os.path.exists("BeforeImpact"):
		os.makedirs("BeforeImpact")

	outputFPA = open("AfterImpact/" + outputAfterFile, 'w')
	outputFPB = open("BeforeImpact/" + outputBeforeFile, 'w')
	#csvWriter = csv.writer(outputFP)
	csvWriterA = csv.writer(outputFPA)
	csvWriterB = csv.writer(outputFPB)
	
	frameCnt = 0
	for row in csv.reader(inputFP):
		#frameCnt += 1
		if frameCnt <= impactTime:
			csvWriterB.writerow(row)
		
		if frameCnt > impactTime:
			csvWriterA.writerow(row)
			
		#if frameCnt >= frameStart and frameCnt <= frameEnd:
		#	csvWriter.writerow(row)
		frameCnt += 1
	
if __name__ == "__main__":
	segmentation() 

