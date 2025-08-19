# test_script.py

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
        print("Double count: " + str(l*2))
        l = l + 1

    m = 0
    while m < 10:
        print("Square: " + str(m*m))
        m = m + 1

    n = 0
    while n < 10:
        print("Cube: " + str(n*n*n))
        n = n + 1

    o = 0
    while o < 10:
        print("Modulo 3: " + str(o % 3))
        o = o + 1

    print("All done, " + user_name + "!")

if __name__ == "__main__":
    main()
