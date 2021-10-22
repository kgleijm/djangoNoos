import os

from django.http import HttpResponse
from django.template import Context, Template
from ..CSS.CSSfile import CSS
from ..Backend.dataManager import TSDataManager
from django.shortcuts import render
import djangoNoos.Backend.graphicsManager as gm
GraphicsManager = gm.GraphicsManager

def getPage(request):
    print("Home.getPage() got request:")
    print(request)
    DataManager = TSDataManager()
    planks = DataManager.getPlanks()

    pageLocation = "overview.html"



    plankList = []
    imgUrlList = []
    IDList = []
    contextlist = []
    for plank in planks:
        ID = plank[0]
        graphName = f"Images/Overview-{ID}.png"
        plankPercentages = DataManager.getMatrixAsPercentagesFromID(ID)



        GraphicsManager.SaveOffsetHeatmap(plankPercentages, graphName)


        totalProducts = 28
        sensorsRead = 0
        totalPercentageValue = 0
        unusedSensors = 0
        for y in range(len(plankPercentages)):
            for x in range(len(plankPercentages[0])):
                if plankPercentages[y][x] == -1:
                    unusedSensors += 1
                else:
                    totalPercentageValue += plankPercentages[y][x]
                    sensorsRead += 1
        averagePercentage = (totalPercentageValue/sensorsRead)/100
        amountOfProducts = averagePercentage * totalProducts

        print(f"\n\n\n\n\n\nAmount of products found on {ID}: {amountOfProducts}\n\n\n\n\n\n\n")








        plankList.append(str(plank))
        imgUrlList.append(graphName)
        IDList.append(plank[0])

        contextlist = zip(plankList, imgUrlList, IDList)

    contextJson = {'planks': contextlist}



    return render(request, pageLocation, context=contextJson)


