import string
import random

def generate_password(
    uppercase: bool, 
    lowercase: bool, 
    digits: bool, 
    specials_char: bool, 
    length: int
) -> str:
  if length < 4:
    return "Error: Please enter a password lenght of at least 4"
  
  population_choice: int = 0
  population: str = ''
  pwd: str = ''
  
  if uppercase:
    # Add upercase char to pwd
    pwd += random.choice(string.ascii_uppercase)
    # Keep in mind that I can use uppercase for the remaning of pwd
    population += string.ascii_uppercase
    # increment populationc choice variable
    population_choice += 1
  
  if lowercase:
    # Add upercase char to pwd
    pwd += random.choice(string.ascii_lowercase)
    # Keep in mind that I can use uppercase for the remaning of pwd
    population += string.ascii_lowercase
    # increment populationc choice variable
    population_choice += 1

  if digits:
    # Add upercase char to pwd
    pwd += random.choice(string.digits)
    # Keep in mind that I can use uppercase for the remaning of pwd
    population += string.digits
    # increment populationc choice variable
    population_choice += 1
  
  if specials_char:
    # Add upercase char to pwd
    pwd += random.choice(string.punctuation)
    # Keep in mind that I can use uppercase for the remaning of pwd
    population += string.punctuation
    # increment populationc choice variable
    population_choice += 1

  if population_choice == 0:
    return "Error: Please select at least one population"
  
  remaining_chars_count: int = length-len(pwd)
  remaining_chars: list[str] = random.choices(population, k=remaining_chars_count)
  pwd_list: list[str] = list(pwd) + remaining_chars
  random.shuffle(pwd_list)
  return "".join(pwd_list)



  

if __name__ == '__main__':
  print(generate_password(True, True, False, False, 10))