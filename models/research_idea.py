"""
Research Idea Model
"""

from dataclasses import dataclass


@dataclass
class ResearchIdea:
    """
    Represents one AI-generated research idea.
    """

    title: str

    motivation: str

    research_gap: str

    proposed_method: str

    expected_contribution: str

    potential_dataset: str

    evaluation_metric: str

    confidence: float = 0.0