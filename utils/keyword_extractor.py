"""
Keyword Extractor
Extracts meaningful research keywords.
"""

import re

from utils.text_cleaner import clean_text


STOP_PHRASES = [

    "this paper",

    "we propose",

    "we present",

    "our approach",

    "our method",

    "in this work",

    "in this paper",

    "the proposed",

    "results show",

    "experimental results",

    "future work",

    "limitations",

    "background"
]


def extract_keyword(text: str):

    text = clean_text(text)

    lower = text.lower()

    for phrase in STOP_PHRASES:

        lower = lower.replace(phrase, "")

    text = lower.strip()

    # keep only first sentence
    text = re.split(r"[.;:]", text)[0]

    # limit length
    words = text.split()

    if len(words) > 10:
        words = words[:10]

    return " ".join(words).title()