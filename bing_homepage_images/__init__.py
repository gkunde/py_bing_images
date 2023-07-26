from typing import Generator

import requests

from .image import Image
from .imagearchive import ImageArchive


class BingHomepageImages:
    """
    Fetch the Bing Homepage daily image feed.

    :param bing_market: A string value that specifies the "market" specific
        feeed desired. Default of `en-US` is used.
    """

    BASE_URL = "https://www.bing.com/"
    FEED_PATH = "HPImageArchive.aspx"

    def __init__(self, bing_market: str = None) -> None:

        self.bing_market = bing_market or "en-US"

        self._session = requests.Session()

        # built to request a single image first (assuming most usage only desires the current image)
        # second and third are setup to create non-overlapping requests
        self.__segments = [
            self._create_image_archive(0, 1),
            self._create_image_archive(1, 6),
            self._create_image_archive(7, 8),
        ]

    def get_images(self) -> Generator[Image, None, None]:
        """
        Generates a collection of Image objects from the image feed.

        :returns: A generator producing Image objects.
        """

        for segment in self.__segments:
            yield from segment.get_images()

    def _create_image_archive(self, index: int, count: int) -> ImageArchive:
        """
        Creates ImageArchive objects that enable access to the paginated image
        feed.

        :param index: An integer value to specify the starting image index location in the feed.

        :param count: An integer value to specify the number of image entries to return.

        :returns: An ImageArchive object.
        """

        image_archive = ImageArchive(index, count)
        image_archive._session = self._session
        image_archive._base_url = self.BASE_URL
        image_archive.market = self.bing_market

        return image_archive
