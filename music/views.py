from django.db import models
from rest_framework import generics, permissions

from .models import Album, Artist
from .serializers import (AlbumSerializer, AlbumSummarySerializer,
                          AlbumWithTracksSerializer, ArtistsSerializer)


class ArtistsListView(generics.ListAPIView):
    serializer_class = ArtistsSerializer

    def get_queryset(self):
        return Artist.objects.all().select_related("artistimage")


class AlbumsListView(generics.ListAPIView):
    serializer_class = AlbumWithTracksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Album.objects.all().prefetch_related("tracks")


class ArtistAlbumsListView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        artist_id = self.kwargs["artist_id"]
        return Album.objects.filter(artist=artist_id)


class AlbumsSummaryListView(generics.ListAPIView):
    serializer_class = AlbumSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Album.objects.annotate(
            track_count=models.Count("tracks"),
            total_duration=models.Sum("tracks__milliseconds"),
            longest_track_duration=models.Max("tracks__milliseconds"),
            shortest_track_duration=models.Min("tracks__milliseconds"),
        ).select_related("artist", "artist__artistimage")
        return queryset
