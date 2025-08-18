"""
main.py - Large sample script for testing refactoring
Only Python built-in modules are used.
"""

import os
import sys
import random
import time
import math
import json
import itertools
from collections import Counter, defaultdict


# =====================
# Section: Math Helpers
# =====================

def factorial(n):
    """Return factorial of n."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n):
    """Return list of first n Fibonacci numbers."""
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def is_prime(num):
    """Check if number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def primes_up_to(n):
    """Return list of primes <= n."""
    return [x for x in range(2, n + 1) if is_prime(x)]


def average(numbers):
    """Return the average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0


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
    s_clean = ''.join(ch for ch in s.lower() if ch.isalnum())
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
# Section: Data Generators
# ========================

def random_numbers(count, lower=0, upper=100):
    """Generate list of random integers."""
    return [random.randint(lower, upper) for _ in range(count)]


def random_strings(count, length=5):
    """Generate list of random lowercase strings."""
    letters = "abcdefghijklmnopqrstuvwxyz"
    return [
        "".join(random.choice(letters) for _ in range(length))
        for _ in range(count)
    ]


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


# ========================
# Section: Menu/CLI
# ========================

def menu():
    """Display menu options."""
    print("\n=== Sample CLI ===")
    print("1. Generate random numbers")
    print("2. Generate random strings")
    print("3. Analyze text file word frequency")
    print("4. Show primes up to N")
    print("5. Quit")


def cli_loop():
    """Run a simple CLI loop."""
    while True:
        menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            nums = random_numbers(10)
            print("Generated numbers:", nums)
            print("Stats:", stats_for_numbers(nums))
        elif choice == "2":
            strs = random_strings(5)
            print("Generated strings:", strs)
        elif choice == "3":
            path = input("Enter file path: ").strip()
            if os.path.exists(path):
                freq = word_frequency_in_file(path)
                print("Top 5 words:", freq.most_common(5))
            else:
                print("File not found.")
        elif choice == "4":
            n = int(input("Enter N: "))
            print("Primes:", primes_up_to(n))
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


# ========================
# Section: Misc Classes
# ========================

class Timer:
    """Simple timer context manager."""

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        print(f"Elapsed: {self.end - self.start:.4f} seconds")


class DataStore:
    """In-memory key-value store."""

    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def keys(self):
        return list(self.data.keys())

    def values(self):
        return list(self.data.values())

    def items(self):
        return list(self.data.items())


# ========================
# Section: Main
# ========================

def main():
    """Main entry point."""
    print("Welcome to the Sample Script.")
    cli_loop()


if __name__ == "__main__":
    main()
