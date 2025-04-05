import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.http import HttpResponse

# Create your views here.


def index(request):
    appid = '60df5caa0b880580fcc637509dbe92ac'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

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

    cities = City.objects.all().order_by('-id')[:5]
    all_cities = []

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

        # if len(all_cities) > 5:
        #     all_cities.pop()




    context = {
        'all_info': all_cities,
        'form': form,
    }


    return render(request, 'weather/index.html', context)


def info(request):
    return render(request, 'weather/info.html')