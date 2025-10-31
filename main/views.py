from django.shortcuts import render
from django.db.models import Prefetch
from .models import Person, Tweet

nama_mhs = "depelemon"

def index(request):
    # Prefetch only parent tweets (parent_tweet is NULL) and their replies (comments)
    parent_tweets_qs = Tweet.objects.filter(parent_tweet__isnull=True).prefetch_related('comments')

    persons = Person.objects.prefetch_related(
        Prefetch('tweet_set', queryset=parent_tweets_qs, to_attr='parent_tweets')
    ).all()

    context = {
        'name': nama_mhs,
        'persons': persons,
    }
    return render(request, 'index.html', context)

