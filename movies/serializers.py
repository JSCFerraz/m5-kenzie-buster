from rest_framework import serializers
from movies.models import Movie, MovieOrder, MovieRating
from users.serializers import UserSerializer


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(
        choices=MovieRating.choices, default=MovieRating.G, required=False
    )
    synopsis = serializers.CharField(required=False)

    user = UserSerializer(read_only=True)

    def create(self, validated_data: dict):
        return Movie.objects.create(**validated_data)


class MovieReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(
        choices=MovieRating.choices, default=MovieRating.G, required=False
    )
    synopsis = serializers.CharField(required=False)

    added_by = serializers.EmailField(source="user.email")


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = serializers.DateTimeField(read_only=True)

    title = serializers.SerializerMethodField()

    buyed_by = serializers.SerializerMethodField()

    def get_title(self, obj) -> str:
        return obj.movie.title

    def get_buyed_by(self, obj) -> str:
        return obj.user.email

    def create(self, validated_data: dict):
        return MovieOrder.objects.create(**validated_data)
