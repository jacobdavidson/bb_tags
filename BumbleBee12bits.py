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

from tagfunctions import getBin, parity, hamming_12_7_encode, drawTag

    
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
    drawTag(s,markBin2,cx,cy,rA,rO,rC,SWC,SWO)

#the set of Tags that was generated
t = Text("Bumble Bee Hamming code (12,7) " + str(numT) + " Tags, " + str(canvasW) + " x " + str(canvasH) + " mm" , 75, canvasH*2-2)
t.set_font_size(8)

s.addElement(t)



#the file is saved
s.save('./testOutput/BumbleBee16bitsEven.svg', encoding='UTF-8')
print('done! ' + str(numT) + ' Tags')
