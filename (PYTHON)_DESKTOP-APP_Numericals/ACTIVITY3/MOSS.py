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
    
def fixedPointIteration():
    #FIXED POINT ITERATION ALGORITHM
    def fixedp(f,x0,tol=tolerance,maxiter=maxIteration):
        e = 1
        itr = 0
        xp = []
        while(e > tol and itr < maxiter):
            x = f(x0)
            e = abs(x0-x)
            x0 = x
            xp.append(x0)
            xp.append(x0)
            itr = itr + 1
        xe = f(x)
        return x,xp,xe
    x0 = float(input("x0: "))
    fpiEquations = []
    for v in range(0, degree+1):
        fpiEquation = ""
        for i in range(0,degree+1):
            coef = x[degree-i]
            if i == v:
                fpiEquation += "".format(coef, degree-i)
            else:
                fpiEquation += "+{0}*x**{1}".format(coef, degree-i)
        fpiEquation = "(-({0})/{1})**(1/{2})".format(fpiEquation, x[degree-v], degree-v)
        fpiEquations.append(fpiEquation)
    fpiEquations.pop(len(fpiEquations)-1)
    picked = 0
    for v in range(len(fpiEquations)):
        f = lambda x : eval(fpiEquations[v])
        try:
            xf, xp, xe = fixedp(f, x0)
        except OverflowError:
            print("can't process")
            choice = 1
            break
        if not len(xp) == maxIteration*2 and not isinstance(xf, complex):
            picked = v
            choice = 2
            break
    if choice == 1:
        fixedPointIteration()
    elif choice == 2:
        f = lambda x : eval(fpiEquations[picked])
        xf, xp, xe = fixedp(f, x0)
        xp.insert(0, x0)
        fpiEquations = []
        for i in range(0,len(xp)-3,4):
            fpiEquations.append([xp[i], xp[i+1], xp[i+2], xp[i+3], "continue"])
        fpiEquations.append([xp[-3], xp[-2], xp[-1], xe, "terminate"])
        print()
        print(tabulate(fpiEquations, headers=['x0', 'x1', "f(x0)", "f(x1)", "Remarks"], tablefmt='simple', floatfmt=".{}f".format(decimalPlace)))
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
        inputCoefficients()
        fixedPointIteration()
    elif numChoose == 2:
        print("Secant Method")
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
    numChoose = 1
    system("cls")
    hasChosed(numChoose)
    input()

if __name__ == "__main__":
    main()
