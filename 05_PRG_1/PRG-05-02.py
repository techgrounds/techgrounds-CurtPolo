while True:
    choice = int(input("Pick the secret number! "))
    if choice > 100:
        print("The number you picked is too high!")
    elif choice < 100:
        print("The number you picked is too low!")
    else:
        print("You Found The Secret Number! ")
        break