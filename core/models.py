from dataclasses import dataclass, field
from typing import List


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