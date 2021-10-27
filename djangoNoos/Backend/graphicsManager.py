import json

import numpy as np
from PIL import Image, ImageDraw
from djangoNoos.Backend.dataManager import TSDataManager
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

zoneSeperationMatrix = [
    [],
    [0],
    [0, 4],
    [0, 3, 5],
    [0, 2, 4, 6]
]


def getZone(x, productList):
    zoneSeperationList = zoneSeperationMatrix[len(productList)]
    if x == 0:
        return 0
    for i in range(len(zoneSeperationList)):
        if x < zoneSeperationList[i]:
            return i - 1
    return i


class GraphicsManager:

    @staticmethod
    def SaveOffsetHeatmap(matrix, name):
        # start canvassing
        imageH = 50 * len(matrix) + 1
        imageW = 50 * len(matrix[0]) + 1
        heatmapcolors = ["#6FEB6F", "#B0F2B4", "#FFE15C", "#DE6C3F", "#BC412B"]
        img = Image.new('RGB', (imageW, imageH), color='white')
        d = ImageDraw.Draw(img)

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                text = f"{matrix[y][x]}%"
                twentyPercentile = min(abs(5 - (matrix[y][x] + 10) // 20), 4)

                rect = [(x * 50, y * 50), ((x + 1) * 50, (y + 1) * 50)]
                if matrix[y][x] == -1:
                    d.rectangle(rect, fill="lightgray", outline="black")
                    d.text((x * 50 + 18, y * 50 + 20), "-%", fill="#000000")
                else:
                    d.rectangle(rect, fill=heatmapcolors[twentyPercentile], outline="black")
                    d.text((x * 50 + 18, y * 50 + 20), text, fill="#000000")

        img.save(name)

    @staticmethod
    def SaveHeatMapFillGrade(matrix, name):
        # simplify matrix to sensor pairs
        simplifiedMatrix = []

        for y in range(len(matrix)):
            ls = []
            for x in range(0, len(matrix[0]), 2):
                # store average of sensor pair in designated location of simplified matrix
                # print(f"Location: x{int(x//2)}:y{y} = {int((matrix[y][x] + matrix[y][x+1])/2)}")
                average = int((matrix[y][x] + matrix[y][x + 1]) / 2)
                ls.append(average)
            simplifiedMatrix.append(ls)

            print(f"simplifiedMatrix at iteration y:{y}")
            for row in simplifiedMatrix:
                print(row)
            print("\n")

        print("simplifiedMatrix after calculations")
        for row in simplifiedMatrix:
            print(row)
        print("\n")

        # start canvassing
        heatmapcolors = ["#6FEB6F", "#B0F2B4", "#FFE15C", "#DE6C3F", "#BC412B"]
        img = Image.new('RGB', (201, 251), color='white')
        d = ImageDraw.Draw(img)

        for y in range(5):
            for x in range(4):
                text = f"{simplifiedMatrix[y][x]}%"
                twentyPercentile = min(abs(5 - (simplifiedMatrix[y][x] + 10) // 20), 4)

                rect = [(x * 50, y * 50), ((x + 1) * 50, (y + 1) * 50)]
                d.rectangle(rect, fill=heatmapcolors[twentyPercentile], outline="black")
                d.text((x * 50 + 18, y * 50 + 20), text, fill="#000000")

        img.save(name)

    @staticmethod
    def saveFillGradeTimeLine(ID, name):

        datamanager = TSDataManager()
        matrices = datamanager.getLastNMatricesWithTimeStampByIDPerMinute(ID)

        # get list of timestamps
        timeStamps = []
        for row in matrices:
            timeStamps.append(row[1])

        print(f"\n\n\nsaveFillGradeTimeline() engaged amd found {len(matrices)} hits")

        # percentify each matrix,
        percentMatrices = datamanager.convertMatricesAsPercentagesByIDFilteringTimeStamps(ID, matrices)
        print(percentMatrices)

        # get amount of zones we're working with
        productListAsString = datamanager.getProductList(ID)
        amountOfZones = len(datamanager.getProductList(ID))

        # loop over every percent matrix to prepare for visualization
        percentageSnapshots = []
        for matrix in percentMatrices:  # for processed matrix from every NoosPoint

            percSnap = []  # create container to store values for averaging out at a later point
            for i in range(amountOfZones):
                percSnap.append([])

            for row in matrix:  # loop over every row of the Noos Datapoint and append value to designated percentageSnapshot adress
                for x in range(len(row)):
                    perc = row[x]
                    if perc >= 0:
                        zone = getZone(x, productListAsString)
                        #print(f"Perc: {perc}, Zone: {zone}")
                        percSnap[zone].append(perc)



            # reduce lists to their average
            percSnap = list(map(lambda v: int(round(sum(v)/len(v))), percSnap))
            percentageSnapshots.append(percSnap)

        for i in range(len(percentageSnapshots)):
            pass
            #print(f"{percentageSnapshots[i]} at {timeStamps[i]}")

        plt.ylim([0, 100])
        plt.plot(list(reversed(timeStamps)), list(reversed(percentageSnapshots)))
        plt.title(f'Fillgrade over time for {ID}')
        plt.xticks(np.arange(0, len(timeStamps) + 1, 20), rotation=90)
        plt.xlabel('Time')
        plt.ylabel('Fillgrade')
        plt.savefig(name)


