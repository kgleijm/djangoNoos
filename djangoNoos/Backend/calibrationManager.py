import json
from time import sleep

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from djangoNoos.Backend import webAdapter
import djangoNoos.Backend.dataManager as data



def calibrate(request):

    #print("calibration function engaged for\n", request)

    if request.is_ajax():
        if request.method == 'POST':
            # print(f'Raw Data: {request.body}')

            # decode incoming json as bytestring to dict
            asString = str(request.body.decode('utf-8'))
            asPairList = asString.split("&")
            incoming = dict()
            for pair in asPairList:
                key, value = pair.split("=")
                incoming[key] = value
            print("incoming as a dict", incoming)

            # check what kind of calibration is requested
            if "calibrate" in incoming:
                if incoming["calibrate"] == "Empty" or incoming["calibrate"] == "Full":

                    dataManager = data.TSDataManager()

                    initialDataPoints = dataManager.getAmountOfPointsByID(incoming["ID"])
                    target = initialDataPoints + 4
                    webAdapter.sendCalibrationRequestTo(incoming["ID"])
                    timeElapsed = 0
                    while(dataManager.getAmountOfPointsByID(incoming["ID"]) < target):
                        sleep(1)
                        timeElapsed += 1
                        if timeElapsed >= 10:
                            return JsonResponse({}, status=400)
                    return JsonResponse({}, status=200)

            else:
                print("No specified calibration request found while calibrationManager got engaged")
                return JsonResponse({}, status=500)

            # delegate update task to webAdapter





    return JsonResponse({}, status=200)
