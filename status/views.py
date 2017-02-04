from django.http import HttpResponse

def index(request):
    return HttpResponse("Q-Bot IO service is running.")
