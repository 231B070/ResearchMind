"""
Contradiction Detection Engine
"""

from models.contradiction import Contradiction


class ContradictionEngine:

    def detect(self, papers):

        contradictions = []

        n = len(papers)

        for i in range(n):

            for j in range(i + 1, n):

                p1 = papers[i]
                p2 = papers[j]

                if not p1.claims or not p2.claims:
                    continue

                c1 = p1.claims[0]
                c2 = p2.claims[0]

                # ---------------------------------------
                # Same problem but different methods
                # ---------------------------------------

                if (
                    c1.problem
                    and c2.problem
                    and c1.problem == c2.problem
                    and c1.proposed_method
                    and c2.proposed_method
                    and c1.proposed_method != c2.proposed_method
                ):

                    contradictions.append(

                        Contradiction(

                            topic=c1.problem,

                            paper1=p1.title,

                            paper2=p2.title,

                            claim1=c1.proposed_method,

                            claim2=c2.proposed_method,

                            confidence=0.82,

                        )

                    )

        return contradictions