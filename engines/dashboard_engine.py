"""
Dashboard Engine
"""

import os


class DashboardEngine:

    def render(
        self,
        html,
        values,
    ):

        for key, value in values.items():

            html = html.replace(

                "{{"+key+"}}",

                str(value)

            )

        os.makedirs(
            "output",
            exist_ok=True
        )

        path = "output/dashboard.html"

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(html)

        return path