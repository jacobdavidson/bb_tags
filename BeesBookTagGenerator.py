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

from tagfunctions import getBin, parity, hamming_12_7_encode, drawTag

    
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