"""K-views model for image classification."""

import numpy as np
from beartype import beartype
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, cluster, rand_score

from cuticulus.console import console
from cuticulus.core.datasets.full import FullDataset
from cuticulus.core.models.helper import ModelHelper


class KViews(ModelHelper):
    """K-views model for image classification."""

    @beartype
    def __init__(
        self,
        dataset: FullDataset,
        k_classes: int,
        n_samples: int,
        n_components: int = 0,
    ):
        """Initialize K-views model.

        Args:
            dataset: Dataset to use.
            k_classes (int): Number of classes.
            n_samples (int): Number of samples per class to use.
            n_components (int): Number of components to use for PCA.
        """
        super().__init__(dataset=dataset, n_samples=n_samples)
        self.k_classes = k_classes
        self.n_components = n_components
        self.model = KMeans(n_clusters=k_classes)

        if n_components > 0:
            self.pca = PCA(n_components=n_components)
            self.reshape_pca()
        else:
            self.pca = None

        self.remapped = False

    def fit(self, analyze: bool = False):
        """Run K-views model.

        Args:
            analyze (bool): Whether to analyze the data.
        """
        self.train()
        self.predict_test()
        self.remap_centers()

        if analyze:
            self.run_analysis()

    def train(self):
        """Train K-views model."""
        train_x = self.train_x

        if self.pca:
            console.log('Fitting PCA...')
            train_x = self.pca.fit_transform(train_x)

        console.log('Fitting K-views model...')
        self.model.fit(train_x)

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess an image before input to predict.

        Args:
            image (np.ndarray): Image to preprocess.

        Returns:
            np.ndarray: Preprocessed image.
        """
        if self.pca:
            shape = (1, image.shape[0] * image.shape[1])
            image = image.reshape(shape)
            return self.pca.transform(image)
        return image

    def predict_test(self):
        """Predict test data."""
        test_x = self.test_x

        if self.pca:
            console.log('Transforming test data...')
            test_x = self.pca.transform(test_x)

        console.log('Predicting test data...')
        self.pred_y = self.predict(test_x)

    def remap_centers(self):
        """Change cluster ids to expected using ground truth."""
        cmatrix = cluster.contingency_matrix(
            self.pred_y,
            self.test_y,
            eps=1,
            dtype=int,
        )
        self.adjusted_centers = linear_sum_assignment(cmatrix, maximize=True)
        self.remapped = True

    @beartype
    def predict(self, images: np.ndarray) -> np.ndarray:
        """Predict labels for given images.

        Args:
            images (np.ndarray): Images to predict labels for.

        Returns:
            np.ndarray: Predicted labels.
        """
        preds = self.model.predict(images)
        if self.remapped:
            preds = np.array(
                [self.adjusted_centers[1][pred] for pred in preds],
            )
        return preds

    @beartype
    def run_analysis(self):
        """Analyze K-views model."""
        console.log('K-views model analysis')

        console.log('Predicted:')
        puniques, pcounts = np.unique(self.pred_y, return_counts=True)
        for pidx, _ in enumerate(puniques):
            console.log('{0}: {1}'.format(puniques[pidx], pcounts[pidx]))

        console.log('Expected:')
        euniques, ecounts = np.unique(self.test_y, return_counts=True)
        for eidx, _ in enumerate(euniques):
            console.log('{0}: {1}'.format(euniques[eidx], ecounts[eidx]))

        console.log('Rand Score: {0}'.format(
            round(rand_score(self.test_y, self.pred_y), 5),
        ))
        console.log('Adjusted Rand Score: {0}'.format(
            round(adjusted_rand_score(self.test_y, self.pred_y), 5),
        ))
