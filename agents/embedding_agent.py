"""
Embedding Agent
Creates embeddings for all ranked papers.
"""

from engines.embedding_engine import EmbeddingEngine


class EmbeddingAgent:

    def run(self, state):

        print("=" * 80)
        print("Creating Semantic Embeddings...\n")

        engine = EmbeddingEngine()

        for index, paper in enumerate(state["ranked_papers"], start=1):

            print(f"[{index}] {paper.title}")

            engine.create_embedding(paper)

        print("\n✓ All embeddings created.")

        return state