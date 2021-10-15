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
    for plank in planks:
        ID = plank[0]
        graphName = f"Images/Overview-{ID}.png"
        plankPercentages = DataManager.getMatrixAsPercentagesFromID(ID)
        GraphicsManager.SaveHeatMapFillGrade(plankPercentages, graphName)



        plankList.append(str(plank))
        imgUrlList.append(graphName)
        IDList.append(plank[0])

        contextlist = zip(plankList, imgUrlList, IDList)

    contextJson = {'planks': contextlist}
    context = Context(contextJson)



    return render(request, pageLocation, context=contextJson)


