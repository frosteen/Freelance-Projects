#include <iostream>
#include <conio.h>
using namespace std;
int * doCalculation(int num);

int main(int argc, char** argv) {
	int doWhiles;
	cout << "How many Do-Whiles? "; cin >> doWhiles;
	char x = 'y';
	int cntr = 0;
	do {
		int num = 0;
		cout << "Input value: "; cin >> num;
		int *answers = doCalculation(num);
		cout << "Even Sums: " << answers[0] << endl;
		cout << "Odd Products: " << answers[1] << endl;
		cout << "Again (y/n)? "; cin >> x;
		cntr += 1;
	} while (cntr < doWhiles && (x == 'y' || x == 'Y'));
	return 0;
}

int * doCalculation(int num) {
	static int values[2];
	values[0] = 0; values[1] = 1;
	for (int i = 1; i <= num; i++) {
		if (i%2 == 0) {
			values[0] += i;
		} else {
			values[1] *= i;
		}
	}
	return values;
}
