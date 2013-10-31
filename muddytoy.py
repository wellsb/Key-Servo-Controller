#!/usr/bin/env python 

from Adafruit_PWM_Servo_Driver import PWM
import sys, time, random

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def adaSetup():
	global pwm
	pwm = PWM(0x40, debug=True)
	pwm.setPWMFreq(60)

def QuitIt():
	sys.exit()

def moveSet(pos, addr, lower, upper):
	global pwm
	pwm.setPWM(addr, 0, pos)

def steppos():
	#260,190 - 320,190 - 345,200 - 360,200 - 365,200 - 365,185 - 350,185 - 365,185 - 375,185 - 350, 185 - 320,185

	xlist = [260,320,345,360,365,365,350,365,375,350,320]
	ylist = [190,190,200,200,200,185,185,185,185,185,185,185]

	ycursor = 0

	for this_xshift in xlist:
		moveSet(this_xshift, 14, lower, upper)
		moveSet(ylist[ycursor], 15, lower, upper)
		ycursor = ycursor + 1
		print ("this_xshift: " + str(this_xshift))
		print ("ylist: " + str(ylist[ycursor]))
		time.sleep(3)
		
def getInput():
	got = int(raw_input('--> '))
	return got

def action(key):
	global xpos, ypos, speed, step, lower, upper
	if key == 'i':
		pos = getInput()

	if key == 'w':
		if xpos <= upper:
				xpos = xpos + step
				moveSet(xpos, 14, lower, upper)
		else:
			pos = lower
			print "Too low"

	if key == 's':
		if xpos >= lower:
			xpos = xpos - step
			moveSet(xpos, 14, lower, upper)
		else:
			xpos = upper
			print "Too high"		
		
	if key == 'a':
		if ypos >= lower:
				ypos = ypos - step
				moveSet(ypos, 15, lower, upper)
		else:
			ypos = lower
			print "Too low"

	if key == 'd':
		if ypos <= upper:
			ypos = ypos + step
			moveSet(ypos, 15, lower, upper)
		else:
			ypos = upper
			print "Too high"
#speed
	if key == 'l':
		speed = speed - 0.01
		print (speed)
	if key == 'k':
		speed = speed + 0.01
		print (speed)
#step
	if key == 'n':
		step = step - 1
		print ("Step: " + str(step))
	if key == 'm':
		step = step + 1
		print ("Step: " + str(step))

	if key == 'o':
		pos = upper
	if key == 'p':
		#pos = 130 # ada
		pos = lower #crap
	if key == '1':
		prog01(lower, upper)
	if key == '2':
		prog02(lower, upper)
	if key == '3':
		prog03(lower, upper)
	if key == 'q':
		print "Exit"
		QuitIt()
	print "Xpos: " + str(xpos) + "\nYpos: " + str(ypos)
	print ("step: " + str(step))
	

#getch = _Getch()
adaSetup()

speed = 0.15
step = 5
upper = 630 #ada large servo
#lower = 130 #ada large servo
lower = 190 #crap
xpos = 420
ypos = 420
intev = 0.001

while True:
	steppos()
	#for n in range(1, 20):
		#print ("offer exit" +str(n))
		#if getch() == 'q':
			#action(getch())
		#else:
			#continue
	print "after loop"
	time.sleep(0.1)
