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
    path('see/<int:movie_id>', views.see, name='see'),
    path('unsee/<int:movie_id>', views.unsee, name='unsee'),
    path('compare/<int:better_movie_id>/<int:worse_movie_id>', views.compare, name='compare'),
]
