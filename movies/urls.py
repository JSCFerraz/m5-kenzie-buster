from .views import MovieOrderView, MovieView, MovieDetailView

# from rest_framework_simplejwt import views
from django.urls import path

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieDetailView.as_view()),
    path("movies/<int:movie_id>/orders/", MovieOrderView.as_view()),
]
