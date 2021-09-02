
import re
import logging
from typing import Dict

import requests
from bs4 import BeautifulSoup

from ..datasets.helper import DatasetHelper

logger = logging.getLogger(__name__)


class SpecimenScraper():
    def __init__(self):
        self.dh = DatasetHelper()
        self.base_url = "https://antweb.org"
        self.images_url = f"{self.base_url}/images.do"
        self.pic_url = f"{self.base_url}/bigPicture.do"

    def get_specimen(self, info: dict) -> str:
        """
            Get specimen using taxonomic information.
        """
        payload = {
            "genus": info["genus"],
            "species": info["species"],
            "rank": "species",
            "project": "allantwebants"
        }
        r = requests.get(self.images_url, params=payload)
        soup = BeautifulSoup(r.text, "html.parser")

        # parse name div
        div = soup.find("div", {"class": "name"})

        name = str(div.text).lower()
        return name

    def get_specimen_by_id(self, _id: int) -> str:
        """
            Get specimen by id.
        """
        ant_info = self.dh.get_ant_info(_id)
        return self.get_specimen(ant_info)

    def get_meta_by_specimen(self, _id: int) -> Dict:
        """
            Get high res image, author and author_url by id.
        """
        payload = {
            "name": self.get_specimen_by_id(_id),
            "shot": "h",
            "number": "1"
        }
        r = requests.get(self.pic_url, params=payload)
        soup = BeautifulSoup(r.text, "html.parser")

        # parse photo_metadata span
        span = soup.find("span", {"id": "photo_metadata"})
        elements = span.find_all("li")

        res = {
            "author": "",
            "author_url": "",
            "image_url": ""
        }
        image_pattern = r"View Highest Resolution"
        author_pattern = r"Photographer: "
        for element in elements:
            if re.match(image_pattern, element.text):
                res["image_url"] = element.a.get("href")
            elif re.match(author_pattern, element.text):
                res["author"] = re.sub(author_pattern, "", element.text)
                res["author_url"] = element.a.get("href")
        return res

    def get_image_by_specimen(self, _id: int) -> str:
        """
            Get headshot image url by id. Backup if highest resolution is not
            available.
        """
        payload = {
            "name": self.get_specimen_by_id(_id),
            "shot": "h",
            "number": "1"
        }
        r = requests.get(self.pic_url, params=payload)
        soup = BeautifulSoup(r.text, "html.parser")

        # parse big_picture div
        div = soup.find("div", {"class": "big_picture"})

        img = div.find("img")
        return img["src"]
