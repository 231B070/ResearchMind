from dataclasses import dataclass


@dataclass
class PaperRecommendation:

    title: str

    similarity: float

    paper_index: int