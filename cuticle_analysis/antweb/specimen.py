
import requests
from bs4 import BeautifulSoup

from ..datasets.helper import DatasetHelper


class SpecimenScraper():
    def __init__(self):
        self.dh = DatasetHelper()
        self.base_url = "https://antweb.org/images.do"

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
        r = requests.get(self.base_url, params=payload)

        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", {"class": "name"})

        url = ""
        name = ""
        if div:
            if div.has_attr("href"):
                url = div["href"]
            name = div.text
        return name, url

    def get_specimen_by_id(self, _id: int) -> str:
        """
            Get specimen by id.
        """
        ant_info = self.dh.get_ant_info(_id)
        return self.get_specimen(ant_info)
