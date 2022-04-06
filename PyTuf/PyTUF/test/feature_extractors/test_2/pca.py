from app.abstract.feature_extractor import FeatureExtractor
from sklearn.decomposition import PCA

class myPCA(FeatureExtractor):
    def __init__(self):
        self.pca = PCA(n_components=1)

    def fit_transform(self, data_set):
        return self.pca.fit_transform(data_set)

    def fit(self, data_set):
        self.pca.fit(data_set)

    def transform(self, data_set):
        return self.pca.transform(data_set)
