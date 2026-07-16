"""
Contradiction Detection Agent
"""

from engines.contradiction_engine import ContradictionEngine


class ContradictionAgent:

    def run(self, state):

        print("\n" + "=" * 80)
        print("🔍 DETECTING RESEARCH CONTRADICTIONS")
        print("=" * 80)

        engine = ContradictionEngine()

        contradictions = engine.detect(
            state["ranked_papers"]
        )

        state["contradictions"] = contradictions

        if not contradictions:

            print("\n✓ No contradictions detected.\n")

            return state

        print(f"\n✓ {len(contradictions)} Potential Contradictions Found\n")

        for i, contradiction in enumerate(contradictions, start=1):

            print("=" * 80)
            print(f"Contradiction #{i}")
            print("=" * 80)

            print(f"Topic      : {contradiction.topic}")
            print(f"Paper 1    : {contradiction.paper1}")
            print(f"Claim      : {contradiction.claim1}")

            print()

            print(f"Paper 2    : {contradiction.paper2}")
            print(f"Claim      : {contradiction.claim2}")

            print()

            print(f"Confidence : {contradiction.confidence:.2f}")
            print()

        return state