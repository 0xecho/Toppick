from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import generic
from django.conf import settings
from django.contrib.auth import login

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
        if genre:
            kwargs['selected_genre'] = genre
            genre = models.Genre.objects.filter(name=genre).first()
            movies = movies.filter(genre=genre)

        if year:
            kwargs['selected_year'] = year
            movies = movies.filter(year=year)

        kwargs['movies'] = movies
        kwargs['q'] = query
        kwargs['genres'] = models.Genre.objects.all()
        kwargs['years'] = map(str, movies.values_list('year', flat=True).distinct())
        return super().get(request, *args, **kwargs)