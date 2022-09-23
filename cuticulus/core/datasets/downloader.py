"""Download raw dataset."""
import logging
from pathlib import Path

from juliacall import Main as jl

from cuticulus import const

log = logging.getLogger('rich')


class Downloader(object):
    """Download raw dataset."""

    def __init__(self):
        """Initialize downloader."""
        name = 'cuticulus-dataset-raw'
        description = """
        Dataset: Cuticle texture ant head image dataset (raw)
        License: MIT
        Website: {website}
        """
        description = description.format(website=const.DATASET_URL)

        register = """
        register(DataDep(
            "{name}",
            "{description}",
            "{url}",
            "{hash}",
            post_fetch_method = unpack,
        ))
        """
        register = register.format(
            name=name,
            description=description,
            url=const.DATASET_URL,
            hash=const.DATASET_HASH,
        )
        # remove new lines
        register = register.replace('\n', '')

        jl.seval('using DataDeps')
        jl.seval(register)
        self.base_path = Path(jl.seval('datadep"{name}"'.format(name=name)))
