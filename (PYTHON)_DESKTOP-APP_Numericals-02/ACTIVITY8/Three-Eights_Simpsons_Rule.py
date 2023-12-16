#MADE BY PAMBID

from os import system
from tabulate import tabulate

degree = 5 #Ito yung default value beshy
decimalPlace = 2
coefX = []

def eqtn(symbl):
    return "coefX[5]*{}**5 + coefX[4]*{}**4 + coefX[3]*{}**3 + coefX[2]*{}**2 + coefX[1]*{}**1 + coefX[0]".format(symbl, symbl, symbl, symbl, symbl)

def numericalIntegration():
    for i in range(degree, -1, -1):
        coefX.insert(0, float(input("Coefficient for x{}: ".format(i))))
    n = int(input("Value for n: "))
    a = float(input("Value for a: "))
    b = float(input("Value for b: "))

    h = (b - a) / n

    i = a
    Headers = ["x", "F(x)", "Trapezoid Product"]
    rows = []
    fxs = []
    num = 0
    cntr = 0
    while round(i, 10) <= b:
        if i == a or cntr == n: num = 1
        elif (cntr % 3) == 0: num = 2
        elif (cntr % 3) != 0: num = 3
        rows.append([i, eval(eqtn("i")), num*eval(eqtn("i"))])
        fxs.append(num*eval(eqtn("i")))
        i += h
        cntr += 1

    print()
    print("Simpson's 3/8 Rule:")
    print(tabulate(rows, headers=Headers, tablefmt='plain', floatfmt='.{}f'.format(decimalPlace)))
    print("∑f(x)s =", round(sum(fxs), decimalPlace+1))
    print("I =", round(3*h/8*sum(fxs), decimalPlace+1))
    print()

    #ROMBERG INTEGRATION
    i = 1
    Headers = ["n", "h", "I(h)", "n=2", "n=3", "n=4", "n=5"]
    rows = []
    iSagot = []
    en2 = []; en3 = []; en4 = []; en5 = []
    while i <= 16:
        h = (b-a)/i
        fxsSum = 0
        num = 0
        ii = a
        cntr = 0
        while round(ii, 10) <= b:
            if ii == a or cntr == i: num = 1
            elif (cntr % 3) == 0: num = 2
            elif (cntr % 3) != 0: num = 3
            fxsSum += num*eval(eqtn("ii"))
            ii += h
            cntr += 1
        rows.append([i, h, 3*h/8*fxsSum])
        iSagot.append(3*h/8*fxsSum)
        i *= 2
    for i in range(4):
        en2.append(round(iSagot[i+1]+(1/(2**2-1)*(iSagot[i+1]-iSagot[i])), decimalPlace))
    en2.append("")
    for i in range(5):
        rows[i].append(en2[i])

    for i in range(3):
        en3.append(round(en2[i+1]+(1/(2**3-1)*(en2[i+1]-en2[i])), decimalPlace))
    en3.append(""); en3.append("")
    for i in range(5):
        rows[i].append(en3[i])

    for i in range(2):
        en4.append(round(en3[i+1]+(1/(2**4-1)*(en3[i+1]-en3[i])), decimalPlace))
    en4.append(""); en4.append(""); en4.append("")
    for i in range(5):
        rows[i].append(en4[i])

    for i in range(1):
        en5.append(round(en4[i+1]+(1/(2**5-1)*(en4[i+1]-en4[i])), decimalPlace))
    en5.append(""); en5.append(""); en5.append(""); en5.append("")
    for i in range(5):
        rows[i].append(en5[i])
    print("Romberg Integration:")
    print(tabulate(rows, headers=Headers, tablefmt='plain', floatfmt='.{}f'.format(decimalPlace)))
    print()

#MAIN PROGRAM            
def main():
    print('Numerical Integration')
    numericalIntegration()
    input()

if __name__ == "__main__":
    main()
