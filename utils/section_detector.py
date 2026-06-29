"""Detect academic paper sections from extracted full text using regex."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# Canonical section names in display order (used for found / missing reporting).
CANONICAL_SECTIONS: List[str] = [
    "Abstract",
    "Introduction",
    "Related Work",
    "Background",
    "Methodology",
    "Dataset",
    "Experiments",
    "Results",
    "Discussion",
    "Limitations",
    "Future Work",
    "Conclusion",
    "References",
]

# Maps each canonical name to regex patterns matched against normalized headings.
SECTION_ALIASES: Dict[str, List[str]] = {
    "Abstract": [r"abstract"],
    "Introduction": [r"introduction"],
    "Related Work": [r"related\s+work"],
    "Background": [r"background"],
    "Methodology": [
        r"methodology",
        r"methods?",
        r"approach(?:es)?",
        r"proposed\s+method",
    ],
    "Dataset": [r"datasets?", r"data\s+set"],
    "Experiments": [r"experiments?", r"experimental\s+setup"],
    "Results": [r"results?", r"evaluation"],
    "Discussion": [r"discussion"],
    "Limitations": [r"limitations?"],
    "Future Work": [r"future\s+work"],
    "Conclusion": [r"conclusions?"],
    "References": [r"references?", r"bibliography"],
}

_HEADING_PREFIX = r"(?:[IVXLC]+|\d+(?:\.\d+)*)\.\s*"

_PREFIXED_HEADING = re.compile(
    rf"^\s*{_HEADING_PREFIX}(?P<title>.+?)\s*$",
    re.MULTILINE,
)

_STANDALONE_CAPS = re.compile(
    r"^\s*(?P<title>[A-Z][A-Z\s\-&]{2,})\s*$",
    re.MULTILINE,
)

_NUMBERED_TITLE_HEADING = re.compile(
    r"^\s*\d+(?:\.\d+)*\.?\s+(?P<title>[A-Z][A-Za-z\s\-&]+)\s*$",
    re.MULTILINE,
)

_PAGE_MARKER = re.compile(r"^\s*--\s*\d+\s+of\s+\d+\s*--\s*$", re.MULTILINE)

_TABLE_LABEL = re.compile(r"(?i)Table\s+[IVXLC\d]+\s*$")

_ABSTRACT_INLINE = re.compile(r"(?i)\bAbstract\s*[—\-–:.]?\s*")

_ABSTRACT_END = re.compile(
    r"(?i)(?:^|\n)(?:"
    r"Keywords|Index Terms|"
    rf"(?:{_HEADING_PREFIX})?(?:INTRODUCTION|Introduction)"
    r")",
    re.MULTILINE,
)

_HEADING_PATTERNS = (
    _PREFIXED_HEADING,
    _STANDALONE_CAPS,
    _NUMBERED_TITLE_HEADING,
)


def detect_sections(full_text: str) -> Dict[str, str]:
    """
    Parse *full_text* and return a mapping of canonical section names to content.

    Headings are matched case-insensitively and may include numeric or Roman
    numeral prefixes (e.g. ``1 Introduction``, ``I. INTRODUCTION``).
    """
    if not full_text or not full_text.strip():
        return {}

    headings = _find_headings(full_text)
    sections: Dict[str, str] = {}

    for index, (start, end, canonical) in enumerate(headings):
        if canonical in sections:
            continue

        content_start = end
        content_end = headings[index + 1][0] if index + 1 < len(headings) else len(full_text)
        content = full_text[content_start:content_end].strip()
        if content:
            sections[canonical] = content

    abstract = _extract_inline_abstract(full_text)
    if abstract and "Abstract" not in sections:
        sections["Abstract"] = abstract

    return sections


def _find_headings(text: str) -> List[Tuple[int, int, str]]:
    """Return sorted ``(start, end, canonical_name)`` tuples for each heading."""
    candidates: List[Tuple[int, int, str]] = []

    for pattern in _HEADING_PATTERNS:
        for match in pattern.finditer(text):
            title = match.group("title").strip()
            if not _is_valid_heading(title, text, match.start()):
                continue

            canonical = _classify_heading(title)
            if canonical is None:
                continue

            candidates.append((match.start(), match.end(), canonical))

    candidates.sort(key=lambda item: item[0])
    return _deduplicate_headings(candidates)


def _deduplicate_headings(
    candidates: List[Tuple[int, int, str]],
) -> List[Tuple[int, int, str]]:
    """Keep the first occurrence of each canonical section."""
    seen: set[str] = set()
    result: List[Tuple[int, int, str]] = []

    for start, end, canonical in candidates:
        if canonical in seen:
            continue
        seen.add(canonical)
        result.append((start, end, canonical))

    return result


def _is_valid_heading(title: str, text: str, start: int) -> bool:
    """Return True when *title* looks like a section heading rather than body text."""
    if _PAGE_MARKER.match(title):
        return False
    if len(title) > 80 or len(title.split()) > 10:
        return False
    if _preceded_by_table_label(text, start):
        return False
    if _classify_heading(title) is None:
        return False
    if _is_all_caps_heading(title):
        return True
    return _is_title_case_heading(title)


def _is_all_caps_heading(title: str) -> bool:
    """Return True when every alphabetic character in *title* is uppercase."""
    letters = [character for character in title if character.isalpha()]
    return bool(letters) and all(character.isupper() for character in letters)


def _is_title_case_heading(title: str) -> bool:
    """Return True when *title* uses title case (e.g. ``Related Work``)."""
    words = title.split()
    if not words or len(words) > 6:
        return False

    minor_words = {"and", "or", "the", "of", "in", "on", "a", "an", "to", "for"}
    for word in words:
        if word.lower() in minor_words:
            continue
        if not word[0].isupper():
            return False
    return True


def _preceded_by_table_label(text: str, start: int) -> bool:
    """Return True when the line immediately before *start* is a table label."""
    before = text[max(0, start - 40):start]
    return bool(_TABLE_LABEL.search(before))


def _classify_heading(title: str) -> Optional[str]:
    """Map a heading title to its canonical section name, if recognized."""
    normalized = re.sub(r"\s+", " ", title.strip().lower())
    best_match: Optional[str] = None
    best_score = 0

    for canonical, patterns in SECTION_ALIASES.items():
        score = _alias_score(normalized, patterns)
        if score > best_score:
            best_score = score
            best_match = canonical

    return best_match


def _alias_score(normalized: str, patterns: List[str]) -> int:
    """Score how well *normalized* matches the given alias patterns."""
    best = 0

    for pattern in patterns:
        match = re.search(rf"\b(?:{pattern})\b", normalized, re.IGNORECASE)
        if match:
            best = max(best, len(match.group()))

    if best == 0:
        return 0

    if (
        re.search(r"\bexperiments?\b", normalized, re.IGNORECASE)
        and re.search(r"\bresults?\b", normalized, re.IGNORECASE)
    ):
        return best

    return best


def _extract_inline_abstract(text: str) -> Optional[str]:
    """Extract abstract content when it appears inline (e.g. ``Abstract—``)."""
    match = _ABSTRACT_INLINE.search(text)
    if not match:
        return None

    start = match.end()
    end_match = _ABSTRACT_END.search(text, start)
    end = end_match.start() if end_match else len(text)
    content = text[start:end].strip()
    return content or None
