#Bumble bee verision
#Uses Hamming code (12,7)
#ToDo: Description
#
#Fernando Wario
#fernando.wario@fu-berlin.de
#March 2016

import math
from pysvg.structure import *
from pysvg.core import *
from pysvg.text import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.style import *
from pysvg.builders import *


#this function returns x in binary with n bits
def getBin (x,n):    
    return (bin(x)[2:].zfill(n))

#this function calculates the partity bit of an integer
def parity(s,opt):
    if opt == 'even':
        return str(str.count(s, "1") % 2)
    elif opt == 'odd':
        return str((str.count(s, "1")-1) % 2)
	
# Encode a customized version of the hamming code with general parity bit, a blockLength from 12 and a msgLength of 7  
def hamming_12_7_encode(bin7):
    # First parity bit
    E1 = parity(bin7[0] + bin7[1] + bin7[3] + bin7[4] + bin7[6], 'even')
    # Second parity bit
    E2 = parity(bin7[0] + bin7[2] + bin7[3] + bin7[5] + bin7[6], 'even')
    # Third parity bit
    E4 = parity(bin7[1] + bin7[2] + bin7[3], 'even')
    # Fourth parity bit
    E8 = parity(bin7[4] + bin7[5] + bin7[6], 'even')
    # Global parity bith
    P  = parity(E1 + E2 + bin7[0] + E4 + bin7[1:4] + E8 + bin7[4:7], 'even')
    
    hamming = E1 + E2 + bin7[0] + E4 + bin7[1:4] + E8 + bin7[4:7] + P
    
    return hamming


#this function draws the Tag
def drawTag (s,x,cx,cy,rC,SWC,rA,rO,SWO):

    #shape builder as auxiliar
    oh = ShapeBuilder()

    #the outer circle is defined with the shape builder class
    s.addElement(oh.createCircle(cx, cy, rC, strokewidth = SWC, stroke = 'black', fill = 'white'))

    #characteristics of two possible kind of arcs
    styleArcB = {"stroke":"none","fill":"black","stroke-width":"none","stroke-opacity":"0"}
    styleArcW = {"stroke":"none","fill":"white","stroke-width":"none","stroke-opacity":"0"}
    
    a = 0
    pi2 = math.pi
    
    #the whole string is analyzed
    while a < len(x):
        
        #print("bit " + str(a+1) + " is " + str(x[a]))

        if a == 0: #1st bit            
            qsx = cx - rA
            qsy = cy
            qex = (1 - math.cos(pi2/6))*rA
            qey = -math.sin(pi2/6)*rA
        elif a == 1: #2nd bit
            qsx = cx - math.cos(pi2/6)*rA
            qsy = cy - math.sin(pi2/6)*rA
            qex = (math.cos(pi2/6) - math.cos(pi2/3))*rA
            qey = -(math.sin(pi2/3) - math.sin(pi2/6))*rA
        elif a == 2: #3rd bit
            qsx = cx - math.cos(pi2/3)*rA
            qsy = cy - math.sin(pi2/3)*rA
            qex = math.cos(pi2/3)*rA
            qey = -(1 - math.sin(pi2/3))*rA
            
        elif a == 3: #4th bit
            qsx = cx
            qsy = cy - rA
            qex = math.cos(pi2/3)*rA
            qey = (1 - math.sin(pi2/3))*rA
        elif a == 4: #5th bit
            qsx = cx + math.cos(pi2/3)*rA
            qsy = cy - math.sin(pi2/3)*rA
            qex = (math.cos(pi2/6) - math.cos(pi2/3))*rA
            qey = (math.sin(pi2/3) - math.sin(pi2/6))*rA
        elif a == 5: #6th bit
            qsx = cx + math.cos(pi2/6)*rA
            qsy = cy - math.sin(pi2/6)*rA
            qex = (1 - math.cos(pi2/6))*rA
            qey = math.sin(pi2/6)*rA
            
        elif a == 6: #7th bit
            qsx = cx + rA
            qsy = cy
            qex = -(1 - math.cos(pi2/6))*rA
            qey = math.sin(pi2/6)*rA
        elif a == 7: #8th bit
            qsx = cx + math.cos(pi2/6)*rA
            qsy = cy + math.sin(pi2/6)*rA
            qex = -(math.cos(pi2/6) - math.cos(pi2/3))*rA
            qey = (math.sin(pi2/3) - math.sin(pi2/6))*rA
        elif a == 8: #9th bit
            qsx = cx + math.cos(pi2/3)*rA
            qsy = cy + math.sin(pi2/3)*rA
            qex = -math.cos(pi2/3)*rA
            qey = (1 - math.sin(pi2/3))*rA
            
        elif a == 9: #10th bit
            qsx = cx
            qsy = cy + rA
            qex = -math.cos(pi2/3)*rA
            qey = -(1 - math.sin(pi2/3))*rA
        elif a == 10: #11th bit
            qsx = cx - math.cos(pi2/3)*rA
            qsy = cy + math.sin(pi2/3)*rA
            qex = -(math.cos(pi2/6) - math.cos(pi2/3))*rA
            qey = -(math.sin(pi2/3) - math.sin(pi2/6))*rA
        elif a == 11: #12th bit
            qsx = cx - math.cos(pi2/6)*rA
            qsy = cy + math.sin(pi2/6)*rA
            qex = -(1 - math.cos(pi2/6))*rA
            qey = -math.sin(pi2/6)*rA

        #the path of the correspondent arc is defined
        q = Path(pathData="M " + str(cx) + "," + str(cy) + " " + str(qsx) + "," + str(qsy) +" a " + str(rA) + "," + str(rA) + " 0 0,1 " + str(qex) + "," + str(qey) + " z")
            
        if x[a] == '0': #print("black")
            q.set_style(StyleBuilder(styleArcB).getStyle())
        else: #print("white")
            q.set_style(StyleBuilder(styleArcW).getStyle())

        #adding the elements to the file
        s.addElement(q)
        
        a+=1

    #characteristics of two possible kind of inner circles for the orientations
    styleOrientW = {"stroke":"black","fill":"white","stroke-width":str(SWO),"stroke-opacity":"1"}
    styleOrientB = {"stroke":"white","fill":"black","stroke-width":str(SWO),"stroke-opacity":"1"}

    #where the inner circles start and end

    #sW
    ssxW = cx-rO
    ssyW = cy+0

    sexW = 2*rO
    seyW = 0

    #sB
    ssxB = cx+rO
    ssyB = cy+0

    sexB = -2*rO
    seyB = 0           

    #the paths for the inner semi-circles
    sW = Path(pathData="M " + str(ssxW) + "," + str(ssyW) +" a " + str(rO) + "," + str(rO) + " 0 0,1 " + str(sexW) + "," + str(seyW))
    sW.set_style(StyleBuilder(styleOrientW).getStyle())

    sB = Path(pathData="M " + str(ssxB) + "," + str(ssyB) +" a " + str(rO) + "," + str(rO) + " 0 0,1 " + str(sexB) + "," + str(seyB))
    sB.set_style(StyleBuilder(styleOrientB).getStyle())

    #the inner semi-circles are drawn
    s.addElement(sW)
    s.addElement(sB)

    
#HERE IS WERE THE ACTUAL PROGRAM BEGINS
#Number of bits to be used for the ID
numBits = 7
maxID = math.pow(2,numBits)

#Units in mm
canvasW = 210
canvasH = 143

#ALL THESE VALUES ARE SET ACCORDING TO THE VIEWBOX
# 2 Uniits = 1 mm

#radius of circle
rC = 4
#stroke width circle
SWC = 0.1

#radius of arcs
rA = 2.6

#radius of orientation semi-circle
rO = 1.2
#stroke width orientation semi-circle
SWO = 0.0

#shape builder as auxiliar
oh = ShapeBuilder()

#the canvas is generated
s = Svg(width = str(canvasW)+"mm", height = str(canvasH)+"mm")
s.set_viewBox("0 0 " + str(2*canvasW) + " " + str(2*canvasH))

#Distance between tags (number of rC)
dst = 4

#Number of rows
row = int(math.floor((canvasH*2-10)/(dst*rC)-1))
#Number of columns
col = int(math.floor((canvasW*2-10)/(dst*rC)-1))

#Number of tags
numT = row*col

#a grid is printed as a guide
for indRow in range(0,row):
	#first the rows
	coordy=(indRow+1)*dst*rC+10		
	s.addElement(oh.createLine(0, coordy, 2*canvasW, coordy, strokewidth=0.5, stroke="black"))

for indCol in range(0,col):
    #and then the columns
    coordx=(indCol+1)*dst*rC+10
    s.addElement(oh.createLine(coordx, 0, coordx, 2*canvasH-10, strokewidth=0.5, stroke="black"))

#Printing the markers
for ind in range (0,numT):
    #x coordinates
    indx = ind%col + 1
    cx = indx*dst*rC+10	
    #y coordinates
    indy = int(math.floor(ind/col))+1
    cy = indy*dst*rC+10
    #Tag's ID
    tID = int(ind%maxID)
    #The ID in 7 bits
    markBin = getBin(tID,numBits)
    #The ID in Hamming code (12,7)
    markBin2= hamming_12_7_encode(markBin)
    #The marker is printed
    drawTag(s,markBin2,cx,cy,rC,SWC,rA,rO,SWO)

#the set of Tags that was generated
t = Text("Bumble Bee Hamming code (12,7) " + str(numT) + " Tags, " + str(canvasW) + " x " + str(canvasH) + " mm" , 75, canvasH*2-2)
t.set_font_size(8)

s.addElement(t)



#the file is saved
s.save('./testOutput/BumbleBee16bitsEven.svg', encoding='UTF-8')
print('done! ' + str(numT) + ' Tags')
