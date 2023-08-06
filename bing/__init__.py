"""
MIT License

Copyright (c) 2023 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_bing_images
"""
import requests

from bing.hpimagearchive import HPImageArchive


class Bing:

    @property
    def hp_image_archive(self) -> HPImageArchive:
        return HPImageArchive(self._session)

    def __init__(self) -> None:

        self._session = requests.Session()
