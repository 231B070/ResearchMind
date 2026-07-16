"""
Research Report Agent

Generates and saves the final ResearchMind report.
"""

import os
import logging

from core.state import ResearchState
from engines.report_engine import ReportEngine

logger = logging.getLogger(__name__)


class ReportAgent:

    def __init__(self):

        self.engine = ReportEngine()

    def run(self, state: ResearchState):

        print("\n" + "=" * 80)
        print("📄 GENERATING FINAL RESEARCH REPORT")
        print("=" * 80)

        report = self.engine.generate(state)

        state["report"] = report

        self._save_txt(report)

        logger.info("Research Report Generated")

        print("\n✓ Report saved successfully")

        return state

    # =====================================================

    def _save_txt(self, report):

        os.makedirs("output", exist_ok=True)

        path = os.path.join(
            "output",
            "research_report.txt"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("=" * 80 + "\n")
            f.write("RESEARCHMIND REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"TOPIC\n\n{report.topic}\n\n")

            f.write("=" * 80 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.executive_summary + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("TOP PAPERS\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.top_papers + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("PAPER SUMMARIES\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.paper_summaries + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("LITERATURE REVIEW\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.literature_review + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("KNOWLEDGE GRAPH\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.knowledge_graph_summary + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("RESEARCH GAPS\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.research_gaps + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("CONTRADICTIONS\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.contradictions + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("RESEARCH IDEAS\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.research_ideas + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("RESEARCH PROPOSAL\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.research_proposal + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("CONCLUSION\n")
            f.write("=" * 80 + "\n\n")
            f.write(report.conclusion + "\n")

        print(f"\n📁 TXT Report Saved : {path}")