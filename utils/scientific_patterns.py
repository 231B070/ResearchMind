"""
Scientific regex patterns
"""

import re

# Percentage
PERCENT_PATTERN = re.compile(r"\d+(\.\d+)?\s*%")

# Accuracy
ACCURACY_PATTERN = re.compile(
    r"accuracy.{0,20}\d+(\.\d+)?%",
    re.IGNORECASE
)

# F1
F1_PATTERN = re.compile(
    r"F1.{0,15}\d+(\.\d+)?",
    re.IGNORECASE
)

# Year
YEAR_PATTERN = re.compile(
    r"(19|20)\d{2}"
)