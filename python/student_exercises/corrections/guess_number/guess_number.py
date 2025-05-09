import random
import math

MAX_NUMBER = 100

def guess_number():
    """
    Function that generates a random number between 1 and 100 and asks the user to guess it.
    :return: None
    """
    # for dychotomy optimal search, the formula is the following: math.log2(100)
    optimal_limit = math.ceil(math.log2(MAX_NUMBER))

    # Generate a random number between 1 and 100
    secret_number: int = random.randint(1, MAX_NUMBER)
    print(secret_number)

    user_number = int(input("Enter a number: "))
    tries = 1

    while secret_number != user_number:
        if user_number < secret_number:
            print("The guess number is higher")
        else:
            print("The guess number is lower")
        
        user_number = int(input("Enter a number: "))
        tries += 1

    if tries <= optimal_limit:
        print(f"Bravo, you found the secret number in {tries} {'try' if tries == 1 else 'tries'}")
    else:
        print(f"You found the secret number in {tries} tries")

if __name__ == '__main__':
    # Run the game
    guess_number()