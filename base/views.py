from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?appid=19a3b749336622570ba40d7107581f71&q={}"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    form = CityForm()

    weather_data = []

    cities = City.objects.all().order_by('-id')

    for city in cities:
        response = requests.get(url.format(city)).json()
        city_weather = {
            'city_name': city.name,
            'temperature': format((response["main"]["temp"] - 273.15), ".2f"),
            'description': response["weather"][0]["description"],
            'icon': response["weather"][0]["icon"]
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'base/weather_base.html', context)
