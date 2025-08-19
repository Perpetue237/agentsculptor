import main_new


def test_functions_exist():
    for name in [
        "greet_user",
        "ask_age",
        "repeat_message",
        "favorite_numbers",
        "simple_math",
        "simple_loop_test",
        "main",
    ]:
        assert hasattr(main_new, name), f"{name} is missing"
        assert callable(getattr(main_new, name)), f"{name} is not callable"
