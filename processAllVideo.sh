#!/bin/bash
declare -i i
declare -i number

date="$1"
dataset=${date}_"$2"_"$3"

#mkdir ~/Batting0321_Output/output_032100${index}_cut
mkdir ~/PaperSkelDatabase/Batting${date}_Output/
mkdir ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}

number="$(find ~/PaperSkelDatabase/Batting${date}/${dataset} -type f | wc -l)"
#echo "${number}"

for (( i=1; i <= number; i++ ))
do
	mkdir ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}
	cd ~/openpose
#	if [ $i -lt 10 ]
#	then
		#./build/examples/openpose/openpose.bin --video ~/PaperDatabase/Batting${date}/${dataset}/${dataset}_${i}.mp4 --write_video ~/PaperDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/${dataset}_${i}_result.avi --write_keypoint_json ~/PaperDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/ --no_display --keypoint_scale=3
		./build/examples/openpose/openpose.bin --video ~/PaperSkelDatabase/Batting${date}/${dataset}/${dataset}_${i}.mp4 --write_video ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/${dataset}_${i}_result.avi --write_keypoint_json ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}/ --no_display --keypoint_scale=3

		# JSON2CSV
		cd ~/mainCode
		python JSON2CSV.py ~/PaperSkelDatabase/Batting${date}_Output/output_${dataset}/${dataset}_${i}
		python CSVTransformer.py ${dataset}_${i}.csv 0

		# Now generate Transformed CSV file (transform from openpose data and then do first normalization, coordinate system transform)
		# T_xxxx_x.csv and P_T_xxxx_x.csv	
		# Process repeated frames
		python checkRepeatedFrame.py ~/PaperSkelDatabase/Batting${date}/${dataset}/${dataset}_${i}.mp4 T_${dataset}_${i}.csv
		python checkRepeatedFrame.py ~/PaperSkelDatabase/Batting${date}/${dataset}/${dataset}_${i}.mp4 P_T_${dataset}_${i}.csv
		

		
#	else		
#		./build/examples/openpose/openpose.bin --video ~/Batting1214/12110${i}.mp4 --write_video ~/Batting1211_Output/output_12110$i/12110${i}_result.avi --write_keypoint_json ~/Batting1214_Output/output_12110$i/ --no_display --keypoint_scale=3
#	fi
done
