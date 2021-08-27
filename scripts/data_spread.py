
import numpy as np

if __name__ == "__main__":
    # TODO: add AllSub, RoughSmoothFull, and AllFull
    # TODO: add class function for representing data spread
    # TODO: save tables to file for paper
    from cuticle_analysis.datasets import RoughSmoothSub  # noqa

    data = RoughSmoothSub((16, 16), save=True, rebuild=True)
    print(np.unique(data.labels))
