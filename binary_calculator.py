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
    display_nor_truth_table()
    display_addition_truth_table()
    display_subtraction_truth_table()
    display_less_than_truth_table()
    program()

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
    '''
    Function for handling the calculation request depending on the given operation
    '''
    #reference the current_state as a global var
    global current_state
    #set the current state to CALCULATION
    current_state = INPUT_STATE.CALCULATION
    #covert the string values to lists
    binary_x = convert_string_to_list(string_x)
    binary_y = convert_string_to_list(string_y)
    #check the type of operation and execute it using the x and y binary values
    if operation == "+":
        addition(binary_x,binary_y)
    else:
        subtraction(binary_x,binary_y)


def addition(binary_x: list[int], binary_y: list[int]):
    '''
    Function that performs the addition operation of binary_x + binary_y
    '''
    #get the max_len between both lists
    max_len = max(len(binary_x),len(binary_y))
    #create copies of the binary lists so we dont modify the originals
    list_x = list(binary_x)
    list_y = list(binary_y)
    #reverse the binary lists so that we are dealing with the least significant digit in both lists
    list_x.reverse()
    list_y.reverse()
    #declare a binary list to hold the sum of the x and y lists
    binary_sum = list()
    #declare a var to hold the bits to be carryover over
    carryover = 0
    #interate over the max_len of the two binary lists in reverse so we start from the
    #least significant digit to the highest
    for i in range(0,max_len):
        #initialise x and y as 0 as a default incase either binary list is shorter in length
        x = 0
        y = 0
        #check the list lengths to see if i is within bounds and set x or y to the item at 
        #the current index
        if i < len(list_x):
            x = list_x[i]
        if i < len(list_y):
            y = list_y[i]
        #append the sum bit to the binary sum list
        binary_sum.append(ADD_BIT(x,y,carryover))
        #calculate the carryover bit
        carryover = CARRY_BIT(x,y,carryover)
    
    #check if the carryover bit for the final addition is 1
    if carryover == 1:
        binary_sum.append(carryover)

    #reverse the binary sum list as we added the values in backwards from right to left
    binary_sum.reverse()
    #display the equation
    display_equation(binary_x,binary_y,binary_sum,"+")
    

def subtraction(binary_x: list[int], binary_y: list[int]):
    '''
    Function that performs the subtraction operation of binary_x - binary_y
    '''
    #get the max_len between both lists
    max_len = max(len(binary_x),len(binary_y))
    #check if binary_x is less than binary_y which would result in a negative result
    is_negative = is_less_than(binary_x,binary_y)
    #create copies of the binary lists so we dont modify the originals
    list_x = list(binary_x)
    list_y = list(binary_y)
    #if the number will be negative, flip the lists so that x == y y == x
    if is_negative:
        list_x,list_y = list_y,list_x
    #reverse the lists 
    list_x.reverse()
    list_y.reverse()
    #declare a binary list to hold the result of the subtraction of x - y
    binary_result = list()
    #declare a var to hold the bits to be borrowed
    borrowed = 0
    #iterate over the binary lists from LSD to MSD (right to left)
    for i in range(0,max_len):
        #initialise x and y as 0 as a default incase either binary list is shorter in length
        x = 0
        y = 0
        #check the list lengths to see if i is within bounds and set x or y to the item at 
        #the current index
        if i < len(list_x):
            x = list_x[i]
        if i < len(list_y):
            y = list_y[i]
        #append the resulting bit to the binary result list
        binary_result.append(SUB_BIT(x,y,borrowed))
        #calculate the carryover bit
        borrowed = BORROW_BIT(x,y,borrowed)
    
    #check if the borrowed bit for the final subtraction is 1
    if borrowed == 1:
        binary_result.append(borrowed)
    
    #reverse the binary result list
    binary_result.reverse()
    #remove the trailing 0's if there are any
    for i in range(0,len(binary_result)):
        #if the item of index i is 1 then slice the list from here
        if binary_result[i] == 1:
            binary_result = binary_result[i:]
            break

    #display the equasion
    display_equation(binary_x,binary_y,binary_result,"-",is_negative)

def is_less_than(binary_x: list[int],binary_y: list[int]) -> bool:
    '''
    function for performing multi bit comparason to see if binary_x is < binary_y and returns a bool
    '''
    #get the max_len between both lists
    max_len = max(len(binary_x),len(binary_y))
    #initalise copies of the lists so we dont work with the references
    x_list = list([0]*(max_len - len(binary_x)) + binary_x)
    y_list = list([0]*(max_len - len(binary_y)) + binary_y)

    #reverse both lists to compare from LSD to MSD
    x_list.reverse()
    y_list.reverse()

    l = 0
    #iterate over each item in both lists
    for i in range(0,max_len):
        #get the items
        x = x_list[i]
        y = y_list[i]
        #compare x and y to determine if x < y
        l = LESS_THAN(x,y,l)
    #return true if x < 1 or false if not
    return l == 1

def NOR(x: int,y: int) -> int:
    '''
    NOR function to get the value of !x&&!y, the invers of an OR function.
    '''
    #if x and y are false, or in this case 0:
    if x == 0 and y == 0:
        #return true, or in this case 1
        return 1
    #NOR is only true when both x and y are false so return false; 0
    else:
        return 0
    
def NOT(x: int) -> int:
    '''
    Not Function that works by pushing x into NOR to get the inverse of x.
    
    E.g. --> x = 1;  xNORx === !x&&!x = !x = 0;
    '''
    return NOR(x,x)

def AND(x: int, y: int) -> int:
    '''
    And function that works by pushing x into a NOT and Y into an NOT then pushing those values
    into a NOR the AND. We are effectively inverting the values of the NOR from !x&&!y into x&&y 
    converting the NOR into an AND.

    E.g. --> x = 1, y = 1; !xNOR!y === !!x&&!!y === x&&y = 1;
    '''
    return NOR(NOT(x),NOT(y))

def OR(x: int, y:int) -> int:
    '''
    Or function that works by getting the NOR of the NORs of x and y. This effectively inverts the
    NOR function into an OR.

    E.g: 
        • OR == True:
            x = 1, y = 0; (xNORy)NOR(xNORy) === !(!x&&!y)&&!(!x&&y!);
            (!x&&!y) = 0, !(!x&&!y) = 1, !(!x&&!y)&&!(!x&&!y) = 1; 
        • OR == False:
            x = 0, y = 0; (xNORy)NOR(xNORy) === !(!x&&!y)&&!(!x&&y!);
            (!x&&!y) = 1, !(!x&&!y) = 0, !(!x&&!y)&&!(!x&&!y) = 0;
    '''
    return NOR(NOR(x,y),NOR(x,y))

def XOR(x: int,y: int) -> int:
    '''
    XOR function that works by following the compound expression of !x&&y||x&&!y.
    '''
    return OR(
        AND(NOT(x),y),
        AND(x,NOT(y))
    )
    
    
def ADD_BIT(x: int,y: int,c: int) -> int:
    '''
    Single bit addition function that sums the x and y values considering the carry over from the previous
    LSD bit; c
    '''
    return XOR(XOR(x,y),c)

def CARRY_BIT(x: int, y: int, c: int):
    '''
    Logic gate function for carrying over the carry value, c, from the sum of x and y to be used in the addition of
    the next more significant digits.
    '''
    return OR(
        AND(x,y),
        AND(
            XOR(x,y),
            c
        )
    )

def SUB_BIT(x: int, y: int,b: int) -> int:
    '''
    Single bit subtraction function that calculates the difference of x - y,
    while considering the borrow value, b ,from the previous LSD.
    '''
    return XOR(XOR(x,y),b)

def BORROW_BIT(x: int, y: int,b: int) -> int:
    '''
    Logic gate function for determining if a bit needs to be borrowed from the next highest digit
    when calculating the subtraction of x - y while considering b.
    '''
    return OR(
            AND(
                NOT(XOR(x,y)),
                b
            ),
            AND(
                NOT(x),
                y
            )
        )

def LESS_THAN(x: int, y: int, l: int) -> int:
    '''
    Single bit comparason function for comparing if x < y, considering the result of the lower digit from
    a previous check; l.
    '''
    return OR(
        AND(
            NOT(x),
            y
        ),
        AND(
            NOT(XOR(x,y)),
            l
        )
    )

def convert_string_to_list(string: str) -> list:
    '''
    Helper method for converting a string of numbers into a list of ints to represent binary numbers
    '''
    return [int(char) for char in string]
        
def validate_input(x: str) -> bool:
    '''
    Function for validating the user's input using the expected output given the current state of the
    program.
    '''
    #reference the current_state as a global var
    global current_state
    #check the current_state
    if current_state == INPUT_STATE.OPERATION:
        if x == None or x.strip().lower() not in operations:
            print("Invalid operation.\n")
            return False
        return True
    elif current_state == INPUT_STATE.VALUES:
        #validate both x and y inputs to ensure that they are only 1's and 0's
        is_valid_x = all(char in {"0","1"} for char in x)
        #check if both x and y are valid
        if not is_valid_x:
            print(f"Not a binary number!\n")
            return False
        return True
    else:
        #something's gone horribly wrong
        print("Invalid operation.\n")
        return False

def display_equation(
        binary_x: list[int],
        binary_y: list[int],
        binary_sum: list[int],
        operationSymbol: str,
        is_negative: bool = False):
    '''
    Function for displaying the calculation equation and the result.
    '''
    #get the max length of the binary lists + two for an extra _ and operator + or -
    max_len = max(len(binary_x),len(binary_y),len(binary_sum)) + 2
    #initialise the display strings using list comprehension to convert the ints of the list into strings
    #then join the converted strings into an empty string for each list
    x_str = [str(bit) for bit in binary_x]
    x_str = "".join(x_str)
    y_str = [str(bit) for bit in binary_y]
    y_str = "".join(y_str)
    sum_str = [str(bit) for bit in binary_sum]
    sum_str = "".join(sum_str)
    #calculate the padding for the binary lists
    x_padding = max_len - len(binary_x)
    y_padding = max_len - len(binary_y) - 2
    sum_padding = max_len - len(binary_sum)
    #print off each line at a time
    print(" "*x_padding,x_str)
    print(f"{operationSymbol}",(" "*y_padding),y_str) 
    print("-"*(max_len+1),)
    if is_negative:
        print(" "*(sum_padding-1),"-"+sum_str+"\n")
    else:
        print(" "*sum_padding,sum_str+"\n")

def display_nor_truth_table():
    '''
    Function for displaying the truth table for the NOR functions.
    '''
    print("NOR\nx y Z\n-----")
    x = 0
    #construct the truth table
    while x < 2:
        for y in range(0,2):
            #get the xNORy
            z = NOR(x,y)
            #display the row
            print(f"{x} {y} {z}")
        x += 1
    print()
    
def display_addition_truth_table():
    '''
    Function for displaying the truth tables for the ADD_BIT and CARRY_BIT functions.
    '''
    print("ADDITION\nc x y Z C\n---------")
    in_c = 0
    #construct the truth table
    while in_c < 2:
        for x in range(0,2):
            for y in range(0,2):
                #get the sum of the bits
                z = ADD_BIT(x,y,in_c)
                #get the carry bit of the sum
                out_c = CARRY_BIT(x,y,in_c)
                #display the row
                print(f"{in_c} {x} {y} {z} {out_c}")
        in_c += 1
    print()

def display_subtraction_truth_table():
    '''
    Function for displaying the truth tables for the SUB_BIT and BORROW functions.
    '''
    print("SUBTRACTION\nb x y Z B\n---------")
    in_b = 0
    while in_b < 2:
        for x in range(0,2):
            for y in range(0,2):
                #get the subtracted bit
                z = SUB_BIT(x,y,in_b)
                #get the borrowed bit
                out_b = BORROW_BIT(x,y,in_b)
                print(f"{in_b} {x} {y} {z} {out_b}")
        in_b += 1
    print()

def display_less_than_truth_table():
    '''
    Function for displaying the truth tables for the LESS_THAN function.
    '''
    print("LESS_THAN\nl x y L\n-------")
    in_l = 0
    #construct the truth table
    while in_l < 2:
        for x in range(0,2):
            for y in range(0,2):
                #get the result of x < y
                out_l = LESS_THAN(x,y,in_l)
                #display the row
                print(f"{in_l} {x} {y} {out_l}")
        in_l += 1 
    print()

def print_author_details():
    '''Function for displaying the details of the author.'''
    print("Author: Travis Strawbridge\nStudent ID: 110340713\nEmail ID: STRTK001\n"+
    "This is my own work as defined by the University's Academic Integrity Policy.\n")

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