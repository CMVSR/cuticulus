"""Main entrypoint."""

from cuticulus.datasets import RoughSmoothFull
from cuticulus.models import KViews


def main():
    """Run main function."""
    ds = RoughSmoothFull((512, 512))

    samples = 750
    model = KViews(ds, 2, n_samples=samples, n_components=3)
    model.fit(analyze=True)


if __name__ == '__main__':
    main()
