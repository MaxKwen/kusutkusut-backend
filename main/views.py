from django.shortcuts import render
from .models import Person, Tweet

nama_mhs = "depelemon"

def index(request):
    persons = Person.objects.all().name()
    tweets = Tweet.objects.all().content()

    response = {'name' : nama_mhs, 'persons' : persons, 'tweets' : tweets}
    return render(request, 'index.html', response)

