# motors.py This file holds all data for all motors and acts as an interface between degree notation and pwm servo control

import adafruit_pca9685
import time
import json
import endpoints

pwm = adafruit_pca9685.PCA9685()
pwm.set_pwm_freq(60)

class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.speed = 0 # a good medium speed is (0.000001)
        self.position = 370 # defualt positions of motors to protect from bottoming out
        self.degree = 0 # list of degree interpreted positions
        self.degreeConversionNum = 0 # this is the scale for converting pos into deg
        self.degreeMax = 180
        self.degreeMin = 0
        if(self.channel in [2, 5, 8, 11]): # sets limits for shoulders
            up = 90
            low = 0
        if(self.channel in [1, 4, 7, 10]): # sets limits for legs
            up = 180
            low = 0
        if(self.channel in [0, 3, 6, 9]): # sets limits for feet
            up = 164
            low = 53
        self.degUpLimit = up
        self.degLowLimit = low
        self.mode = 0
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
        degSpan = self.degreeMax - self.degreeMin
        posSpan = self.max - self.min
        valueScaled = float(value - self.degreeMin) / float(degSpan)
        return int(self.min + (valueScaled * posSpan))


    def setSpeed(self, speed):
        self.speed = speed


    def setDeg(self, degTarget):
        if degTarget > self.degUpLimit:
            degTarget = self.degUpLimit
        if degTarget < self.degLowLimit:
            degTarget = self.degLowLimit
        target = self.mapValue(degTarget)
        self.degree = target
        self.setPos(target)


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
legList = [[motorList[i] for i in range(3)], [motorList[i] for i in range(3, 6)], [motorList[i] for i in range(6, 9)], [motorList[i] for i in range(9, 12)]]


def setLegPos(legNum, speed=0, hipSpeed=0, hipAng=0, legSpeed=0, legAng=0, footSpeed=0, footAng=0):
    directions = [1, 1, 1]
    targets = [footAng, legAng, hipAng]
    joints = [legList[legNum][i] for i in range(3)]
    if(speed == 0 and hipSpeed == 0 and legSpeed == 0 and footSpeed == 0):
            for i in range(3):
                joints[i].setDeg(targets[i])
            return
    elif((speed == 0) and (hipSpeed != 0 or legSpeed != 0 or footSpeed != 0)):
        speeds = [footSpeed, legSpeed, hipSpeed]
    elif(speed != 0):
        speeds = [speed, speed, speed]
    for i in range(3):
        if(joints[i].degree >= targets[i]):
            directions[i] = -1
    while((joints[0].degree != targets[0]) or (joints[1].degree != targets[1]) or (joints[2].degree != targets[2])):
        for i in range(3):
            if(joints[i].degree != targets[i]):
                joints[i].setDeg(joints[i].degree + directions[i])
                time.sleep(speeds[i])


def syncSaves():
    print('Initializing bot motors...\n')
    with open('calibrationProfile.txt') as limits_file:
        limitProfile = json.load(limits_file)
    for motor in motorList:
        i = motor.channel
        motor.min = limitProfile['min'][i]
        motor.max = limitProfile['max'][i]
        motor.mid = limitProfile['mid'][i]
        if(motor.min < motor.max):
            motor.mode = (motor.max-motor.min)
            motor.direction = 1
        if(motor.max < motor.min):
            motor.mode = (motor.min-motor.max)
            motor.direction = -1
    for i in range(12):
        motorList[i].degreeConversionNum = (180/motorList[i].mode)


def initialSit():
    stance = [320, 612, 544, 428, 146, 208, 288, 174, 213, 324, 570, 519]
    for i in range(12):
        motorList[i].setPos(stance[i])


def getMotorsTable(): # Returns a multidimentional table of the motors respective to their legs
    motors = []
    cols=0
    while(cols<12):
        motors.append([])
        for rows in range(3):
            motors[int(cols/3)].append(motorList[cols+rows])
        cols+=3
    return(motors)


def moveUpAndDownTest():
    print('Moving up and down test\n')
    while True:
        height = int(input('    Enter a height in mm: '))
        for point in endpointList:
            point.setPointUpDown(50, 50, height, legDegree=45)
            setLegPos(point.leg, hipAng=point.getHipDeg, legAng=point.getLegDeg, footAng=point.getFootDeg)
        print('\n')


def Logs():
    for motor in motorList:
        print('Motor:'+str(motor.channel)+' Speed:'+str(motor.speed)+' Position:'+str(motor.position)+
        ' Degree:'+str(motor.degree)+' DegreeConversionNum:'+str(round(motor.degreeConversionNum, 7))+' mid:'+
        str(motor.mid)+' min:'+str(motor.min)+' max:'+str(motor.max)+' Mode:'+str(motor.mode)+' Direction:'+
        str(motor.direction)+' DegreeRange:'+str(motor.degreeRange)+'\n')


if True:
    syncSaves()
#    moveUpAndDownTest()
#    initialSit()
    Logs()
