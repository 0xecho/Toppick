from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', views.TelegramLoginView.as_view(), name='telegram_login'),
    path('login/handler/', views.TelegramLoginHandlerView.as_view(), name='telegram_login_handler'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('select_movies/', views.SelectMoviesView.as_view(), name='select_movies'),
]
