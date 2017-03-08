##################################################################################
#BeesBook tags
#
#This script generate a set of tags following the beesbook design.
#
#Standard coded tags
#The list of the 12 bits IDs for the tags is provided in the form of a CSV file
#
###################################################################################
#use: TagGenerator.py -c <coding> -p <parityType>
#Input arguments:
#Path to the csv file with the IDs
#
#Output:
#It doesn't return any output, it only generates the PDF file with the tags.
#Check the wiki for more information
###################################################################################
#Fernando Wario
#fernando.wario@fu-berlin.de
#March 2017

import math
import sys, getopt
import csv
import os
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
	# Check if path exits	
	path = sys.argv[1]
	if not os.path.exists(path):
		print ('Not a valid path')
		sys.exit(2)
	#Reading CSV file
	with open('ldpc-ids-5bit.csv', 'rb') as csvfile:
		IDreader = list(csv.reader(csvfile))

	# Parameters that can be modified through arguments
	# Tag Size in mm
	tagSize = 3
	# Number of tags in a set
	maxID = len(IDreader)

	# ALL THE VALUES ARE SET ACCORDING TO THE VIEWBOX !!!!!!
	# 1 Unit = 1 mm !!!!!!

	# Size of the canvas
	canvasW = 210
	canvasH = 297

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
		
		#Read the ID from the CSV file
		markBin = IDreader[tID]
				
		#The marker is printed
		drawTag(s,markBin,cx,cy,rA,rO,rC,SWC)

	#the set of Tags that was generated    
	t = Text("BeesBook Tags with (5,7) " + str(numT) + " Tags, " + str(canvasW) + " x " + str(canvasH) + " mm" , 45, canvasH-2)
	fileName = 'BeesBookTags_5.svg'
	t.set_font_size(4)

	s.addElement(t)

	#the file is saved

	s.save('./testOutput/' + fileName, encoding='UTF-8')
	print('done! ' + str(numT) + ' Tags')
	print ('saved under ./testOutput/' + fileName)

if __name__ == "__main__":
    main(sys.argv[1:])