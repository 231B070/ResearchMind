"""
Literature Review Agent

Generates a structured literature review from analyzed papers.
"""

import logging

from core.state import ResearchState
from engines.literature_review_engine import LiteratureReviewEngine

logger = logging.getLogger(__name__)


class LiteratureReviewAgent:

    def __init__(self):

        self.engine = LiteratureReviewEngine()

    def run(self, state: ResearchState):

        print("\n" + "=" * 80)
        print("📚 GENERATING LITERATURE REVIEW")
        print("=" * 80)

        review = self.engine.generate(state)

        state["literature_review"] = review

        logger.info("Literature review generated.")

        self._print_review(review)

        print("\n" + "=" * 80)
        print("✓ Literature Review Generated")
        print("=" * 80)

        return state

    # ======================================================

    def _print_review(self, review):

        print("\n📖 INTRODUCTION")
        print("-" * 60)
        print(review.introduction)

        print("\n⚙ EXISTING METHODS")
        print("-" * 60)
        print(review.existing_methods)

        print("\n📚 DATASETS")
        print("-" * 60)
        print(review.datasets)

        print("\n📈 RESEARCH TRENDS")
        print("-" * 60)
        print(review.research_trends)

        print("\n🔍 RESEARCH GAPS")
        print("-" * 60)
        print(review.research_gaps)

        print("\n🏁 CONCLUSION")
        print("-" * 60)
        print(review.conclusion)