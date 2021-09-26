
import logging
from typing import Type

import pandas as pd

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis.datasets import Dataset  # noqa
from cuticle_analysis.models import Model  # noqa

logger = logging.getLogger(__name__)

RES_COLS = ['size', 'samples_per_class', 'run',
            'loss', 'accuracy', 'error (mse)']


class ExperimentRunner:
    def __init__(self, name: str, dataset_type: Type[Dataset], model_type: Type[Model]):
        self.name = name
        self.dataset_type = dataset_type
        self.model_type = model_type
        self.res_df = pd.DataFrame(columns=RES_COLS)

    def append_df(self, df: pd.DataFrame):
        self.res_df = self.res_df.append(df, ignore_index=True)

    def save_df(self):
        self.res_df.to_csv(f'./output/{self.name}.csv')

    def run(self,
            samples: int,
            size: tuple,
            runs: int = 10,
            epochs: int = 10,
            excludes: list = []):
        dataset = self.dataset_type(size=size, excludes=excludes, save=True)

        for run in range(runs):
            model = self.model_type(dataset)
            model.train(epochs, samples)
            loss, acc, err = model.evaluate()

            # save results
            run_df = pd.DataFrame(
                [[
                    size,
                    samples,
                    run,
                    loss,
                    acc,
                    err
                ]], columns=RES_COLS)
            self.append_df(run_df)
            self.save_df()
