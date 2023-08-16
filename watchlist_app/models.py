from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=10)
    about = models.CharField(max_length=20)
    website = models.URLField(max_length=30)
    
    def __str__(self):
        return self.name
    

class WatchList(models.Model):
    title = models.CharField(max_length=200)
    storyline = models.TextField()
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    avg_rating = models.FloatField(default=0)
    num_rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title  
