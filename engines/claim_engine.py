"""Rule-based scientific claim extraction from parsed research papers."""

from __future__ import annotations

import logging
import re
from typing import Dict, List, Tuple

from core.models import Paper, ResearchClaim

logger = logging.getLogger(__name__)

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(0-9\"'])")

_METRIC_ALIASES: Dict[str, str] = {
    r"\bcharacter[- ]level accuracy\b": "Character-level Accuracy",
    r"\bword[- ]level accuracy\b": "Word-level Accuracy",
    r"\baccuracy\b": "Accuracy",
    r"\bprecision\b": "Precision",
    r"\brecall\b": "Recall",
    r"\bf1[- ]?score\b": "F1-score",
    r"\bbleu\b": "BLEU",
    r"\brouge\b": "ROUGE",
}

_PROBLEM_PATTERNS = (
    r"motivat(?:ed|es)",
    r"limitation(?:s)? of",
    r"(?:the|a|an)\s+(?:key\s+)?problem",
    r"challenge(?:s)?",
    r"lack of",
    r"difficult(?:y|ies)",
    r"drawback(?:s)?",
    r"suffers? from",
)

_METHOD_PATTERNS = (
    r"this paper presents",
    r"we propose",
    r"we present",
    r"we develop",
    r"we introduce",
    r"our (?:method|approach|model|system|framework|OCR)",
    r"in this (?:paper|work)",
)

_DATASET_PATTERNS = (
    r"learned with",
    r"trained (?:on|with|by)",
    r"text line(?: images)?",
    r"training set",
    r"test set",
    r"validation set",
    r"dataset",
    r"benchmark",
    r"corpus",
    r"collected from",
)

_BASELINE_PATTERNS = (
    r"compared(?:\s+\w+){0,4}\s+(?:with|to|against)",
    r"baseline",
    r"state[- ]of[- ]the[- ]art",
    r"\bSOTA\b",
    r"previous (?:work|method|approach)",
    r"outperforms?",
    r"tesseract",
    r"google drive",
)

_LIMITATION_PATTERNS = (
    r"limitation(?:s)?",
    r"drawback(?:s)?",
    r"shortcoming(?:s)?",
    r"does not",
    r"cannot",
    r"unable to",
    r"failure to",
    r"weakness(?:es)?",
)

_FUTURE_WORK_PATTERNS = (
    r"future work",
    r"our future work",
    r"we plan",
    r"we intend",
    r"we shall",
    r"future research",
    r"we also plan",
    r"we will",
)


def extract_claims(paper: Paper) -> List[ResearchClaim]:
    """
    Extract structured scientific claims from a parsed *paper*.

    Uses regex, keyword matching, and section-aware heuristics.
    Returns a list containing one primary claim per paper.
    """
    logger.info("Extracting claims for paper: %s", paper.title)

    metric, results, improvement = _extract_metric_results(paper)

    claim = ResearchClaim(
        problem=_extract_from_sections(paper, ("Introduction", "Abstract"), _PROBLEM_PATTERNS),
        proposed_method=_extract_from_sections(paper, ("Abstract", "Methodology"), _METHOD_PATTERNS),
        dataset=_extract_from_sections(paper, ("Dataset", "Experiments", "Methodology"), _DATASET_PATTERNS),
        baseline=_extract_from_sections(paper, ("Results", "Experiments", "Discussion"), _BASELINE_PATTERNS),
        metric=metric,
        results=results,
        improvement=improvement or _find_improvement(paper, metric),
        limitations=_extract_from_sections(paper, ("Limitations", "Discussion", "Introduction"), _LIMITATION_PATTERNS),
        future_work=_extract_from_sections(paper, ("Future Work", "Conclusion"), _FUTURE_WORK_PATTERNS),
    )

    logger.debug(
        "Claim extracted — metric=%s, improvement=%s",
        claim.metric or "(none)",
        claim.improvement or "(none)",
    )
    return [claim]


def _extract_from_sections(
    paper: Paper,
    section_names: Tuple[str, ...],
    patterns: Tuple[str, ...],
) -> str:
    """Return the best matching sentence across prioritized *section_names*."""
    for name in section_names:
        sentence = _best_matching_sentence(_section_text(paper, name), patterns)
        if sentence:
            return sentence
    return _best_matching_sentence(paper.full_text, patterns)


def _extract_metric_results(paper: Paper) -> Tuple[str, str, str]:
    """Extract metric name, results sentence, and improvement value."""
    for section in ("Abstract", "Results", "Experiments", "Conclusion"):
        result = _parse_metric_from_text(_section_text(paper, section))
        if result[0]:
            return result
    return _parse_metric_from_text(paper.full_text)


def _parse_metric_from_text(text: str) -> Tuple[str, str, str]:
    """Parse metric, results, and improvement from *text*."""
    if not text:
        return "", "", ""

    best: Tuple[int, str, str, str] = (0, "", "", "")

    for sentence in _split_sentences(text):
        if not _is_usable_sentence(sentence):
            continue

        metric_name = _detect_metric_name(sentence)
        if not metric_name or not _has_numeric_result(sentence):
            continue

        score = _score_result_sentence(sentence)
        improvement = _parse_improvement(sentence, metric_name)
        if score > best[0]:
            best = (score, metric_name, sentence.strip(), improvement)

    if best[0]:
        return best[1], best[2], best[3]
    return "", "", ""


def _find_improvement(paper: Paper, metric: str) -> str:
    """Search all sections for an improvement statement related to *metric*."""
    for section in ("Results", "Experiments", "Abstract", "Conclusion"):
        text = _section_text(paper, section)
        for sentence in _split_sentences(text):
            if not _is_usable_sentence(sentence):
                continue
            value = _parse_improvement(sentence, metric or "Accuracy")
            if value:
                return value
    return ""


def _best_matching_sentence(text: str, patterns: Tuple[str, ...]) -> str:
    """Return the first usable sentence matching any pattern in priority order."""
    if not text:
        return ""
    for pattern in patterns:
        for sentence in _split_sentences(text):
            if not _is_usable_sentence(sentence):
                continue
            if re.search(pattern, sentence, re.IGNORECASE):
                return sentence.strip()
    return ""


def _section_text(paper: Paper, name: str) -> str:
    """Return section content by canonical name, or empty string."""
    return paper.sections.get(name, "")


def _split_sentences(text: str) -> List[str]:
    """Split *text* into sentences using punctuation heuristics."""
    if not text:
        return []
    normalized = _normalize_text(text)
    parts = _SENTENCE_SPLIT.split(normalized.strip())
    return [part.strip() for part in parts if part.strip()]


def _normalize_text(text: str) -> str:
    """Join PDF line wraps so sentence boundaries can be detected reliably."""
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    return re.sub(r"\s+", " ", text)


def _is_usable_sentence(sentence: str) -> bool:
    """Return True when *sentence* looks like prose rather than a table fragment."""
    if len(sentence) < 25:
        return False
    if sentence.count("\n") > 2:
        return False
    if re.search(r"(?i)^Table\s+[IVXLC\d]+", sentence):
        return False
    if re.search(r"(?i)TEST RESULTS|System/method", sentence):
        return False
    return bool(re.search(r"[a-zA-Z]{3}", sentence))


def _score_result_sentence(sentence: str) -> int:
    """Score how likely *sentence* is a primary quantitative result."""
    score = 0
    if re.search(r"(?i)(?:accuracy|precision|recall|f1)[^.]{0,40}\d+(?:\.\d+)?%?", sentence):
        score += 10
    if re.search(r"(?i)(?:produced|achiev(?:ed|es)|obtain(?:ed|s)|report(?:s|ed))", sentence):
        score += 5
    if re.search(r"(?i)improv(?:es|ed)|better than|outperform", sentence):
        score += 3
    return score


def _detect_metric_name(sentence: str) -> str:
    """Return the canonical metric name found in *sentence*, if any."""
    for pattern, name in _METRIC_ALIASES.items():
        if re.search(pattern, sentence, re.IGNORECASE):
            return name
    return ""


def _has_numeric_result(sentence: str) -> bool:
    """Return True when *sentence* contains a numeric measurement."""
    return bool(re.search(r"\d+(?:\.\d+)?%?", sentence))


def _parse_improvement(sentence: str, metric_name: str) -> str:
    """Extract improvement value from *sentence* for the given *metric_name*."""
    metric_token = metric_name.split()[-1]

    by_pattern = re.compile(
        rf"(?i){re.escape(metric_token)}[^.]*?"
        rf"(?:improv(?:es|ed)|increas(?:es|ed)|gain(?:ed)?)\s+(?:by\s+)?"
        rf"([\d.]+%?)"
    )
    match = by_pattern.search(sentence)
    if match:
        return match.group(1)

    from_to = re.compile(
        rf"(?i){re.escape(metric_token)}[^.]*?"
        rf"from\s+([\d.]+%?)\s+to\s+([\d.]+%?)"
    )
    match = from_to.search(sentence)
    if match:
        return f"{match.group(1)} to {match.group(2)}"

    generic_by = re.search(
        r"(?i)(?:improv(?:es|ed|ement)|increase(?:s|d)?)\s+(?:by\s+)?([\d.]+%?)",
        sentence,
    )
    if generic_by:
        return generic_by.group(1)

    if re.search(
        r"(?i)(?:better than|outperforms?)\s+(?:the\s+)?"
        r"(?:baseline|state[- ]of[- ]the[- ]art|\bSOTA\b|GDS|previous)",
        sentence,
    ):
        return "outperforms baseline"

    return ""
