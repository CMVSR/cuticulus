
import logging

from cuticle_analysis.datasets import GaborRoughSmoothFull
from cuticle_analysis.models import CNN

import base

logger = logging.getLogger(__name__)

sizes = [64, 128, 256, 512]
samples_per_class = [250, 500, 750]
exp = base.ExperimentRunner('experiment_1', GaborRoughSmoothFull, CNN)

for size in sizes:
    for samples in samples_per_class:
        exp.run(samples, size, runs=10, epochs=20, excludes=[])
