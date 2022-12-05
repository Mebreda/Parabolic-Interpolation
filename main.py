import math
from io import StringIO
import sys
import os


tmp = sys.stdout
my_result = StringIO()
sys.stdout = my_result
derivation = ""
"""
Function that will asks for the equation and the initial guesses
Returns x0, x1, and x2
"""


def input_values():
    # Asks for inputs
    equation = input("f(x) = ")
    print("Enter the initial guesses")
    x0 = float(input("x0 = "))
    x1 = float(input("x1 = "))
    x2 = float(input("x2 = "))
    return x0, x1, x2


"""
Main process of the Parabolic Interpolation
Returns the x(x3) and the true value(f(x3))
"""


def parabolic_interpolation(x0, x1, x2, equation):
    value_repeat_ctr = 0  # Counter that will check if the f(x) is repeating
    iteration_ctr = 1  # Counter for the number of iterations
    temp_f3 = 0  # Temporary f(x3). used to check if f(x) is repeating
    # Substitutes the values of the initial guesses to the equation
    f0, f1, f2 = solve(x0, equation), solve(x1, equation), solve(x2, equation)
    print("%1s %10s %10s %10s %10s %10s %10s %10s %10s" % (
        "i", "x0", "x1", "x2", "x3", "f0", "f1", "f2", "f3"))  # Print header
    # Loop for the parabolic_interpolation
    # Checks if f(x) is repeating more than 3 times
    while value_repeat_ctr < 2:
        # Formula for the Parabolic Interpolation
        x3 = (f0 * (x1 ** 2 - x2 ** 2) + f1 * (x2 ** 2 - x0 ** 2) + f2 * (x0 ** 2 - x1 ** 2)) / \
             (2 * f0 * (x1 - x2) + 2 * f1 * (x2 - x0) + 2 * f2 * (x0 - x1))

        # store_derivation(str(f0) + " * (" + str(x1) + "^2 - " + str(x2) + "^2) +" + str(f1) + " * (" + str(x2) + "^2 - " + str(x0) + "^2) +" + str(f2) + " * (" + str(x0) + "^2 - " + str(x1) + "^2)")
        # store_derivation("2 * " + str(f0) + " * (" + str(x1) + " - " + str(x2) + ") + 2 * " + str(f1) + " * (" + str(x2) + " - " + str(x0) + ") + 2 * " + str(f2) + " * (" + str(x0) + " - " + str(x1) + ")")
        f3 = solve(x3, equation)  # Substitutes the x3 to the equation
        print_values(iteration_ctr, x0, x1, x2, x3, f0, f1, f2, f3)
        # Checks if f(x) is repeating
        if round(f3, 6) == round(temp_f3, 6):
            value_repeat_ctr += 1

        temp_f3 = f3  # Stores f3 to temp_f3 for checking
        # Stores the new position of the variables
        # If the function value of x3 is higher than x1 and the value of x3 is higher than x1, x0 is discarded
        # x1 will be stored to x0, and x3 will be stored to x1
        if f3 >= f1 and x3 > x1:
            x0, x1, x2 = x1, x3, x2
            f0, f1, f2 = f1, f3, f2
        # Else, discard x3, x1 will be stored to x3
        else:
            x0, x1, x2 = x0, x3, x1
            f0, f1, f2 = f0, f3, f1

        iteration_ctr += 1  # Add 1 to iteration counter

    return x3, f3


"""
Prints the values
"""


def print_values(i, x0, x1, x2, x3, f0, f1, f2, f3):
    print("%1d %10f %10f %10f %10f %10f %10f %10f %10f" % (i, x0, x1, x2, x3, f0, f1, f2, f3))


"""
Converts the equation to python language
Evaluates the equation 
"""


def solve(x, equation):
    temp_equation = equation.replace("sin", "math.sin")
    temp_equation = temp_equation.replace("cos", "math.cos")
    temp_equation = temp_equation.replace("tan", "math.tan")
    temp_equation = temp_equation.replace("^", "**")
    return eval(temp_equation)


def store_derivation(str, str2):
    str = str + '\n'
    str = str + "---------------------------------------------------------------"



"""
Main method
"""
if __name__ == '__main__':
    x0, x1, x2 = input_values()
    global equation
    # equation = '2*sin(x)-((x**2)/10)'
    x0 = float(0)
    x1 = float(1)
    x2 = float(4)
    x3, f3 = parabolic_interpolation(x0, x1, x2, equation)
    print("x = ", x3)
    print("true value = ", f3)
