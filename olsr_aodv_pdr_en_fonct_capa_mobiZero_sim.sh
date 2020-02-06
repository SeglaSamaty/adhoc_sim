#!/bin/bash
# 
simulation () {
 	#if [ "$#" -ne 2 ]; then
 	echo "ntrvl(sec) #Pckts" > $3
 	for debit in `seq 0.1 0.05 4`; do
 		resultat=0
 		tmp=0 
		tmp=`./waf --run "scratch/$1 --seed=7497 --run=707 --protocol=$2 --debit=$debit" 2>&1 |grep "server received"|wc -l`
		resultat=$(($tmp+$resultat))
		echo $tmp
		tmp=`./waf --run "scratch/$1 --seed=4497 --run=1617 --protocol=$2 --debit=$debit" 2>&1 |grep "received"|wc -l`
		resultat=$(($tmp+$resultat))
		echo $tmp
		tmp=`./waf --run "scratch/$1 --seed=4467 --run=147 --protocol=$2 --debit=$debit" 2>&1 |grep "received"|wc -l`
		resultat=$(($tmp+$resultat))
		echo $tmp
		tmp=`./waf --run "scratch/$1 --seed=4467 --run=97 --protocol=$2 --debit=$debit" 2>&1 |grep "received"|wc -l`
		resultat=$(($tmp+$resultat))
		echo $tmp
		tmp=`./waf --run "scratch/$1 --seed=1678 --run=868 --protocol=$2 --debit=$debit" 2>&1 |grep "received"|wc -l`
		resultat=$(($tmp+$resultat))
		echo $tmp
		#tmp=`./waf --run "scratch/$1 --protocol=$2 --interval=$interv " 2>&1 |grep "received"|wc -l`
	
		
		resultat=$(($resultat/5))
		echo "res: $resultat"
		echo "$debit   $resultat" >> $3 
	done
    #fi
 }


echo "---OLSR---"
simulation adhocRouting-2019 1 output.2a.OLSR.txt
echo "---AODV---"
simulation adhocRouting-2019 2 output.2a.AODV.txt

