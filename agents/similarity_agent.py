"""
Similarity Agent
Computes similarity among research papers and recommends similar papers.
"""

from engines.similarity_engine import SimilarityEngine
from utils.similarity_utils import top_k_similar


class SimilarityAgent:

    def run(self, state):

        print("=" * 80)
        print("Computing Paper Similarity...\n")

        papers = state["ranked_papers"]

        engine = SimilarityEngine()

        similarity_matrix = engine.compute_similarity(papers)

        state["similarity_matrix"] = similarity_matrix

        print("✓ Similarity Matrix Created\n")

        print("=" * 80)
        print("PAPER RECOMMENDATIONS")
        print("=" * 80)

        recommendations = {}

        for paper_index, paper in enumerate(papers):

            print("\n" + "=" * 80)
            print(f"Paper:\n{paper.title}\n")
            print("Most Similar Papers\n")

            top_papers = top_k_similar(
                papers,
                similarity_matrix,
                paper_index,
                k=3
            )

            recommendations[paper.title] = top_papers

            for rank, rec in enumerate(top_papers, start=1):

                print(f"{rank}. {rec.title}")
                print(f"Similarity : {rec.similarity:.4f}\n")

        state["similar_papers"] = recommendations

        return state