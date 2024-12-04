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

#this function draws #this function draws the Tag
# Input:
# s -------- Canvas
# x -------- 12 bits encoded ID
# cx ------- x center coordinates
# cy ------- y center coordinates
# rA ------- radius of the arcs
# rO ------- radius of the orientation semi-circles
# rC ------- radius of the circle (this is not part of the tag, it is only printed as auxiliar for the punch out process)
# SWC ------ stroke of the circle (this is not part of the tag, it is only printed as auxiliar for the punch out process)
# SWO ------ stroke of the orientation circle
# Output:
# It doesn't return any value it only generates a svg file with the tags Tag
def drawTag(s,x,cx,cy,rA,rO,rC,SWC,SWO=0):

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