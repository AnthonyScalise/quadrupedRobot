from motors import *
import keyboard
import os


def testWith(program):
    def runTestProg():
        os.system('sudo python3 '+program+'.py')

    threading.Thread(target=a).start()
    threading.Thread(target=emergancyStop).start()


def emergancyStop():
    while True:
        try:
            if keyboard.is_pressed(' '):
                print('\n\n')
                print('------------------------------------------------------')
                print('---------------------  E STOP  -----------------------')
                print('------------------------------------------------------')
                while True:
                    for i in [2, 5, 8, 11]:
                        motorList[i].setDeg(45)
                        for i in [1, 4, 7, 10]:
                            motorList[i].setDeg(135)
                        for i in [0, 3, 6, 9]:
                            motorList[i].setDeg(90)
        except:
            break


def moveJoint():
    def getInput():
        try:
            print('\n')
            motorSelection = int(input('Motor \#:  '))
            degSelection = int(input('Degree:  '))
            motorList[motorSelection].setDeg(degSelection)
            print('Set motor '+str(motorSelection)+' to '+str(degSelection)+' degrees')
        except:
            break

    while True:
        threading.Thread(target=getInput).start()
        threading.Thread(target=emergancyStop).start()
