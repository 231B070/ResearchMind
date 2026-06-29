from utils.pdf_parser import extract_text


class PDFReaderAgent:

    def run(self, state):

        print("\n" + "=" * 80)

        print("📖 Reading PDFs...\n")

        for paper in state["ranked_papers"]:

            print(f"Reading : {paper.title}")

            print("PDF Path :", paper.local_pdf)

            text = extract_text(paper.local_pdf)

            paper.full_text = text

            print(f"Characters extracted : {len(text)}")

            print("-" * 80)

        return state