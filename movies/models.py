from django.db import models


class MovieRating(models.TextChoices):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, default=None)
    rating = models.CharField(
        max_length=20, choices=MovieRating.choices, default=MovieRating.G, blank=True
    )
    synopsis = models.TextField(blank=True, null=True, default=None)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="movies",
        blank=True,
    )

    buyed_by = models.ManyToManyField(
        "users.User",
        through="movies.MovieOrder",
        related_name="movies_bought",
    )

    def __repr__(self) -> str:
        return f"<Movie [{self.id}] - {self.title}>"


class MovieOrder(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_bought_movie"
    )
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="ordered_movie"
    )

    price = models.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f"<MovieOrder [{self.id}] - {self.movie.title}>"
