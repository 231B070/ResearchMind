

from engines.gap_engine import GapEngine


class GapAgent:

    def run(self, state):

        print("=" * 80)
        print("DISCOVERING RESEARCH GAPS")
        print("=" * 80)

        engine = GapEngine()

        gaps = engine.discover_gaps(
            state["ranked_papers"]
        )

        state["research_gaps"] = gaps

        print(f"\n✓ {len(gaps)} Research Gaps Found\n")

        for index, gap in enumerate(gaps, start=1):

            print("=" * 80)
            print(f"Research Gap #{index}")
            print("=" * 80)

            print(f"Research Area : {gap.research_area}")
            print(f"Observation   : {gap.observation}")
            print(f"Gap           : {gap.gap}")
            print(f"Opportunity   : {gap.opportunity}")
            print(f"Confidence    : {gap.confidence:.2f}")

            print()

        return state