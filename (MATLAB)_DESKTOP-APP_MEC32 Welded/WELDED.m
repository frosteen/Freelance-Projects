clc;
disp('--WELD PROBLEM SOLVER--');
%get inputs from the problem
D = input('Input dead load: ');
L = input('Input live load: ');
t = input('Input connected parts thickness: ');
Fy = input('Input Fy: ');
Fu = input('Input Fu: ');
%display solution
disp('SOLUTION:');
disp('~Using the EQ Pu = 1.2D + 1.6L');
Pu = 1.2*D+1.6*L;
fprintf("\tPu = %f N/mm\n", Pu);
disp('~Shear strength per mm');
fprintf('\t244.956 * 4 = %f N/mm\n', 244.956*4);
disp('~Shear yield strength of the base metal (0.6*Fy*t)');
fprintf('\t0.6*Fy*t  = %f N/mm\n', 0.6*Fy*t);
disp('~Shear rupture strength of the base metal (0.45*Fu*t)');
fprintf('\t0.45*Fu*t = %f N/mm\n', 0.45*Fu*t);
minVal = min([244.956*4,0.6*Fy*t,0.45*Fu*t]); %find minimum
disp('~Weld strength that governs');
fprintf('\tWeld Strength = %f N/mm\n', minVal);
disp('~Total length required');
%display final answer
fprintf('\t->Pu/WeldStrength = %f mm\n', Pu/minVal);



