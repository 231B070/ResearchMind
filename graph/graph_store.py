"""
Knowledge Graph Storage
-----------------------
Wrapper around NetworkX MultiDiGraph.
"""

from typing import Any, Dict, List, Optional
import json
import networkx as nx


class KnowledgeGraph:
    """Knowledge Graph wrapper."""

    def __init__(self):
        self.graph = nx.MultiDiGraph()

    # ==========================================================
    # Add Node
    # ==========================================================

    def add_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:

        if metadata is None:
            metadata = {}

        # GraphML cannot store dicts directly.
        # Store metadata as JSON string.
        metadata_json = json.dumps(metadata)

        if not self.graph.has_node(node_id):

            self.graph.add_node(
                node_id,
                type=node_type,
                label=label,
                metadata=metadata_json,
            )

    # ==========================================================
    # Add Edge
    # ==========================================================

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
    ) -> None:

        self.graph.add_edge(
            source,
            target,
            relation=relation,
        )

    # ==========================================================
    # Find Node
    # ==========================================================

    def find_node(self, label: str):

        for node_id, data in self.graph.nodes(data=True):

            if data.get("label") == label:
                return node_id, data

        return None

    # ==========================================================
    # Find Nodes By Type
    # ==========================================================

    def find_nodes_by_type(self, node_type: str):

        result = []

        for node_id, data in self.graph.nodes(data=True):

            if data.get("type") == node_type:
                result.append((node_id, data))

        return result

    # ==========================================================
    # Node Exists
    # ==========================================================

    def node_exists(self, node_id: str):

        return self.graph.has_node(node_id)

    # ==========================================================
    # Neighbors
    # ==========================================================

    def get_neighbors(self, node_id: str):

        if not self.graph.has_node(node_id):
            return []

        return list(self.graph.neighbors(node_id))

    # ==========================================================
    # Statistics
    # ==========================================================

    def statistics(self):

        stats = {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
        }

        node_types = {}

        for _, data in self.graph.nodes(data=True):

            node_type = data.get("type", "Unknown")

            node_types[node_type] = node_types.get(node_type, 0) + 1

        stats["node_types"] = node_types

        return stats

    # ==========================================================
    # Export
    # ==========================================================

    def export_graphml(self, path: str):

        try:

            nx.write_graphml(self.graph, path)

            print(f"\n✓ Graph exported to {path}")

        except Exception as e:

            print(f"\n⚠ Graph export skipped")

            print(e)