from motors import *
import math

# dimentions in mm
hip = 27
leg = 54
foot = 80

xyz = [[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]],[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]],[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]],[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]]
# Legs*************
# ******Joints*****
# **************xyz

def calcHip():
    i = 2
    while(i<12):
        xyz[int((i-2)/3)][2][0] = (hip*(math.cos(math.radians(motorList[i].getDegPos()))))
        xyz[int((i-2)/3)][2][1] = (hip*(math.sin(math.radians(motorList[i].getDegPos()))))
        xyz[int((i-2)/3)][2][2] = 26 #height from bottom of frame is 26mm
        i+=3

def calcLeg():
    i = 1
    while(i<12):
        legDegree = (motorList[i].getDegPos())
        hipDegree = (motorList[i+1].getDegPos())
        legProjectionHeight = 0
        legProjectionLen = 0
        if(legDegree<=90):
            legProjectionLen = (leg*(math.sin(math.radians(legDegree))))
            legProjectionHeight = ((leg*(math.cos(math.radians(legDegree))))*(-1))
        if(legDegree>90 and legDegree<=180):
            legProjectionLen = (leg*(math.cos(math.radians(legDegree-90))))
            legProjectionHeight = (leg*(math.sin(math.radians(legDegree-90))))
        if(legDegree>180):
            legProjectionLen = ((leg*(math.sin(math.radians(legDegree-180))))*(-1))
            legProjectionHeight = (leg*(math.cos(math.radians(legDegree-180))))
        xyz[int((i-1)/3)][1][0] = ((legProjectionLen*(math.cos(math.radians(hipDegree))))+(hip*(math.cos(math.radians(motorList[i+1].getDegPos())))))
        xyz[int((i-1)/3)][1][1] = ((legProjectionLen*(math.sin(math.radians(hipDegree))))+(hip*(math.sin(math.radians(motorList[i+1].getDegPos())))))
        xyz[int((i-1)/3)][1][2] = (legProjectionHeight+(26))
        i+=3

def calcFoot():
    i = 0
    while(i<12):
        footProjectionLen = 0
        footProjectionHeight = 0
        hipAngle = (motorList[i+2].getDegPos())
        extendedAngle = ((motorList[i].getDegPos()-38)+motorList[i+1].getDegPos())
        legFootLen = ((foot*(math.sin(math.radians(extendedAngle))))+(leg*(math.sin(math.radians(motorList[i+1].getDegPos())))))
        xyz[int(i/3)][0][0] = (legFootLen*(math.cos(math.radians(hipAngle))))
        xyz[int(i/3)][0][1] = (legFootLen*(math.sin(math.radians(hipAngle))))
        xyz[int(i/3)][0][2] = (((foot*(math.cos(math.radians(extendedAngle))))+(leg*(math.cos(math.radians(motorList[i+1].getDegPos())))))+(26))
        i+=3

#def kinLegUp():



#def kinLegDown():



#def kinLegOut():



#def kinLegIn():


def printOutData():
    calcHip()
    calcLeg()
    calcFoot()
    print('Current XYZ coordinates:\n')
    a=0
    while(a<12):
        print('         Leg ' + str(a/3) + ':')
        b=0
        while(b<3):
            if(b==0):
                print('Foot:')
            if(b==1):
                print('Leg:')
            if(b==2):
                print('Hip:')
            c=0
            while(c<3):
                if(c==0):
                    print('  X:', end=' ')
                if(c==1):
                    print('  Y:', end=' ')
                if(c==2):
                    print('  Z:', end=' ')
                print(str(xyz[int(a/3)][b][c]))
                c+=1
            b+=1
        print('\n')
        a+=3


if True:
    printOutData()
