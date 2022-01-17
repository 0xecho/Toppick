from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from typing import Any, Dict
from itertools import permutations
from random_username.generate import generate_username
import requests
import random
import botogram

from . import models
from .authentication import verify_auth
import movies
# Create your views here.

telegram_bot = botogram.create(settings.TELEGRAM_BOT_TOKEN)

class TelegramLoginView(generic.TemplateView):
    template_name = 'movies/telegram_login.html'
    
class TelegramLoginHandlerView(generic.View):
    def get(self, request, *args, **kwargs):
        data = request.GET
        token = settings.TELEGRAM_BOT_TOKEN
        if verify_auth(data, token):
            user, created = models.CustomUser.objects.get_or_create(
                telegram_id=data['id'],
                defaults={
                    'username': data.get('username', generate_username()),
                    'first_name': data.get('first_name', ''),
                    'last_name': data.get('last_name', ''),
                }
            )
            if created:
                telegram_bot.chat(data['id']).send(
                    f'Welcome to the movies bot, {user.username}!\n'
                    'You can now use the web interface to rank movies you have seen.'
                )
                telegram_bot.chat(settings.TELEGRAM_ADMIN_ID).send(
                    f'New user @{user.username} - {user.first_name} {user.last_name} - {user.telegram_id} registered.'
                )
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
        for row in data.get('Search', []):
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
        seen_movies = models.MovieSeen.objects.filter(user=self.request.user).prefetch_related('movie')
        shuffled_seen_movies = list(seen_movies)
        random.shuffle(shuffled_seen_movies)
        for movie in shuffled_seen_movies:
            remaining_seen_movies = models.MovieSeen.objects.filter(user=self.request.user).filter(
                Q(id__lt=movie.id) & Q(id__gt=movie.last_checked_movie_index))
            if remaining_seen_movies:
                kwargs['movies'] = [movie.movie, remaining_seen_movies[0].movie]
                break
        return super().get_context_data(**kwargs)
    
class TopRankingsView(LoginRequiredMixin, generic.ListView):
    template_name = 'movies/top_rankings.html'
    paginate_by = 10
    
    def get_queryset(self):
        return list(map(lambda movieseen: movieseen.movie, models.MovieSeen.objects.filter(user=self.request.user).order_by('-score')))

class PublicTopRankingsView(generic.ListView):
    template_name = 'movies/public_top_rankings.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        uuid = self.kwargs['uuid']
        kwargs["user_name"] = models.CustomUser.objects.get(public_url_uuid=uuid)
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        uuid = self.kwargs['uuid']
        user = models.CustomUser.objects.get(public_url_uuid=uuid)
        return list(map(lambda movieseen: movieseen.movie, models.MovieSeen.objects.filter(user=user).order_by('-score')))


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
def compare(request, main_movie_id, other_movie_id, is_main_movie_better):
    main_movie_seen = models.MovieSeen.objects.get(user=request.user, movie__id=main_movie_id)
    other_movie_seen = models.MovieSeen.objects.get(user=request.user, movie__id=other_movie_id)
    if is_main_movie_better:
        main_movie_seen.score += 1
        other_movie_seen.score -= 1
    else:
        main_movie_seen.score -= 1
        other_movie_seen.score += 1
    main_movie_seen.last_checked_movie_index = other_movie_seen.id
    main_movie_seen.save()
    other_movie_seen.save()
    return redirect(reverse_lazy('rank_movies'))