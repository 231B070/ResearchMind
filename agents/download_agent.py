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

        print("\n⬇️ Downloading PDFs...\n")

        for paper in state["ranked_papers"]:

            filename = self.sanitize_filename(paper.title) + ".pdf"

            filepath = os.path.join(self.save_dir, filename)

            # ⭐ IMPORTANT
            # Always save the local path, even if the PDF already exists.
            paper.local_pdf = filepath

            if os.path.exists(filepath):
                print(f"✓ Already exists : {filename}")
                continue

            print(f"Downloading : {paper.title}")

            try:

                response = requests.get(
                    paper.pdf_url,
                    stream=True,
                    timeout=30
                )

                if response.status_code != 200:
                    print(f"❌ Failed ({response.status_code})")
                    continue

                print("Content-Type:", response.headers.get("content-type"))

                total = int(response.headers.get("content-length", 0))

                with open(filepath, "wb") as file:

                    for chunk in tqdm(
                        response.iter_content(chunk_size=1024),
                        total=total // 1024 if total else None,
                        unit="KB"
                    ):
                        if chunk:
                            file.write(chunk)

                print(f"✅ Saved : {filename}\n")

            except Exception as e:
                print(f"❌ Error downloading {paper.title}")
                print(e)

        return state