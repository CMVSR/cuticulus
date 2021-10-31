"""Download raw dataset."""

import logging
from pathlib import Path
from zipfile import PyZipFile

import gdown
import questionary

from cuticulus import const
from cuticulus.console import console

log = logging.getLogger('rich')


class Download(object):
    """Download raw dataset."""

    def __init__(self):
        """Initialize Download class."""
        self.raw = Path.cwd() / 'dataset.zip'
        self.base_path = Path.cwd() / 'dataset'
        self.download()

    def download_zip(self):
        """Download raw dataset .zip file."""
        if not self.raw.exists():
            console.log('Dataset .zip not found.')

            prompt = 'Okay to download dataset to: "{0}"?'.format(self.raw)
            if questionary.confirm(prompt).ask():
                log.info('Downloading dataset...')
                gdown.download(const.DATASET_URL, str(self.raw))
                log.info('Downloaded dataset!')
            else:
                console.log('Download cancelled.')

    def unzip_dataset(self):
        """Unzip dataset to the proper path."""
        if not self.base_path.exists():
            console.log('Dataset directory not found.')

            prompt = 'Okay to unzip dataset to: "{0}"?'.format(self.base_path)
            if questionary.confirm(prompt).ask():
                log.info('Extracting dataset...')
                PyZipFile(self.raw).extractall(str(self.base_path))
                log.info('Extracted dataset!')
            else:
                console.log('Extraction cancelled.')

    def download(self):
        """Download dataset.

        Raises:
            FileNotFoundError: cannot find zip or dataset
        """
        self.download_zip()
        self.unzip_dataset()

        if not self.raw.exists():
            raise FileNotFoundError

        if not self.base_path.exists():
            raise FileNotFoundError
