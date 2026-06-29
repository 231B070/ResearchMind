from core.state import ResearchState

from agents.search_agent import SearchAgent
from agents.ranking_agent import RankingAgent
from agents.download_agent import DownloadAgent


def main():

    state: ResearchState = {

        "topic": "Multilingual OCR",

        "papers": [],

        "ranked_papers": [],

        "extracted_claims": [],

        "knowledge_graph": {},

        "contradictions": [],

        "research_gaps": [],

        "research_ideas": [],

        "experiment_plan": {},

        "proposal": ""

    }

    print("\n" + "=" * 80)
    print("RESEARCHMIND")
    print("=" * 80)

    print("\n🔍 Searching Papers...\n")

    search_agent = SearchAgent()
    state = search_agent.run(state)

    print("✅ Papers Found:", len(state["papers"]))

    print("\n📊 Ranking Papers...\n")

    ranking_agent = RankingAgent()
    state = ranking_agent.run(state)

    print("✅ Papers Ranked:", len(state["ranked_papers"]))

    print("\n📄 Top Ranked Papers\n")

    for i, paper in enumerate(state["ranked_papers"], start=1):

        print("=" * 80)
        print(f"{i}. {paper.title}")
        print(f"Authors   : {', '.join(paper.authors)}")
        print(f"Published : {paper.published}")
        print(f"Source    : {paper.source}")
        print(f"PDF       : {paper.pdf_url}")

    print("\n⬇️ Downloading PDFs...\n")

    downloader = DownloadAgent()
    state = downloader.run(state)

    print("\n" + "=" * 80)
    print("✅ Milestone 6 Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()