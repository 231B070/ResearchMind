from dataclasses import dataclass


@dataclass
class ResearchProposal:
    """
    Represents an automatically generated research proposal.
    """

    title: str = ""

    abstract: str = ""

    problem_statement: str = ""

    objectives: str = ""

    methodology: str = ""

    dataset: str = ""

    evaluation: str = ""

    expected_contributions: str = ""

    future_scope: str = ""

    confidence: float = 0.0