import requests
from django.shortcuts import render
from .models import City

# Create your views here.


def index(request):
    appid = '60df5caa0b880580fcc637509dbe92ac'
    cities = City.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+appid

    all_cities =  []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"],
        }
        all_cities.append(city_info)



    context = {
        'all_info': all_cities,
    }


    return render(request, 'weather/index.html', context)