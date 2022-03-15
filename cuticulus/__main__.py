"""Main entrypoint."""

from cuticulus.datasets import AllFull, RoughSmoothFull


def main():
    """Run main function."""
    size = (256, 256)
    ds = AllFull(size)

    ds = RoughSmoothFull(size)
    ds.stratified_split(n_samples=800)
    ds.split_validation()


if __name__ == '__main__':
    main()
