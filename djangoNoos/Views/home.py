from django.http import HttpResponse
from ..CSS.CSSgenerator import getCSS

def getPage(request):
    print("Home.getPage() got request:")
    print(request)
    return HttpResponse("Hello, you're at home!")