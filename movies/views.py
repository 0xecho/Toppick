from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from itertools import permutations
import requests
import random

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

class SelectMoviesView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'movies/select_movies.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if not query:
            return redirect(reverse_lazy('home'))
        
        # genre = request.GET.get('genre')
        year = request.GET.get('year')
        try:
            API_URL = f"http://www.omdbapi.com/?apikey=b38a0c33&s={query}"  
        except:
            # Internal server error, notify user
            return redirect(reverse_lazy('home'))
        resp = requests.get(API_URL)
        data = resp.json()
        for row in data['Search']:
            print(row)
            try:
                try:
                    row_year = int(row['Year'].split('–')[0])
                except:
                    row_year = 0

                new_movie = models.Movie.objects.get_or_create(
                    title=row['Title'],
                    year=row_year,
                    poster=row['Poster'],
                )
                if new_movie[0].poster == 'N/A':
                    resp = requests.get(f"http://www.omdbapi.com/?apikey=b38a0c33&t={row['Title']}")
                    data = resp.json()
                    new_movie[0].poster = data['Poster']
                    new_movie[0].save()

            except Exception as e:
                print(e)
                pass
        
        movies = models.Movie.objects.filter(title__icontains=query)
        print("MOVIES:", movies)
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
        # kwargs['genres'] = models.Genre.objects.all()
        return super().get(request, *args, **kwargs)

class WatchedMoviesView(LoginRequiredMixin, generic.ListView):
    template_name = 'movies/watched_movies.html'
    paginate_by = 9

    def get_queryset(self):
        return list(map(lambda movieseen: movieseen.movie, models.MovieSeen.objects.filter(user=self.request.user)))

class RankMoviesView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'movies/rank_movies.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # select 2 random movies from table MovieSeen that are not in table MovieComparision and return in context
        seen_movies = models.MovieSeen.objects.filter(user=self.request.user).values_list('movie__id', flat=True)
        seen_movies = list(seen_movies)
        random.shuffle(seen_movies)
        kwargs['movies'] = False
        for movie_1, movie_2 in permutations(seen_movies, 2):
            if models.MovieComparision.objects.filter(better_movie=movie_1, worse_movie=movie_2).exists() or models.MovieComparision.objects.filter(better_movie=movie_2, worse_movie=movie_1).exists():
                continue
            kwargs['movies'] = [models.Movie.objects.get(id=movie_1), models.Movie.objects.get(id=movie_2)]
            break
        return super().get_context_data(**kwargs)
    
# paginated view
# seen_movies = models.MovieSeen.objects.filter(user=self.request.user).values_list('movie__id', flat=True)
# ordered_movies = models.Movie.objects.filter(id__in=seen_movies).order_by('-score')
class TopRankingsView(LoginRequiredMixin, generic.ListView):
    template_name = 'movies/top_rankings.html'
    paginate_by = 10
    
    def get_queryset(self):
        seen_movies = models.MovieSeen.objects.filter(user=self.request.user).values_list('movie__id', flat=True)
        ordered_movies = models.Movie.objects.filter(id__in=seen_movies).order_by('-score')
        return ordered_movies


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

@login_required
def compare(request, better_movie_id, worse_movie_id):
    better_movie = models.Movie.objects.get(id=better_movie_id)
    worse_movie = models.Movie.objects.get(id=worse_movie_id)
    models.MovieComparision.objects.get_or_create(
        better_movie=better_movie,
        worse_movie=worse_movie,
        user=request.user
    )
    better_movie.score += 1
    worse_movie.score -= 1
    better_movie.save()
    worse_movie.save()
    return redirect(reverse_lazy('rank_movies'))