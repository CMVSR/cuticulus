"""Model helper class for handling data before passing to model."""

from cuticulus.datasets import FullDataset


class ModelHelper(object):
    """Model helper class for handling data before passing to model."""

    def __init__(
        self,
        dataset: FullDataset,
        n_samples: int,
        validate: bool = False,
    ):
        """Initialize model helper class.

        Args:
            dataset (FullDataset): Dataset object.
            n_samples (int): Number of samples to use per class.
            validate (bool): Whether to use validation set.
        """
        self.ds = dataset
        self.validate = validate
        self.ds.stratified_split(n_samples)

        if self.validate:
            self.ds.split_validation()

        self.load()

    def load(self):
        """Load the dataset splits for model evaluation."""
        train_x, train_y = self.ds.train()
        self.train_x = train_x
        self.train_y = train_y

        test_x, test_y = self.ds.test()
        self.test_x = test_x
        self.test_y = test_y

        if self.validate:
            valid_x, valid_y = self.ds.validate()
            self.valid_x = valid_x
            self.valid_y = valid_y

    def reshape_pca(self):
        """Reshape dataset for PCA."""
        self.train_x = self.train_x.reshape(self.train_x.shape[0], -1)
        self.test_x = self.test_x.reshape(self.test_x.shape[0], -1)

        if self.validate:
            self.valid_x = self.valid_x.reshape(self.valid_x.shape[0], -1)
