"""
Research Gap Engine
Discovers research gaps from extracted claims.
"""

from collections import Counter

from models.research_gap import ResearchGap
from utils.keyword_extractor import extract_keyword


class GapEngine:

    def discover_gaps(self, papers):

        datasets = []
        methods = []
        problems = []

        # ---------------------------------------
        # Collect cleaned keywords
        # ---------------------------------------

        for paper in papers:

            if not hasattr(paper, "claims"):
                continue

            for claim in paper.claims:

                # -------------------------------
                # Dataset
                # -------------------------------
                if claim.dataset:

                    dataset = extract_keyword(claim.dataset)

                    if dataset:

                        for d in dataset.split(","):

                            d = d.strip()

                            if d:
                                datasets.append(d)

                # -------------------------------
                # Method
                # -------------------------------
                if claim.proposed_method:

                    method = extract_keyword(claim.proposed_method)

                    if method:

                        for m in method.split(","):

                            m = m.strip()

                            if m:
                                methods.append(m)

                # -------------------------------
                # Problem
                # -------------------------------
                if claim.problem:

                    problem = extract_keyword(claim.problem)

                    if problem:

                        for p in problem.split(","):

                            p = p.strip()

                            if p:
                                problems.append(p)

        dataset_counter = Counter(datasets)
        method_counter = Counter(methods)
        problem_counter = Counter(problems)

        gaps = []

        # =====================================================
        # DATASET GAP
        # =====================================================

        if dataset_counter:

            dataset, count = dataset_counter.most_common()[-1]

            gaps.append(

                ResearchGap(

                    research_area="Datasets",

                    observation=f"{len(dataset_counter)} unique datasets identified.",

                    gap=f"Dataset '{dataset}' appears only {count} time(s).",

                    opportunity="This dataset appears underexplored and could be expanded.",

                    confidence=0.75,

                )

            )

        # =====================================================
        # METHOD GAP
        # =====================================================

        if method_counter:

            method, count = method_counter.most_common()[-1]

            gaps.append(

                ResearchGap(

                    research_area="Methods",

                    observation=f"{len(method_counter)} unique methods identified.",

                    gap=f"Method '{method}' appears only {count} time(s).",

                    opportunity="Investigate or improve this method.",

                    confidence=0.70,

                )

            )

        # =====================================================
        # PROBLEM GAP
        # =====================================================

        if problem_counter:

            problem, count = problem_counter.most_common()[-1]

            gaps.append(

                ResearchGap(

                    research_area="Problems",

                    observation=f"{len(problem_counter)} unique problems identified.",

                    gap=f"Problem '{problem}' appears only {count} time(s).",

                    opportunity="This problem seems underexplored and deserves further research.",

                    confidence=0.68,

                )

            )

        return gaps