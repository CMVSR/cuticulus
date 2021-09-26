
import logging

import experiment
from cuticle_analysis.datasets import GaborRoughSmoothFull
from cuticle_analysis.models import CNN

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sizes = [64, 128, 256, 512]
    samples_per_class = [250, 500, 750]
    exp = experiment.ExperimentRunner(
        'experiment_1', GaborRoughSmoothFull, CNN)

    for size in sizes:
        for samples in samples_per_class:
            exp.run(samples, (size, size), runs=10, epochs=20, excludes=[])
