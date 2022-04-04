from app.feature_extractor import FeatureExtractor


class NoFE(FeatureExtractor):
    def fit_transform(self, data_set):
        return data_set

    def fit(self, data_set):
        return data_set

    def transform(self, data_set):
        return data_set

