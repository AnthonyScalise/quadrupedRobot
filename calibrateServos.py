import adafruit_pca9685
import json
import time
from motors import *

# Uncomment to enable logging
#import logging
#logging.basicConfig(level=logging.DEBUG)

adjustSize = 2

with open('calibrationConfig.txt') as calibration_profile:
    saves = json.load(calibration_profile)

dataSets = [saves["zero"], saves["fourtyFive"], saves["ninety"], saves["maximum"]]
dataSetNames = ["zero", "fourtyFive", "ninety", "maximum"]
messages = ['Calibrating 0 degrees Servo ', 'Calibrating 45 degrees Sevo ', 'Calibrating 90 degrees Servo ', 'Calibrating Max degrees Servo ']
conversions = [0 for i in range(12)]

pwm = adafruit_pca9685.PCA9685()
pwm.set_pwm_freq(60)

def dealJson():
    data = {}
    for i in range(4):
        data[dataSetNames[i]] = dataSets[i]
    with open('calibrationConfig.txt', 'w') as outfile:
        json.dump(data, outfile)

def calculateDegreeConversion(servo):
    if(dataSets[0][servo] < dataSets[3][servo]):
        fourtyFiveRange = (((dataSets[1][servo]-dataSets[0][servo])+(dataSets[2][servo]-dataSets[1][servo]))/2)
        ninetyRange = (dataSets[2][servo]-dataSets[0][servo])
    if(dataSets[3][servo] < dataSets[0][servo]):
        fourtyFiveRange = (((dataSets[1][servo]-dataSets[2][servo])+(dataSets[0][servo]-dataSets[1][servo]))/2)
        ninetyRange = (dataSets[0][servo]-dataSets[2][servo])
    degreeConversion = (((45/fourtyFiveRange)+(90/ninetyRange))/2)
    return degreeConversion

possibleKeys = [' ', 'w', 's']
def checkKeyPress():
    val = input('--> ')
    if val in possibleKeys:
        return(possibleKeys.index(val))
    else:
        return(3)

print('\n\nCalibrating servos...\n ')
while True:
    done = False
    while(not done):
        print('Adjustment step size: ' + str(adjustSize))
        key = checkKeyPress()
        while(key==3):
            key = checkKeyPress()
        if(key==0):
            done = True
        if(key==1):
            adjustSize += 1 
        if(key==2):
            adjustSize -= 1

    for i in range(12):
        for m in range(4):
            done = False
            print('\n')
            print(messages[m] + str(i) + ':')
            while(not done):
                pwm.set_pwm(i, 0, dataSets[m][i])
                print(str(dataSets[m][i]))
                key = checkKeyPress()
                while(key==3):
                    key = checkKeyPress()
                if(key==0):
                    done = True
                elif(key==1):
                    dataSets[m][i] += adjustSize
                elif(key==2):
                    dataSets[m][i] -= adjustSize
            pwm.set_pwm(i, 0, dataSets[m][i])
    print('\n')
    dealJson()
    for i in range(12):
        print('Servo ' + str(i) + '  Zero: ' + str(dataSets[0][i]) + '  FourtyFive: ' + str(dataSets[1][i]) + 
              '  Ninety: ' + str(dataSets[2][i]) + '  Max: ' + str(dataSets[3][i])  + '  DegreeConversion: ' + str(calculateDegreeConversion(i)) + '\n')
    print('\n\n')
