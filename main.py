import time

from core.state import ResearchState

from agents.search_agent import SearchAgent
from agents.ranking_agent import RankingAgent
from agents.download_agent import DownloadAgent
from agents.pdf_reader import PDFReaderAgent
from agents.paper_parser import PaperParserAgent
from agents.claim_extractor import ClaimExtractorAgent
from agents.paper_summary_agent import PaperSummaryAgent
from agents.graph_builder import GraphBuilderAgent
from agents.embedding_agent import EmbeddingAgent
from agents.similarity_agent import SimilarityAgent
from agents.gap_agent import GapAgent
from agents.contradiction_agent import ContradictionAgent
from agents.research_idea_agent import ResearchIdeaAgent
from agents.literature_review_agent import LiteratureReviewAgent
from agents.proposal_agent import ProposalAgent
from agents.report_agent import ReportAgent
from agents.dashboard_agent import DashboardAgent


def main():

    print("\n" + "=" * 80)
    print("🔬 RESEARCHMIND")
    print("=" * 80)

    topic = input("\n🔍 Enter Research Topic: ").strip()

    if not topic:
        topic = "Multilingual OCR"

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

        "proposal": None,

        "literature_review": None,

        "report": None
    }

    start_time = time.time()

    # ==========================================================
    # 1. Search Papers
    # ==========================================================

    print("\n[1/13] 🔍 Searching Papers...\n")

    search_agent = SearchAgent()
    state = search_agent.run(state)

    if not state["papers"]:

        print("\n" + "=" * 80)
        print("❌ NO PAPERS FOUND")
        print("=" * 80)

        print(f"\nNo research papers found for '{topic}'.")

        print("Please try another research topic.")

        return

    print(f"✅ Papers Found : {len(state['papers'])}")

    # ==========================================================
    # 2. Rank Papers
    # ==========================================================

    print("\n[2/13] 📊 Ranking Papers...\n")

    ranking_agent = RankingAgent()
    state = ranking_agent.run(state)

    print(f"✅ Papers Ranked : {len(state['ranked_papers'])}")

    print("\n📄 Top Ranked Papers\n")

    for i, paper in enumerate(state["ranked_papers"], start=1):

        print("=" * 80)
        print(f"{i}. {paper.title}")
        print(f"Authors   : {', '.join(paper.authors)}")
        print(f"Published : {paper.published}")
        print(f"Source    : {paper.source}")
        print(f"PDF       : {paper.pdf_url}")

    # ==========================================================
    # 3. Download PDFs
    # ==========================================================

    print("\n[3/13] ⬇️ Downloading PDFs...\n")

    downloader = DownloadAgent()
    state = downloader.run(state)

    # ==========================================================
    # 4. Read PDFs
    # ==========================================================

    print("\n[4/13] 📖 Reading PDFs...\n")

    reader = PDFReaderAgent()
    state = reader.run(state)

    # ==========================================================
    # 5. Parse Papers
    # ==========================================================

    print("\n[5/13] 📑 Parsing Papers...\n")

    parser = PaperParserAgent()
    state = parser.run(state)

    # ==========================================================
    # 6. Claim Extraction
    # ==========================================================

    print("\n[6/13] 🧠 Extracting Claims...\n")

    claim_extractor = ClaimExtractorAgent()
    state = claim_extractor.run(state)

    # ==========================================================
    # 7. Paper Summaries
    # ==========================================================

    print("\n[7/13] 📄 Generating Paper Summaries...\n")

    summary_agent = PaperSummaryAgent()
    state = summary_agent.run(state)

    # ==========================================================
    # 8. Knowledge Graph
    # ==========================================================

    print("\n[8/13] 🕸️ Building Knowledge Graph...\n")

    graph_builder = GraphBuilderAgent()
    state = graph_builder.run(state)

    # ==========================================================
    # 9. Embeddings + Similarity
    # ==========================================================

    print("\n[9/13] 🤖 Computing Semantic Similarity...\n")

    embedding_agent = EmbeddingAgent()
    state = embedding_agent.run(state)

    similarity_agent = SimilarityAgent()
    state = similarity_agent.run(state)

    # ==========================================================
    # 10. Research Gaps
    # ==========================================================

    print("\n[10/13] 🔍 Discovering Research Gaps...\n")

    gap_agent = GapAgent()
    state = gap_agent.run(state)

    # ==========================================================
    # 11. Contradictions + Ideas
    # ==========================================================

    print("\n[11/13] 💡 Generating Research Ideas...\n")

    contradiction_agent = ContradictionAgent()
    state = contradiction_agent.run(state)

    idea_agent = ResearchIdeaAgent()
    state = idea_agent.run(state)

    # ==========================================================
    # 12. Literature Review + Proposal
    # ==========================================================

    print("\n[12/13] 📚 Generating Literature Review...\n")

    literature_agent = LiteratureReviewAgent()
    state = literature_agent.run(state)

    proposal_agent = ProposalAgent()
    state = proposal_agent.run(state)

    # ==========================================================
    # 13. Final Report
    # ==========================================================

    print("\n[13/13] 📄 Generating Final Report...\n")

    report_agent = ReportAgent()
    state = report_agent.run(state)

    dashboard_agent = DashboardAgent()
    state = dashboard_agent.run(state)

    # ==========================================================
    # Sample Outputs
    # ==========================================================

    if state["ranked_papers"]:

        paper = state["ranked_papers"][0]

        print("\n" + "=" * 80)

        print("\nDetected Sections for First Paper")
        print(paper.sections.keys())

        if paper.claims:

            print("\nFirst Extracted Claim")
            print(paper.claims[0])

        if hasattr(paper, "paper_summary") and paper.paper_summary:

            print("\nFirst Paper Executive Summary")
            print(paper.paper_summary.executive_summary)

    if state["literature_review"]:

        print("\nLiterature Review Generated Successfully.")

    # ==========================================================
    # Execution Summary
    # ==========================================================

    execution_time = time.time() - start_time

    graph = state["knowledge_graph"]

    if graph:

        stats = graph.statistics()

        nodes = stats["nodes"]
        edges = stats["edges"]

    else:

        nodes = 0
        edges = 0

    print("\n" + "=" * 80)
    print("📊 EXECUTION SUMMARY")
    print("=" * 80)

    print(f"Topic              : {state['topic']}")
    print(f"Papers Retrieved   : {len(state['ranked_papers'])}")
    print(f"Knowledge Nodes    : {nodes}")
    print(f"Knowledge Edges    : {edges}")
    print(f"Research Gaps      : {len(state['research_gaps'])}")
    print(f"Research Ideas     : {len(state['research_ideas'])}")
    print(f"Contradictions     : {len(state['contradictions'])}")
    print(f"Execution Time     : {execution_time:.2f} seconds")
    print("Report Saved       : output/research_report.txt")
    print("Knowledge Graph    : output/research_graph.graphml")
    print("Dashboard          : output/dashboard.html")

    print("\n" + "=" * 80)
    print("✅ RESEARCHMIND PIPELINE COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()