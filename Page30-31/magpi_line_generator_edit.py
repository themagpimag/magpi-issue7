#!/usr/bin/python

# line generator with command line arguments
# By ColinD - 03 October 2012

import os, pygame, argparse, sys
from pygame.locals import *

# initialise pygame (to render the image)
pygame.init()

# Define two functions that will be used:

# 1) fnAppend2Log write a line to a log file
def fnAppend2Log( line2write ):
    logfile = open('lines.log', 'a')
    logfile.write(line2write + '\n')
    logfile.close()

# 2) fnPlotLines will render a quarter of the shape.
# Uses the previous co-ordinates as the new starting co-ordinates
def fnPlotLines(quarter, sX, sY, eX, eY, incSX, incSY, incEX, incEY ):
    fnAppend2Log(quarter + ' quarter co-ordinates:')

    # calculate and loop through line co-ordinates
    for i in range(0,iterations, args.step):
        nSX = sX + (incSX * i) # start X
        nSY = sY + (incSY * i) # start Y
        nEX = eX + (incEX * i) # end X
        nEY = eY + (incEY * i) # end Y
        
        # draw a line between the pair of co-ordinates.
        pygame.draw.line(screen,(lineColour),(nSX,nSY),(nEX,nEY),1)
 
        coordText = '('+str(nSX)+','+str(nSY)+')-('+str(nEX)+','+str(nEY)+')'
       # render the image line by line (takes longer)?
        if args.renderlines == 'y':
            pygame.display.update();
            pygame.display.set_caption(coordText)

        # output co-ordinates to the log
        fnAppend2Log(coordText)

    # return a tuple containing the final calculated co-ordinates
    return (nSX, nSY, nEX, nEY);

# define our command line arguments:
parser = argparse.ArgumentParser(description='Render shape')
parser.add_argument('-s', action='store', dest='scale', type=int, 
                    default=2, help='Render size, default=2, 200x200px)')
parser.add_argument('-t', action='store', dest='step', type=int,
                    default=5, help='Step value (default=5): lower the value for denser lines')
parser.add_argument('-r', action='store', dest='renderlines', choices=('y','n'), default='y', help='Render line by line (slower) (y) or only display finished object (faster) (n)? (default=y)')
args = parser.parse_args()

# Define the variables that will be needed
sz = 100*args.scale # size (in pixels horiz and vert) of any quarter image
iterations = sz +5 # number of lines to render per quarter
lineColour = 0,0,255 # the colour of the line to draw (blue)

# open a pygame screen on which to render our objects
# the image size will need to be twice the object to be rendered as we render 4 quarters
screen = pygame.display.set_mode([sz*2,sz*2],0,32)

# Draw the lines, quarter by quarter, returning the co-ordinate pairs
# The starting co-ordinates equal the end co-ordinates from the last quarter rendered
sx, sy, ex, ey = fnPlotLines('Top left', sz, 0, sz, sz, 0, 1, -1, 0 )
sx, sy, ex, ey = fnPlotLines('Bottom left', ex, ey, sx, sy, 1, 0, 0, 1 ) 
sx, sy, ex, ey = fnPlotLines('Bottom right', ex, ey, sx, sy, 0, -1, 1, 0 )
sx, sy, ex, ey = fnPlotLines('Top right', ex, ey, sx, sy, -1, 0, 0, -1 )

# if rendering each line is suppressed then display the final image
if args.renderlines == 'n':
    pygame.display.update();

# save the rendered image to a file
pygame.image.save(screen, 'lineimage.png')

# display the result for 10 seconds
pygame.time.wait(10000)
