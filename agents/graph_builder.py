"""
Graph Builder Agent
Builds the Research Knowledge Graph from extracted claims.
"""

import os
from engines.knowledge_graph_engine import KnowledgeGraphEngine


class GraphBuilderAgent:

    def run(self, state):

        print("\n" + "=" * 80)
        print("🕸️ Building Knowledge Graph...\n")

        engine = KnowledgeGraphEngine()

        for paper in state["ranked_papers"]:

            print(f"Processing : {paper.title}")

            engine.build_graph(paper)

        graph = engine.graph

        state["knowledge_graph"] = graph

        stats = graph.statistics()

        print("\n" + "=" * 80)
        print("Knowledge Graph Summary")
        print("=" * 80)

        print(f"Total Nodes : {stats['nodes']}")
        print(f"Total Edges : {stats['edges']}")

        print("\nNode Types")

        for node_type, count in stats["node_types"].items():
            print(f"{node_type:15} : {count}")

        os.makedirs("output", exist_ok=True)

        graph.export_graphml("output/research_graph.graphml")

        print("\n✓ Graph exported to output/research_graph.graphml")

        return state