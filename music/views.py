from rest_framework import generics, permissions
from .models import Artists, Albums
from .serializers import (
    ArtistsSerializer,
    AlbumWithTracksSerializer,
    AlbumSerializer,
    AlbumSummarySerializer,
)
from django.db import models


class ArtistsListView(generics.ListAPIView):
    serializer_class = ArtistsSerializer

    def get_queryset(self):
        return Artists.objects.all().select_related("artistimage")


class AlbumsListView(generics.ListAPIView):
    serializer_class = AlbumWithTracksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Albums.objects.all().prefetch_related("tracks")


class ArtistAlbumsListView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        artist_id = self.kwargs["artist_id"]
        return Albums.objects.filter(artistid=artist_id)


class AlbumsSummaryListView(generics.ListAPIView):
    serializer_class = AlbumSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Albums.objects.annotate(
            track_count=models.Count("tracks"),
            total_duration=models.Sum("tracks__milliseconds"),
            longest_track_duration=models.Max("tracks__milliseconds"),
            shortest_track_duration=models.Min("tracks__milliseconds"),
        ).select_related("artistid", "artistid__artistimage")
        return queryset
