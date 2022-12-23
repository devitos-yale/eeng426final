import string

m2pad = 2
top_m2min = 100
bottom_m2min = 100

notes_x = 0
notes_y = 0

def updateWarningPos(labels):
    global notes_y
    notes_y -= 4
    labels.write("move to %d %d\n" % (notes_x, notes_y) )

def getRects(filepath):
    
    #List with wire name, material, coordinates
    rect_list = []
    inputs = []
    outputs = []

    #Open file and read in rect coords
    with open(filepath, "r") as f:
        
        #get box coords
        rect_box = (f.readline()).split()
        del rect_box[0]

        #get rect coords and IO names
        for line in f:
            rect = (line.split())

            #update I/O names
            if (rect[1] == 'Vdd') or (rect[1] == 'GND') or ('#' in rect[1]) or ('_' in rect[1]):
                pass
            elif (any(rect[1] == name for name in inputs)):
                pass
            elif (any(rect[1] == name for name in outputs)):
                pass
            else:
                if 'in' in rect[1]:
                    inputs.append(rect[1])
                elif 'out' in rect[1]:
                    outputs.append(rect[1])
                elif string.ascii_uppercase.index(rect[1]) < 12:
                    inputs.append(rect[1])
                elif string.ascii_uppercase.index(rect[1]) > 12:
                    outputs.append(rect[1])

            #trim rect
            if len(rect) > 7: del rect[7:]
            del rect[0]

            rect_list.append(rect)

    f.close()  
    return rect_list, rect_box, inputs, outputs


def getRectLists(filepath,labels):

    #Initialize empty lists
    rect_list = []
    box = []
    INPUT_NAMES = []
    OUTPUT_NAMES = []

    #List of rects by wire
    vdd_list = []
    gnd_list = []
    input_list = []
    output_list = []
    obstacle_list = []
    ports = []

    #Function to get rect file data
    rect_list, box, INPUT_NAMES, OUTPUT_NAMES = getRects(filepath)

    firstNotes(labels)

    #Organize rect_list data
    for row in rect_list:
        if row[0] == 'Vdd':
            vdd_list.append(row)
            if row[1] == 'm2': ports.append(row)
        elif row[0] == 'GND':
            gnd_list.append(row)
            if row[1] == 'm2': ports.append(row)
        elif any(wire in row for wire in OUTPUT_NAMES):
            for wire in OUTPUT_NAMES:
                if row[0] == wire:
                    output_list.append(row)
                    if row[1] == 'm2' or row[1] == 'm1':
                        ports.append(row)
                    break
        elif any(wire in row for wire in INPUT_NAMES):
            for wire in INPUT_NAMES:
                if row[0] == wire:
                    input_list.append(row)
                    if row[1] == 'm2' or row[1] == 'm1':
                        ports.append(row)
                    break
        else:
            obstacle_list.append(row)

    return rect_list, box, ports, vdd_list, gnd_list, output_list, input_list, obstacle_list, INPUT_NAMES, OUTPUT_NAMES

def checkPathToPerimeter(p,ports,rects):
    row = ports[p[2]]
    x1 = int(row[2])
    x2 = int(row[4])
    y1 = int(row[3])
    y2 = int(row[5])
    path = True

    for i in rects:
        if i == row:
            pass
        elif (p[1]):    
            if (int(i[3])<y1): 
                if (int(i[2])<x2+m2pad) or (int(i[4])>x1-m2pad):
                    path = False
                    break
        elif not (p[1]):    
            if (int(i[5])>y2):
                if (int(i[2])<x2) or (int(i[4])<x1):
                    path = False
                    break
    return path


def checkPerim(labels, ports,rect_list,bbox,name,layer1, layer2='m2'):
    maxdist = 4
    myports = []

    for p in ports:

        ymin = []

        if (p[1] == layer1 or p[1] == layer2) and (p[0] == name):
            # Rank the named ports from outermost to innermost vertical distance
            # myports :  [ [ymin, (top/bottom), 'ports' index] ]
            # myports[1] : False means closer to bottom, True means closer to top

            y_top = int(p[5]) - int(bbox[3])
            y_bottom = int(p[3])
            if abs(y_top) < y_bottom: 
                ymin = y_top
            else:
                ymin = y_bottom
            pid = ports.index(p)
            myports.append([abs(ymin), (ymin>0), pid])

    myports.sort()

    a = min(myports, key=lambda x: x[0])
    if a[0] >= maxdist:

        for n,p in enumerate(myports):
            
            b = checkPathToPerimeter(p,ports,rect_list)
            
            if b:       
                x = int(ports[p[2]][2])+1
                y = int(ports[p[2]][3])+1
                labels.write("move to %d %d\n" % (x,y) )
                labels.write("label EXTEND_%s_HERE\n" % (name))
                break

            elif n == len(myports)-1:
                updateWarningPos(labels)
                labels.write("label Router's_path_to_%s_is_blocked right\n" % (name))
    else:
        pass
  
    #update values
    global bottom_m2min
    global top_m2min

    for p in myports:
        if (p[1]) and (ports[myports[0][2]][1] == 'm2'):
            bottom_m2min = min(int(a[0]), bottom_m2min)
            break
    
    for p in myports:
        if (not p[1]) and (ports[myports[0][2]][1] == 'm2'):
            top_m2min = min(int(a[0]), top_m2min)
            break


def flagM2(labels, ports, tmin, bmin, box):

    for p in ports: 
        if ((int(p[3])<bmin) or (int(box[3])-int(p[5])<tmin)) and (p[1]=='m2'):
            
            x=int(p[2])+1
            y=int(p[3])+1
            labels.write("move to %d %d \n" % (x, y) )
            labels.write("label M2_ON_EDGE \n")


def firstNotes(labels):

    updateWarningPos(labels)
    labels.write("label WARNINGS right\n")


def relabel(labels, rect_list, name):
  for r in rect_list:
      if r[0] == name:
        x=int(r[2])+1
        y=int(r[3])+1
        labels.write("move to %d %d\n" % (x,y))
        labels.write("label %s\n" % (name))
        labels.write("port make\n")
        break