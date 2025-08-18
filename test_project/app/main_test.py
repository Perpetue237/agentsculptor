import os
import tempfile

# Import functions directly from the module in the same folder
from main import (
    factorial,
    fibonacci,
    is_prime,
    primes_up_to,
    average,
    normalize_text,
    count_words,
    reverse_words,
    is_palindrome,
    read_file,
    write_file,
    random_numbers,
    random_strings,
    word_frequency_in_file,
    stats_for_numbers,
    Timer,
    DataStore,
)


def test_factorial():
    assert factorial(0) == 1
    assert factorial(5) == 120
    assert factorial(1) == 1


def test_fibonacci():
    assert fibonacci(0) == []
    assert fibonacci(1) == [0]
    assert fibonacci(6) == [0, 1, 1, 2, 3, 5]


def test_is_prime():
    assert not is_prime(0)
    assert not is_prime(1)
    assert is_prime(2)
    assert is_prime(13)
    assert not is_prime(15)


def test_primes_up_to():
    assert primes_up_to(10) == [2, 3, 5, 7]


def test_average():
    assert average([1, 2, 3, 4]) == 2.5
    assert average([]) == 0


def test_string_helpers():
    text = "  Hello World  "
    assert normalize_text(text) == "hello world"
    cw = count_words("a a b")
    assert cw["a"] == 2 and cw["b"] == 1
    assert reverse_words("one two three") == "three two one"
    assert is_palindrome("A man a plan a canal Panama")


def test_random_numbers_and_strings():
    nums = random_numbers(5, 0, 10)
    assert len(nums) == 5
    assert all(0 <= n <= 10 for n in nums)
    strs = random_strings(3, 4)
    assert len(strs) == 3
    assert all(len(s) == 4 for s in strs)


def test_file_io_and_analysis(tmp_path):
    file_path = tmp_path / "sample.txt"
    content = "Hello hello world"
    write_file(str(file_path), content)
    read_back = read_file(str(file_path))
    assert read_back == content
    freq = word_frequency_in_file(str(file_path))
    assert freq["hello"] == 2
    assert freq["world"] == 1


def test_stats_for_numbers():
    data = [1, 2, 3, 4]
    stats = stats_for_numbers(data)
    assert stats["min"] == 1
    assert stats["max"] == 4
    assert stats["avg"] == 2.5


def test_timer_context_manager():
    with Timer() as t:
        pass
    assert hasattr(t, "start") and hasattr(t, "end")
    assert t.end >= t.start


def test_datastore():
    ds = DataStore()
    ds.set("key", "value")
    assert ds.get("key") == "value"
    assert ds.keys() == ["key"]
    assert ds.values() == ["value"]
    assert ds.items() == [("key", "value")]
