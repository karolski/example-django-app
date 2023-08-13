import json
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection, reset_queries
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Album, Artist, ArtistImage, MediaTypes, Track

User = get_user_model()


def to_dict(paylaod: OrderedDict) -> dict:
    return json.loads(json.dumps(paylaod))


class BaseTestCaseWithArtistsAlbumsTracks(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(  # type: ignore
            username="testuser", password="testpassword"
        )
        self.artist1 = Artist.objects.create(name="Artist 1", artistid=1)
        self.artist2 = Artist.objects.create(name="Artist 2", artistid=2)
        ArtistImage.objects.create(artist=self.artist1, image="fakeimage.jpg")
        self.album1 = Album.objects.create(
            title="Album 1", artist=self.artist1, albumid=1
        )
        self.album2 = Album.objects.create(
            title="Album 2", artist=self.artist2, albumid=2
        )
        mediatype = MediaTypes.objects.create(name="test", mediatypeid=1)
        self.track = Track.objects.create(
            name="test track",
            album=self.album1,
            milliseconds=3333,
            mediatype=mediatype,
        )


class TestListArtists(BaseTestCaseWithArtistsAlbumsTracks):
    def test_list_artists(self):
        with self.assertNumQueries(2):
            response = self.client.get(reverse("artists-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            to_dict(response.data),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "artistid": 1,
                        "image_url": "/media/fakeimage.jpg",
                        "name": "Artist 1",
                    },
                    {"artistid": 2, "image_url": None, "name": "Artist 2"},
                ],
            },
        )


class AlbumsTests(BaseTestCaseWithArtistsAlbumsTracks):
    def test_list_albums_authenticated(self):
        url = reverse("albums-list")
        self.client.force_authenticate(
            user=self.user
        )  # Replace with an authenticated user
        reset_queries()
        with self.assertNumQueries(
            3
        ):  # one query for count, one for albums and one for related tracks
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            dict(response.data),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "albumid": 1,
                        "tracks": [
                            {
                                "trackid": 1,
                                "name": "test track",
                                "composer": None,
                                "milliseconds": 3333,
                                "bytes": None,
                                "unitprice": "",
                                "album": 1,
                                "mediatype": 1,
                                "genre": None,
                            }
                        ],
                        "title": "Album 1",
                        "artist": 1,
                    },
                    {"albumid": 2, "tracks": [], "title": "Album 2", "artist": 2},
                ],
            },
        )

    def test_list_albums_unauthenticated(self):
        url = reverse("albums-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_artist_albums_authenticated(self):
        artist = Artist.objects.first()
        url = reverse("artist-albums-list", args=[artist.artistid])
        self.client.force_authenticate(user=self.user)
        with self.assertNumQueries(2):
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            to_dict(response.data),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"albumid": 1, "title": "Album 1", "artist": 1}],
            },
        )

    def test_list_artist_albums_unauthenticated(self):
        artist = Artist.objects.first()
        url = reverse("artist-albums-list", args=[artist.artistid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_albums_summary_authenticated(self):
        url = reverse("albums-summary-list")
        self.client.force_authenticate(user=self.user)
        with self.assertNumQueries(2):
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            to_dict(response.data),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "albumid": 1,
                        "track_count": 1,
                        "total_duration": 3333,
                        "longest_track_duration": 3333,
                        "shortest_track_duration": 3333,
                        "artist": {
                            "artistid": 1,
                            "image_url": "/media/fakeimage.jpg",
                            "name": "Artist 1",
                        },
                        "title": "Album 1",
                    },
                    {
                        "albumid": 2,
                        "track_count": 0,
                        "total_duration": None,
                        "longest_track_duration": None,
                        "shortest_track_duration": None,
                        "artist": {
                            "artistid": 2,
                            "image_url": None,
                            "name": "Artist 2",
                        },
                        "title": "Album 2",
                    },
                ],
            },
        )

    def test_list_albums_summary_unauthenticated(self):
        url = reverse("albums-summary-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
