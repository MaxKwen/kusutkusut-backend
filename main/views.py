from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Tweet, Person
from django.db.models import Count
from django.utils import timezone

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    TODO:
    - Ambil "username" and "password" dari request.data
    - Validate: not empty, password length >= X
    - Check if username already exists -> return 400 | Hint: Pakai User.object.filter(username=username).exist() sebagai condition
    - Create user pakai User.object.create_user()
    - Return 201 with: { "message": "registered"}
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username:
        return Response({"detail": "Username tidak boleh kosong."}, status=status.HTTP_400_BAD_REQUEST)
    elif len(password) < 6:
        return Response({"detail": "Panjang password minimal 6 huruf."}, status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(username=username).exists():
        return Response({"detail": "Username sudah diambil."}, status=status.HTTP_400_BAD_REQUEST)
    else:   
        User.objects.create_user(username=username, password=password)
        return Response({"message": "Registrasi sukses."}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    TODO:
    - Ambil username/password dari request.data
    - Cek kredensial user | Hint: Pakai authenticate(...)
    - If fail -> return invalid credentials 400
    - Else return { "token": <token> }
    """

    username = request.data.get("username")
    password = request.data.get("password")

    authenticated_user = authenticate(username=username, password=password)
    if authenticated_user is None:
        return Response({"detail": "Kredensial invalid."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        token, created = Token.objects.get_or_create(user=authenticated_user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def secret(request):
    """
    TODO:
    Buat function bebas, sekreatif atau sekocak mungkin
    Examples:
    - Return random number
    - Return custom message
    - Return a JSON list of your favorite movies
    - Return https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ
    - Anything
    """

    # original track URLs (may include query params). We'll convert them to embed URLs
    songs = [
        "https://open.spotify.com/track/6BV77pE4JyUQUtaqnXeKa5?si=c97fb92b44734eae",
        "https://open.spotify.com/track/2Xztg4QQc8x8MK6I7TuIV7?si=5b855bab95e141da",
        "https://open.spotify.com/track/4XHijJfABTtUCW3Bp6KFvr?si=559c1531b1a54ec5",
    ]

    # Convert to embed URLs and strip query parameters for clean embed src
    embed_songs = []
    for url in songs:
        base = url.split('?')[0]
        embed = base.replace('/track/', '/embed/track/')
        embed_songs.append(embed)

    context = {
        'name': 'sigmoby',
        'message': '6 7',
        'song_list': embed_songs,
    }

    return render(request, "spotify.html", context)

@api_view(["GET"])
@permission_classes([AllowAny])
def hello(request):
    return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def tweets_list(request):
    """Return all tweets sorted by published_date (newest first).

    This is a simple JSON endpoint using DRF's Response. The Tweet model is a
    Python class (defined in models.py) and you can import/use it in views
    (we imported it above). To send model data over HTTP you must serialize
    the model instances (below we build a Python dict for each tweet).
    """
    # Get all tweets ordered newest first
    # annotate with replies count to avoid extra DB queries per tweet
    tweets = (
        Tweet.objects.select_related('author')
        .annotate(replies_count=Count('comments'))
        .order_by('-published_date')
    )

    data = []
    for t in tweets:
        author = t.author
        data.append({
            'id': t.id,
            'content': t.content,
            'likes': t.likes,
            'replies_count': t.replies_count,
            'published_date': t.published_date.isoformat() if t.published_date else None,
            'author': {
                'id': author.id,
                'name': author.name,
                'username': author.username,
                'profile_picture': author.profile_picture.url if author.profile_picture else None,
            },
            'parent_tweet': t.parent_tweet.id if t.parent_tweet else None,
        })

    return Response(data, status=status.HTTP_200_OK)