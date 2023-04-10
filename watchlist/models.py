from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=200)
    website = models.URLField()

    def __str__(self) -> str:
        return self.name # name of platform

    class Meta:
        verbose_name_plural = 'Stream Platforms'


# Create your models here.
class WatchList(models.Model):
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    description = models.CharField(max_length=500)
    rating_avg = models.FloatField(default=0.0)
    total_rating = models.IntegerField(default=0)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title # name of movie

    class Meta:
        verbose_name_plural = 'Watch Lists'


# validators for review
def minValue(value: int, ):
    if value < 1:
        raise ValidationError("Minimum rating should be 1")

def maxValue(value: int, ):
    if value > 5:
        raise ValidationError("Maximum rating should be 5")

# reviews
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveBigIntegerField(validators=[minValue, maxValue]) 
    description = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f'{self.rating}'
    
    def save(self, *args, **kwargs):

        if(self.watchlist.total_rating == 0):
            self.watchlist.rating_avg = self.rating
        else:
            self.watchlist.rating_avg = (self.rating + self.watchlist.rating_avg) / 2

        self.watchlist.total_rating += 1 # increment total rating by 1

        self.watchlist.save()

        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        new_reviews = self.watchlist.rating_avg * self.watchlist.total_rating
        self.watchlist.total_rating -= 1

        self.watchlist.rating_avg = new_reviews / self.watchlist.total_rating
        self.watchlist.save()

        super().delete()