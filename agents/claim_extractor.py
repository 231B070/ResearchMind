"""Agent that extracts structured scientific claims from parsed papers."""

from __future__ import annotations

import logging
from typing import List, Tuple

from core.models import Paper, ResearchClaim
from core.state import ResearchState
from engines.claim_engine import extract_claims

logger = logging.getLogger(__name__)

_CLAIM_FIELDS: List[Tuple[str, str, str]] = [
    ("problem", "Problem"),
    ("proposed_method", "Method"),
    ("dataset", "Dataset"),
    ("metric", "Metric"),
    ("results", "Results"),
    ("improvement", "Improvement"),
]


class ClaimExtractorAgent:
    """Extract and store structured research claims for each ranked paper."""

    def run(self, state: ResearchState) -> ResearchState:
        """
        Run claim extraction on every paper in ``state["ranked_papers"]``.

        Populates ``paper.claims`` and prints a summary for each paper.
        """
        for paper in state["ranked_papers"]:
            paper.claims = extract_claims(paper)
            self._print_summary(paper)
            logger.info(
                "Extracted %d claim(s) for '%s'",
                len(paper.claims),
                paper.title,
            )

        return state

    def _print_summary(self, paper: Paper) -> None:
        """Print extracted claim fields for a single paper."""
        claim = paper.claims[0] if paper.claims else ResearchClaim()

        print("----------------------------------")
        print("Paper")
        print(paper.title)
        print("\nClaims Extracted\n")

        for field_name, label in _CLAIM_FIELDS:
            value = getattr(claim, field_name, "")
            if value:
                print(f"✓ {label}")

        print("----------------------------------")
