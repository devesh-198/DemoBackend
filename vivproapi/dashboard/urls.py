from django.urls import path
from .views.vivpro_apis import DanceProfileListView, setStarRating

urlpatterns = [
    path('api/dance-profiles/', DanceProfileListView.as_view(), name='dance-profile-list'),
    path('api/dance-rating/', setStarRating, name='dance-profile-rating'),
]
