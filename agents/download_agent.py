import os
import requests
from tqdm import tqdm


class DownloadAgent:

    def __init__(self):

        self.save_dir = "data/papers"

        os.makedirs(self.save_dir, exist_ok=True)

    def sanitize_filename(self, text):

        invalid = '<>:"/\\|?*'

        for ch in invalid:
            text = text.replace(ch, "")

        return text[:100]

    def run(self, state):

        for paper in state["ranked_papers"]:

            filename = self.sanitize_filename(paper.title) + ".pdf"

            filepath = os.path.join(self.save_dir, filename)

            if os.path.exists(filepath):
                print(f"✓ Already exists : {filename}")
                continue

            print(f"Downloading : {paper.title}")

            response = requests.get(
                paper.pdf_url,
                stream=True,
                timeout=30
            )

            if response.status_code != 200:
                print("Failed")
                continue

            total = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as file:

                for chunk in tqdm(
                        response.iter_content(1024),
                        total=total // 1024,
                        unit="KB"):

                    file.write(chunk)

            print("Saved\n")

        return state