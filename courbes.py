"""
	Ce script calcul et cree toutes les courbes
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import preproc

def courbe802_11():
	"""
		This is to plot the curves of the destination rate regardind the distance for the three 802.11 standard
		data are in the output files
	"""
	simulationTime = 2 # Temps total de la simulation ici deux secondes

	data_6Mb = preproc.preprocX_distYRRate('output.6Mb.txt', simulationTime)
	data_54Mb = preproc.preprocX_distYRRate('output.54Mb.txt', simulationTime)
	data_802_11g = preproc.preprocX_distYRRate('output.802.11g.txt', simulationTime)
	data_802_11n = preproc.preprocX_distYRRate('output.802.11n.txt', simulationTime)

	fig = plt.figure()

	plt.plot( data_6Mb[0], data_6Mb[1], marker='v', markerfacecolor='m', markersize=2, color='r', linewidth=1, label="802.11a_6Mbps ")
	plt.plot( data_54Mb[0], data_54Mb[1], marker='^', markerfacecolor='g', markersize=2, color='r', linewidth=1, label="802.11a_54Mbps")
	plt.plot( data_802_11g[0], data_802_11g[1], marker='o', markerfacecolor='b', markersize=2, color='b', linewidth=1, label="802.11g")
	plt.plot( data_802_11n[0], data_802_11n[1], marker='o', markerfacecolor='g', markersize=2, color='g', linewidth=1, label="802.11n")

	plt.legend()

	plt.yticks(np.arange(0, 65, 5))

	fig.suptitle('Debit en reception en fonction de la distance', fontsize=12)
	plt.xlabel('Distance (m)', fontsize=10)
	plt.ylabel('Debit en reception (Mbps)', fontsize=10)

	plt.savefig('courbes/courbe_802.2_DebReceptio__Dist.svg',format='svg', dpi=1200)

def courbe_A_O_MobiNo():
	"""
		This is to plot the curve of the nomber of received packets regardind the source rate for the two routing protocol namely OLSR and AODV
		data are in the output files
	"""
	simulationTime = 30 # Temps total de la simulation ici deux secondes

	olsr = preproc.preprocXSrate_YNbPck('output.2a.OLSR.txt')
	aodv = preproc.preprocXSrate_YNbPck('output.2a.AODV.txt')

	fig = plt.figure()

	plt.plot( olsr[0], olsr[1], marker='o', markerfacecolor='b', markersize=2, color='b', linewidth=1, label="OLSR")
	plt.plot( aodv[0], aodv[1], marker='o', markerfacecolor='red', markersize=2, color='red', linewidth=1, label="AODV")

	#print(olsr)

	plt.legend()

	plt.yticks(np.arange(0, 17000, 1000))

	fig.suptitle('Nombre de paquets reçus en fonction du débit source', fontsize=12)
	plt.xlabel('Débit source (Mbps)', fontsize=10)
	plt.ylabel('Nombre de paquets reçus', fontsize=10)

	plt.savefig('courbes/courbe_OLSR_AODV_sansMobi.svg',format='svg', dpi=1200)

def courbe_A_O_MobiYes():
	"""
		This is to plot the curve of the Packet Delivery Ratio (PDR) regardind the highest mobility speed of the nodes for the two routing protocol namely OLSR and AODV
		data are in the output files
	"""
	olsr = preproc.preprocXspeed_YPDR('output.2b.MOBILITY.OLSR.txt')
	aodv = preproc.preprocXspeed_YPDR('output.2b.MOBILITY.AODV.txt')

	fig = plt.figure()

	plt.plot( olsr[0], olsr[1], marker='o', markerfacecolor='b', markersize=2, color='b', linewidth=1, label="OLSR")
	plt.plot( aodv[0], aodv[1], marker='o', markerfacecolor='red', markersize=2, color='red', linewidth=1, label="AODV")

	plt.legend()

	plt.yticks(np.arange(0, 1, 0.05))

	fig.suptitle('PDR en fonction de la vitesse maximale', fontsize=12)
	plt.xlabel('Vitesse max (m/s)', fontsize=10)
	plt.ylabel('PDR', fontsize=10)

	plt.savefig('courbes/courbe_OLSR_AODV_avecNobi_PDR.Vit.svg',format='svg', dpi=1200)

def courbe_A_O_MobiYes2():
	"""
		This is to plot the curve of Overhead Packet regardind the highest mobility speed of the nodes for the two routing protocol namely OLSR and AODV
		data are in the output files
	"""
	olsr = preproc.preprocXspeed_YNbOvhd('output.2b.MOBILITY.OLSR.txt')
	aodv = preproc.preprocXspeed_YNbOvhd('output.2b.MOBILITY.AODV.txt')

	fig = plt.figure()

	plt.plot( olsr[0], olsr[1], marker='o', markerfacecolor='b', markersize=2, color='b', linewidth=1, label="OLSR")
	plt.plot( aodv[0], aodv[1], marker='o', markerfacecolor='red', markersize=2, color='red', linewidth=1, label="AODV")

	#print(olsr)

	plt.legend()

	plt.yticks(np.arange(3000, 17000, 1000))

	fig.suptitle('Nombre de paquets Overhead en fonction de la vitesse max', fontsize=12)
	plt.xlabel('Vitesse max (m/s)', fontsize=10)
	plt.ylabel('#Paquets Overhead', fontsize=10)

	plt.savefig('courbes/courbe_OLSR_AODV_avecMobi_Over.Vit.svg',format='svg', dpi=1200)



if __name__ == '__main__':
	courbe802_11()
	courbe_A_O_MobiNo()
	courbe_A_O_MobiYes()
	courbe_A_O_MobiYes2()