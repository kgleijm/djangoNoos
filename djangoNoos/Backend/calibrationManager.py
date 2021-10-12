from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def calibrate(request):

    print("calibration function engaged for\n", request)

    if request.is_ajax():
        if request.method == 'POST':
            print('Raw Data: "%s"' % request.body)

    return JsonResponse({}, status=200)
