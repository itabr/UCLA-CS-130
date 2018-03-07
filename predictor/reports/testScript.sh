#! /bin/bash
array=("math" "dp" "geometry" "implementation" "greedy" "search" "bitmasks" "combinatorics" "constructivealgorithms" "datastructures" "games"  "graph" "numbertheory" "probabilities"  "sortings" "strings" "twopointers")

rm -f res.txt
for element in ${array[@]}
do
	python ./testModelLog.py $element >> res.txt
	echo >> res.txt
	
done