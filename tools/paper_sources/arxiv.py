import feedparser
import urllib.parse

from core.models import Paper

BASE_URL = "https://export.arxiv.org/api/query?"


def search_arxiv(query: str, max_results: int = 5):

    search_query = urllib.parse.quote(query)

    url = (
        f"{BASE_URL}"
        f"search_query=all:{search_query}"
        f"&start=0"
        f"&max_results={max_results}"
    )

    feed = feedparser.parse(url)

    papers = []

    for entry in feed.entries:

        paper = Paper(
            title=entry.title,
            authors=[author.name for author in entry.authors],
            published=entry.published,
            summary=entry.summary,
            pdf_url=entry.id.replace("abs", "pdf") + ".pdf"
        )

        papers.append(paper)

    return papers