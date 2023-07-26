from datetime import datetime
from io import BytesIO
from typing import Any
from urllib.parse import SplitResult, parse_qsl, urlsplit

import requests


class Image:

    BASE_URL = "https://www.bing.com/"

    def __init__(
            self,
            startdate: datetime = None,
            fullstartdate: datetime = None,
            enddate: datetime = None,
            url: str = None,
            urlbase: str = None,
            copyright: str = None,
            copyrightlink: str = None,
            title: str = None,
            quiz: str = None,
            wp: bool = None,
            hsh: str = None,
            drk: Any = None,
            top: Any = None,
            bot: Any = None,
            hs: list[Any] = None,
            base_url: str = None,
            session: requests.Session = None) -> None:

        self.startdate = startdate
        self.fullstartdate = fullstartdate
        self.enddate = enddate
        self.url = url
        self.urlbase = urlbase
        self.copyright = copyright
        self.copyrightlink = copyrightlink
        self.title = title
        self.quiz = quiz
        self.wp = wp
        self.hsh = hsh
        self.drk = drk
        self.top = top
        self.bot = bot
        self.hs = hs

        self._base_url = base_url or self.BASE_URL

        self._session = session or requests.Session()

    def save_image(self, file: BytesIO) -> None:
        """
        """

        split_url = urlsplit(self._base_url)

        # make a new split url object with the path included.
        split_url = SplitResult(
            split_url.scheme,
            split_url.netloc,
            self.url,
            None,
            None)

        # split again to extract the query string
        split_url = urlsplit(split_url.geturl())

        # capture query string
        params = parse_qsl(split_url.query)

        # build split object without query string
        split_url = SplitResult(
            split_url.scheme,
            split_url.netloc,
            split_url.path,
            None,
            None)

        response = self._session.get(
            split_url.geturl(),
            params=params,
            stream=True)

        response.raise_for_status()

        for block in response.iter_content(4096):
            file.write(block)
