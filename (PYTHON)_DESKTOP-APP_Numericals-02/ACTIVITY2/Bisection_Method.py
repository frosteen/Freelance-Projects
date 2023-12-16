from tabulate import tabulate

x = [0,0,0,0,0,0]
decimalPlace = 2
numChoose = 0

def BisectionCoeff():

    a0 = float(input("Coefficient for x5: "))
    a1 = float(input("Coefficient for x4: "))
    a2 = float(input("Coefficient for x3: "))
    a3 = float(input("Coefficient for x2: "))
    a4 = float(input("Coefficient for x1: "))
    a5 = float(input("Coefficient for x0: "))

    x[0] = a0
    x[1] = a1
    x[2] = a2
    x[3] = a3
    x[4] = a4
    x[5] = a5
    
    Bisection()

def Bisection():
    x0 = float(input("Initial value x0: "))
    x1 = float(input("Initial value x1: "))

    a0 = x[0]
    a1 = x[1]
    a2 = x[2]
    a3 = x[3]
    a4 = x[4]
    a5 = x[5]

    fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
    fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)

    if (fx0>0 and fx1>0) or (fx0<0 and fx1<0):
        print("Error initial conditions")
        Bisection()
    else:

        x2 = ((x0+x1)/2)
        fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)

        rows = []
        rows.append([x0, x1, x2, fx0, fx1, fx2, "CONTINUE"])
        
        error = 1
            
        while error > 0.01:
            fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
            fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)
        
            x2 = ((x0+x1)/2)
            fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)

            
            prevx2 = x2
            if ((fx2*fx1)>0):
                x1 = x2
                x0 = x0
                fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
                fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)
                x2 = ((x0+x1)/2)
                fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)
                error = (abs(x2 - x1))
                
            elif ((fx2*fx0)>0):
                x0 = x2
                x1 = x1
                fx0 = (a0*x0**5 + a1*x0**4 + a2*x0**3 + a3*x0**2 + a4*x0**1 + a5)
                fx1 = (a0*x1**5 + a1*x1**4 + a2*x1**3 + a3*x1**2 + a4*x1**1 + a5)
                x2 = ((x0+x1)/2)
                fx2 = (a0*x2**5 + a1*x2**4 + a2*x2**3 + a3*x2**2 + a4*x2**1 + a5)
                error = (abs(x2 - x1))
            error = abs(prevx2 - x2)
            if error > 0.01:
                rows.append([x0, x1, x2, fx0, fx1, fx2, "CONTINUE"])
            elif error < 0.01 or error == 0.01:
                rows.append([x0, x1, x2, fx0, fx1, fx2, "TERMINATE"])

        print()  
        print(tabulate(rows, headers=['x0', 'x1', "x2", "f(x0)", "f(x1)", "f(x2)", "REMARKS"], tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
        print()
        print("Root:", round(x2, decimalPlace))
        print()
    
def main():
    print("Bisection Method")
    BisectionCoeff()
    input()
    
main()
