"""
Paper Summary Agent
Generates structured AI summaries for every research paper.
"""

import logging

from core.state import ResearchState
from engines.summary_engine import SummaryEngine

logger = logging.getLogger(__name__)


class PaperSummaryAgent:

    def __init__(self):
        self.engine = SummaryEngine()

    def run(self, state: ResearchState):

        print("\n" + "=" * 80)
        print("📄 GENERATING PAPER SUMMARIES")
        print("=" * 80)

        papers = state["ranked_papers"]

        for index, paper in enumerate(papers, start=1):

            paper.paper_summary = self.engine.generate(paper)
            print("\nDEBUG SUMMARY OBJECT")
            print("Methodology :", paper.paper_summary.methodology)
            print("Dataset     :", paper.paper_summary.dataset)
            print("Results     :", paper.paper_summary.results)
            print("-" * 50)
            logger.info(
                "Summary generated for '%s'",
                paper.title,
            )

            self._print_summary(index, paper)

        print("\n" + "=" * 80)
        print(f"✓ {len(papers)} Paper Summaries Generated")
        print("=" * 80)

        return state

    # =========================================================

    def _print_summary(self, index, paper):

        summary = paper.paper_summary

        print("\n" + "=" * 80)

        print(f"Paper {index}")

        print("=" * 80)

        print(paper.title)

        print("\n📄 Executive Summary")
        print("-" * 60)
        print(summary.executive_summary)

        print("\n⚙ Technical Summary")
        print("-" * 60)
        print(summary.technical_summary)

        print("\n🔬 Research Insights")
        print("-" * 60)
        print(summary.research_insights)

        print("\n⭐ Contribution")
        print("-" * 60)
        print(summary.contribution)

        print("\n📚 Dataset")
        print("-" * 60)
        print(summary.dataset)

        print("\n📈 Results")
        print("-" * 60)
        print(summary.results)

        print("\n⚠ Limitations")
        print("-" * 60)
        print(summary.limitations)

        print("\n🔮 Future Work")
        print("-" * 60)
        print(summary.future_work)

        print("\n💡 Research Gap")
        print("-" * 60)
        print(summary.research_gap)

        print("\n🚀 Novelty Score")
        print("-" * 60)
        print(f"{summary.novelty_score:.1f}/10")