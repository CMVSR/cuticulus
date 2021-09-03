
import logging

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis.antweb import SpecimenScraper  # noqa

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    scraper = SpecimenScraper()
    fig = scraper.build_figure(1)
