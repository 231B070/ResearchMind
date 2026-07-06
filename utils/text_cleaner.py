"""
Text Cleaner
Cleans extracted research text.
"""

import re


def clean_text(text: str) -> str:

    if not text:
        return ""

    # remove newlines
    text = text.replace("\n", " ")

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # remove citations like [12]
    text = re.sub(r"\[\d+\]", "", text)

    # remove section numbers
    text = re.sub(r"\d+\.\d+", "", text)

    # remove parentheses
    text = text.replace("(", "")
    text = text.replace(")", "")

    return text.strip()