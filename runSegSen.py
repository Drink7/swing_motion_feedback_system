import os
import sys
import csv
from subprocess import call

infoFile = open(sys.argv[1], 'r')
lineCnt = 0
date = infoFile.readline().strip()
who = infoFile.readline().strip()

# Ref: http://www.runoob.com/python/file-readlines.html
	# roundNum = 1, 2, 3 ......	
roundNum = infoFile.readline().strip()
while roundNum:

	# motionNum = 6 or 7 (or 8)
	motionNum = int(infoFile.readline().strip())
	for index in range(1, motionNum + 1):
		data = infoFile.readline().strip().split(' ')

		# run
		cmd = "python sensorFindMotion.py ~/PaperSenDatabase/Batting{}/{}_{}_{}.csv {} {} {} {} {}".format(str(date), str(date), str(who), str(roundNum), str(motionNum), str(data[0]), str(data[1]), str(data[2]), str(data[3]))
		print(cmd)
		call(cmd, shell=True)
	
	# roundNum = 1, 2, 3 ......	
	roundNum = infoFile.readline().strip()
	
infoFile.close()

