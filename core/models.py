from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ResearchClaim:
    """Structured scientific knowledge extracted from a research paper."""

    problem: str = ""
    proposed_method: str = ""
    dataset: str = ""
    baseline: str = ""
    metric: str = ""
    results: str = ""
    improvement: str = ""
    limitations: str = ""
    future_work: str = ""


@dataclass
class Paper:

    title: str

    authors: List[str]

    published: str

    summary: str

    pdf_url: str

    score: float = 0.0

    keywords: List[str] = field(default_factory=list)

    source: str = "arXiv"

    # NEW

    local_pdf: str = ""

    full_text: str = ""

    sections: Dict = field(default_factory=dict)

    claims: List[ResearchClaim] = field(default_factory=list)
