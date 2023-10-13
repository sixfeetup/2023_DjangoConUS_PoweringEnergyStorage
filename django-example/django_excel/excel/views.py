from django.http import HttpResponse


def index(request):
    return HttpResponse("Powering Energy Storage Beyond Excel")
