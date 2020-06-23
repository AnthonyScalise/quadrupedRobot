# motors.py This file holds all data for all motors and acts as an interface between degree notation and pwm servo control

import adafruit_pca9685
import time
import json

pwm = adafruit_pca9685.PCA9685()
pwm.set_pwm_freq(60)

class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.speed = 0 # a good medium speed is (0.000001)
        self.position = 370 # defualt positions of motors to protect from bottoming out
        self.degree = 0 # list of degree interpreted positions
        self.degreeConversionNum = 0 # this is the scale for converting pos into deg
        self.mode = 0
        self.degreeRange = 0
        self.ninety = 0
        self.mid = 0
        self.max = 0
        self.min = 0
        self.direction = 0

    def getDegPos(self):
        return self.degree

    def posToDeg(self, pos):
        deg = 0
        if(self.direction==1):
            deg = (pos-self.min)
        if(self.direction==(-1)):
            deg = (pos-self.max)
        deg = int(deg*self.degreeConversionNum)
        return deg

    def mapValue(self, value):
        degMax = self.degreeRange
        degMin = 0
        if(self.direction == 1):
            posMax = self.max
            posMin = self.min
        if(self.direction == -1):
            posMax = self.min
            posMin = self.max
        degSpan = degMax - degMin
        posSpan = posMax - posMin
        valueScaled = float(value - degMin) / float(degSpan)
        return int(posMin + (valueScaled * posSpan))

    def setSpeed(self, speed):
        self.speed = speed

    def setDeg(self, degTarget):
        target = self.mapValue(degTarget)
        self.degree = target
        self.setPos(target)
#       if(self.channel in [0, 3, 6, 9]):
#           target = (degTarget-38)
#       self.degree = target
#       self.setPos(target)


    def setPos(self, target):
        if(self.speed == 0):
            self.position = target
            self.degree = self.posToDeg(target)
            pwm.set_pwm(self.channel, 0, target)
        else:
            direction = 1
            if(self.position >= target):
                direction = -1
            for pos in range(self.position, (target+1), direction):
                self.position = pos
                self.degree = self.posToDeg(pos)
                pwm.set_pwm(self.channel, 0, pos)
                time.sleep(self.speed)

motorList = [Motor(i) for i in range(12)] # one dimentional list of all motor objects
positions = [motorList[i].position for i in range(12)] # list of all positions in motorList order

def syncSaves():
    if(positions == [370 for i in range(12)]):
        print('Initializing bot motors...\n')
        with open('calibrationProfile.txt') as limits_file:
            limitProfile = json.load(limits_file)
        i=0
        for motor in motorList:
            motor.min = limitProfile['min'][i]
            motor.max = limitProfile['max'][i]
            motor.mid = limitProfile['mid'][i]
            if(motor.min < motor.max):
                motor.mode = (motor.max-motor.min)
                motor.ninety = (motor.mid-motor.min)
                motor.direction = 1
            if(motor.max < motor.min):
                motor.mode = (motor.min-motor.max)
                motor.ninety = (motor.mid-motor.max)
                motor.direction = -1
            i+=1
        #feet
        i=0
        while(i<12):
            motorList[i].degreeConversionNum = (180/motorList[i].mode)
            motorList[i].degreeRange = 180
            i+=3
        #legs
        i=1
        while(i<12):
            motorList[i].degreeConversionNum = (180/motorList[i].mode)
            motorList[i].degreeRange = 180
            i+=3
        #hips
        i=2
        while(i<12):
            motorList[i].degreeConversionNum = (90/motorList[i].mode)
            motorList[i].degreeRange = 90
            i+=3
        initialSit()

def initialSit():
    stance = [320, 612, 544, 428, 146, 208, 288, 174, 213, 324, 570, 519]
    for i in range(12):
        motorList[i].setPos(stance[i])

def getMotors(): # Returns a multidimentional table of the motors respective to their legs
    motors = []
    cols=0
    while(cols<12):
        motors.append([])
        for rows in range(3):
            motors[int(cols/3)].append(motorList[cols+rows])
        cols+=3
    return(motors)

def godLog():
    for motor in motorList:
        print('Motor:'+str(motor.channel)+' Speed:'+str(motor.speed)+' Position:'+str(motor.position)+
        ' Degree:'+str(motor.degree)+' DegreeConversionNum:'+str(round(motor.degreeConversionNum, 7))+' mid:'+
        str(motor.mid)+' min:'+str(motor.min)+' max:'+str(motor.max)+' Mode:'+str(motor.mode)+' NinetyRange:'+
        str(motor.ninety)+' Direction:'+str(motor.direction)+' DegreeRange:'+str(motor.degreeRange)+'\n')

if True:
    syncSaves()
#    godLog()
