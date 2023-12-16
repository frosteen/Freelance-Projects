from tabulate import tabulate

x = [0,0,0,0,0,0]
decimalPlace = 2
numChoose = 0
err = 0.01

def RegulaCoeff():
    a0 = float(input("a5: "))
    a1 = float(input("a4: "))
    a2 = float(input("a3: "))
    a3 = float(input("a2: "))
    a4 = float(input("a1: "))
    a5 = float(input("a0: "))

    x[0] = a0
    x[1] = a1
    x[2] = a2
    x[3] = a3
    x[4] = a4
    x[5] = a5
    Regula()

def Regula():
    x0 = float(input("x0: "))
    x1 = float(input("x1: "))

    a0 = x[0]
    a1 = x[1]
    a2 = x[2]
    a3 = x[3]
    a4 = x[4]
    a5 = x[5]

    fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
    fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)

    if (fx0>0 and fx1>0) or (fx0<0 and fx1<0):
        print("can't process")
        Regula()
    else:

        x2 = (x0-(fx0*(x1-x0)/(fx1-fx0)))
        fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)

        rows = []
        rows.append([x0, x1, x2, fx0, fx1, fx2, "continue"])

        error = 1
        while error > err:
            fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
            fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)

            x2 = (x0-(fx0*(x1-x0)/(fx1-fx0)))
            fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)
            prevx2 = x2
            if ((fx2)>0):
                x1 = x2
                x0 = x0
                fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
                fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)
                x2 = (x0-(fx0*(x1-x0)/(fx1-fx0)))
                fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)
                #error = round(abs(fx2))
                
            elif ((fx2)<0):
                x0 = x2
                x1 = x1
                fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
                fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)
                x2 = (x0-(fx0*(x1-x0)/(fx1-fx0)))
                fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)
                #error = round(abs(fx2))
            #error = (abs(prevx2-x2))
            error = abs(prevx2 - x2)
            if error > err:
                rows.append([x0, x1, x2, fx0, fx1, fx2, "continue"])
            elif error < err or error == err:
                rows.append([x0, x1, x2, fx0, fx1, fx2, "terminate"])

        print()
        print(tabulate(rows, headers=['x0', 'x1', "x2", "f(x0)", "f(x1)", "f(x2)", "Remarks"], tablefmt='simple', floatfmt=".{}f".format(decimalPlace)))
        print()
    
def main():
    RegulaCoeff()
    input()
    
main()
