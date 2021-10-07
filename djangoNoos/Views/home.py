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
    for plank in planks:
        plankList.append(str(plank))

    contextJson = {'planks': plankList}
    context = Context(contextJson)

    return render(request, pageLocation, context=contextJson)


    #for plank in planks:
    #    response += f"<div class=\"noosWidgetHome\"><img src=\"Images/py.png\">{str(plank)}</div>"

    #return HttpResponse("Hello, you're at home!<br>" + response)
