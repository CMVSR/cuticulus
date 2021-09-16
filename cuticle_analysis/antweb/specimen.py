
import os
import re
import logging
from typing import Dict, Tuple

import cv2
import requests
import pylatex
from pylatex.utils import escape_latex, NoEscape
from bs4 import BeautifulSoup

from ..datasets.helper import DatasetHelper

logger = logging.getLogger(__name__)

ANT_WEB_URL = "https://antweb.org/"
CC_URL = "https://creativecommons.org/licenses/by/4.0/"


def hyperlink(url: str, text: str) -> str:
    """
    Helper function to create a hyperlink.

    Args:
        url: The url to link to.
        tex: The text to be displayed in the hyperlink.

    Returns:
        The hyperlinked text.
    """
    text = escape_latex(text)
    return NoEscape(r'\href{' + url + '}{' + text + '}')


class SpecimenScraper():
    def __init__(self):
        self.dh = DatasetHelper()
        self.images_url = f"{self.base_url}/images.do"
        self.pic_url = f"{self.base_url}/bigPicture.do"
        self.assets_path = "./paper/assets"
        self.images_path = "./paper/assets/images"

        self.antweb_str = hyperlink(ANT_WEB_URL, "AntWeb")
        self.cc_str = hyperlink(CC_URL, "CC BY 4.0")

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
        specimen = self.get_specimen_by_id(_id)
        payload = {
            "name": specimen,
            "shot": "h",
            "number": "1"
        }
        r = requests.get(self.pic_url, params=payload)
        soup = BeautifulSoup(r.text, "html.parser")

        # parse photo_metadata span
        span = soup.find("span", {"id": "photo_metadata"})
        elements = span.find_all("li")

        res = {
            "specimen": specimen.upper(),
            "specimen_url": r.url,
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

        # run backup request if high res image is not available
        if not res["author_url"]:
            res["author_url"] = self.get_image_by_specimen(_id)

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

    def download_image(self, url: str, path: str) -> None:
        """
            Given an image url and path, download the image to the
            path.
        """
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(f"{path}.tif", "wb") as f:
                for chunk in r:
                    f.write(chunk)

        # convert to jpg
        im = cv2.imread(f"{path}.tif")
        cv2.imwrite(f"{path}.jpg", im)

        # remove tif
        os.remove(f"{path}.tif")

    def build_figure(self, _id: int) -> Tuple[Dict, pylatex.Figure]:
        """
            Build latex figure with included image and CC attribution from a
            list of given ids
        """
        fig = pylatex.Figure()

        # get meta data
        info = self.get_meta_by_specimen(_id)
        self.download_image(info["image_url"],
                            f"{self.images_path}/{info['specimen']}")

        # add image and caption
        fig.add_image(f"assets/images/{info['specimen']}.jpg",
                      width=NoEscape(r'0.2\textwidth'))
        specimen_str = hyperlink(info['specimen_url'], info['specimen'])
        author_str = hyperlink(info['author_url'], info['author'])
        fig.add_caption(
            NoEscape(str(
                specimen_str
                + " by " + author_str
                + ", from " + self.antweb_str
                + ", is licensed under " + self.cc_str)))

    def save_figure(self, info: dict, fig: pylatex.Figure):
        # save to file
        filename = f"{info['specimen']}.tex"
        logger.debug(f"Saving figure to {filename}")
        with open(f"{self.assets_path}/{filename}", "w") as f:
            f.write(fig.dumps())

        return fig
