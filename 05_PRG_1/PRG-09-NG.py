import random

def guess_number():
    secret_number = random.randint(1, 100)
    attempts = 0
    score = 100

    print("Guess a number between 1 and 100!")

    while True:
        try:
            user_guess = int(input("Enter your guess: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue

        attempts += 1

        if user_guess < secret_number:
            print("Too low! Try again.")
        elif user_guess > secret_number:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You guessed the number {secret_number}!")
            break

        score -= 2

    print(f"Your score is: {score}")

guess_number()
