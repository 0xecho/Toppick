from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.contrib.auth import login

from . import models
from .authentication import verify_auth
# Create your views here.

class TelegramLoginView(generic.TemplateView):
    template_name = 'telegram_login.html'
    
class TelegramLoginHandlerView(generic.View):
    def post(self, request, *args, **kwargs):
        data = request.POST
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
            return redirect(reverse_lazy("home"))
        return redirect(reverse_lazy("telegram_login"), {"error": "Invalid credentials"})