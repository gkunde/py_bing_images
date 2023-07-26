import json
from datetime import datetime
from typing import Generator
from urllib.parse import SplitResult, urlsplit

import requests

from .image import Image


class ImageArchive:

    BASE_URL = "https://www.bing.com/"
    FEED_PATH = "HPImageArchive.aspx"
    DEFAULT_MKT = "en-US"
    DEFAULT_FORMAT = "js"

    def __init__(self, index: int, count: int, market: str = None, session: requests.Session = None, base_url: str = None) -> None:

        self.index = index
        self.count = count

        self.raw_data: str = None

        self.market = market or self.DEFAULT_MKT

        self._session = session or requests.Session()

        self._base_url = base_url or self.BASE_URL

    def get_images(self) -> Generator[Image, None, None]:
        """
        """

        self.__fetch_json()

        _json = json.loads(self.raw_data)

        for image in _json.get("images", []):

            startdate = self.__parse_date(image.get("startdate", None))

            enddate = self.__parse_date(image.get("enddate", None))

            fullstartdate = self.__parse_datetime(
                image.get("startfulldate", None))

            yield Image(
                startdate=startdate,
                fullstartdate=fullstartdate,
                enddate=enddate,
                url=image.get("url", None),
                urlbase=image.get("urlbase", None),
                copyright=image.get("copyright", None),
                copyrightlink=image.get("copyrightlink", None),
                title=image.get("title", None),
                quiz=image.get("quiz", None),
                wp=image.get("wp", None),
                hsh=image.get("image", None),
                drk=image.get("drk", None),
                top=image.get("top", None),
                bot=image.get("bot", None),
                hs=image.get("hs", None),
                base_url=self.BASE_URL,
                session=self._session)

    def __parse_date(self, date: str) -> datetime:
        """
        """

        if not date:
            return None

        return datetime.strptime(date, "%Y%m%d")

    def __parse_datetime(self, fulldate: str) -> datetime:
        """
        """

        if not fulldate:
            return None

        return datetime.strptime(fulldate, "%Y%m%d%H%M")

    def __fetch_json(self) -> None:
        """
        """

        split_url = urlsplit(self._base_url)

        # make a new split url object with the path included.
        split_url = SplitResult(
            split_url.scheme,
            split_url.netloc,
            self.FEED_PATH,
            None,
            None)

        params = [
            ("format", self.DEFAULT_FORMAT, ),
            ("mkt", self.market, ),
            ("n", self.count, ),
            ("idx", self.index, ),
        ]

        response = self._session.get(split_url.geturl(), params=params)
        response.raise_for_status()

        self.raw_data = response.content
