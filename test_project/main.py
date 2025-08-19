from utils import (
    greet_user,
    ask_age,
    repeat_message,
    favorite_numbers,
    simple_math,
    simple_loop_test,
)


def main():
    user_name = greet_user()
    user_age = ask_age()
    repeat_message("This is a repeated message.", 3)
    nums = favorite_numbers()
    simple_math()
    simple_loop_test()

    # Some extra dummy code to inflate lines
    k = 0
    while k < 10:
        print("Counting: " + str(k))
        k = k + 1

    l = 0
    while l < 10:
        print("Double count: " + str(l * 2))
        l = l + 1

    m = 0
    while m < 10:
        print("Square: " + str(m * m))
        m = m + 1

    n = 0
    while n < 10:
        print("Cube: " + str(n * n * n))
        n = n + 1

    o = 0
    while o < 10:
        print("Modulo 3: " + str(o % 3))
        o = o + 1

    print("All done, " + user_name + "!")


if __name__ == "__main__":
    main()
