from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings

@login_required
def index(request):
    # return HttpResponse("¡Bienvenido a la aplicación Django!")
    data = {
        'title': "Landing Page' Dashboard",
    }
    return render(request, 'dashboard/index.html', data)
