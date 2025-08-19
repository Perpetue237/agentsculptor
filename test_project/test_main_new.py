import builtins
import io
import sys
import pytest
from main_new import greet_user, main

def test_greet_user(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'TestUser')
    captured = io.StringIO()
    sys.stdout = captured
    name = greet_user()
    sys.stdout = sys.__stdout__
    assert name == 'TestUser'
    assert "Hello, TestUser!" in captured.getvalue()

def test_main_runs(monkeypatch):
    # Provide inputs for greet_user, ask_age, three favorite_numbers, and two simple_math numbers
    inputs = iter(['TestUser', '25', '1', '2', '3', '4', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    captured = io.StringIO()
    sys.stdout = captured
    main()
    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert "All done, TestUser!" in output
