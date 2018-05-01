import numpy as np
from PIL import Image
from PIL import ImageChops
import cv2
from skimage.measure import compare_ssim  as ssim
import matplotlib.pyplot as plt
import sys
import csv

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)

	# setup the figure
	#fig = plt.figure(title)
	#plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

	# show first image
	#ax = fig.add_subplot(1, 2, 1)
	#plt.imshow(imageA, cmap = plt.cm.gray)
	#plt.axis("off")

	# show the second image
	#ax = fig.add_subplot(1, 2, 2)
	#plt.imshow(imageB, cmap = plt.cm.gray)
	#plt.axis("off")

	# show the images
	#plt.show()
	#if m < 10:
		#print("m:{}, s:{}".format(m, s))
	return m

# Extracting and Saving Video Frames
# https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
videoFile = sys.argv[1]
skelCSVFile = sys.argv[2]

# find the column number of csvfile
tmpCSVFile = open(skelCSVFile, 'r')
tmpCSVReader = csv.reader(tmpCSVFile)
numCol = len(next(tmpCSVReader))
tmpCSVFile.close()
jointNum = 18

# Read csv and save data
csvFileOrigin = open(skelCSVFile, 'r')
numRow = 0
data = np.empty((0, numCol), float)
reader = csv.reader(csvFileOrigin)
for row in reader:
	data = np.vstack((data, row))
	numRow += 1
csvFileOrigin.close()

# Write to the same file
csvFileProcessed = open(skelCSVFile, 'w')
csvFileFailData = open("FailData.txt", 'w')
csvWriter = csv.writer(csvFileProcessed)
csvFailWriter = csv.writer(csvFileFailData)

vidcap = cv2.VideoCapture(videoFile)
success,image = vidcap.read()
prev_img = image
count = 0
repeatedList = []
success = True
while success:
	success,image = vidcap.read()
	count += 1
	if success:

		# Handle repeated frames
		cur_img = image
		prev_img_gray = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)
		cur_img_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
		#print("Frame {} and frame {}".format(count-1, count))
		m = compare_images(prev_img_gray, cur_img_gray)
		
		# Frame count-1 and count repeat!
		# Modify the repeated frame, count-1
		# Threshold set to 18
		# Process repeated frames, interpolation
		if m < 18:
			#print("Count:{}".format(count))			
			repeatedList.append(count)
				
		else:
			repeatedNum = len(repeatedList)
			if repeatedNum != 0:	
				# repeateNum + 1 is the consequtive number
				# repeated frames number are 2 or 3, if repeated frames more than 3, discard!
				if repeatedNum + 1 == 2:

						# r-1 and r repeated
						r = int(repeatedList[0])

						# loop all joints
						for i in range(jointNum):
							data[r, i*3+1] = (float(data[r-1, i*3+1]) + float(data[r+1, i*3+1])) / 2.0
							data[r, i*3+2] = (float(data[r-1, i*3+2]) + float(data[r+1, i*3+2])) / 2.0
							#print((float(data[r-2, i*3+1]) + float(data[r, i*3+1])) / 2.0)
							#print((float(data[r-2, i*3+2]) + float(data[r, i*3+2])) / 2.0)
							
				elif repeatedNum +1 == 3:

						# r-1, r r+1 repeated
						# r remain!
						r = int(repeatedList[0])
						if r == 1:
							repeatedList=[]
							continue

						# process r = (r-1)*2 - (r-2)
						# loop all joints
						for i in range(jointNum):
							data[r, i*3+1] = (float(data[r-1, i*3+1]) * 2.0 - float(data[r-2, i*3+1])) 
							data[r, i*3+2] = (float(data[r-1, i*3+2]) * 2.0 - float(data[r-2, i*3+2])) 
						
						# process r+1
						# loop all joints
						for i in range(jointNum):
							data[r+1, i*3+1] = (float(data[r, i*3+1]) + float(data[r+2, i*3+1])) / 2.0
							data[r+1, i*3+2] = (float(data[r, i*3+2]) + float(data[r+2, i*3+2])) / 2.0
				
				else:
					print("Fail data, return")
					csvFailWriter.writerow(skelCSVFile)
					break
					
					
			repeatedList=[]
		
	prev_img = cur_img

# write result to file
for row in range(numRow):
	csvWriter.writerow(data[row])

print("Total:{}".format(count))
csvFileProcessed.close()
