#GAWA NI PAMBID

from tabulate import tabulate
import cmath
from os import system

decimalPlace = 2
tol = 0.01
coefX = []
rows = []
x3 = 0

def mullersNaMalupet(func, x0, x1, x2, max_steps=100):
    x = [x0,x1,x2]
    datingRoot = 0
    error = 1
    root = 0
    while error > tol:
        datingRoot = root
        y = func(x[0]), func(x[1]), func(x[2])
        h0 = x[1]-x[0]
        h1 = x[2]-x[1]
        lam0 = (y[1] - y[0])/h0
        lam1 = (y[2] - y[1])/h1
        a = (lam1-lam0)/(h1+h0)
        b = a*h1 + lam1
        c = y[2]
        D  = (b**2 - 4.0*a*c)**0.5
        if abs(b+D) > abs(b-D):
            root = x[2] - ((2.0*c)/(b + D))
        else:
            root = x[2] - ((2.0*c)/(b - D))
        error = abs(datingRoot - root)
        rows.append([x[0],x[1],x[2],h0,h1,lam0,lam1,a,b,c,D,root])
        global x3
        x3 = root
        del x[0]
        x.append(root)

def bairstowsNaMalupet(a,r,s,g,roots):
    if(g<1):
            return None
    if((g==1) and (a[1]!=0)):
            roots.append(float(-a[0])/float(a[1]))
            return None
    if(g==2):
            D = (a[1]**2.0)-(4.0)*(a[2])*(a[0])
            X1 = (-a[1] - cmath.sqrt(D))/(2.0*a[2])
            X2 = (-a[1] + cmath.sqrt(D))/(2.0*a[2])
            roots.append(X1)
            roots.append(X2)
            return None
    n = len(a)
    b = [0]*len(a)
    c = [0]*len(a)
    b[n-1] = a[n-1]
    b[n-2] = a[n-2] + r*b[n-1]
    i = n - 3
    while(i>=0):
            b[i] = a[i] + r*b[i+1] + s*b[i+2]
            i = i - 1
    c[n-1] = b[n-1]
    c[n-2] = b[n-2] + r*c[n-1]
    i = n - 3
    while(i>=0):
            c[i] = b[i] + r*c[i+1] + s*c[i+2]
            i = i - 1
    Din = ((c[2]*c[2])-(c[3]*c[1]))**(-1.0)
    if n == 6:
        rows.append([r, s, b[0], b[1], b[2], b[3], b[4], b[5], c[0], c[1], c[2], c[3], c[4]])
    r = r + (Din)*((c[2])*(-b[1])+(-c[3])*(-b[0]))
    s = s + (Din)*((-c[1])*(-b[1])+(c[2])*(-b[0]))
    if(abs(b[0])>tol or abs(b[1])>tol):
        return bairstowsNaMalupet(a,r,s,g,roots)
    if (g>=3):
        Dis = ((-r)**(2.0))-((4.0)*(1.0)*(-s))
        X1 = (r - (cmath.sqrt(Dis)))/(2.0)
        X2 = (r + (cmath.sqrt(Dis)))/(2.0)
        roots.append(X1)
        roots.append(X2)
        return bairstowsNaMalupet(b[2:],r,s,g-2,roots)

x0,x1,x2 = 0, 0, 0

def main():
    print("Roots of Non-Linear Equations")
    for i in range(5, -1,-1):
        coefX.append(float(input("x^{}: ".format(i))))
    r = float(input("r: "))
    s = float(input("s: "))
    def doItAgain():
        global x0,x1,x2
        x0 = float(input("x1: "))
        x1 = float(input("x2: "))
        x2 = float(input("x3: "))
        def computeThis(x):
            return coefX[0]*x**5 + coefX[1]*x**4 + coefX[2]*x**3 + coefX[3]*x**2 + coefX[4]*x**1 + coefX[5]
        if x0 == x1 or x1 == x2:
            print("x1,x2,x3 are invalid")
            doItAgain()
        mullersNaMalupet(lambda x: coefX[0]*x**5 + coefX[1]*x**4 + coefX[2]*x**3 + coefX[3]*x**2 + coefX[4]*x**1 + coefX[5], x0,x1,x2)
        if isinstance(x3, complex):
            print("x1,x2,x3 are invalid")
            doItAgain()
    doItAgain()
    #BAIRSTOWSESHIES
    system("cls")
    print("Bairstow's Method:"); print()
    del rows[:]
    coefX.reverse()
    roots = []
    bairstowsNaMalupet(coefX, r, s, len(coefX)-1, roots)
    k = 0
    print(tabulate(rows, headers=["r","s","b0","b1","b2","b3","b4", "b5","c0","c1","c2","c3", "c4"], tablefmt='simple', floatfmt=".{}f".format(decimalPlace)))
    print()
    for r in roots:
        if not isinstance(r, complex):
            print("r" + str(k) + " = " + str(round(r, decimalPlace))+"    ", end='')
        else:
            print("r" + str(k) + " = " + str(round(r.real, decimalPlace))+ " + " + str(round(r.imag, decimalPlace)) + "j"+"    ", end='')
        k += 1

    #MULLERSMETHODNAMAN
    coefX.reverse()
    print(); print()
    print("Muller's Method:"); print()
    del rows[:]
    mullersNaMalupet(lambda x: coefX[0]*x**5 + coefX[1]*x**4 + coefX[2]*x**3 + coefX[3]*x**2 + coefX[4]*x**1 + coefX[5], x0,x1,x2)
    print(tabulate(rows, headers=["x0","x1","x2","h0","h1","lambda0","lambda1","a","b","c","D","x3"], tablefmt='simple', floatfmt=".{}f".format(decimalPlace)))
    print()
    print("x3 =",round(x3, decimalPlace))
    print()
    input()

main()
