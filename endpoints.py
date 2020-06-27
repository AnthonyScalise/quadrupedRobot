# This class handles all inverse kinematics endpoint functions for motors.py to use

import math

footLen = 67.328 #mm
legLen = 51.446 #mm
hipLen = 27.40 #mm

hipHeight = 30 #mm

minX = -48.594 #mm
maxX = 161.283 #mm
minY = 0 #mm
maxY = 161.283 #mm
minZ = -132.27209 #mm
maxZ = 133.883 #mm

class Endpoint:
    def __init__(self, leg):
        self.leg = leg
        self.x = 0
        self.y = 0
        self.z = 0
        self.legFootPlaneX = 0
        self.legFootPlaneY = 0
        self.legFootPlaneHypo = 0
        self.footDeg = 0
        self.legDeg = 0
        self.hipDeg = 0

    def setPointUpDown(self, x, y, z, legDegree):
        self.x = x
        self.y = y
        self.z = z
        self.legDeg = legDegree
        self.hipDeg = math.degrees(math.atan(self.y / self.x))
        self.legFootPlaneX = ((self.x * math.cos(math.radians(self.hipDeg)))-hip)
        self.legFootPlaneY = self.z - hipHeight
        self.legFootPlaneHypo = math.sqrt((math.pow(self.legFootPlaneX, 2)+math.pow(self.legFootPlaneY, 2)))
        self.footDeg = math.degrees(math.asin((math.sin(math.radians(legDegree))/foot)*self.legFootPlaneHypo))

    #def setPositionForwardBack(self, x, y, z, ):

    def solveKinematics(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.hipDeg = math.degrees(math.atan2(y, x))
        legDegreeA = (math.atan2(z, legLen))
        legDiag = math.sqrt(math.pow(legLen, 2) + math.pow(x, 2))
        legDegreeB = math.acos((math.pow(legLen, 2) + math.pow(legDiag, 2) - math.pow(footLen, 2))/(2 * legLen * legDiag))
        self.legDeg = math.degrees(legDegreeA+legDegreeB)
        self.footDeg = math.degrees(math.acos((math.pow(legLen, 2) + math.pow(footLen, 2) - math.pow(legDiag, 2))/(2 * legLen * footLen)))

    def getFootDeg(self):
        return self.footDeg

    def getLegDeg(self):
        return self.legDeg

    def getHipDeg(self):
        return self.hipDeg

endpointList = [Endpoint(i) for i in range(4)]

def getEndpointList():
    return endpointList
