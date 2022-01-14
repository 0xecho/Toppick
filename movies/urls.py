from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.TelegramLoginView.as_view(), name='telegram_login'),
    path('login/handler/', views.TelegramLoginHandlerView.as_view(), name='telegram_login_handler'),
]
