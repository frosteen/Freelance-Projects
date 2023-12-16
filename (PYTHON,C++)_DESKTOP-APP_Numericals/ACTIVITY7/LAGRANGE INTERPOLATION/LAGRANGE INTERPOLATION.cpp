//ACTIIVTY7 MGA BESSHYWAPZ

#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>

using namespace std;

int spcng = 12;
double coefXs[5]; //makeThisGlobalBwisetHAHAHAHA
double coefX[5];

void showTheseValues(string name, double *mgaValues) {
	cout << name << endl;
	cout << "x^4" << setw(spcng) << "x^3" << setw(spcng) << "x^2" << setw(spcng) << "x" << setw(spcng) << "k";
	cout << endl;
	cout << (mgaValues[0]) << setw(spcng) << (mgaValues[1]) << setw(spcng) << (mgaValues[2]) << setw(spcng) << (mgaValues[3]) << setw(spcng) << (mgaValues[4]);
	cout << endl;
	for(int i = 0; i < 5; i++) {
		coefX[i] += mgaValues[i];
	}
}

double *computeNatin(double a, double b, double c, double d, double yungWala, double fx) {
	coefXs[5];
	double mulSaLahat = (1/((yungWala-a)*(yungWala-b)*(yungWala-c)*(yungWala-d)));
	coefXs[0] = 1*fx*mulSaLahat; //x^4
	coefXs[1] = (-d-c-b-a)*fx*mulSaLahat; //x^3
	coefXs[2] = (c*d+b*d+b*c+a*d+a*c+a*b)*fx*mulSaLahat; //x^2
	coefXs[3] = (-b*c*d-a*c*d-a*b*d-a*b*c)*fx*mulSaLahat; // x^1
	coefXs[4] = a*b*c*d*fx*mulSaLahat; // x^0 or k
	return coefXs;
}

int main() {
	cout.precision(2);
	cout.setf(ios::fixed);
	
	//CURVE FITTING
	
	double xPoints[5];
	double yPoints[5];
	cout << "CURVE FITTING: INTERPOLATION" << endl;
	for(int i = 0; i < 5; i++) {
		cout << "Value for x" << i+1 << ": "; cin >> xPoints[i];
	}
	for(int i = 0; i < 5; i++) {
		cout << "Value for f(x" << i+1 << "): "; cin >> yPoints[i];
	}
	cout << endl;
	
	//VALUES NG X MGA BESHIES
	
	cout << "POINTS:" << endl << endl;
	cout << "x" << setw(spcng) << xPoints[0] << setw(spcng) << xPoints[1] << setw(spcng) << xPoints[2] << setw(spcng) << xPoints[3] << setw(spcng) << xPoints[4] << endl;
	cout << "y" << setw(spcng) << yPoints[0] << setw(spcng) << yPoints[1] << setw(spcng) << yPoints[2] << setw(spcng) << yPoints[3] << setw(spcng) << yPoints[4] << endl;
	cout << endl;

	cout << "LARGRANGE INTERPOLATING POLYNOMIAL:" << endl;
	
	cout << endl;
	
	//COMPUTATION TIME
	
	showTheseValues("L0(x)f(x0):", computeNatin(xPoints[1],xPoints[2],xPoints[3],xPoints[4], xPoints[0], yPoints[0]));
	cout << endl;
	showTheseValues("L1(x)f(x1):", computeNatin(xPoints[0],xPoints[2],xPoints[3],xPoints[4], xPoints[1], yPoints[1]));
	cout << endl;
	showTheseValues("L2(x)f(x2):", computeNatin(xPoints[1],xPoints[0],xPoints[3],xPoints[4], xPoints[2], yPoints[2]));
	cout << endl;
	showTheseValues("L3(x)f(x3):", computeNatin(xPoints[1],xPoints[2],xPoints[0],xPoints[4], xPoints[3], yPoints[3]));
	cout << endl;
	showTheseValues("L4(x)f(x4):", computeNatin(xPoints[1],xPoints[2],xPoints[3],xPoints[0], xPoints[4], yPoints[4]));
	cout << endl;
	
	cout << "fn(x) = " << coefX[0] << "x^4 + " << coefX[1] << "x^3 + " << coefX[2] << "x^2 + " << coefX[3] << "x + " << coefX[4] << endl;
	
	cout << endl;
	system("pause");
	return 0;
}
