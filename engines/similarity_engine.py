"""
Similarity Engine
Computes semantic similarity between research papers.
"""

from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:

    def compute_similarity(self, papers):

        embeddings = []

        for paper in papers:
            embeddings.append(paper.embedding)

        similarity_matrix = cosine_similarity(embeddings)

        return similarity_matrix