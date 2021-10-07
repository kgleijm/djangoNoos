zoneSeperationMatrix = [
    [],
    [0],
    [0,4],
    [0,3,5],
    [0,2,4,6]
]

def getZone(x, calibrationDict):
    zoneSeperationList = zoneSeperationMatrix[len(calibrationDict)]
    if x == 0:
        return 0
    for i in range(len(zoneSeperationList)):
        if x < zoneSeperationList[i]:
            return i - 1
    return i

print(getZone(7, zoneSeperationMatrix[1]))