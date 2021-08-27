
import logging

from cuticle_analysis.core import init
init()

from cuticle_analysis.datasets import RoughSmoothFull  # noqa
from cuticle_analysis.datasets import RoughSmoothSub  # noqa

logger = logging.getLogger(__name__)

rss = RoughSmoothSub((16, 16), save=True)
rsf = RoughSmoothFull((512, 512), save=True)

logger.info(f"type: subimage, size: {rss.size}, {rss.class_data()}")
logger.info(f"type: full, size: {rsf.size}, {rsf.class_data()}")

# TODO: add AllSub, and AllFull
# TODO: add class function for representing data spread
# TODO: save tables to file for paper
