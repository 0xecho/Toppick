from django.db import models

from accounts.models import CustomUser

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    poster = models.ImageField(upload_to='posters/')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Director(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name

class MovieSeen(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title

class MovieComparision(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    better_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='better_movie')
    worse_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='worse_movie')

    def __str__(self):
        return f'{self.better_movie.title} > {self.worse_movie.title}'