from django.db import models


class Albums(models.Model):
    albumid = models.AutoField(db_column="AlbumId", primary_key=True)
    title = models.TextField(db_column="Title")
    artistid = models.ForeignKey("Artists", models.CASCADE, db_column="ArtistId")

    class Meta:
        db_table = "albums"


class Artists(models.Model):
    artistid = models.AutoField(db_column="ArtistId", primary_key=True)
    name = models.TextField(db_column="Name", blank=True, null=True)

    class Meta:
        db_table = "artists"


class Genres(models.Model):
    genreid = models.AutoField(db_column="GenreId", primary_key=True)
    name = models.TextField(db_column="Name", blank=True, null=True)

    class Meta:
        db_table = "genres"


class MediaTypes(models.Model):
    mediatypeid = models.AutoField(db_column="MediaTypeId", primary_key=True)
    name = models.TextField(db_column="Name", blank=True, null=True)

    class Meta:
        db_table = "media_types"


class Tracks(models.Model):
    trackid = models.AutoField(db_column="TrackId", primary_key=True)
    name = models.TextField(db_column="Name")
    albumid = models.ForeignKey(
        Albums,
        models.SET_NULL,
        db_column="AlbumId",
        blank=True,
        null=True,
        related_name="tracks",
    )
    mediatypeid = models.ForeignKey(
        MediaTypes, models.DO_NOTHING, db_column="MediaTypeId"
    )
    genreid = models.ForeignKey(
        Genres, models.SET_NULL, db_column="GenreId", blank=True, null=True
    )
    composer = models.TextField(db_column="Composer", blank=True, null=True)
    milliseconds = models.IntegerField(db_column="Milliseconds")
    bytes = models.IntegerField(db_column="Bytes", blank=True, null=True)
    unitprice = models.TextField(db_column="UnitPrice")

    class Meta:
        db_table = "tracks"


class ArtistImage(models.Model):
    artist = models.OneToOneField(Artists, models.CASCADE)
    image = models.FileField()
