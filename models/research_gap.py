
from dataclasses import dataclass


@dataclass
class ResearchGap:
    """
    Represents one discovered research gap.
    """

    research_area: str

    observation: str

    gap: str

    opportunity: str

    confidence: float = 0.0