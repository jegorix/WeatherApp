import requests
from django.shortcuts import render

# Create your views here.


def index(request):
    appid = '60df5caa0b880580fcc637509dbe92ac'
    city = 'London'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={appid}'
    res = requests.get(url).json()

    city_info = {
        'city': city,
        'temp': res["main"]["temp"],
        'icon': res["weather"][0]["icon"],
    }

    context = {
        'info': city_info,
    }


    return render(request, 'weather/index.html', context)