"""
section3.py - CLI, misc classes, and entry point
"""

import os
import time
from collections import Counter
from .section1 import random_numbers, random_strings
from .section2 import word_frequency_in_file, stats_for_numbers

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
            from .section1 import primes_up_to

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
