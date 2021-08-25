
import logging
import os

import questionary


logger = logging.getLogger(__name__)


def download_dataset():
    import gdown  # type: ignore

    logger.info("Downloading dataset...")
    url = "https://drive.google.com/uc?id=1xABlWE790uWmT0mMxbDjn9KZlNUB6Y57"
    output = "./dataset.zip"
    gdown.download(url, output, quiet=False)

    assert os.path.isfile(output)
    logger.info("Downloaded dataset!")


def unzip_dataset(path="./dataset.zip"):
    logger.info("Extracting dataset...")
    out_path = os.path.join(os.curdir, "dataset")

    try:
        if not os.path.isdir(out_path):
            if os.path.isfile(path):
                from zipfile import PyZipFile
                zf = PyZipFile(path)
                zf.extractall(path=out_path)

                assert os.path.isdir(out_path)
                logger.info("Extracted dataset!")
            else:
                raise Exception(f"Failed to find {path}.")
        else:
            raise Exception(f"Directory {out_path} already exists.")

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
