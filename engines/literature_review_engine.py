"""
Literature Review Engine

Synthesizes multiple paper summaries into a structured
literature review.
"""

from models.literature_review import LiteratureReview


class LiteratureReviewEngine:

    def generate(self, state):

        papers = state["ranked_papers"]

        intro = self._build_introduction(state["topic"], papers)

        methods = self._build_methods(papers)

        datasets = self._build_datasets(papers)

        trends = self._build_trends(papers)

        gaps = self._build_gaps(state)

        conclusion = self._build_conclusion()

        return LiteratureReview(

            introduction=intro,

            existing_methods=methods,

            datasets=datasets,

            research_trends=trends,

            research_gaps=gaps,

            conclusion=conclusion

        )

    # ======================================================

    def _build_introduction(self, topic, papers):

        return (
            f"Recent research on {topic} has shown rapid progress "
            f"through deep learning, transformer-based architectures "
            f"and improved OCR techniques. "
            f"This review analyzes {len(papers)} representative papers "
            f"to understand current methodologies, datasets and "
            f"future research directions."
        )

    # ======================================================

    def _build_methods(self, papers):

        methods = set()

        for paper in papers:

            if paper.paper_summary:

                method = paper.paper_summary.methodology

                if method:

                    methods.add(method)

        if not methods:

            return "No common methodologies identified."

        return (
            "The surveyed literature primarily employs the following "
            "methods:\n\n• "
            + "\n• ".join(sorted(methods))
        )

    # ======================================================

    def _build_datasets(self, papers):

        datasets = set()

        for paper in papers:

            if paper.paper_summary:

                dataset = paper.paper_summary.dataset

                if dataset:

                    datasets.add(dataset)

        if not datasets:

            return "Dataset information unavailable."

        return (
            "Frequently used datasets include:\n\n• "
            + "\n• ".join(sorted(datasets))
        )

    # ======================================================

    def _build_trends(self, papers):

        trends = []

        methods = []

        for paper in papers:

            if paper.paper_summary:

                methods.append(
                    paper.paper_summary.methodology.lower()
                )

        joined = " ".join(methods)

        if "transformer" in joined:

            trends.append(
                "Growing adoption of Transformer-based architectures."
            )

        if "lstm" in joined:

            trends.append(
                "Sequence learning using LSTM/BLSTM remains common."
            )

        if "ocr" in joined:

            trends.append(
                "OCR systems increasingly integrate language models."
            )

        if not trends:

            trends.append(
                "Current research explores multiple OCR architectures."
            )

        return "\n• " + "\n• ".join(trends)

    # ======================================================

    def _build_gaps(self, state):

        gaps = state["research_gaps"]

        if not gaps:

            return "No research gaps identified."

        lines = []

        for gap in gaps:

            lines.append(gap.gap)

        return "\n• " + "\n• ".join(lines)

    # ======================================================

    def _build_conclusion(self):

        return (
            "The surveyed literature demonstrates significant progress "
            "in OCR systems. However, multilingual robustness, "
            "dataset diversity and generalization remain active "
            "research challenges."
        )