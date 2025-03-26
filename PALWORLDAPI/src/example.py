import math

def add_numbers(a,b): # 콤마 뒤 공백 없음 (PEP8 위반)
    result = a + b
    return result

def divide(x, y):
    if y == 0:
        print("Cannot divide by zero")
    else:
        return x / y

unused_variable = 42  # 사용되지 않음 (pylint 경고)

divide(10, 0)
