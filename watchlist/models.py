from django.db import models
from django.core.exceptions import ValidationError


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
    description = models.CharField(max_length=500)
    active = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title # name of movie

    class Meta:
        verbose_name_plural = 'WatchList'

# validators for review
def minValue(value: int, ):
    if value < 1:
        raise ValidationError("Minimum rating should be 1")

def maxValue(value: int, ):
    if value > 5:
        raise ValidationError("Maximum rating should be 5")

# reviews
class Review(models.Model):
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveBigIntegerField(validators=[minValue, maxValue]) 
    description = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f'{self.rating}'