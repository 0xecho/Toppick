from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
import botogram

from accounts.models import CustomUser

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

class BroadcastPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/broadcast.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # take message from post request and send it to all users
        message = request.POST.get('message')
        bot = botogram.create(settings.TELEGRAM_BOT_TOKEN)
        for user in CustomUser.objects.all():
            try:
                bot.chat(user.telegram_id).send(message)
            except:
                pass
        return redirect(reverse_lazy('broadcast'))