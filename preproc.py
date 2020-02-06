"""
	Contient les fonctions qui preparent les donnees et calcule les courbes
"""

def preprocX_distYRRate(filepath, simulationTime):
	x_axis_Data = []
	y_axis_Data = []

	with open(filepath) as fp:
		line = fp.readline()
		cnt = False
		while line:
			if cnt:
				x_axis_Data.append(float(line.strip().split()[0]))

				#calcul du debit
				tmp = float(line.strip().split()[1])
				tmp = tmp*1500*8
				tmp = tmp*10**(-6)
				tmp = tmp/simulationTime
				y_axis_Data.append(tmp)

			line = fp.readline()
			cnt = True

	return [x_axis_Data, y_axis_Data]

def preprocXSrate_YNbPck(filepath):
	x_axis_Data = []
	y_axis_Data = []

	with open(filepath) as fp:
		line = fp.readline()
		cnt = False
		while line:
			if cnt:
				x_axis_Data.append(float(line.strip().split()[0]))
				y_axis_Data.append(float(line.strip().split()[1]))

			line = fp.readline()
			cnt = True

	return [x_axis_Data, y_axis_Data]


def preprocXspeed_YPDR(filepath):
	x_axis_Data = []
	y_axis_Data = []

	with open(filepath) as fp:
		line = fp.readline()
		cnt = False
		while line:
			if cnt:
				x_axis_Data.append(float(line.strip().split()[0]))
				tmp = float(line.strip().split()[1])
				tmp = tmp/70
				y_axis_Data.append(tmp)

			line = fp.readline()
			cnt = True

	return [x_axis_Data, y_axis_Data]

def preprocXspeed_YNbOvhd(filepath):
	x_axis_Data = []
	y_axis_Data = []

	with open(filepath) as fp:
		line = fp.readline()
		cnt = False
		while line:
			if cnt:
				x_axis_Data.append(float(line.strip().split()[0]))
				y_axis_Data.append(float(line.strip().split()[2]))

			line = fp.readline()
			cnt = True

	return [x_axis_Data, y_axis_Data]