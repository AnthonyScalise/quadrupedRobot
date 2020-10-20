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
