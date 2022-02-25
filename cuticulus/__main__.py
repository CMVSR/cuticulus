"""Main entrypoint."""

from rich import inspect

from cuticulus.datasets import RoughSmoothFull


def main():
    """Run main function."""
    ds = RoughSmoothFull((512, 512), rebuild=True)
    inspect(ds)


if __name__ == '__main__':
    main()
