"""Dataset class for splitting for training, testing and validation."""

import numpy as np
from beartype import beartype

from cuticulus.console import console
from cuticulus.core.datasets.builder import DatasetBuilder


class DatasetSplitter(DatasetBuilder):
    """Dataset class for splitting for training, testing and validation."""

    @beartype
    def __init__(
        self,
        size: tuple[int, int] = (0, 0),
        name: str = '',
        rebuild: bool = False,
        save: bool = True,
    ):
        """Initialize the dataset.

        Args:
            size (tuple): Tuple with (rows, cols).
            name (str): The name of the dataset.
            rebuild (bool): Whether to rebuild the dataset.
            save(bool): Whether to save the generated files for the dataset.
        """
        super().__init__(
            size=size,
            name=name,
            rebuild=rebuild,
            save=save,
        )
        self.split = False
        self.split_val = False

    @beartype
    def stratified_split(
        self,
        n_samples: int,
        clamp: bool = False,
    ) -> None:
        """Stratified split with n_samples per class for training.

        Args:
            n_samples (int): Number of samples per class.
            clamp (bool): Whether to clamp the number of test samples to the
                minimum number of samples per class.
        """
        uniques = np.unique(self.labels)

        train_idxs = []
        for _, unique in enumerate(uniques):
            idxs = np.where(self.labels == unique)[0]
            np.random.shuffle(idxs)
            train_idxs.append(idxs[:n_samples])

        train_idxs = np.concatenate(train_idxs)
        test_idxs = np.setdiff1d(np.arange(len(self.labels)), train_idxs)

        self.train_idxs = train_idxs
        self.test_idxs = test_idxs
        self.split = True

        if clamp:
            # get number to clamp test samples to
            n_test = len(self.test_idxs)
            for unique in uniques:
                n_test_unique = len(
                    np.where(self.labels == unique)[0],
                ) - n_samples
                if n_test_unique < n_test:
                    n_test = n_test_unique

            # stratify test samples
            test_idxs = []
            for _, unique in enumerate(uniques):
                idxs = np.where(self.labels == unique)[0]
                idxs = np.intersect1d(idxs, self.test_idxs)
                np.random.shuffle(idxs)
                test_idxs.append(idxs[:n_test])

            self.test_idxs = np.concatenate(test_idxs).astype(int)

        assert not np.intersect1d(self.test_idxs, self.train_idxs).any()

        console.log('After splitting train and test:')
        self.print_split()

    def print_split(self):
        """Print the split.

        Raises:
            ValueError: If the dataset is not split.
        """
        if not self.split:
            raise ValueError('Dataset not split for training.')

        console.log('Training set:')
        _, trlabels = self.train()
        self.print_labels(trlabels)

        console.log('Testing set:')
        _, talabels = self.test()
        self.print_labels(talabels)

        if self.split_val:
            console.log('Validation set:')
            _, vlabels = self.validate()
            self.print_labels(vlabels)

    @beartype
    def split_validation(self, split: float = 0.5):
        """Split the dataset into training and validation.

        Args:
            split (float): The split ratio.

        Raises:
            ValueError: If the dataset is not split.
        """
        if not self.split:
            raise ValueError('Dataset not split.')

        val_idxs = np.random.choice(
            self.test_idxs,
            size=int(len(self.test_idxs) * split),
            replace=False,
        )

        self.val_idxs = val_idxs
        self.test_idxs = np.setdiff1d(self.test_idxs, val_idxs)
        self.split_val = True

        console.log('After splitting validation:')
        self.print_split()

    @beartype
    def train(self) -> tuple[np.ndarray, np.ndarray]:
        """Get the training data.

        Returns:
            tuple: Tuple with (X, y).

        Raises:
            ValueError: If the dataset is not split.
        """
        if not self.split:
            raise ValueError('Dataset not split.')

        return self.images[self.train_idxs], self.labels[self.train_idxs]

    @beartype
    def test(self) -> tuple[np.ndarray, np.ndarray]:
        """Get the testing data.

        Returns:
            tuple: Tuple with (X, y).

        Raises:
            ValueError: If the dataset is not split.
        """
        if not self.split:
            raise ValueError('Dataset not split.')

        return self.images[self.test_idxs], self.labels[self.test_idxs]

    @beartype
    def validate(self) -> tuple[np.ndarray, np.ndarray]:
        """Get the validation data.

        Returns:
            tuple: Tuple with (X, y).

        Raises:
            ValueError: If the dataset is not split.
        """
        if not self.split_val:
            raise ValueError('Dataset not split for validation.')

        return self.images[self.val_idxs], self.labels[self.val_idxs]
