from django.urls import path

from .views import HomePageView, AboutPageView, BroadcastPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('broadcast/', BroadcastPageView.as_view(), name='broadcast'),
]
