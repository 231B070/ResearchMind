"""
Contradiction Model
"""

from dataclasses import dataclass


@dataclass
class Contradiction:
    """
    Represents a possible contradiction between two research papers.
    """

    topic: str

    paper1: str

    paper2: str

    claim1: str

    claim2: str

    confidence: float = 0.0