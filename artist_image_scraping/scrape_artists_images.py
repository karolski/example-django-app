"""
Script to update images of the artists
"""
import os
from logging import getLogger
from typing import List, Optional
from urllib.parse import urlparse, quote

import requests
from django.core.files.base import ContentFile
from lxml import html
from rest_framework import status
from tqdm import tqdm

from artist_image_scraping.constants import DEFAULT_HEADERS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "centric_app.settings")
os.environ.setdefault("DEBUG", "1")
import django

django.setup()

from music.models import Artists, ArtistImage

logger = getLogger(__name__)


def update_artists_images() -> None:
    artists = Artists.objects.filter(name__isnull=False)
    logger.info(f"got {len(artists)} to scrape")
    artist_image_urls = get_artists_image_urls([artist.name for artist in artists])  # type: ignore
    n_image_urls = len([img for img in artist_image_urls if img is not None])
    logger.info(f"got {n_image_urls} image urls")

    updated_objs = []
    for artist, image_url in zip(artists, artist_image_urls):
        if image_url is None or artist.name is None:
            continue

        response = requests.get(image_url)
        if response.status_code != status.HTTP_200_OK:
            logger.error(
                f"could not fetch image {response.status_code}, {response.content!r}"
            )
            continue

        image_obj = ArtistImage.objects.filter(artist=artist).first() or ArtistImage(
            artist=artist
        )
        filename = (
            artist.name.replace("/", "_")
            + "_"
            + urlparse(image_url).path.split("/")[-1]
        )
        image_obj.image.save(filename, ContentFile(response.content), save=True)
        updated_objs.append(image_obj)
        image_obj.save()

    logger.info(f"updated {len(updated_objs)} artist image objects.")


def parse_image_url_from_page(html_content: bytes, artist_name: str) -> Optional[str]:
    tree = html.fromstring(html_content)

    if not tree.xpath(f'//ul//li[contains(@class, "artist")]'):
        logger.warning(f'no search results for "{artist_name}"')
        return None

    image_element = tree.xpath(
        f'//ul//li[contains(@class, "artist")]//img[contains(@alt, "{artist_name}")]'
    )

    if not image_element:
        return None
    else:
        return image_element[0].get("src")  # type: ignore


def get_artists_image_urls(artist_names: List[str]) -> List[Optional[str]]:
    """given a list of artist names return a list of image urls (or None-s)"""
    artist_images: List[Optional[str]] = []
    for name in tqdm(artist_names, "getting image urls"):
        search_url = (
            f'https://www.allmusic.com/search/all/{quote(name.lower(), safe="")}'
        )
        response = requests.get(search_url, headers=DEFAULT_HEADERS)
        if response.status_code != status.HTTP_200_OK:
            logger.error("could not crawl page", response.status_code, response.content)
            artist_images.append(None)
            continue
        img_src = parse_image_url_from_page(response.content, name)
        artist_images.append(img_src)
    return artist_images


if __name__ == "__main__":
    update_artists_images()
