
import logging
import os

import questionary


logger = logging.getLogger(__name__)


def download_dataset():
    import gdown  # type: ignore

    output = "./dataset.zip"

    if not os.path.isfile(output):
        logger.info("Downloading dataset...")
        url = "https://drive.google.com/uc?id=1xABlWE790uWmT0mMxbDjn9KZlNUB6Y57"
        gdown.download(url, output, quiet=False)
        assert os.path.isfile(output)
        logger.info("Downloaded dataset!")

    else:
        logger.info("Found dataset!")


def unzip_dataset(path="./dataset.zip"):
    out_path = os.path.join(os.curdir, "dataset")

    try:
        if not os.path.isdir(out_path):
            logger.info("Extracting dataset...")
            if os.path.isfile(path):
                from zipfile import PyZipFile
                zf = PyZipFile(path)
                zf.extractall(path=out_path)

                assert os.path.isdir(out_path)
                logger.info("Extracted dataset!")
            else:
                raise Exception(f"Failed to find {path}.")
        else:
            logger.info("Skipping extract...")

    except Exception as e:
        logger.error(f'Failed to unzip dataset:" {e}')
        raise e


def dataset_setup():
    if os.path.isdir("dataset"):
        logger.info("Found dataset!")
        return
    else:
        res = questionary.select("How should the dataset be initialized?",
                                 choices=[
                                     "Download dataset.zip from Google Drive",
                                     "I already have dataset.zip"
                                 ]
                                 ).ask()

        if res == "Download dataset.zip from Google Drive":
            download_dataset()
            unzip_dataset()
        elif res == "I already have dataset.zip":
            res = questionary.path("Path to dataset.zip").ask()
            res = res.replace("\\", "/")
            if res.endswith("dataset.zip"):
                os.rename(res, "dataset.zip")
                unzip_dataset(res)

    assert(os.path.isdir("dataset"))
    logger.info("Successfully initialized dataset.")
