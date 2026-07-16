"""
Research Proposal Engine

Generates a complete research proposal using:

• Literature Review
• Research Ideas
• Research Gaps
• Paper Summaries
"""

from models.research_proposal import ResearchProposal


class ProposalEngine:

    def generate(self, state):

        topic = state["topic"]

        ideas = state["research_ideas"]

        gaps = state["research_gaps"]

        literature = state["literature_review"]

        papers = state["ranked_papers"]

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = self._generate_title(topic, ideas)

        # ----------------------------------------------------
        # Abstract
        # ----------------------------------------------------

        abstract = self._generate_abstract(
            topic,
            literature,
            ideas,
            gaps
        )

        # ----------------------------------------------------
        # Problem Statement
        # ----------------------------------------------------

        problem = self._generate_problem_statement(gaps)

        # ----------------------------------------------------
        # Objectives
        # ----------------------------------------------------

        objectives = self._generate_objectives(gaps)

        # ----------------------------------------------------
        # Methodology
        # ----------------------------------------------------

        methodology = self._generate_methodology(
            ideas,
            papers
        )

        # ----------------------------------------------------
        # Dataset
        # ----------------------------------------------------

        dataset = self._generate_dataset(
            ideas,
            papers
        )

        # ----------------------------------------------------
        # Evaluation
        # ----------------------------------------------------

        evaluation = self._generate_evaluation(
            ideas,
            papers
        )

        # ----------------------------------------------------
        # Contributions
        # ----------------------------------------------------

        contributions = self._generate_contributions(gaps)

        # ----------------------------------------------------
        # Future Scope
        # ----------------------------------------------------

        future_scope = self._generate_future_scope(
            literature,
            papers
        )

        return ResearchProposal(

            title=title,

            abstract=abstract,

            problem_statement=problem,

            objectives=objectives,

            methodology=methodology,

            dataset=dataset,

            evaluation=evaluation,

            expected_contributions=contributions,

            future_scope=future_scope,

            confidence=0.92

        )

    # ======================================================
    # TITLE
    # ======================================================

    def _generate_title(self, topic, ideas):

        if ideas:

            return ideas[0].title

        return f"Novel Research Proposal on {topic}"

    # ======================================================
    # ABSTRACT
    # ======================================================

    def _generate_abstract(

        self,

        topic,

        literature,

        ideas,

        gaps

    ):

        abstract = []

        abstract.append(

            f"Recent advances in {topic} have significantly improved "

            "research performance through deep learning, attention "

            "mechanisms and language-aware architectures."

        )

        if gaps:

            abstract.append(

                f"However, current literature reveals that "

                f"{gaps[0].gap.lower()}."

            )

        if ideas:

            abstract.append(

                f"This proposal introduces "

                f"{ideas[0].proposed_method.lower()} "

                "to address the identified research gap."

            )

        abstract.append(

            "The proposed system will be evaluated on benchmark "

            "datasets using standard evaluation metrics."

        )

        abstract.append(

            "The expected outcome is a more robust and accurate "

            "solution capable of improving current state-of-the-art "

            "performance."

        )

        return " ".join(abstract)

    # ======================================================
    # PROBLEM
    # ======================================================

    def _generate_problem_statement(self, gaps):

        if not gaps:

            return (

                "Current literature indicates several unresolved "

                "research challenges."

            )

        return (

            "The primary problem identified during literature "

            "analysis is:\n\n"

            f"{gaps[0].gap}"

        )

    # ======================================================
    # OBJECTIVES
    # ======================================================

    def _generate_objectives(self, gaps):

        objectives = [

            "• Improve the performance of existing approaches.",

            "• Address the identified research gap.",

            "• Evaluate the proposed solution on benchmark datasets.",

            "• Compare results against existing state-of-the-art methods."

        ]

        if gaps:

            objectives.append(

                f"• Specifically investigate {gaps[0].research_area.lower()}."

            )

        return "\n".join(objectives)

    # ======================================================
    # METHODOLOGY
    # ======================================================

    def _generate_methodology(self, ideas, papers):

        if ideas:

            return ideas[0].proposed_method

        if papers and papers[0].claims:

            return papers[0].claims[0].proposed_method

        return "To be determined"

    # ======================================================
    # DATASET
    # ======================================================

    def _generate_dataset(self, ideas, papers):

        if ideas:

            return ideas[0].potential_dataset

        if papers and papers[0].claims:

            return papers[0].claims[0].dataset

        return "Benchmark Dataset"

    # ======================================================
    # EVALUATION
    # ======================================================

    def _generate_evaluation(self, ideas, papers):

        if ideas:

            return ideas[0].evaluation_metric

        if papers and papers[0].claims:

            return papers[0].claims[0].metric

        return "Accuracy"

    # ======================================================
    # CONTRIBUTIONS
    # ======================================================

    def _generate_contributions(self, gaps):

        contributions = [

            "• Improved research methodology.",

            "• Better benchmark evaluation.",

            "• More robust solution.",

            "• Improved reproducibility."

        ]

        if gaps:

            contributions.append(

                f"• Addresses the gap in {gaps[0].research_area.lower()}."

            )

        return "\n".join(contributions)

    # ======================================================
    # FUTURE SCOPE
    # ======================================================

    def _generate_future_scope(self, literature, papers):

        scope = [

            "• Extend evaluation to larger multilingual datasets.",

            "• Explore Transformer-based architectures.",

            "• Integrate Large Language Models.",

            "• Improve real-world deployment."

        ]

        for paper in papers:

            if paper.claims:

                future = paper.claims[0].future_work

                if future:

                    scope.append(

                        f"• {future}"

                    )

                    break

        return "\n".join(scope)