
from django.http import HttpResponse


def getPage(request):
    print(request)
    plankId = str(request).split("ID=")[1].split("'>")[0]

    return HttpResponse(f"You requested: {plankId}")