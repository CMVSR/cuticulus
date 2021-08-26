
import numpy as np

if __name__ == "__main__":
    import cuticle_analysis
    print(cuticle_analysis)

    # for debugging
    # from cuticle_analysis.core import init
    # init()

    from cuticle_analysis.datasets import RoughSmoothSub  # noqa

    data = RoughSmoothSub((16, 16), save=True, rebuild=True)
    print(np.unique(data.labels))
