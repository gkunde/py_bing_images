import requests
from bing.hpimagearchive import HPImageArchive


class Bing:

    @property
    def hp_image_archive(self) -> HPImageArchive:
        return HPImageArchive(self._session)
    
    def __init__(self) -> None:
        
        self._session = requests.Session()