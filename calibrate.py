import adafruit_pca9685
import json
import time
from motors import *

# Uncomment to enable logging
#import logging
#logging.basicConfig(level=logging.DEBUG)

adjustSize = 1
doneList = [2, 5, 8, 11]

with open('calibrationProfile.txt') as calibration_profile:
    saves = json.load(calibration_profile)

dataSets = [saves["min"], saves["mid"], saves["max"]]
dataSetNames = ["min", "mid", "max"]
messages = ['Calibrating 0 degrees Servo ', 'Calibrating 90 degrees Sevo ', 'Calibrating 180 degrees Servo ']

pwm = adafruit_pca9685.PCA9685()
pwm.set_pwm_freq(60)

def dealJson():
    data = {}
    for i in range(3):
        data[dataSetNames[i]] = dataSets[i]
    with open('calibrationProfile.txt', 'w') as outfile:
        json.dump(data, outfile)

possibleKeys = [' ', 'w', 's', 'set']
def checkKeyPress():
    val = input('--> ')
    for x in range(3):
        if possibleKeys[x] == val:
            return(x)
    if val == possibleKeys[3]:
        try:
            return([4, int(input('    Enter num: '))])
        except:
            return(3)
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
        elif(key==1):
            adjustSize += 1
        elif(key==2):
            adjustSize -= 1
        elif(key[0]==4):
            adjustSize = key[1]

    for i in range(12):
        if i in doneList:
            continue
        for m in range(3):
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
                elif(key[0]==4):
                    dataSets[m][i] = key[1]
            pwm.set_pwm(i, 0, dataSets[m][i])
    print('\n')
    dealJson()
    for i in range(12):
        print('Servo ' + str(i) + '  Min: ' + str(dataSets[0][i]) + '  Mid: ' + str(dataSets[1][i]) +
              '  Max: ' + str(dataSets[2][i]) + '\n')
    print('\n\n')
