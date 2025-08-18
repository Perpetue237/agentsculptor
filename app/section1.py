"""
section1.py - Math helpers and data generators
"""

import random
import math

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
# Section: Data Generators
# ========================


def random_numbers(count, lower=0, upper=100):
    """Generate list of random integers."""
    return [random.randint(lower, upper) for _ in range(count)]


def random_strings(count, length=5):
    """Generate list of random lowercase strings."""
    letters = "abcdefghijklmnopqrstuvwxyz"
    return [
        "".join(random.choice(letters) for _ in range(length)) for _ in range(count)
    ]
