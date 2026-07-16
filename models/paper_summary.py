from dataclasses import dataclass


@dataclass
class PaperSummary:
    """
    AI-generated structured summary of a research paper.
    """

    # Easy-to-read summary
    executive_summary: str = ""

    # Technical details
    technical_summary: str = ""

    # Researcher's perspective
    research_insights: str = ""

    # Structured fields
    contribution: str = ""

    methodology: str = ""

    dataset: str = ""

    metric: str = ""

    results: str = ""

    limitations: str = ""

    future_work: str = ""

    research_gap: str = ""

    novelty_score: float = 0.0