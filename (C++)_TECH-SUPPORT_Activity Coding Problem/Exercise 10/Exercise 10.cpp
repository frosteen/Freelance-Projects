#include <iostream>
#include <conio.h>
#include <iomanip>

using namespace std;
int doFactorial(int num);

int main(int argc, char** argv) {
	int num = 0;
	cout << "Enter the value of n: "; cin >> num;
	cout << endl;
	cout << "Integer" << setw(20) << "Factorial" << endl;
	for (int i = 1; i <= num; i++) {
		cout << setw(4) << i << setw(20) << doFactorial(i) << endl;
	}
	getch();
	return 0;
}

int doFactorial(int num) {
	int sum = 1;
	for (int i = 1; i <= num; i++) {
		sum = sum*i;
	}
	return sum;
}
