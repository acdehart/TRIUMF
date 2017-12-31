#!/bin/bash

# File: report.sh
# Author: A.C. DeHart
# Comment: This file is placed on the R-Pi unit that makes resistance measurements of the thermistors in the lab and on the ULE vacuum chamber. Once every sixty seconds, it finds the newest temperature data file and prints the last line of data. This can also be used to verify that the R-Pi is actively taking data as this script also reports the time stamp of the last data taken.

cd 
cd temperature_data/
while true; do
fn=$(ls -t | head -n1)
line=$(grep "." "$fn" | tail -1)
arr=( $line )

#echo $line
#echo ${arr[2]}
#echo ${#arr[@]}
#eval array=( $line )
#echo $ {array[2]}
#array = ( $line )
#echo ${array[1]}

printf "ULE: %sC, Room: %sC --- %s %s\n" "${arr[3]}" "${arr[4]}" "${arr[0]}" "${arr[1]}"

sleep 60
done

#2017-6-21 13:38:57 1498077537 25.7104 20.5338 24.9118 inf inf inf inf inf

