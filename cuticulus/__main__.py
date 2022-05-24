"""Main entrypoint."""

from cuticulus.datasets import BackgroundSub

from rich import inspect


def main():
    """Run main function."""
    patch_size = (16, 16)
    ds = BackgroundSub(
        size=patch_size,
    )
    ds.stratified_split(n_samples=5000, clamp=True)


if __name__ == '__main__':
    main()
