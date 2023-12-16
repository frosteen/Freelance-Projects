clc
syms y t;
disp("Solving Eigen Value Problems (Euler's Method)");
disp("");
fprintf("EQUATION: y' + %s * y = 0\n", num2str(char(955)));
h = input('h: '); %h step
fprintf('%s: ', num2str(char(955))); lambda = input(''); %input value lambda
f_e = -lambda * y; % y' = -lambda * y
tn = input('x0: '); %initial x0
yn = input('y0: '); %initial y0
n = 0;
t_end = input('x: '); %input value x
fprintf('n\t\ttn\t\t\tyn\n'); %headers nung table
yAnswer = 0; %dito mastostore yung answer
for x = tn:h:t_end
    y1 = yn + subs(eval(f_e), t, x) * h; %equation nung eulers
    y2 = subs(y1, y, yn); %sub yung initial values
    fprintf('%d\t %f\t %f\n', n, x, yn); %display yung values
    yAnswer = yn; %store yung final answer
    
    %paglipat ng values
    yn = y2;
    n = n+1;
end
fprintf("Answer: %f\n", yAnswer); %display values