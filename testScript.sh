#! /bin/bash
array=("math" "dp" "geometry" "implementation" "flows" "greedy" "2-sat" "binarysearch" "bitmasks" "bruteforce" "chineseremaindertheorem" "combinatorics" "constructivealgorithms" "datastructures" "dfsandsimilar" "divideandconquer" "expressionparsing" "fft" "games" "graphmatchings" "graphs" "hashing" "matrices" "meet-in-the-middle" "numbertheory" "probabilities" "schedules" "shortestpaths" "sortings" "strings" "stringsuffixstructures" "ternarysearch" "trees" "twopointers")

rm -f res.txt
for element in ${array[@]}
do
	python ./testModelLog.py $element >> res.txt
	echo >> res.txt
	
done