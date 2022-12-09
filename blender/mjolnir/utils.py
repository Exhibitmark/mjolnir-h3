import math

# Takes the euler angle, snaps it to the nearest snap angle and returns the angle in radians   
def snapping(input, snap_angle):
    input = math.degrees(snap_angle)
    return math.radians(snap_angle * round( input / snap_angle ))

def setBit(n, bitIndex):
    bitMask = 1 << bitIndex
    return n | bitMask

def getFlagsVal(flag,val = 0):
    for x in range(len(flag)):
        if flag[x]:
            val = setBit(val,x)
    return val