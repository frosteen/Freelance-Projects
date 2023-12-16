#MADE BY PAMBID

from os import system
from tabulate import tabulate
from numpy import array
from numpy import linalg

degree = 5 #Ito yung default value beshy
decimalPlace = 2

def regressionAnalysis():
    def ulitinNatinBesy():
        n = int(input("Input number of points (min of 6): "))
        if n < (degree+1):
            print("Error.")
            ulitinNatinBesy()
        else:
            values = [[],[]]
            for i in range(1, n+1):
                values[0].append(float(input("x"+str(i)+": ")))
            for i in range(1, n+1):
                values[1].append(float(input("f(x"+str(i)+"): ")))
            rows1 = []
            headers1 = ["Xi", "Yi", "Xi^2", "Xi^3", "Xi^4", "Xi^5", "Xi^6", "Xi^7", "Xi^8", "Xi^9", "Xi^10"]
            rows2 = []
            headers2 = ["Xi*Yi", "Xi^2*Yi", "Xi^3*Yi", "Xi^4*Yi", "Xi^5*Yi", "Ym", "ei"]
            sumValues = []
            sumValuesCol = []

            for i in range(1, 11):
                sumValues.append(sum(x**i for x in values[0]))
            for i in range(0, 6):
                sumValuesCol.append(sum((x**i)*(y) for x, y in zip(values[0], values[1])))
            
            #MatrixBessy
            rowMatrix1 = [n, sumValues[0], sumValues[1], sumValues[2], sumValues[3], sumValues[4]]
            rowMatrix2 = [sumValues[0], sumValues[1], sumValues[2], sumValues[3], sumValues[4], sumValues[5]]
            rowMatrix3 = [sumValues[1], sumValues[2], sumValues[3], sumValues[4], sumValues[5], sumValues[6]]
            rowMatrix4 = [sumValues[2], sumValues[3], sumValues[4], sumValues[5], sumValues[6], sumValues[7]]
            rowMatrix5 = [sumValues[3], sumValues[4], sumValues[5], sumValues[6], sumValues[7], sumValues[8]]
            rowMatrix6 = [sumValues[4], sumValues[5], sumValues[6], sumValues[7], sumValues[8], sumValues[9]]
            colMatrix = [sumValuesCol[0], sumValuesCol[1], sumValuesCol[2], sumValuesCol[3], sumValuesCol[4], sumValuesCol[5]]
            A = array([rowMatrix1,rowMatrix2,rowMatrix3,rowMatrix4,rowMatrix5,rowMatrix6])
            B = array(colMatrix)
            x = linalg.solve(A, B)

            err = 0
            for i in range(0, n):
                ym = x[0] + x[1]*values[0][i] + x[2]*values[0][i]**2 + x[3]*values[0][i]**3 + x[4]*values[0][i]**4 + x[5]*values[0][i]**5 + err
                rows1.append([values[0][i], values[1][i], values[0][i]**2, values[0][i]**3, values[0][i]**4, values[0][i]**5, values[0][i]**6, values[0][i]**7, values[0][i]**8, values[0][i]**9, values[0][i]**10])
                rows2.append([values[0][i]*values[1][i], values[0][i]**2*values[1][i], values[0][i]**3*values[1][i], values[0][i]**4*values[1][i], values[0][i]**5*values[1][i], ym, err])
                err = abs(values[1][i] - ym)
                             
            values[0].insert(0, "x"); values[1].insert(0, "f(x)")
            print()
            print("POINTS:")
            print()
            print(tabulate(values, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
            print()
            print("POLYNOMIAL REGRESSION:")
            print()
            print(tabulate(rows1, headers=headers1, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
            print()
            print(tabulate(rows2, headers=headers2, tablefmt='plain', floatfmt=".{}f".format(decimalPlace)))
            print()
            xValues = []
            for i in range(0, 6):
                xValues.append(round(x[i], decimalPlace))
            print()
            print("f2(x) = ",xValues[0],"+",str(xValues[1])+"x","+",str(xValues[2])+"x^2","+",str(xValues[3])+"x^3","+",str(xValues[4])+"x^4","+",str(xValues[5])+"x^5")
            print()            
    ulitinNatinBesy()
            
def main():
    #MAIN PROGRAM
    print("REGRESSION ANALYSIS (5th Degree)")
    regressionAnalysis()
    input()

if __name__ == "__main__":
    main()
