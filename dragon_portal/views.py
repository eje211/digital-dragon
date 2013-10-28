from django.http          import HttpResponse

from dragon_portal.models import DragonUser, ParentProfile

def adminParent(request):
    return HttpResponse("Hello, world. I'm a parent profile!")

def profileParent(request):
    return HttpResponse("Hello, world. I'm a parent profile!")

def actionParent(request):
    return HttpResponse("Hello, world. I'm a parent profile!")