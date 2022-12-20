import sys

ports = []
m1 = []
m2 = []

port_distance = 3 #min distance between ports

#sys.argv[1] should be a .rect file
if (len(sys.argv) != 2):
  print ("Usage python rectcheck.py <rect_file>")
  sys.exit (1)

if (sys.argv[1][-5:] != ".rect"):
  print ("Expecting .rect extension")
  sys.exit (1)
  

#read in rect file
old_rect_file = open(sys.argv[1], "r")

#look at each line in input .rect file
for line in old_rect_file:
	a = line.split()
	if a[0] == "bbox":
		bbox = a
	
	#we are counting input/output ports as inrect/outrect rectangles with correct labels,
	#and Vdd/GND ports as m2 with Vdd and GND labels
	if (a[0] == "outrect") or (a[0] == "inrect"): #input/output ports
		ports.append(a)
	if (a[1] == 'GND' or a[1] == 'Vdd') and (a[2] == 'm2'): #Vdd/GND ports
		ports.append(a)

	#create lists of m1 and m2 rectangles
	if a[2] == "m1":
		m1.append(a)
	if a[2] == "m2":
		m2.append(a)

#check if the ports are < port_distance from each other
for p in ports:
	xmin = int(p[3]) - port_distance
	xmax = int(p[5]) + port_distance
	ymin = int(p[4]) - port_distance
	ymax = int(p[6]) + port_distance
	for rest in ports:
		#check bottom right corner of each other port
		if ((int(rest[3]) > xmin and int(rest[3]) < xmax) and (int(rest[4]) > ymin and int(rest[4]) < ymax)) and (rest[1] != p[1]):
			print(rest)
		
		#check upper left corner of each other port
		if ((int(rest[5]) > xmin and int(rest[5]) < xmax) and (int(rest[6]) > ymin and int(rest[6]) < ymax)) and (rest[1] != p[1]):
			print(rest)