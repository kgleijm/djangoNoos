from django.http import HttpResponse
from ..CSS.CSSgenerator import getCSS
from ..Backend.dataManager import TSDataManager


def getPage(request):
    print("Home.getPage() got request:")
    print(request)
    response = ""
    DataManager = TSDataManager()
    planks = DataManager.getPlanks()
    for plank in planks:
        response += str(plank) + "<br>"

    return HttpResponse("Hello, you're at home!<br>" + response)