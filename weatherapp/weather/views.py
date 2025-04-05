import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.http import HttpResponse

# Create your views here.


appid = '60df5caa0b880580fcc637509dbe92ac'
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

wide_cities = []


def index(request):


    if(request.method == 'POST'):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            if not City.objects.filter(name=city_name):
                form.save()

    if City.objects.count() > 5:
        oldest_city = City.objects.first()
        oldest_city.delete()

    form = CityForm()
    all_cities = []

    cities = City.objects.all().order_by('-id')[:5]


    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if "main" in res and "weather" in res:
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"],
            }
            all_cities.append(city_info)
        else:
            print(f"Ошибка получения данных для города: {city.name}")



    context = {
        'all_info': all_cities,
        'form': form,
    }


    return render(request, 'weather/index.html', context)


def info(request):
    cities = City.objects.all().order_by('-id')
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if "main" in res:
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'feels_like': res["main"]["feels_like"],
                'pressure': res["main"]["pressure"],
                'humidity': res["main"]["humidity"],
                'wind': res["wind"]["speed"],
                'clouds': res["clouds"]["all"],
                'icon': res["weather"][0]["icon"],

            }
            if city_info not in wide_cities:
                wide_cities.append(city_info)

    context = {
        'wide_info': wide_cities,
    }

    return render(request, 'weather/info.html' , context)

def doc(request):
    return render(request, 'weather/doc.html')

def support(request):
    return render(request, 'weather/support.html')