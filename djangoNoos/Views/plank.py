
from django.http import HttpResponse
from django.shortcuts import render
import djangoNoos.Backend.dataManager as data
from djangoNoos.Backend.graphicsManager import GraphicsManager

def getPage(request):
    print(request)
    plankId = str(request).split("ID=")[1].split("'>")[0]
    pageLocation = "plankDetails.html"

    contextJson = {'ID': plankId,
                   'statusMessage': 0
                   }

    dataManager = data.TSDataManager()
    percentageMatrices = dataManager.getMatrixAsPercentagesFromID(plankId, n=200)

    graphName = f"Images/Specification-{plankId}.png"
    GraphicsManager.saveFillGradeTimeLine(plankId, graphName)



    return render(request, pageLocation, context=contextJson)

    # return HttpResponse(f"You requested: {plankId}")