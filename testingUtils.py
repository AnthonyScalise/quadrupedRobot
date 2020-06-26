from threading import Thread
from motors import *
import keyboard
import os

#active = True

def testWith(program):
    os.system('sudo python3 '+program+'.py&')
    emergancyStop()


def emergancyStop():
    print('\n\n')
    print('------------------------------------------------------')
    print('---------------------  E STOP  -----------------------')
    print('------------------------------------------------------')
    for i in [2, 5, 8, 11]:
        motorList[i].setDeg(45)
    for i in [1, 4, 7, 10]:
        motorList[i].setDeg(135)
    for i in [0, 3, 6, 9]:
        motorList[i].setDeg(90)
    while True:
        estop()


def moveJoint():
    while True:
        print('\n')
        motorSelection = input('Motor Channel:  ')
        if motorSelection == ' ':
            emergancyStop()
        else:
            motorSelection = int(motorSelection)
        degSelection = input('Degree:  ')
        if degSelection == ' ':
            emergancyStop()
        else:
            degSelection = int(degSelection)
        motorList[motorSelection].setDeg(degSelection)
        print('Set motor '+str(motorSelection)+' to '+str(degSelection)+' degrees')


if True:
    print('\n\n')
    print('Estop Enabled\n')
    moveJoint()
