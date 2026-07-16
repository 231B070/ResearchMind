"""
Intelligent Paper Summary Engine
Generates research-quality summaries using extracted claims
and parsed paper sections.
"""

from core.models import Paper
from models.paper_summary import PaperSummary


class SummaryEngine:

    def generate(self, paper: Paper) -> PaperSummary:

        claim = paper.claims[0] if paper.claims else None

        if claim is None:
            return PaperSummary()

        # --------------------------------------------------
        # Executive Summary
        # --------------------------------------------------

        executive = self._generate_executive_summary(claim)

        # --------------------------------------------------
        # Technical Summary
        # --------------------------------------------------

        technical = self._generate_technical_summary(claim)

        # --------------------------------------------------
        # Research Insights
        # --------------------------------------------------

        insights = self._generate_research_insights(claim)

        # --------------------------------------------------
        # Research Gap
        # --------------------------------------------------

        gap = ""

        if claim.future_work:
            gap = (
                "Future work suggests that further research "
                "can improve the proposed approach."
            )

        elif claim.limitations:
            gap = (
                "Current limitations indicate opportunities "
                "for future research."
            )

        # --------------------------------------------------
        # Novelty Score
        # --------------------------------------------------

        score = self._compute_novelty_score(claim)

        # --------------------------------------------------

        return PaperSummary(

            executive_summary=executive,

            technical_summary=technical,

            research_insights=insights,

            contribution=self._generate_contribution(claim),

            methodology=claim.proposed_method,

            dataset=claim.dataset,

            metric=claim.metric,

            results=claim.results,

            limitations=claim.limitations,

            future_work=claim.future_work,

            research_gap=gap,

            novelty_score=score,

        )

    # ==========================================================
    # Executive Summary
    # ==========================================================

    def _generate_executive_summary(self, claim):

        sentences = []

        if claim.problem:

            sentences.append(
                f"This paper addresses {claim.problem.lower()}."
            )

        if claim.proposed_method:

            sentences.append(
                f"It introduces {claim.proposed_method}."
            )

        if claim.dataset:

            sentences.append(
                f"The proposed approach is evaluated on {claim.dataset}."
            )

        if claim.results:

            sentences.append(
                f"Experimental evaluation demonstrates {claim.results}"
            )

        return " ".join(sentences)

    # ==========================================================
    # Technical Summary
    # ==========================================================

    def _generate_technical_summary(self, claim):

        text = ""

        if claim.proposed_method:

            text += f"Method: {claim.proposed_method}\n\n"

        if claim.dataset:

            text += f"Dataset: {claim.dataset}\n\n"

        if claim.metric:

            text += f"Metric: {claim.metric}\n\n"

        if claim.results:

            text += f"Results: {claim.results}"

        return text.strip()

    # ==========================================================
    # Research Insights
    # ==========================================================

    def _generate_research_insights(self, claim):

        insights = []

        if claim.proposed_method:

            insights.append(
                f"Contribution: Introduces {claim.proposed_method}."
            )

        if claim.limitations:

            insights.append(
                f"Limitation: {claim.limitations}"
            )

        if claim.future_work:

            insights.append(
                f"Future Work: {claim.future_work}"
            )

        return "\n\n".join(insights)

    # ==========================================================
    # Contribution
    # ==========================================================

    def _generate_contribution(self, claim):

        if claim.proposed_method:

            return (
                f"The paper proposes "
                f"{claim.proposed_method}."
            )

        return ""

   
    def _compute_novelty_score(self, claim):

        score = 5.0

        if claim.proposed_method:
            score += 1.5

        if claim.dataset:
            score += 1.0

        if claim.results:
            score += 1.0

        if claim.improvement:
            score += 1.0

        if claim.future_work:
            score += 0.5

        return min(score, 10.0)