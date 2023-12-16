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
	cout << "Curve Fitting: Interpolation" << endl;
	
	cout << endl;
	cout << "POINTS FOR x:" << endl;
	for(int i = 0; i < 5; i++) {
		cout << "x" << i+1 << ": "; cin >> xPoints[i];
	}
	cout << endl;
	cout << "POINTS FOR f(x):" << endl;
	for(int i = 0; i < 5; i++) {
		cout << "f(x" << i+1 << "): "; cin >> yPoints[i];
	}
	cout << endl;
	system("cls");
	
	//VALUES NG X MGA BESHIES
	
	cout << "DATA POINTS:" << endl;
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
	
	cout << endl << endl;
	
	//NEWTON'S INTERPOLATION
	
	double f1x[5], f2x[5], f3x[5], f4x[5];
	
	for(int i = 0; i < 4; i++) {
		f1x[i] = (yPoints[i+1]-yPoints[i])/(xPoints[i+1]-xPoints[i]);
	}
	
	for(int i = 0; i < 3; i++) {
		f2x[i] = (f1x[i+1]-f1x[i])/(xPoints[i+2]-xPoints[i]);
	}
	
	for(int i = 0; i < 2; i++) {
		f3x[i] = (f2x[i+1]-f2x[i])/(xPoints[i+3]-xPoints[i]);
	}
	
	for(int i = 0; i < 1; i++) {
		f4x[i] = (f3x[i+1]-f3x[i])/(xPoints[i+4]-xPoints[i]);
	}
	
	cout << "NEWTON'S DIVIDED DIFFERENCES INTERPOLATING POLYNOMIAL:" << endl << endl;
	cout << "xi" << setw(spcng) << "f(xi)" << setw(spcng) << "f'[x]"<< setw(spcng) << "f''[x]"<< setw(spcng) << "f'''[x]"<< setw(spcng) << "f''''[x]" << endl;

	cout << xPoints[0] << setw(spcng) << yPoints[0] << setw(spcng) << f1x[0] << setw(spcng) << f2x[0] << setw(spcng) << f3x[0]<< setw(spcng) << f4x[0] << endl;
	cout << xPoints[1] << setw(spcng) << yPoints[1] << setw(spcng) << f1x[1] << setw(spcng) << f2x[1] << setw(spcng) << f3x[1]<< setw(spcng) << "" << endl;
	cout << xPoints[2] << setw(spcng) << yPoints[2] << setw(spcng) << f1x[2] << setw(spcng) << f2x[2] << setw(spcng) << "" << setw(spcng) << "" << endl;
	cout << xPoints[3] << setw(spcng) << yPoints[3] << setw(spcng) << f1x[3] << setw(spcng) << "" << setw(spcng) << "" << setw(spcng) << "" << endl;
	cout << xPoints[4] << setw(spcng) << yPoints[4] << setw(spcng) << "" << setw(spcng) << "" << setw(spcng) << ""<< setw(spcng) << "" << endl;
	
	cout << endl;
	
	cout << "b0 = " << yPoints[0] << endl;
	cout << "b1 = " << f1x[0] << endl;
	cout << "b2 = " << f2x[0] << endl;
	cout << "b3 = " << f3x[0] << endl;
	cout << "b4 = " << f4x[0] << endl;
	
	cout << endl;
	cout << "fn(x) = "<<yPoints[0]<<" + "<<f1x[0]<<"(x-"<<xPoints[0]<<") + "<<f2x[0]<<"(x-"<<xPoints[0]<<")(x-"<<xPoints[1]<<") + "<<f3x[0]<<"(x-"<<xPoints[0]<<")(x-"<<xPoints[1]<<")(x-"<<xPoints[2]<<") + "<<f4x[0]<<"(x-"<<xPoints[0]<<")(x-"<<xPoints[1]<<")(x-"<<xPoints[2]<<")(x-"<<xPoints[3]<<")"<<endl;
	cout << "fn(x) = " << coefX[0] << "x^4 + " << coefX[1] << "x^3 + " << coefX[2] << "x^2 + " << coefX[3] << "x + " << coefX[4] << endl;
	cout << endl;
	
	system("pause");
	return 0;
}
