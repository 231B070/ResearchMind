import json

from services.llm_client import client


class TopicAnalyzerAgent:

    def run(self, topic):

        prompt = f"""
You are an expert AI research planner.

Analyze the following research topic:

{topic}

Return ONLY valid JSON.

Schema:

{{
    "primary_domain":"",
    "sub_domains":[],
    "search_queries":[]
}}
"""

        response = client.chat.completions.create(
    from config.settings import MODEL

...

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

        return json.loads(response.choices[0].message.content)