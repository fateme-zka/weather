from django.shortcuts import render
import requests


def index(request):
    # if request.method =='POST':
    url = "http://api.openweathermap.org/data/2.5/weather?appid=19a3b749336622570ba40d7107581f71&q={}"
    city = 'tokyo'
    response = requests.get(url.format(city)).json()

    city_weather = {
        'city_name': city,
        'temperature': format((response["main"]["temp"] - 273.15), ".2f"),
        'description': response["weather"][0]["description"],
        'icon': response["weather"][0]["icon"]
    }

    context = {'city_weather': city_weather}

    return render(request, 'base/weather_base.html', context)
