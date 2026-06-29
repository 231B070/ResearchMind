"""Agent that parses structured sections from paper full text."""

from __future__ import annotations

from core.state import ResearchState
from core.models import Paper
from utils.section_detector import CANONICAL_SECTIONS, detect_sections


class PaperParserAgent:
    """Detect and store academic sections for each ranked paper."""

    def run(self, state: ResearchState) -> ResearchState:
        """
        Parse ``full_text`` for every paper in ``state["ranked_papers"]``.

        Populates ``paper.sections`` and prints a summary for each paper.
        """
        for paper in state["ranked_papers"]:
            paper.sections = detect_sections(paper.full_text)
            self._print_summary(paper)

        return state

    def _print_summary(self, paper: Paper) -> None:
        """Print detected and missing sections for a single paper."""
        found = [name for name in CANONICAL_SECTIONS if name in paper.sections]
        missing = [name for name in CANONICAL_SECTIONS if name not in paper.sections]

        print("------------------------------------")
        print(f"Paper:\n{paper.title}\n")
        print("Sections Found:")
        for name in found:
            print(f"✓ {name}")

        print("\nMissing:")
        if missing:
            for name in missing:
                print(name)
        else:
            print("(none)")

        print("------------------------------------")
