"""
Research Idea Generator Agent
"""

from engines.research_idea_engine import ResearchIdeaEngine


class ResearchIdeaAgent:

    def run(self, state):

        print("\n" + "=" * 80)
        print("💡 GENERATING RESEARCH IDEAS")
        print("=" * 80)

        engine = ResearchIdeaEngine()

        ideas = engine.generate(state)

        state["research_ideas"] = ideas

        if not ideas:

            print("\nNo research ideas generated.\n")

            return state

        print(f"\n✓ {len(ideas)} Research Ideas Generated\n")

        for i, idea in enumerate(ideas, start=1):

            print("=" * 80)
            print(f"Research Idea #{i}")
            print("=" * 80)

            print(f"Title                 : {idea.title}")
            print(f"Motivation            : {idea.motivation}")
            print(f"Research Gap          : {idea.research_gap}")
            print(f"Proposed Method       : {idea.proposed_method}")
            print(f"Potential Dataset     : {idea.potential_dataset}")
            print(f"Evaluation Metric     : {idea.evaluation_metric}")
            print(f"Expected Contribution : {idea.expected_contribution}")
            print(f"Confidence            : {idea.confidence:.2f}")

            print()

        return state