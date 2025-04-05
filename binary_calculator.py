
from enum import Enum

class INPUT_STATE(Enum):
    '''
        Enum to represent the program's current state
    '''
    OPERATION = 0,
    VALUES = 1
    CALCULATION = 2


#a list of valid inputs for selecting a given operation
operations = ['+','-','q']

def run():
    '''
        Entry point of our program.
    '''
    print_author_details()
    program()
    pass

def program():
    '''
        The main program cycle for calculating binary numbers using the users inputs
    '''
    #reference the current_state as a global var
    global current_state
    #set the current state to OPERATION
    current_state = INPUT_STATE.OPERATION
    #declare a var for holding operation
    operation = str(input("Choose operation [+, -, q]: "))
    #validate the user input to ensure that it only contains digits +, - or q
    while not validate_input(operation):
            operation = str(input("Choose operation [+, -, q]: "))
    #loop the operation process - while the user hasn't quit
    while operation != "q":
        #set the current state to OPERATION
        current_state = INPUT_STATE.VALUES
        #capture the x and y inputs to perform the operation
        value_x = str(input("X: "))
        #validate the x value
        while not validate_input(value_x):
            value_x = str(input("X: "))
        value_y = str(input("Y: "))
        #validate the y value
        while not validate_input(value_y):
            value_y = str(input("Y: "))
        #perform operation
        perform_Calculation(value_x,value_y,operation)
        #set the current state to OPERATION
        current_state = INPUT_STATE.OPERATION
        #prompt the user again
        operation = str(input("Choose operation [+, -, q]: "))
        #validate the user input to ensure that it only contains digits +, - or q
        while not validate_input(operation):
            operation = str(input("Choose operation [+, -, q]: "))
        

def perform_Calculation(string_x: str, string_y: str, operation: str):
    print("DEBUG: Performing CALCULATION\n")
    #reference the current_state as a global var
    global current_state
    #set the current state to CALCULATION
    current_state = INPUT_STATE.CALCULATION
    #covert the string values to lists

def convert_string_to_lists(string: str) -> list:
    pass

        
def validate_input(x: str) -> bool:
    #reference the current_state as a global var
    global current_state
    #check the current_state
    if current_state == INPUT_STATE.OPERATION:
        if x == None or x.strip().lower() not in operations:
            print("Invalid operation.\n\n")
            return False
        return True
    elif current_state == INPUT_STATE.VALUES:
        #validate both x and y inputs to ensure that they are only 1's and 0's
        is_valid_x = all(char in {"0","1"} for char in x)
        #check if both x and y are valid
        if not is_valid_x:
            print(f"Not a binary number! {is_valid_x}\n\n")
            return False
        return True
    else:
        #something's gone horribly wrong
        print("Invalid operation.\n\n")
        return False
    

def print_author_details():
    print("Author: Travis Strawbridge\nStudent ID: 110340713\nEmail ID: STRTK001\nThis is my own work as defined by the University's Academic Integrity Policy.\n\n")

if __name__ == "__main__":
    run()

'''
Aim:
    To write a console program that calculates the addition or substraction of CALCULATION numbers 
    with an arbitrary number of digits.

Requirements:
    • The system must first prompt the user to input the operation type (+ or -) then ask
      for two CALCULATION numbers with an arbitrary number of bits as strings.
        - The system must then convert each input string into an array of bits
        - The system must then calculate the sum or difference the give an output of the 
          results in specified format in the specs doc.
    • The system must validate the user input and handle errors gracefully
    • The system must repeat the 
'''