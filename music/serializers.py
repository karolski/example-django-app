from rest_framework import serializers
from .models import Artists, Albums, Tracks


class ArtistsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = Artists
        fields = "__all__"

    def get_image_url(self, obj: Artists):
        return obj.artistimage.image.url if hasattr(obj, "artistimage") else None


class TracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = "__all__"


class AlbumWithTracksSerializer(serializers.ModelSerializer):
    tracks = TracksSerializer(many=True, read_only=True)

    class Meta:
        model = Albums
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = "__all__"


class AlbumSummarySerializer(serializers.ModelSerializer):
    track_count = serializers.ReadOnlyField()
    total_duration = serializers.ReadOnlyField()
    longest_track_duration = serializers.ReadOnlyField()
    shortest_track_duration = serializers.ReadOnlyField()
    artistid = ArtistsSerializer()

    class Meta:
        model = Albums
        fields = "__all__"
