#!/usr/bin/env python 

from Adafruit_PWM_Servo_Driver import PWM
import sys, time, random

updown = 4

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
	pwm.setPWMFreq(90) #70 better than 60
	#unused_channels = [1,2,4,5,6,7,8,9,10,11,12,13,14,15]
	#for this_chan in unused_channels:
		#pwm.setPWM(this_chan, 0, 0)

def QuitIt():
	sys.exit()

def moveSet(pos, addr, lower, upper):
	global pwm
	pwm.setPWM(addr, 0, pos)

def prog01(lower, upper):
	global speed, updown
	print "Go Prog01"
	posit = [400,394,397,390,391,395,384,377]
	for n in range(1, 2):
		for this_pos in posit:
			print chr(27) + "[2J"
			print ("speed:" +str(speed) + "\nIteraction: " + str(n) + "\nThis Pos: " + str(this_pos))
			moveSet(this_pos, updown, lower, upper)
			time.sleep(speed)

		for this_pos in reversed(posit):
			print chr(27) + "[2J"
			print ("speed:" +str(speed) + "\nIteraction: " + str(n) + "\nThis Pos: " + str(this_pos))
			moveSet(this_pos, updown, lower, upper)
			time.sleep(speed)

def prog02(lower, upper):
	global speed
	print "Go Prog02"
	for n in range(1, 50):
		this_pos = random.randint(375,400)
		print chr(27) + "[2J"
		print ("speed:" +str(speed) + "\nIteraction: " + str(n) + "\nThis Pos: " + str(this_pos))
		moveSet(this_pos, lower, upper)
		time.sleep(speed)

def prog03(lower, upper):
	global speed
	print "Go Prog03"
	for n in range(375, 410):
		print chr(27) + "[2J"
		print ("speed:" +str(speed) + "\nIteraction: " + str(n) + "\nThis Pos: " + str(n))
		moveSet(n, 0, lower, upper)
		time.sleep(speed)
	for n in range(410, 375, -1):
		print chr(27) + "[2J"
		print ("speed:" +str(speed) + "\nIteraction: " + str(n) + "\nThis Pos: " + str(n))
		moveSet(n, 0, lower, upper)
		time.sleep(speed)
		
def getInput():
	got = int(raw_input('--> '))
	return got

def action(key):
	global xpos, ypos, speed, step, lower, upper
	if key == 'i':
		#pos = getInput()
		moveSet(220, 0, lower, upper)
		moveSet(920, 3, lower, upper)

	if key == 'w':
		if (xpos + step) < upper:
			xpos = xpos + step
			moveSet(xpos, 0, lower, upper)
		else:
			xpos = upper - step
			moveSet(xpos, 0, lower, upper)
			print "Too high, using upper"

	if key == 's':
		if (xpos - step) > lower:
			xpos = xpos - step
			moveSet(xpos, 0, lower, upper) #14
		else:
			xpos = lower + step
			moveSet(xpos, 0, lower, upper) #14
			print "Too low, using lower"		
		
	if key == 'a':
		if ypos >= lower:
				ypos = ypos + step
				moveSet(ypos, 4, lower, upper)
		else:
			ypos = lower
			print "Too low"

	if key == 'd':
		if ypos <= upper:
			ypos = ypos - step
			moveSet(ypos, 4, lower, upper)
		else:
			ypos = upper
			print "Too high"

	if key == 't':
		moveSet(620, 0, lower, upper)
		time.sleep(speed)
		moveSet(660, 0, lower, upper)
		time.sleep(speed)
		moveSet(620, 0, lower, upper)
		time.sleep(speed)

	if key == 'y':
		moveSet(620, 4, lower, upper)
		time.sleep(speed)
		moveSet(580, 4, lower, upper)
		time.sleep(speed)
		moveSet(620, 4, lower, upper)
		time.sleep(speed)

	if key == 'o':
		moveSet(200, 0, lower, upper)
		moveSet(200, 4, lower, upper)

	if key == 'p':
		moveSet(900, 0, lower, upper)
		moveSet(900, 4, lower, upper)

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

	if key == '1':
		prog01(lower, upper)
	if key == '2':
		prog02(lower, upper)
	if key == '3':
		prog03(lower, upper)
	if key == 'q':
		print "Exit"
		QuitIt()
	print chr(27) + "[2J"
	print "Xpos: " + str(xpos) + "\nYpos: " + str(ypos)
	print ("step: " + str(step))
	print ("speed: " + str(speed))
	

getch = _Getch()
adaSetup()

speed = 0.06
step = 10
upper = 940 #ada large servo
lower = 270#195crap

xpos = 420
ypos = 420


while True:
	action(getch())
