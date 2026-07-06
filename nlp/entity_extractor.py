"""
Scientific Entity Extractor
Extracts methods, datasets, metrics and research problems.
"""

from nlp.scientific_dictionary import (
    METHODS,
    DATASETS,
    METRICS,
    PROBLEMS,
)


class EntityExtractor:

    def __init__(self):

        self.methods = METHODS
        self.datasets = DATASETS
        self.metrics = METRICS
        self.problems = PROBLEMS

    # ======================================================

    def extract_methods(self, text):

        return self._find_matches(text, self.methods)

    # ======================================================

    def extract_datasets(self, text):

        return self._find_matches(text, self.datasets)

    # ======================================================

    def extract_metrics(self, text):

        return self._find_matches(text, self.metrics)

    # ======================================================

    def extract_problems(self, text):

        return self._find_matches(text, self.problems)

    # ======================================================

    def _find_matches(self, text, dictionary):

        if not text:
            return []

        lower = text.lower()

        matches = []

        for item in dictionary:

            if item.lower() in lower:

                matches.append(item)

        return list(dict.fromkeys(matches))