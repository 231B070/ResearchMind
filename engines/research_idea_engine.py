"""
Research Idea Engine
Professional Version
"""

import re

from models.research_idea import ResearchIdea


class ResearchIdeaEngine:

    def generate(self, state):

        ideas = []

        gaps = state.get("research_gaps", [])

        papers = state.get("ranked_papers", [])

        if not gaps or not papers:

            return ideas

        first_claim = papers[0].claims[0]

        best_method = self._best_method(
            first_claim.proposed_method
        )

        best_dataset = self._best_dataset(
            first_claim.dataset
        )

        metric = first_claim.metric or "Accuracy"

        for gap in gaps:

            gap_type, keyword = self._parse_gap(
                gap.gap
            )

            title = self._generate_title(
                best_method,
                gap_type,
                keyword
            )

            motivation = self._generate_motivation(
                gap_type,
                keyword
            )

            contribution = self._generate_contribution(
                best_method,
                keyword
            )

            confidence = self._confidence(
                best_method,
                best_dataset,
                metric
            )

            ideas.append(

                ResearchIdea(

                    title=title,

                    motivation=motivation,

                    research_gap=gap.gap,

                    proposed_method=best_method,

                    expected_contribution=contribution,

                    potential_dataset=best_dataset,

                    evaluation_metric=metric,

                    confidence=confidence,

                )

            )

        return ideas

    # ==========================================================
    # Helpers
    # ==========================================================

    def _best_method(self, methods):

        if not methods:

            return "Transformer"

        priority = [

            "Vision Transformer",

            "Transformer",

            "Line-Level OCR",

            "Post-OCR Text Correction",

            "CRNN",

            "BLSTM",

            "CNN",

            "OCR",

        ]

        for p in priority:

            if p.lower() in methods.lower():

                return p

        return methods.split(",")[0].strip()

    def _best_dataset(self, datasets):

        if not datasets:

            return "Public OCR Dataset"

        return datasets.split(",")[0].strip()

    def _parse_gap(self, gap):

        if "Dataset" in gap:

            m = re.search(r"'([^']+)'", gap)

            if m:

                return "dataset", m.group(1)

        if "Method" in gap:

            m = re.search(r"'([^']+)'", gap)

            if m:

                return "method", m.group(1)

        if "Problem" in gap:

            m = re.search(r"'([^']+)'", gap)

            if m:

                return "problem", m.group(1)

        return "general", "OCR"

    def _generate_title(
        self,
        method,
        gap_type,
        keyword,
    ):

        if gap_type == "dataset":

            return f"{method} for Low-Resource {keyword} Documents"

        if gap_type == "problem":

            return f"{method} for {keyword}"

        if gap_type == "method":

            return f"Hybrid {method} with {keyword}"

        return f"Advanced {method} for OCR"

    def _generate_motivation(
        self,
        gap_type,
        keyword,
    ):

        if gap_type == "dataset":

            return (
                f"Existing literature contains limited evaluation "
                f"on the {keyword} dataset."
            )

        if gap_type == "problem":

            return (
                f"The problem of {keyword.lower()} remains "
                f"underexplored in current literature."
            )

        if gap_type == "method":

            return (
                f"There is limited work combining "
                f"{keyword} with modern OCR techniques."
            )

        return (
            "Current literature reveals opportunities "
            "for improving OCR systems."
        )

    def _generate_contribution(
        self,
        method,
        keyword,
    ):

        return (
            f"Develop a robust {method} framework capable of "
            f"improving OCR performance for {keyword}."
        )

    def _confidence(
        self,
        method,
        dataset,
        metric,
    ):

        score = 0.70

        if method:

            score += 0.08

        if dataset:

            score += 0.07

        if metric:

            score += 0.05

        return round(min(score, 0.95), 2)