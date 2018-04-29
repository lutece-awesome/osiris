#!/bin/bash

# script to judge

time_limit=$1
memory_limit=$2
output_limit=$3
stack_limit=$4
checker=$5
running_core=./core.bin
running_arguments=$6
data_dir=/opt
case_number=$7

for(( i = 1 ; i <= case_number ; ++ i))
do
	result=$(${running_core} ${time_limit} ${memory_limit} ${output_limit} ${stack_limit} "${data_dir}/${i}.in" user.out "${data_dir}/${i}.out" "${running_arguments}" "${checker}")
	status_code=$?
	printf '{"case":"%s","info":%s}\n' "$i" "$result"
	if [ $status_code -ne 0 ]; then
		exit -1
	fi
	echo "$result" | grep -q "Accepted"
	if [ $? -ne 0 ]; then
		exit 0
	fi
done