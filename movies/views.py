from functools import reduce
from shutil import move
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from typing import Any, Dict

from . import models
from .authentication import verify_auth
# Create your views here.

class TelegramLoginView(generic.TemplateView):
    template_name = 'movies/telegram_login.html'
    
class TelegramLoginHandlerView(generic.View):
    def get(self, request, *args, **kwargs):
        data = request.GET
        token = settings.TELEGRAM_BOT_TOKEN
        if verify_auth(data, token):
            user = models.CustomUser.objects.get_or_create(
                telegram_id=data['id'],
                defaults={
                    'username': data['username'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )[0]
            login(request, user)
            return redirect(reverse_lazy('home'))
        return redirect(reverse_lazy('telegram_login'))

class SelectMoviesView(generic.TemplateView):
    template_name = 'movies/select_movies.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if not query:
            return redirect(reverse_lazy('home'))
        
        genre = request.GET.get('genre')
        year = request.GET.get('year')
        
        movies = models.Movie.objects.filter(title__icontains=query)
        # filter out movies that are seen from table MovieSeen
        # movies = movies.exclude(id__in=models.MovieSeen.objects.filter(user=request.user).values_list('movie_id', flat=True))
        if genre:
            kwargs['selected_genre'] = genre
            genre = models.Genre.objects.filter(name=genre).first()
            movies = movies.filter(genre=genre)

        if year:
            kwargs['selected_year'] = year
            movies = movies.filter(year=year)

        seen_movies = models.MovieSeen.objects.filter(user=request.user).values_list('movie_id', flat=True)
        for movie in movies:
            if movie.id in seen_movies:
                movie.is_seen = True
            else:
                movie.is_seen = False

        kwargs['movies'] = movies
        kwargs['q'] = query
        kwargs['years'] = map(str, movies.values_list('year', flat=True).distinct())
        kwargs['genres'] = models.Genre.objects.all()
        return super().get(request, *args, **kwargs)

class WatchedMoviesView(generic.TemplateView):
    template_name = 'movies/watched_movies.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs['movies'] = map(lambda movieseen: movieseen.movie, models.MovieSeen.objects.filter(user=self.request.user))
        return super().get_context_data(**kwargs)

@login_required
def see(request, movie_id):
    movie = models.Movie.objects.get(id=movie_id)
    models.MovieSeen.objects.get_or_create(user=request.user, movie=movie)
    try:
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect(reverse_lazy('home'))

@login_required
def unsee(request, movie_id):
    movie = models.Movie.objects.get(id=movie_id)
    models.MovieSeen.objects.filter(user=request.user, movie=movie).delete()
    return redirect(reverse_lazy('watched_movies'))