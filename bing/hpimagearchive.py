"""
MIT License

Copyright (c) 2023 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_bing_images
"""
from io import IOBase
from urllib.parse import SplitResult, parse_qsl, urlsplit

import requests

from bing.hpimagearchive_response import HPImageArchiveResponse


class HPImageArchive:
    """
    Connection to Bing's Homepage Image Archive endpoint for capturing Bing's
    image of the day.

    :param session: A Session object, or compatible requests.Session, for
        interacting with the endpoint.
    """

    DEFAULT_MARKET = "en-US"
    DEFAULT_FEED_FORMAT = "js"

    BASE_URI = "https://www.bing.com"
    ENDPOINT = "/HPImageArchive.aspx"

    def __init__(self, session: requests.Session = None) -> None:

        self._session = session or requests.Session()

    def get_feed(
            self,
            count: int,
            index: int = 0,
            market: str = None,
            feed_format: str = None) -> HPImageArchiveResponse:
        """
        Queries the feed service for a listing of images.

        :param count: An integer value, specifies the number of image to
            return. A valid value is between 1 and 8, inclusive.

        :param index: An integer value, specifies an image by the number of
            days ago it appeared in the feed.

        :param market: A string value, Language and country/region information
            for the feed. Complete list of supported values:
            https://learn.microsoft.com/en-us/previous-versions/bing/search/dd251064(v=msdn.10)

        :param feed_format: A string value, specifies the content type of the
            feed. Valid options are "rss", "js", "xml"

        :returns: A HPImageArchiveResponse object.
        """

        if not count or count < 1 or count > 8:
            raise ValueError(
                "`index` must be a value greater than 0 and less than 9.")

        params = [
            ("n", count),
            ("idx", index or 0),
            ("mkt", market or self.DEFAULT_MARKET),
            ("format", feed_format or self.DEFAULT_FEED_FORMAT),
        ]

        response = self._session.get(
            self.__join_url_and_endpoint(self.BASE_URI, self.ENDPOINT),
            params=params)

        return HPImageArchiveResponse(
            status_code=response.status_code,
            content_type=response.headers.get("content-type", None),
            content=response.content,
            encoding=response.encoding or response.apparent_encoding)

    def get_image(self, endpoint: str, file: IOBase) -> HPImageArchiveResponse:
        """
        Fetches a image file from the given path, writes to given file.

        :param path: A string value giving the endpoint for the image file.

        :param file: A IOBase type object to write the file data received from
            the given path.

        :returns: A HPImageArchiveResponse object, without encoding or
            content populated.
        """

        split_url = urlsplit(
            self.__join_url_and_endpoint(self.BASE_URI, endpoint))

        url = SplitResult(
            split_url.scheme,
            split_url.netloc,
            split_url.path,
            None,
            None).geturl()

        params = parse_qsl(split_url.query)

        response = self._session.get(url, params=params, stream=True)

        if response.ok:

            for block in response.iter_content(4096):
                file.write(block)

        return HPImageArchiveResponse(
            status_code=response.status_code,
            content_type=response.headers.get("content-type", None),
            content=None,
            encoding=None)

    def __join_url_and_endpoint(self, url: str, endpoint: str) -> str:
        """
        Joins a URL netloc to an endpoint path.

        :param url: A string value containing a url scheme and domain.

        :param endpoint: A string value containing the endpoint.

        :returns: A string containing a fully qualified URL.
        """

        base_split = urlsplit(url)
        path_split = urlsplit(endpoint)

        return SplitResult(
            base_split.scheme,
            base_split.netloc,
            path_split.path,
            path_split.query,
            path_split.fragment).geturl()
