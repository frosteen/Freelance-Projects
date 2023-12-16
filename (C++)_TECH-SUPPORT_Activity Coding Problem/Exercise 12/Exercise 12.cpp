#include <iostream>
#include <conio.h>

using namespace std;

int main(int argc, char** argv) {
	cout << "Choose Arithmetic Operation:" << endl;
	cout << "[1] Addition" << endl;
	cout << "[2] Subtraction" << endl;
	cout << "[3] Multiplication" << endl;
	cout << "[4] Division" << endl;
	char x;
	cin >> x;
	long double a;
	cout << "Value for A: ";
	cin >> a;
	long double b;
	cout << "Value for B: ";
	cin >> b;
	switch (x) {
		case '1':
			cout << "Answer: " << (a+b) << endl;
			getch();
			break;
		case '2':
			cout << "Answer: " << (a-b) << endl;
			getch();
			break;
		case '3':
			cout << "Answer: " << (a*b) << endl;
			getch();
			break;
		case '4':
			cout << "Answer: " << (a/b) << endl;
			getch();
			break;
		default:
			cout << "Invalid choice. Program will now terminate." << endl;
			getch();
			break;
	}
	return 0;
}
