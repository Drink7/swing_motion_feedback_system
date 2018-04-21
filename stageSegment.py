import numpy as np
import sys
import os
import csv

def segmentation():
	inputFile = sys.argv[1] 
	#fileNum = sys.argv[2]
	frameStart = int(sys.argv[2])
	#impactTime = int(sys.argv[2])
	frameEnd = int(sys.argv[3])
	outputFile = sys.argv[4]
	#outputAfterFile = inputFile.split('.')[0] + "_A.csv"
	#outputBeforeFile = inputFile.split('.')[0] + "_B.csv"
	#outputFile = sys.argv[5]
	inputFP = open(inputFile, 'r')
	outputFP = open(outputFile, 'w')
	#outputFPA = open(outputAfterFile, 'w')
	#outputFPB = open(outputBeforeFile, 'w')
	csvWriter = csv.writer(outputFP)
	#csvWriterA = csv.writer(outputFPA)
	#csvWriterB = csv.writer(outputFPB)
	
	frameCnt = 0
	for row in csv.reader(inputFP):
		#frameCnt += 1
		#if frameCnt <= impactTime:
		#	csvWriterB.writerow(row)
		
		#if frameCnt > impactTime:
		#	csvWriterA.writerow(row)
			
		if frameCnt >= frameStart and frameCnt < frameEnd:
			csvWriter.writerow(row)
		frameCnt += 1
	
if __name__ == "__main__":
	segmentation() 

