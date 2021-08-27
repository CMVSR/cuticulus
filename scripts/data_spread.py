
from cuticle_analysis.core import init
init()

from cuticle_analysis.datasets import RoughSmoothFull  # noqa
from cuticle_analysis.datasets import RoughSmoothSub  # noqa
from cuticle_analysis.datasets import AllFull  # noqa


rsf = RoughSmoothFull((512, 512), save=True)
rss = RoughSmoothSub((16, 16), save=True)
af = AllFull((512, 512), save=True)

print(f"type: full, size: {rsf.size}, {rsf.class_data()}")
print(f"type: subimage, size: {rss.size}, {rss.class_data()}")
print(f"type: full, size: {af.size}, {af.class_data()}")

# TODO: save tables to file for paper
