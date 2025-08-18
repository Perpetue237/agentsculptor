"""
section2.py - String helpers and analysis tools
"""

import os
import json
import itertools
from collections import Counter, defaultdict

# ========================
# Section: String Helpers
# ========================


def normalize_text(text):
    """Lowercase and strip whitespace."""
    return text.strip().lower()


def count_words(text):
    """Count words in a text."""
    words = text.split()
    return Counter(words)


def reverse_words(text):
    """Reverse order of words."""
    return " ".join(reversed(text.split()))


def is_palindrome(s):
    """Check if a string is palindrome."""
    s_clean = "".join(ch for ch in s.lower() if ch.isalnum())
    return s_clean == s_clean[::-1]


# ========================
# Section: File Utilities
# ========================


def read_file(path):
    """Read file content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """Write content to file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def find_files_with_extension(directory, extension):
    """Return list of files ending with given extension."""
    result = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.join(root, file))
    return result


def append_to_file(path, line):
    """Append line to file."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ========================
# Section: Analysis Tools
# ========================


def word_frequency_in_file(path):
    """Return word frequency from file."""
    content = read_file(path)
    return count_words(normalize_text(content))


def stats_for_numbers(numbers):
    """Return min, max, avg."""
    return {
        "min": min(numbers) if numbers else None,
        "max": max(numbers) if numbers else None,
        "avg": average(numbers),
    }
