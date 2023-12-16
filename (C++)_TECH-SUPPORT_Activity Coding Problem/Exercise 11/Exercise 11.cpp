#include <iostream>
#include <conio.h>

using namespace std;
void doPattern();

int main(int argc, char** argv) {
	
	//INTRODUCTION
	cout << "Do you want to draw the pattern or quit?" << endl;
	cout << "Y (or y) - Yes" << endl;
	cout << "Q (or q) - Quit" << endl;
	//
	
	char x;
	cin >> x;
	if (x == 'Y' || x == 'y') {
		doPattern();
		cout << "Press any key to continue.";
		getch();
	} else if (x == 'Q' || x == 'q') {
		cout << "Program will now exit." << endl;
		cout << "Press any key to continue.";
		getch();
	} else {
		cout << "Input not recognized. Program will now exit." << endl;
		cout << "Press any key to continue.";
		getch();
	}
	return 0;
}


void doPattern() {
	for (int x = 0; x < 8; x++) {
		if (x % 2 == 0) {	
			for (int i = 0; i < 9; i ++) {
				cout << "* ";
			}	
		} else {	
			for (int i = 0; i < 9; i ++) {
				cout << " *";
			}	
		}
		cout << endl;
	}
}
