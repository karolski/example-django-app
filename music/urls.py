from django.urls import path

from .views import (
    AlbumsListView,
    AlbumsSummaryListView,
    ArtistAlbumsListView,
    ArtistsListView,
)

urlpatterns = [
    path("artists/", ArtistsListView.as_view(), name="artists-list"),
    path("albums/", AlbumsListView.as_view(), name="albums-list"),
    path(
        "albums/artist/<int:artist_id>/",
        ArtistAlbumsListView.as_view(),
        name="artist-albums-list",
    ),
    path(
        "albums/summary/", AlbumsSummaryListView.as_view(), name="albums-summary-list"
    ),
]
