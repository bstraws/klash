from django.shortcuts import render

def index(request):
    return render(request, 'klash/index.html', {})
