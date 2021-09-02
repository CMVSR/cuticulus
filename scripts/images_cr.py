
import logging

from bs4 import BeautifulSoup

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis.antweb import SpecimenScraper  # noqa

scraper = SpecimenScraper()
logger = logging.getLogger(__name__)

ids = [1]
for _id in ids:
    logger.info(f"Processing  ID: {_id}")
    res = scraper.get_specimen_by_id(_id)
    if res:
        logger.info(res)
    else:
        logger.info(f"No data found for ID: {_id}")
