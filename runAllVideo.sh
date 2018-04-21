#!/bin/bash
declare -i i
declare -i number=3

date=0413
dataset=${date}_14_3

#mkdir ~/Batting0321_Output/output_032100${index}_cut
mkdir ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}

for (( i=1; i <= number; i++ ))
do
	mkdir ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}
	cd openpose
#	if [ $i -lt 10 ]
#	then
		#./build/examples/openpose/openpose.bin --video ~/PaperDatabase/Batting${date}/${dataset}/${dataset}_${i}.mp4 --write_video ~/PaperDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/${dataset}_${i}_result.avi --write_keypoint_json ~/PaperDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/ --no_display --keypoint_scale=3
		./build/examples/openpose/openpose.bin --video ~/PaperSkelDatabase/Batting${date}/${dataset}/${dataset}_${i}.mp4 --write_video ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/${dataset}_${i}_result.avi --write_keypoint_json ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/ --no_display 

		# JSON2CSV
		cd ~/
		python JSON2CSV.py ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}
		python CSVTransformer.py ${dataset}_${i}.csv 0
#	else		
#		./build/examples/openpose/openpose.bin --video ~/Batting1214/12110${i}.mp4 --write_video ~/Batting1211_Output/output_12110$i/12110${i}_result.avi --write_keypoint_json ~/Batting1214_Output/output_12110$i/ --no_display --keypoint_scale=3
#	fi
done
