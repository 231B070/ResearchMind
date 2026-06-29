from tools.paper_sources.arxiv import search_arxiv


class SearchAgent:

    def run(self, state):

        topic = state["topic"]

        papers = search_arxiv(topic)

        state["papers"] = papers

        return state