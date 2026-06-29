from dataclasses import dataclass

@dataclass
class ResearchPlan:
    topic: str
    steps: list

class PlannerAgent:

    def create_plan(self, topic: str):

        steps = [
            "Search Research Papers",
            "Rank Papers",
            "Read PDFs",
            "Extract Claims",
            "Build Knowledge Graph",
            "Detect Contradictions",
            "Find Research Gaps",
            "Generate Research Ideas",
            "Plan Experiments",
            "Generate Proposal"
        ]

        return ResearchPlan(topic, steps)