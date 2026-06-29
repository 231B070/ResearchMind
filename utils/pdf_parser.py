import fitz


def extract_text(pdf_path):

    try:

        doc = fitz.open(pdf_path)

        print(f"Pages : {len(doc)}")

        text = ""

        for page_number in range(len(doc)):

            page = doc.load_page(page_number)

            page_text = page.get_text("text")

            print(
                f"Page {page_number + 1} : {len(page_text)} characters"
            )

            text += page_text

        doc.close()

        return text

    except Exception as e:

        print("PDF Read Error :", e)

        return ""