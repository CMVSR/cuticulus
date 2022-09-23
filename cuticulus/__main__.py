"""Main entrypoint."""
import shutil
from pathlib import Path

from dotenv import load_dotenv

from cuticulus.datasets import RoughSmoothFull


def main():
    """Run main function."""
    # load environment variables
    if not Path('.env').exists():
        shutil.copy('.env.example', '.env')
    load_dotenv()

    # build the dataset
    image_size = (256, 256)
    ds = RoughSmoothFull(
        size=image_size,
    )

    # create output directory
    output_path = Path('dataset')
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)
    shutil.copytree(ds.dir_path, output_path / ds.dir_path.name)

    # create output zip file
    if Path('{0}.zip').exists():
        shutil.rmtree(Path('{0}.zip'))
    shutil.make_archive(output_path, 'zip', output_path)


if __name__ == '__main__':
    main()
