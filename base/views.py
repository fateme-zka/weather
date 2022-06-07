from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?appid=19a3b749336622570ba40d7107581f71&q={}"
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                response = requests.get(url.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully.'
            message_class = 'is-success'

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

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'base/weather_base.html', context)


def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')