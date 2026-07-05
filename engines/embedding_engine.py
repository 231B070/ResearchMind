"""
Embedding Engine
Creates semantic embeddings for research papers.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingEngine:

    def __init__(self):

        print("\nLoading Embedding Model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("✓ Model Loaded\n")

    # ====================================================

    def create_embedding(self, paper):

        text = ""

        if hasattr(paper, "title"):
            text += paper.title + "\n"

        if hasattr(paper, "abstract"):
            text += paper.abstract + "\n"

        if hasattr(paper, "full_text"):

            # only first 3000 chars
            text += paper.full_text[:3000]

        embedding = self.model.encode(
            text,
            convert_to_tensor=False
        )

        paper.embedding = embedding

        return embedding