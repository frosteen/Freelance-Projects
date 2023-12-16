import scipy
import scipy.linalg
from tabulate import tabulate

decimalPlace = 2

def crout(A):

    L = scipy.zeros((10, 10))
    U = scipy.zeros((10, 10))

    for k in range(0, 10):
        U[k, k] = 1

        for j in range(k, 10):
            sum0 = sum(L[k, s] * U[s, j] for s in range(1, k-1))
            #reversed
            L[j, k] = A[k, k] - sum0

        for j in range(k, 10):
            sum1 = sum(L[k, s] * U[s, j] for s in range(1, k-1))
            U[k, j] = (A[k, j] - sum1) / L[k, k]
    return L, U

def jacobi(A, b, x, n):

    D = scipy.diag(A)
    R = A - scipy.diagflat(D)
    
    for i in range(n):
        x = (b - scipy.dot(R,x))/ D
    return x

def gauss(A, b, x, n):

    L = scipy.tril(A)
    U = A - L
    for i in range(n):
        x = scipy.dot(scipy.linalg.inv(L), b - scipy.dot(U, x))
    return x

def main():
    #MANAGE INPUTS
    print("SYSTEM OF LINEAR EQUATIONS")
    withConstMatrix = []
    noConstMatrix = []
    constMatrix = []
    
    for i in range(0, 10):
        withConstMatrix.append([])
        for v in range(10, -1, -1):
            if v != 0:
                withConstMatrix[i].append(float(input("Coefficient x^{0} of Polynomial[{1}]: ".format(v, i+1))))
            else:
                withConstMatrix[i].append(float(input("k of Polynomial[{1}]: ".format(v, i+1))))
                
    noConstMatrix = []
    for i in range(0, 10):
        noConstMatrix.append([])
        for v in range(0, 10):
            noConstMatrix[i].append(withConstMatrix[i][v])
    for i in range(0, 10):
        constMatrix.append(withConstMatrix[i][10])
    print()
    A = scipy.array(noConstMatrix)
    P, L, U = scipy.linalg.lu(A)
    x = scipy.linalg.solve(A, scipy.array(constMatrix))
    L = L.tolist()
    U = U.tolist()
    rows = []
    
    #L DECOMPOSITION
    print("DOOLITTLE METHOD")
    print()
    print("MATRIX[L] ARRAY:")
    print()
    for i in range(0, 10):
        rows.append([])
        for v in range(0, 10):
            rows[i].append("L"+str(i+1)+str(v+1))
    for i, z in zip(range(1, 20, 2), range(0, 10)):
        rows.insert(i, [])
        for v in range(0, 10):
            rows[i].append("%.{}f".format(decimalPlace) % float(L[z][v]))
    print(tabulate(rows, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))

    print()
    
    rows = []
    #U DECOMPOSITION
    print("MATRIX[U] ARRAY:")
    print()
    for i in range(0, 10):
        rows.append([])
        for v in range(0, 10):
            rows[i].append("U"+str(i+1)+str(v+1))
    for i, z in zip(range(1, 20, 2), range(0, 10)):
        rows.insert(i, [])
        for v in range(0, 10):
            rows[i].append("%.2f" % float(U[z][v]))
    print(tabulate(rows, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
    print()
    print("ANSWERS:")
    print()
    for i in range(0,10):
        print("x{}:".format(i+1),"%.{}f".format(decimalPlace) % x[i])

    print(); print()
    
    print("CROUT'S METHOD")
    print()
    L, U = crout(scipy.array(noConstMatrix))
    rows = []
    print("MATRIX[L] ARRAY:")
    print()
    for i in range(0, 10):
        rows.append([])
        for v in range(0, 10):
            rows[i].append("L"+str(i+1)+str(v+1))
    for i, z in zip(range(1, 20, 2), range(0, 10)):
        rows.insert(i, [])
        for v in range(0, 10):
            rows[i].append("%.{}f".format(decimalPlace) % float(L[z][v]))
    print(tabulate(rows, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))

    print()

    rows = []
    #U DECOMPOSITION
    print("MATRIX[U] ARRAY:")
    print()
    for i in range(0, 10):
        rows.append([])
        for v in range(0, 10):
            rows[i].append("U"+str(i+1)+str(v+1))
    for i, z in zip(range(1, 20, 2), range(0, 10)):
        rows.insert(i, [])
        for v in range(0, 10):
            rows[i].append("%.2f" % float(U[z][v]))
    print(tabulate(rows, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
    print()
    print("ANSWERS:")
    print()
    for i in range(0,10):
        print("x{}:".format(i+1),"%.{}f".format(decimalPlace) % x[i])

    print(); print()

    #GAUSS JACOBI METHOD
    
    print("GAUSS-JACOBI METHOD")
    print()
    rows = [];
    e = 1
    cntr = 0
    prev = 1
    sol = 0
    while e >= 0.01:
        sol = jacobi(scipy.array(noConstMatrix),scipy.array(constMatrix),[0,0,0,0,0,0,0,0,0,0],cntr)
        e = abs(prev - sol[0])
        prev = sol[0]
        rows.append([cntr, "%.{}f".format(decimalPlace) % sol[0], "%.{}f".format(decimalPlace) % sol[1], "%.{}f".format(decimalPlace) % sol[2], "%.{}f".format(decimalPlace) % sol[3], "%.{}f".format(decimalPlace) % sol[4], "%.{}f".format(decimalPlace) % sol[5], "%.{}f".format(decimalPlace) % sol[6], "%.{}f".format(decimalPlace) % sol[7], "%.{}f".format(decimalPlace) % sol[8], "%.{}f".format(decimalPlace) % sol[9]])
        cntr += 1
    print(tabulate(rows, headers=["k","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10"], tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
    print()
    print("ANSWERS:")
    print()
    for i in range(0,10):
        print("x{}:".format(i+1),"%.{}f".format(decimalPlace) % sol[i])

    print(); print()
    
    print("GAUSS-SEIDEL METHOD")
    print()
    rows = [];
    e = 1
    cntr = 0
    prev = 1
    sol = 0
    while e >= 0.01:
        sol = gauss(scipy.array(noConstMatrix),scipy.array(constMatrix),[0,0,0,0,0,0,0,0,0,0],cntr)
        e = abs(prev - sol[0])
        prev = sol[0]
        rows.append([cntr, "%.{}f".format(decimalPlace) % sol[0], "%.{}f".format(decimalPlace) % sol[1], "%.{}f".format(decimalPlace) % sol[2], "%.{}f".format(decimalPlace) % sol[3], "%.{}f".format(decimalPlace) % sol[4], "%.{}f".format(decimalPlace) % sol[5], "%.{}f".format(decimalPlace) % sol[6], "%.{}f".format(decimalPlace) % sol[7], "%.{}f".format(decimalPlace) % sol[8], "%.{}f".format(decimalPlace) % sol[9]])
        cntr += 1
    print(tabulate(rows, headers=["k","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10"], tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
    print()
    print("ANSWERS:")
    print()
    for i in range(0,10):
        print("x{}:".format(i+1),"%.{}f".format(decimalPlace) % sol[i])
    input()
main()
