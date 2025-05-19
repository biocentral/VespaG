from __future__ import annotations

import math
import numpy as np
import sklearn.preprocessing

from typing import Literal, Iterable
from collections.abc import Sequence


GEMME_ALPHABET = "ACDEFGHIKLMNPQRSTVWY"
VESPA_ALPHABET = "ALGVSREDTIPKFQNYMHWC"
AMINO_ACIDS = sorted(GEMME_ALPHABET)

MODEL_VERSION = "v2"

# TODO make this more elegant, e.g. through .npz file
raw_vespag_scores = {
    "esm2": np.sort(np.loadtxt("data/score_transformation/vespag_scores.csv", delimiter=",")),
    "prott5": np.sort(np.loadtxt("data/score_transformation/vespag_scores_prott5.csv", delimiter=","))
}
gemme_scores = np.sort(np.loadtxt("data/score_transformation/sorted_gemme_scores.csv", delimiter=","))
target_space = np.linspace(0, 1, len(gemme_scores))


def transform_scores(scores: np.typing.ArrayLike[float], embedding_type: EmbeddingType = "esm2") -> list[float]:
    """Transform VespaG score distribution by mapping it to a known distribution of GEMME scores through its quantile"""
    quantiles = np.searchsorted(raw_vespag_scores[embedding_type], scores, side="right") / len(raw_vespag_scores[embedding_type])
    return np.interp(quantiles, target_space, gemme_scores)


class ScoreNormalizer:
    def __init__(self, type: Literal["sigmoid", "minmax"]) -> None:
        self.type = type
        if type == "minmax":
            self.scaler = sklearn.preprocessing.MinMaxScaler()
        else:
            self.scaler = None

    def fit(self, all_scores: np.ndarray | Iterable[float]) -> None:
        if type(all_scores) != np.ndarray:
            all_scores = np.array(all_scores)
        if self.type == "minmax":
            self.scaler.fit(all_scores.reshape(-1, 1))
        else:
            pass

    def normalize_score(self, score: float) -> float:
        """Normalize VespaG score to range."""
        return self.normalize_scores([score])[0]

    def normalize_scores(self, scores: np.ndarray | Sequence[float]) -> list[float]:
        """Normalize VespaG scores to range."""
        if self.type == "sigmoid":
            return [1 / (1 + math.exp(-score)) for score in scores]
        elif self.type == "minmax":
            if type(scores) != np.ndarray:
                scores = np.array(scores)
            return list(self.scaler.transform(scores.reshape(-1, 1)).reshape(-1))
