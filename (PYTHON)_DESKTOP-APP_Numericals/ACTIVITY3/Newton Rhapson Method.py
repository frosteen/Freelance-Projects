from os import system
from tabulate import tabulate

x = []
degreePoly = 5
degree = 0
maxIteration = 100
tolerance = 0.01
decimalPlace = 2

def toEquation(char):
    #CONVERTS INPUTS TO EQUATION
    equation = ""
    for i in range(0, degree+1):
        coef = x[degree-i]
        equation += "+{0}*{1}**{2}".format(coef, char, degree-i)
    return equation

def derivative(symbol, num):
    fpiEquation = ""
    #FIRST DERIVATIVE
    if num == 1:
        for i in range(0,degree+1):
            coef = x[degree-i]
            fpiEquation += "+{0}*{1}*{3}**{2}".format(coef, degree-i, degree-i-1, symbol)
    #SECOND DERIVATIVE
    elif num == 2:
        for i in range(0,degree+1):
            coef = x[degree-i]
            fpiEquation += "+{0}*{2}*{1}*{3}**({2}-1)".format(coef, degree-i, degree-i-1, symbol)
    return fpiEquation

def toStringEquation():
    #CONVERTS INPUTS TO STRING EQUATION
    equation = "f(x) = "
    for i in range(degree+1):
        coef = x[degree-i]
        if i == 0:
            equation += "{0}x^{1}".format(coef, degree-i)
        elif coef == 0:
            equation += ""
        elif coef < 0:
            if i == degree:
                equation += " - {0}".format(abs(coef))
            else:
                equation += " - {0}x^{1}".format(abs(coef), degree-i)
        elif coef > 0:
            if i == degree:
                equation += " + {0}".format(abs(coef))
            else:
                equation += " + {0}x^{1}".format(abs(coef), degree-i)
    return equation

def newton_raphsonMethod():
    #NEWTON RHAPSON METHOD ALGORITHM
    x0 = float(input("x0: "))
    fx0 = eval(toEquation("x0"))
    fx01 = eval(derivative("x0", 1))
    fx02 = eval(derivative("x0", 2))
    converge = abs((fx0 * fx02) / (fx01 ** 2))
    e = 1
    if converge < 1:
        rows = []
        while e > tolerance:
            fx0 = eval(toEquation("x0"))
            fx01 = eval(derivative("x0", 1))
            x1 = x0 - (fx0)/(fx01)
            fx1 = eval(toEquation("x1"))
            e = abs(x1 - x0)
            if e <= tolerance:
                rows.append([x0, x1, fx0, fx01, fx1, "terminate"])
            else:
                rows.append([x0, x1, fx0, fx01, fx1, "continue"])
            x0 = x1
        print()
        print(tabulate(rows, headers=['x0', 'x1', "f(x0)", "f'(x0)", "f(x1)", "Remarks"], tablefmt='simple', floatfmt=".{}f".format(decimalPlace)))
        print()
    else:
        print("can't process")
        newton_raphsonMethod()

def inputCoefficients():
    #INPUT COEFFICIENTS
    def jump():
        global degree
        degree = 5
        if degree >= degreePoly:
            for i in range(degree,-1,-1):
                x.append(float(input("a{}: ".format(i))))
            x.reverse()
        else:
            #print("Warning: Degree must be greater than or equal to " + str(degreePoly))
            jump()
    jump()

def hasChosed(numChoose):
    #CHOOSE MENU
    if numChoose == 1:
        print("Fixed Point Iteration (MOSS)")
        inputCoefficients()
        fixedPointIteration()
    elif numChoose == 2:
        print("Secant Method")
        inputCoefficients()
        secantMethod()
    elif numChoose == 3:
        inputCoefficients()
        newton_raphsonMethod()
    else:
        system("cls")
        main()

def main():
    #MAIN PROGRAM
    numChoose = 3
    system("cls")
    hasChosed(numChoose)
    input()

if __name__ == "__main__":
    main()
