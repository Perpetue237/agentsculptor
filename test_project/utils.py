def greet_user():
    print("Welcome to the Non-Pythonic Test Script!")
    name = input("Enter your name: ")
    print("Hello, " + name + "!")
    return name


def ask_age():
    age = input("How old are you? ")
    try:
        age_int = int(age)
    except:
        print("That's not a number. Defaulting to 0.")
        age_int = 0
    print("You are " + str(age_int) + " years old.")
    return age_int


def repeat_message(msg, times):
    i = 0
    while i < times:
        print(msg)
        i = i + 1


def favorite_numbers():
    numbers = []
    i = 0
    while i < 3:
        num = input("Enter a favorite number: ")
        try:
            n = int(num)
            numbers.append(n)
        except:
            print("Invalid number, skipping.")
        i = i + 1
    print("Your numbers are:")
    j = 0
    while j < len(numbers):
        print(numbers[j])
        j = j + 1
    return numbers


def simple_math():
    a = input("Enter a number: ")
    b = input("Enter another number: ")
    try:
        a_int = int(a)
        b_int = int(b)
        print("Addition: " + str(a_int + b_int))
        print("Subtraction: " + str(a_int - b_int))
        print("Multiplication: " + str(a_int * b_int))
        if b_int != 0:
            print("Division: " + str(a_int / b_int))
        else:
            print("Division by zero!")
    except:
        print("Invalid numbers.")


def simple_loop_test():
    i = 0
    while i < 5:
        print("Loop number " + str(i))
        i = i + 1
