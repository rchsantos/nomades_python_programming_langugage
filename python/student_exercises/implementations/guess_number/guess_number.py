import random
import math

MAX_NUMBER = 100

def guess_number():
    """
    Function that generates a random number between 1 and 100 and asks the user to guess it.
    :return: None
    """
    # for dychotomy optimal search, the formula is the following: math.log2(100)


    # Generate a random number between 1 and 100
    secret_number: int = random.randint(1, MAX_NUMBER)
    print(secret_number)
    # TODO: ask user for a number uisng `input` function /!\ hint don't forget to convert the result of input as int
    # TODO: check if user number is equal to secret number, if not display "The guess number is higher" or "The guess number is lower" accordingly
    
    # to ask user to enter the number use the function input
    print("bravo")

if __name__ == '__main__':
    # Run the game
    guess_number()