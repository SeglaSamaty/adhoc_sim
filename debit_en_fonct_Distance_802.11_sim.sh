#!/bin/bash
#exercice 1.b
#Automatise les simulation de communications entres deux nodes utilisant des versions diff du 802.11
simulation () {
 	if [ "$#" -ne 2 ]; then
 		echo "distance   nombrePaquets" > $3
 		for dist in `seq 1 2 150`; do
 			echo "simulation distance $dist with modulation $2"
 			resultat=`./../waf --run "../scratch/$1 --distance=$dist --modulation=$2 --packetSize=1500" 2>&1 |grep "RX"|wc -l`
 			echo "$dist   $resultat" >> $3
 		done
 	else
 		echo "distance   nombrePaquets" > $2
 		echo "" >> $2
 		for dist in `seq 1 2 150`; do
 			echo "simulation distance $dist"
 			resultat=`./../waf --run "../scratch/$1 --distance=$dist --packetSize=1500" 2>&1 |grep "RX"|wc -l`
 			echo "$dist   $resultat" >> $2
 		done
    fi
 }

for eachModulation in "OfdmRate54Mbps OfdmRate6Mbps"; do
	echo " 54Mbps "
    simulation tp-ifi-exo1-2019 OfdmRate54Mbps output.54Mb.txt
    echo " 6Mps "
    simulation tp-ifi-exo1-2019 OfdmRate6Mbps output.6Mb.txt
done

echo " 802.11g "
simulation tp-ifi-exo1-2019_2.b output.802.11g.txt
echo " 802.11n "
simulation tp-ifi-exo1-2019_2.c output.802.11n.txt