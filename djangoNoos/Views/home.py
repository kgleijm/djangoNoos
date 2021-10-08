import os

from django.http import HttpResponse
from django.template import Context, Template
from ..CSS.CSSfile import CSS
from ..Backend.dataManager import TSDataManager
from django.shortcuts import render


def getPage(request):
    print("Home.getPage() got request:")
    print(request)
    #response = CSS
    DataManager = TSDataManager()
    planks = DataManager.getPlanks()

    pageLocation = "overview.html"

    plankList = []
    imgUrlList = []
    IDList = []
    for plank in planks:
        plankPercentages = None

        plankList.append(str(plank))
        imgUrlList.append("Images/py.png")
        IDList.append(plank[0])

        contextlist = zip(plankList, imgUrlList, IDList)

    contextJson = {'planks': contextlist}
    context = Context(contextJson)



    return render(request, pageLocation, context=contextJson)


    #for plank in planks:
    #    response += f"<div class=\"noosWidgetHome\"><img src=\"Images/py.png\">{str(plank)}</div>"

    #return HttpResponse("Hello, you're at home!<br>" + response)
