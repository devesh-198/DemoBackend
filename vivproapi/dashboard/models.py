from django.db import models

# Create your models here.
class DanceProfile(models.Model):
    STAR_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    id = models.CharField(max_length=100, null=False, blank=False, primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    danceability = models.FloatField(max_length=100, null=False, blank=False)
    energy = models.FloatField(max_length=100, null=False, blank=False)
    mode = models.IntegerField(max_length=100, null=False, blank=False)
    acousticness = models.FloatField(max_length=100, null=False, blank=False)
    tempo = models.FloatField(max_length=100, null=False, blank=False)
    duration_ms = models.IntegerField(max_length=100, null=False, blank=False)
    num_sections = models.IntegerField(max_length=100, null=False, blank=False)
    num_segments = models.IntegerField(max_length=100, null=False, blank=False)
    rating = models.IntegerField(choices=STAR_CHOICES, default=0, blank=True, null=True)

    def __str__(self):
        return self.title

