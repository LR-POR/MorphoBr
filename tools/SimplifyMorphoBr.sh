#! /bin/bash 

for i in $*
do 
NAME=$(echo "$i" | awk 'BEGIN {FS= "."} { print $1}')
SimplifyEntries.py "$i" > "$NAME".edt.txt
done 
