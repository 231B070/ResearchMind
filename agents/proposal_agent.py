"""
Research Proposal Agent

Generates a complete research proposal from:
- Literature Review
- Research Gaps
- Research Ideas
"""

import logging

from core.state import ResearchState
from engines.proposal_engine import ProposalEngine

logger = logging.getLogger(__name__)


class ProposalAgent:

    def __init__(self):

        self.engine = ProposalEngine()

    def run(self, state: ResearchState):

        print("\n" + "=" * 80)
        print("📝 GENERATING RESEARCH PROPOSAL")
        print("=" * 80)

        proposal = self.engine.generate(state)

        state["proposal"] = proposal

        logger.info("Research Proposal Generated.")

        self._print(proposal)

        print("\n" + "=" * 80)
        print("✓ Research Proposal Generated")
        print("=" * 80)

        return state

    # =====================================================

    def _print(self, proposal):

        print("\nTITLE")
        print("-" * 60)
        print(proposal.title)

        print("\nABSTRACT")
        print("-" * 60)
        print(proposal.abstract)

        print("\nPROBLEM STATEMENT")
        print("-" * 60)
        print(proposal.problem_statement)

        print("\nOBJECTIVES")
        print("-" * 60)
        print(proposal.objectives)

        print("\nMETHODOLOGY")
        print("-" * 60)
        print(proposal.methodology)

        print("\nDATASET")
        print("-" * 60)
        print(proposal.dataset)

        print("\nEVALUATION")
        print("-" * 60)
        print(proposal.evaluation)

        print("\nEXPECTED CONTRIBUTIONS")
        print("-" * 60)
        print(proposal.expected_contributions)

        print("\nFUTURE SCOPE")
        print("-" * 60)
        print(proposal.future_scope)

        print("\nCONFIDENCE")
        print("-" * 60)
        print(f"{proposal.confidence:.2f}")