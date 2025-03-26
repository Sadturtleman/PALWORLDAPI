# Description: This file contains the example functions that will be used in the API

def add_numbers(a,b) : 
    # This function adds two numbers
    result = a + b
    return result

def divide(x, y) :
    # This function divides two numbers
    if y == 0:
        print("Cannot divide by zero")
    else:
        return x / y
