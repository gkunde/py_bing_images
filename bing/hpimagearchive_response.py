"""
MIT License

Copyright (c) 2023 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_bing_images
"""
from dataclasses import dataclass


@dataclass
class HPImageArchiveResponse:
    """
    Class for storing HTTP response information and content from a request.
    """

    status_code: int = None
    content_type: str = None
    content: bytes = None
    encoding: str = None
