
import logging

import pandas as pd

from cuticle_analysis.datasets import GaborRoughSmoothFull
from cuticle_analysis.models import CNN

logger = logging.getLogger(__name__)

res_cols = ['size', 'samples_per_class', 'run', 'test_loss', 'test_accuracy']


if __name__ == "__main__":
    # use first 500 images for dataset
    excludes = list(range(500, 2877))

    sizes = [64, 128, 256, 512]
    samples_per_class = [250, 500, 750]

    # results
    df = pd.DataFrame(columns=res_cols)

    for size in sizes:
        for run in range(10):
            # build dataset
            data = GaborRoughSmoothFull(
                size=(size, size), excludes=excludes, save=True)
            for s in samples_per_class:
                # train and evaluate model
                model = CNN(data)
                model.train(1, s)
                loss, acc = model.evaluate()

                # save results
                run_df = pd.DataFrame([[size, s, loss, acc]], columns=res_cols)
                df.append(run_df, ignore_index=True)
                df.to_csv('./output/experiment_1.csv')
