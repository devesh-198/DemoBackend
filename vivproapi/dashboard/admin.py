from django.contrib import admin
from django.contrib import admin
from django.contrib import admin
from .models  import DanceProfile

class DancePrifileAdmin(admin.ModelAdmin):
    list_display = ('title', 'danceability', 'energy', 'mode', 'rating')
    list_filter = ('mode', 'rating')
    search_fields = ('title', 'energy', 'mode')
    ordering = ('-id',)  # Sort by creation date in descending order

# Register your models here.
admin.site.register(DanceProfile, DancePrifileAdmin)
