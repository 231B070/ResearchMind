from core.state import ResearchState
from agents.paper_summary_agent import PaperSummaryAgent
from agents.search_agent import SearchAgent
from agents.ranking_agent import RankingAgent
from agents.download_agent import DownloadAgent
from agents.pdf_reader import PDFReaderAgent
from agents.paper_parser import PaperParserAgent
from agents.claim_extractor import ClaimExtractorAgent
from agents.graph_builder import GraphBuilderAgent
from agents.embedding_agent import EmbeddingAgent
from agents.similarity_agent import SimilarityAgent
from agents.gap_agent import GapAgent
from agents.contradiction_agent import ContradictionAgent
from agents.research_idea_agent import ResearchIdeaAgent
from typing import Optional
from agents.literature_review_agent import LiteratureReviewAgent
from agents.proposal_agent import ProposalAgent

def run_pipeline(topic: str):

    state: ResearchState = {

        "topic": topic,

        "papers": [],

        "ranked_papers": [],

        "extracted_claims": [],

        "knowledge_graph": {},

        "contradictions": [],

        "research_gaps": [],

        "research_ideas": [],

        "experiment_plan": {},

        "proposal": ""

        literature_review: Optional[LiteratureReview]
    }

    state = SearchAgent().run(state)

    state = RankingAgent().run(state)

    state = DownloadAgent().run(state)

    state = PDFReaderAgent().run(state)

    state = PaperParserAgent().run(state)

    state = ClaimExtractorAgent().run(state)

    state = PaperSummaryAgent().run(state)
    
    state = LiteratureReviewAgent().run(state)

    state = ProposalAgent().run(state)
    
    state = GraphBuilderAgent().run(state)

    state = EmbeddingAgent().run(state)

    state = SimilarityAgent().run(state)

    state = GapAgent().run(state)

    state = ContradictionAgent().run(state)

    state = ResearchIdeaAgent().run(state)

    
    return state