##################################################################################
#BeesBook tags
#
#This script generates 2048 tags following the beesbook design
#It suports Hamming coding
#
#Standard coded tags (without Hamming coding)
#For the standard coded tags (without Hamming coding), a set consists of 2048 different tags
#either with even or odd parity bit (11 bits + parity bit)
#Sets with even and odd parity ar complementary and can be used simultaneously as a set
#of 4096 tags without parity
#
#Hamming coded tags
#For the Hamming coded tags, a set consists of 128 different tags
#(7 bits information + 5 parity bits)
###################################################################################
#use: TagGenerator.py -c <coding> -p <parityType>
#Input arguments:
#-c --coding: none/hamming
#-p --parity: even/odd (only valid for no hamming coding)
#Consult the wiki for more information
###################################################################################
#Fernando Wario
#fernando.wario@fu-berlin.de
#Juli 2016

import math
import sys, getopt
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


# This function returns x in binary with n bits
# Input:
# x -------- number in decimal
# n -------- number of bits for the output
# Output:
# return --- x coded in binary with a length of n bits
def getBin (x,n):    
    return (bin(x)[2:].zfill(n))

# This function calculates the partity bit for an integer
# Input:
# s -------- binary number
# opt ------ kind of parity: "even" or "odd"
# Output:
# return --- parity bit
def parity(s,opt):
    if opt == 'even':
        return str(str.count(s, "1") % 2)
    elif opt == 'odd':
        return str((str.count(s, "1")-1) % 2)
    else:
        print (opt + 'is not a type of parity (even/odd)')
    
# Encode a customized version of the hamming code with general parity bit, a blockLength of 12 bits and a msgLength of 7.
# Input:
# bin7 ----- binary number with a length of 7 bits
# Output:
# hamming -- bin7 encoded in hamming with 5 parity bits
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
    # Resulting Hamming code
    hamming = E1 + E2 + bin7[0] + E4 + bin7[1:4] + E8 + bin7[4:7] + P
    
    return hamming


#this function draws the Tag
# Input:
# s -------- Canvas
# x -------- 12 bits encoded ID
# cx ------- x center coordinates
# cy ------- y center coordinates
# rA ------- radius of the arcs
# rO ------- radius of the orientation semi-circles
# rC ------- radius of the circle (this is not part of the tag, it is only printed as auxiliar for the punch out process)
# SWC ------ stroke of the circle (this is not part of the tag, it is only printed as auxiliar for the punch out process)
# Output:
# It doesn't return any value it only generates a svg file with the tags
def drawTag (s,x,cx,cy,rA,rO,rC,SWC):

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
    styleOrientW = {"stroke":"black","fill":"white","stroke-width":"0","stroke-opacity":"1"}
    styleOrientB = {"stroke":"white","fill":"black","stroke-width":"0","stroke-opacity":"1"}

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

    #The paths for the inner semi-circles
    sW = Path(pathData="M " + str(ssxW) + "," + str(ssyW) +" a " + str(rO) + "," + str(rO) + " 0 0,1 " + str(sexW) + "," + str(seyW))
    sW.set_style(StyleBuilder(styleOrientW).getStyle())

    sB = Path(pathData="M " + str(ssxB) + "," + str(ssyB) +" a " + str(rO) + "," + str(rO) + " 0 0,1 " + str(sexB) + "," + str(seyB))
    sB.set_style(StyleBuilder(styleOrientB).getStyle())

    #The inner semi-circles are drawn
    s.addElement(sW)
    s.addElement(sB)

    
# HERE IS WERE THE ACTUAL PROGRAM BEGINS
def main(argv):
    # Parameters that can be modified through arguments
    # Tag Size in mm
    tagSize = 3
	# Coding type (none/hamming)
    codingType = 'none'
	# parityType, applies only for no hamming tags
    parityType = 'even'
    
    try:
        opts, args = getopt.getopt(argv, 'hc:p:',['coding=','parity='])
    except getopt.GetoptError:
        print ('TagGenerator.py -c <coding> -p <parityType>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('TagGenerator.py -c <coding> -p <parityType>')
            print ('coding: none/hamming')
            print ('parityType: even/odd')
            sys.exit()
        elif opt in ('-c', '--coding'):
            codingType = arg
            if codingType not in ('none','hamming'):
                print('Not a valid kind of coding (none/hamming)')
                sys.exit(2)				
        elif opt in ('-p', '--parity'):
            parityType = arg
            if codingType == 'none' and parityType not in ('even','odd'):
                print('Not a valid type of parity (even/odd)')
                sys.exit(2)				
    
    # 7 bits for Hamming coded IDs
    # 11 bits for not encoded IDs
    if codingType == 'none':
	    numBits = 11
    elif codingType == 'hamming':
        numBits = 7
	
	# Number of tags in a set
    maxID = math.pow(2,numBits)

    # ALL THE VALUES ARE SET ACCORDING TO THE VIEWBOX !!!!!!
    # 1 Unit = 1 mm !!!!!!

    # Size of the canvas
    canvasW = 210
    canvasH = 405

    # Tag's diameter
    tS = tagSize
    # radius of circle
    rC = tS/2+0.25
    # stroke width circle
    SWC = 0.05

    # radius of arcs
    rA = tS*1.1/3

    #radius of orientation semi-circle
    rO = tS*0.6/3

    #shape builder as auxiliar
    oh = ShapeBuilder()

    #the canvas is generated
    s = Svg(width = str(canvasW)+"mm", height = str(canvasH)+"mm")
    s.set_viewBox("0 0 " + str(canvasW) + " " + str(canvasH))

    #Distance between tags (in fuction of rC)
    dst = 3.5

    #Number of rows
    row = int(math.floor((canvasH-5)/(dst*rC)-1))
    #Number of columns
    col = int(math.floor((canvasW-5)/(dst*rC)-1))

    #Number of tags
    numT = row*col

    #a grid is printed as a guide
    for indRow in range(0,row):
        #first the rows
        coordy=(indRow+1)*dst*rC+5      
        s.addElement(oh.createLine(0, coordy, canvasW, coordy, strokewidth=0.25, stroke="black"))

    for indCol in range(0,col):
        #and then the columns
        coordx=(indCol+1)*dst*rC+5
        s.addElement(oh.createLine(coordx, 0, coordx, canvasH-5, strokewidth=0.25, stroke="black"))

    #Printing the markers
    for ind in range (0,numT):
        #x coordinates
        indx = ind%col + 1
        cx = indx*dst*rC+5  
        #y coordinates
        indy = int(math.floor(ind/col))+1
        cy = indy*dst*rC+5
        #Tag's ID
        tID = int(ind%maxID)
        #The ID coded in simple binary
        markBin = getBin(tID,numBits)
        if numBits == 7:
            markBin2= hamming_12_7_encode(markBin)
        elif numBits == 11:
            eh=parity(markBin,parityType)
            #The ID with a 12th parity bit
            markBin2= markBin+str(eh)    
        #The marker is printed
        drawTag(s,markBin2,cx,cy,rA,rO,rC,SWC)

    #the set of Tags that was generated
    if numBits == 7:
        t = Text("BeesBook Tags with Hamming code (12,7) " + str(numT) + " Tags, " + str(canvasW) + " x " + str(canvasH) + " mm" , 45, canvasH-2)
        fileName = 'BeesBookTags_12_' + str(numBits) + '_bits_Hamming' + '.svg'
    elif numBits == 11:
        t = Text("BeesBook Tags " + str(numT) + " Tags with " + parityType + " parity, " + str(canvasW) + " x " + str(canvasH) + " mm" , 45, canvasH-2)
        fileName = 'BeesBookTags_' + str(numBits) + '_bits_' + parityType + '_parity' + '.svg'
    t.set_font_size(4)

    s.addElement(t)

    #the file is saved

    s.save('./testOutput/' + fileName, encoding='UTF-8')
    print('done! ' + str(numT) + ' Tags')
    print ('saved under ./testOutput/' + fileName)

if __name__ == "__main__":
    main(sys.argv[1:])