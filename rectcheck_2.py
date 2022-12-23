import functions as f
import sys

#Initialize lists for readrect
INPUT_NAMES = []
OUTPUT_NAMES = []

rect_list = []
bbox = []
vdd_list = []
gnd_list = []
input_list = []
output_list = []
obstacle_list = []
ports = []

#sys.argv[1] should be a .rect file
if (len(sys.argv) != 2):
  print ("Usage python rectcheck.py <rect_file>")
  sys.exit (1)

if (sys.argv[1][-5:] != ".rect"):
  print ("Expecting .rect extension")
  sys.exit (1)

myfile = sys.argv[1]
labels = open("labels.scr","w+")

rect_list, bbox, ports, vdd_list, gnd_list, output_list, input_list, obstacle_list, \
  INPUT_NAMES, OUTPUT_NAMES = f.getRectLists(myfile, labels)

#do the perimeter checks 
f.checkPerim(labels, ports,rect_list,bbox,'Vdd','m2')
f.relabel(labels, rect_list,'Vdd')

f.checkPerim(labels, ports,rect_list,bbox,'GND','m2')
f.relabel(labels, rect_list,'GND')

for i in INPUT_NAMES:
    f.checkPerim(labels, ports,rect_list,bbox,i,'m1','m2')
    f.relabel(labels, rect_list,i)

for o in OUTPUT_NAMES:
   f.checkPerim(labels, ports,rect_list,bbox,o,'m1','m2')
   f.relabel(labels, rect_list, o)

f.flagM2(labels, ports, f.top_m2min, f.bottom_m2min, bbox)


