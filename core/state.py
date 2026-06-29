from typing import TypedDict, List, Dict, Any
from core.models import Paper


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

    proposal: str