"""Main entrypoint."""

from cuticulus.core.collages import build_collage
from cuticulus.datasets import RoughSmoothSub


def main():
    """Run main function."""
    patch_size = (32, 32)
    ds = RoughSmoothSub(
        size=patch_size,
        rebuild=True,
    )

    build_collage(
        ds.labels,
        ds.images,
        name='rs',
        rows=10,
        cols=10,
    )


if __name__ == '__main__':
    main()
