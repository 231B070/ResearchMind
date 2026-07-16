"""
Dashboard Agent
"""

import webbrowser
import pathlib
from engines.dashboard_engine import DashboardEngine


class DashboardAgent:

    def run(self, state):

        print("\n" + "=" * 80)
        print("📊 GENERATING DASHBOARD")
        print("=" * 80)

        graph = state["knowledge_graph"]

        stats = graph.statistics()

        papers = len(state["ranked_papers"])
        gaps = len(state.get("research_gaps", []))
        ideas = len(state.get("research_ideas", []))
        contradictions = len(state.get("contradictions", []))

        # ---------------------------------------
        # Research Ideas Table
        # ---------------------------------------

        idea_table = """
        <table>

        <tr>

        <th>Title</th>

        <th>Method</th>

        <th>Dataset</th>

        <th>Confidence</th>

        </tr>
        """

        for idea in state.get("research_ideas", []):

            idea_table += f"""

            <tr>

            <td>{idea.title}</td>

            <td>{idea.proposed_method}</td>

            <td>{idea.potential_dataset}</td>

            <td>{idea.confidence:.2f}</td>

            </tr>

            """

        idea_table += "</table>"

        # ---------------------------------------
        # Research Gap Table
        # ---------------------------------------

        gap_table = """
        <table>

        <tr>

        <th>Area</th>

        <th>Gap</th>

        <th>Confidence</th>

        </tr>
        """

        for gap in state.get("research_gaps", []):

            gap_table += f"""

            <tr>

            <td>{gap.research_area}</td>

            <td>{gap.gap}</td>

            <td>{gap.confidence:.2f}</td>

            </tr>

            """

        gap_table += "</table>"

        # ---------------------------------------
        # Load HTML Template
        # ---------------------------------------

        with open(
            "templates/dashboard.html",
            encoding="utf-8"
        ) as f:

            html = f.read()

        engine = DashboardEngine()

        path = engine.render(

            html,

            {

                "papers": papers,

                "nodes": stats["nodes"],

                "gaps": gaps,

                "ideas": ideas,

                "contradictions": contradictions,

                "idea_table": idea_table,

                "gap_table": gap_table,

            },

        )

        print(f"\n✓ Dashboard saved to {path}")


        webbrowser.open(
            pathlib.Path(path).resolve().as_uri()
        )

        return state