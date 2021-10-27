import json

from django.http import JsonResponse
from djangoNoos.Backend import dataManager


def updateProducts(request):

    if request.is_ajax():
        if request.method == 'POST':
            data = dataManager.TSDataManager()
            incomingAsDict = json.loads(request.body.decode('utf-8'))
            print(f"incomingDict: *{incomingAsDict}*")
            incomingType = incomingAsDict['type']

            print("incoming type", incomingType)
            if incomingType == 'save':
                incomingProductList = str(incomingAsDict['productConfiguration'])
                data.setProductList(incomingAsDict['ID'],incomingProductList)
                return JsonResponse({}, status=200)

            elif incomingType == 'load':
                outgoingProductList = data.getProductList(incomingAsDict['ID'])
                print("outgoing:", outgoingProductList)
                if outgoingProductList == "undefined":
                    outgoingProductList = "[]"
                return JsonResponse({"productList": outgoingProductList}, status=200)
    return JsonResponse({}, status=200)

