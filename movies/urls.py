from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', views.TelegramLoginView.as_view(), name='telegram_login'),
    path('login/handler/', views.TelegramLoginHandlerView.as_view(), name='telegram_login_handler'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('select_movies/', views.SelectMoviesView.as_view(), name='select_movies'),
    path('watched_movies/', views.WatchedMoviesView.as_view(), name='watched_movies'),
    path('rank_movies/', views.RankMoviesView.as_view(), name='rank_movies'),
    path('top_movies/', views.TopRankingsView.as_view(), name='top_movies'),
    path('user/<uuid:uuid>/', views.PublicTopRankingsView.as_view(), name='public_top_movies'),
    path('discover_movies/', views.DiscoverMovies.as_view(), name='discover_movies'),
    path('see/<int:movie_id>', views.see, name='see'),
    path('unsee/<int:movie_id>', views.unsee, name='unsee'),
    path('api/seen/<int:movie_id>', views.seen_api, name='seen_api'),
    path('api/notseen/<int:movie_id>', views.notseen_api, name='notseen_api'),
    path('compare/<int:main_movie_id>/<int:other_movie_id>/<int:is_main_movie_better>', views.compare, name='compare'),
]
