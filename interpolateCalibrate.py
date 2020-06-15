import adafruit_pca9685
import json
import time
from motors import *

# Uncomment to enable logging
#import logging
#logging.basicConfig(level=logging.DEBUG)

data = {}
data['ninety'] = []
data['maxs'] = []
data['mains'] = []

with open('limitProfile.txt') as json_file:
    saves = json.load(json_file)

ninetys = saves['ninety']
maxs = saves['maxs']
mins = saves['mins']

#ninetys = [370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370]
#maxs = [370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370]
#mins = [370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370]

def dealJson():
    data['ninety'] = ninetys
    data['maxs'] = maxs
    data['mins'] =  mins
    jsonDataFile = json.dumps(data)
    with open('limitProfile.txt', 'w') as outfile:
        json.dump(data, outfile)

adjustSize = 2

pwm = adafruit_pca9685.PCA9685()
pwm.set_pwm_freq(60)


def checkKeyPress():
    val = input('--> ')
    if (val == ' '):
        return(0)
    elif(val == 'w'):
        return(1)
    elif(val == 's'):
        return(-1)
    else:
        return(2)

print('Calibrating interpolation set points...\n ')
while True:
    i = 0
    while(i < 12):
        done = False
        print('\n')
        print('Calibrating 90 degrees servo ' + str(i) + '\n')
        while(not done):
            pwm.set_pwm(i, 0, ninetys[i])
            print(str(ninetys[i]) + '\n')
            key = checkKeyPress()
            while(key == 2):
                key = checkKeyPress()
            if(key == 0):
                done = True
            elif(key == 1):
                ninetys[i] += adjustSize
            elif(key == -1):
                ninetys[i] -= adjustSize
        print('\n')
        print('Calibrating max degrees servo  ' + str(i) + '\n')
        done = False
        while(not done):
            pwm.set_pwm(i, 0, maxs[i])
            print(str(maxs[i]) + '\n')
            key = checkKeyPress()
            while(key == 2):
                key = checkKeyPress()
            if(key == 0):
                done = True
            elif(key == 1):
                maxs[i] += adjustSize
            elif(key == -1):
                maxs[i] -= adjustSize
        print('\n')
        print('Calibrating min degrees servo ' + str(i) + '\n')
        done = False
        while(not done):
            pwm.set_pwm(i, 0, mins[i])
            print(str(mins[i]) + '\n')
            key = checkKeyPress()
            while(key == 2):
                key = checkKeyPress()
            if(key == 0):
                done = True
            elif(key == 1):
                mins[i] += adjustSize
            elif(key == -1):
                mins[i] -= adjustSize
        print('\n\n')
        pwm.set_pwm(i, 0, ninetys[i])
        i += 1

    dealJson()
    i = 0
    while(i < 12):
        print('Servo ' + str(i) + '  Min: ' + str(mins[i]) + '  Max: ' + str(maxs[i]) + '  Ninety: ' + str(ninetys[i]) +'\n')
        i += 1
