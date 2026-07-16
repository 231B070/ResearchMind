"""
Research Report Engine

Combines every module output into one final report.
"""

from models.research_report import ResearchReport


class ReportEngine:

    def generate(self, state):

        report = ResearchReport()

        report.topic = state["topic"]

        report.executive_summary = self._executive_summary(state)

        report.top_papers = self._top_papers(state)

        report.paper_summaries = self._paper_summaries(state)

        report.literature_review = self._literature_review(state)

        report.knowledge_graph_summary = self._knowledge_graph(state)

        report.research_gaps = self._research_gaps(state)

        report.contradictions = self._contradictions(state)

        report.research_ideas = self._research_ideas(state)

        report.research_proposal = self._proposal(state)

        report.conclusion = self._conclusion(state)

        return report

    # =====================================================

    def _executive_summary(self, state):

        return (
            f"This report presents an automated analysis of "
            f"{len(state['ranked_papers'])} research papers "
            f"related to '{state['topic']}'. "
            "ResearchMind extracted scientific claims, generated "
            "paper summaries, discovered research gaps, detected "
            "contradictions, produced research ideas, synthesized "
            "a literature review and generated a research proposal."
        )

    # =====================================================

    def _top_papers(self, state):

        lines = []

        for i, paper in enumerate(state["ranked_papers"], start=1):

            lines.append(
                f"{i}. {paper.title}"
            )

            lines.append(
                f"   Authors : {', '.join(paper.authors)}"
            )

            lines.append(
                f"   Published : {paper.published}"
            )

            lines.append(
                f"   Score : {paper.score:.2f}"
            )

            lines.append("")

        return "\n".join(lines)

    # =====================================================

    def _paper_summaries(self, state):

        lines = []

        for i, paper in enumerate(state["ranked_papers"], start=1):

            if not paper.paper_summary:
                continue

            summary = paper.paper_summary

            lines.append(f"PAPER {i}")

            lines.append(
                "-" * 40
            )

            lines.append(summary.executive_summary)

            lines.append("")

        return "\n".join(lines)

    # =====================================================

    def _literature_review(self, state):

        review = state["literature_review"]

        if review is None:

            return "No literature review generated."

        return f"""
INTRODUCTION

{review.introduction}

METHODS

{review.existing_methods}

DATASETS

{review.datasets}

RESEARCH TRENDS

{review.research_trends}

RESEARCH GAPS

{review.research_gaps}

CONCLUSION

{review.conclusion}
"""

    # =====================================================

    def _knowledge_graph(self, state):

        graph = state["knowledge_graph"]

        if not graph:

            return "Knowledge graph unavailable."

        stats = graph.statistics()

        return (
            f"Nodes : {stats['nodes']}\n"
            f"Edges : {stats['edges']}"
        )

    # =====================================================

    def _research_gaps(self, state):

        if not state["research_gaps"]:

            return "No research gaps detected."

        lines = []

        for gap in state["research_gaps"]:

            lines.append(f"• {gap.gap}")

        return "\n".join(lines)

    # =====================================================

    def _contradictions(self, state):

        if not state["contradictions"]:

            return "No contradictions detected."

        lines = []

        for item in state["contradictions"]:

            lines.append(str(item))

        return "\n".join(lines)

    # =====================================================

    def _research_ideas(self, state):

        if not state["research_ideas"]:

            return "No research ideas generated."

        lines = []

        for idea in state["research_ideas"]:

            lines.append(idea.title)

        return "\n".join(lines)

    # =====================================================

    def _proposal(self, state):

        proposal = state["proposal"]

        if proposal is None:

            return "Proposal unavailable."

        return f"""
TITLE

{proposal.title}

ABSTRACT

{proposal.abstract}

OBJECTIVES

{proposal.objectives}

METHODOLOGY

{proposal.methodology}

DATASET

{proposal.dataset}

EVALUATION

{proposal.evaluation}

EXPECTED CONTRIBUTIONS

{proposal.expected_contributions}

FUTURE SCOPE

{proposal.future_scope}
"""

    # =====================================================

    def _conclusion(self, state):

        return (
            f"ResearchMind successfully analyzed "
            f"{len(state['ranked_papers'])} papers and generated "
            f"{len(state['research_gaps'])} research gaps, "
            f"{len(state['research_ideas'])} research ideas, "
            "a complete literature review and an automatically "
            "generated research proposal."
        )