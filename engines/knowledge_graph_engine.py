"""
Knowledge Graph Engine
Converts ResearchClaim objects into Knowledge Graph nodes and edges.
"""

from graph.graph_store import KnowledgeGraph


class KnowledgeGraphEngine:

    def __init__(self):
        self.graph = KnowledgeGraph()

    def build_graph(self, paper):

        # -------------------------
        # Create Paper Node
        # -------------------------

        paper_id = paper.title

        self.graph.add_node(
            node_id=paper_id,
            node_type="Paper",
            label=paper.title,
            metadata={
                "year": paper.published,
                "source": paper.source
            }
        )

        # -------------------------
        # Authors
        # -------------------------

        for author in paper.authors:

            self.graph.add_node(
                node_id=author,
                node_type="Author",
                label=author
            )

            self.graph.add_edge(
                paper_id,
                author,
                "WRITTEN_BY"
            )

        # -------------------------
        # Claims
        # -------------------------

        for claim in paper.claims:

            self._add_claim(paper_id, claim)

        return self.graph

    # ===================================

    def _add_claim(self, paper_id, claim):

        self._create_node(
            paper_id,
            claim.problem,
            "Problem",
            "HAS_PROBLEM"
        )

        self._create_node(
            paper_id,
            claim.proposed_method,
            "Method",
            "PROPOSES"
        )

        self._create_node(
            paper_id,
            claim.dataset,
            "Dataset",
            "EVALUATED_ON"
        )

        self._create_node(
            paper_id,
            claim.metric,
            "Metric",
            "REPORTS"
        )

        self._create_node(
            paper_id,
            claim.improvement,
            "Improvement",
            "IMPROVES"
        )

        self._create_node(
            paper_id,
            claim.future_work,
            "FutureWork",
            "FUTURE_WORK"
        )

    # ===================================

    def _create_node(
        self,
        paper_id,
        value,
        node_type,
        relation
    ):

        if not value:
            return

        node_id = f"{node_type}:{value}"

        self.graph.add_node(
            node_id=node_id,
            node_type=node_type,
            label=value
        )

        self.graph.add_edge(
            paper_id,
            node_id,
            relation
        )