class RankingAgent:

    def run(self, state):

        papers = state["papers"]

        ranked = sorted(

            papers,

            key=lambda x: x.published,

            reverse=True

        )

        state["ranked_papers"] = ranked

        return state