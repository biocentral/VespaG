from __future__ import annotations

import os
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
# write test that Spearman on PG stays the same
import os

# Get the directory where this utils.py file is located
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load files relative to this module's location
raw_score_cdf = np.loadtxt(os.path.join(PACKAGE_DIR, "data/score_transformation/vespag_scores.csv"),
                           delimiter=",")
sorted_gemme_scores = np.loadtxt(os.path.join(PACKAGE_DIR, "data/score_transformation/sorted_gemme_scores.csv"),
                                 delimiter=",")


def transform_scores(scores: np.typing.ArrayLike[float]) -> list[float]:
    """Transform VespaG score distribution by mapping it to a known distribution of GEMME scores through its quantile"""
    # TODO vectorize, this is quick and dirty
    transformed_scores = []
    for score in scores:
        quantile = (raw_score_cdf <= score).mean()
        transformed_scores.append(np.interp(quantile, np.linspace(0, 1, len(sorted_gemme_scores)), sorted_gemme_scores))
    return transformed_scores


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
