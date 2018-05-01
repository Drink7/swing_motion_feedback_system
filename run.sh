#!/bin/bash
declare -i i
#declare -i number=36

#date="$1"
#who="$2"
#number="$3"

for (( i=1; i<=$3; i++ ))
do
	bash processAllVideo.sh $1 $2 ${i}
done

