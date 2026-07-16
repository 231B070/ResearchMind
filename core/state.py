from typing import TypedDict, List, Dict, Any
from core.models import Paper
from models.literature_review import LiteratureReview
from typing import Optional
from models.research_proposal import ResearchProposal
from models.research_report import ResearchReport
from typing import Optional

class ResearchState(TypedDict):

    topic: str

    papers: List[Paper]

    ranked_papers: List[Paper]

    extracted_claims: List[Dict[str, Any]]

    knowledge_graph: Dict[str, Any]

    contradictions: List[Dict[str, Any]]

    research_gaps: List[str]

    research_ideas: List[str]

    experiment_plan: Dict[str, Any]

    proposal: Optional[ResearchProposal]

    literature_review: LiteratureReview

    report: Optional[ResearchReport]