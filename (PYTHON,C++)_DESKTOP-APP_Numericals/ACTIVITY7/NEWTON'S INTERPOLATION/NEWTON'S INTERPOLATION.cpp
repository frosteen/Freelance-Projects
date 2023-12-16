//ACTIIVTY7 MGA BESSHYWAPZ

#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>

using namespace std;

int spcng = 12;

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
	cout << endl;
	
	system("pause");
	return 0;
}
