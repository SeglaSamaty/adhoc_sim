#!/bin/bash
simulation () {
 	echo "ntrvl(sec) #Pckts  #PcktsOvHd" > $3

	exec 3<> tmp.txt
	./waf --run "scratch/$1 --protocol=$2 --nodeSpeed=0.1" 2>&3
	exec 3>&-

	tmp=0
	resultat=0

	for i in `seq 10 1 20`; do 
		tmp=`cat tmp.txt| grep -c "server received 1500 bytes from 10.1.1.$i"`
		resultat=$(( resultat+tmp ))
		tmp=0
	done

	if [ $2 -eq 1 ]
		then
		tmp=`cat trace-ifi-ns32b.tr| grep -c "olsr::P"`
	else 
		tmp=`cat trace-ifi-ns32b.tr| grep -c "aodv::T"`
	fi

	echo "0.1   $resultat   $tmp" >> $3	
	
 	for vit in `seq 0.5 0.5 30`; do
 		resultat=0
 		tmp=0 

		exec 3<> tmp.txt
		./waf --run "scratch/$1 --protocol=$2 --nodeSpeed=$vit" 2>&3
		exec 3>&-
		
		for i in `seq 10 1 20`; do 
			tmp=`cat tmp.txt| grep -c "server received 1500 bytes from 10.1.1.$i"`
			resultat=$(( resultat+tmp ))
			tmp=0
		done

		if [ $2 -eq 1 ]
			then
			tmp=`cat trace-ifi-ns32b.tr| grep -c "olsr::P"`
		else 
			tmp=`cat trace-ifi-ns32b.tr| grep -c "aodv::T"`
		fi
		
		#resultat=$(echo $resultat/70 | bc -l)
		echo "res: $resultat"
		echo "$vit   $resultat   $tmp" >> $3
	done
    #fi
 }


echo "---OLSR---"
simulation adhocRouting-2019b 1 output.2b.MOBILITY.OLSR.txt
echo "---AODV---"
simulation adhocRouting-2019b 2 output.2b.MOBILITY.AODV.txt
