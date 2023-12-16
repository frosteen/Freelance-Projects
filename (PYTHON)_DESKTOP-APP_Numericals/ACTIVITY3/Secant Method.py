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

def secantMethod():
    #SECANT METHOD ALGORITHM
    x0 = float(input("x0: "))
    x1 = float(input("x1: "))
    rows = []
    e = 1
    while e > tolerance:
        fx0 = eval(toEquation("x0"))
        fx1 = eval(toEquation("x1"))
        x2 = x0 - fx0 * ((x1 - x0) / (fx1 - fx0))
        e = abs(x0 - x1)
        fx2 = eval(toEquation("x2"))
        if abs(x0 - x1) <= tolerance:
            rows.append([x0, x1, x2, fx0, fx1, fx2, "terminate"])
        else:
            rows.append([x0, x1, x2, fx0, fx1, fx2, "continue"])
        x0 = x1
        x1 = x2
    print()
    print(tabulate(rows, headers=['x0', 'x1', "x2", "f(x0)", "f(x1)", "f(x2)", "Remarks"], tablefmt='simple', floatfmt=".{}f".format(decimalPlace)))
    print()

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
        inputCoefficients()
        secantMethod()
    elif numChoose == 3:
        print("Newton-Raphson Method")
        inputCoefficients()
        newton_raphsonMethod()
    else:
        system("cls")
        main()

def main():
    #MAIN PROGRAM
    numChoose = 2
    system("cls")
    hasChosed(numChoose)
    input()

if __name__ == "__main__":
    main()
