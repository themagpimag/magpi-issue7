# Pseudo-3D line generator

# By ColinD - 03 July 2012

import os, pygame, argparse, sys
from pygame.locals import *

pygame.init()

# fnAppend2Log will write a line to the log file when called
def fnAppend2Log( line2write ):
     # if the user has opted for a log then output one
    if args.outputlog == 'y':
        logfile = open(logFilename, 'a')
        logfile.write(line2write + '\n')
        logfile.close()

# -----------------------------------------------------------------------------
# The function fnPlotLines will render a portion of a shape, typically a quadrant, and therefore will be called multiple times, with
# each call after the first using the return end x and end y point values as the start x and y point values.
def fnPlotLines(startX, startY, endX, endY, incrementStartX, incrementStartY, incrementEndX, incrementEndY ):
    for i in range(0,iterations, args.step):
        # we calculate the start and end co-ordinates based on the previous co-ordinate + either a positive or negative number multiplied by a counter
        startX_new = startX + (incrementStartX * i)
        startY_new = startY + (incrementStartY * i)
        endX_new = endX + (incrementEndX * i)
        endY_new = endY + (incrementEndY * i)

        pygame.draw.line(screen,(lineColour),(startX_new,startY_new),(endX_new,endY_new),1)
        # slow down the rendering time if this has been specified on the command line
        pygame.time.wait(args.slowrender)
 
       # if the user has not suppressed rendering of each individual line then display as we generate the image (takes more time)
        if args.renderlines == 'y':
            pygame.display.update();
            pygame.display.set_caption('start:(' + str(startX_new) + ',' + str(startY_new) + ')' + ' end:(' + str(endX_new) + ',' + str(endY_new) + ')')
        # if the user has opted for a log then output one
        fnAppend2Log('('+str(startX_new)+','+str(startY_new)+')+('+str(endX_new)+','+str(endY_new)+')')
    # we need a tuple (could have used a list instead with [] instead of () ) to store and return the final calculated start and end x and y points as these will need to be returned
    return (startX_new, startY_new, endX_new, endY_new);
# END def fnPlotLines
# -----------------------------------------------------------------------------

# define our command line arguments
parser = argparse.ArgumentParser(description='Generate line graph objects.')
parser.add_argument('-s', action='store', dest='scale', type=int, default=2, help='scale factor (how big to render, default = 2, ie: window will be 200x200px)')
parser.add_argument('-t', action='store', dest='step', type=int, default=5, help='step value (default= 5)')
parser.add_argument('-w', action='store', dest='timerwait', type=int, default=2, help='amount of time in seconds to display final image for (default = 2)')
parser.add_argument('-x', action='store', dest='slowrender', type=int, default=0, help='Number of ms to pause between rendering each line (used to slow down rendering to aid in debugging) (default = 0)')

parser.add_argument('-r', action='store', dest='renderlines', choices=('y','n'), default='y', help='PERFORMANCE render line by line? (y) or display finished object (n) - it takes time to render line by line (default=y)')
parser.add_argument('-o', action='store', dest='outputimage', choices=('y','n'), default='n', help='Output the generated image as a PNG (default=n)')
parser.add_argument('-l', action='store', dest='outputlog', choices=('y','n'), default='n', help='Output co-ordinates to the log (default=n)')

args = parser.parse_args()

# Define the variables that will be needed - some of these are calculated based on the scale value
iterations = 100*args.scale + 5 # the +5 is here to make the last line (straight, y to y)
resx = 100*args.scale*2 # the screen resolution x and y will need to be twice that of the object to be rendered as we render 4 objects
resy = 100*args.scale*2
logFilename = 'lines.log'

lineColour = 0,0,255

# open a pygame screen on which to render our objects
screen = pygame.display.set_mode([resx,resy],0,32)

# Draw a series of lines to render a cross
fnAppend2Log('Top left quarter co-ordinates:')
sx, sy, ex, ey = fnPlotLines(100*args.scale, 0, 100*args.scale, 100*args.scale, 0, 1, -1, 0 )
fnAppend2Log('Bottom left quarter co-ordinates:')
sx, sy, ex, ey = fnPlotLines(ex, ey, sx, sy, 1, 0, 0, 1 ) # the start x,y co-ordinate is equivalent to the end x,y co-ordinate from the last quarter that was rendered
fnAppend2Log('Bottom right quarter co-ordinates:')
sx, sy, ex, ey = fnPlotLines(ex, ey, sx, sy, 0, -1, 1, 0 )
fnAppend2Log('Top right quarter co-ordinates:')
sx, sy, ex, ey = fnPlotLines(ex, ey, sx, sy, -1, 0, 0, -1 )


# if the user has suppressed rendering of each individual line then we need to display the generated shape
if args.renderlines == 'n':
    pygame.display.update();

if args.outputimage == 'y':
    pygame.image.save(screen, 'lineimage.png')

# wait for a period of time (configurable on command line) displaying the image        
pygame.time.wait(args.timerwait*1000)
