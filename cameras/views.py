from django.shortcuts import render


def camera_01(request):
        return render(request, 'cameras/01.html', {})
