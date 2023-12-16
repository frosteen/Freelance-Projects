clc
syms phi y s t;
disp("Solving Eigen Value Problems (Picard's Method)");
disp("");
fprintf("EQUATION: y'' + %s * y = 0\n", num2str(char(955)));
fprintf('%s: ', num2str(char(955))); lambda = input(''); %input value lambda
n = input('x0: '); %input value x0
yn = input('y0: '); %input value y0
t_end = input('x: '); %input value x
f_e = -lambda * y; % y'' = -lambda * y
n_ctr = 2; % 2nd integral, phi(2)
while n < n_ctr
    y1 = subs(f_e, t, s); %sub s
    y2 = subs(y1, y, yn); %sub initials y0
    y3 = int(y2, s, 0, t); %sub t
    fprintf('PHI(%d) = ', n+1); %display value of phi
    disp(expand(y3)); %expand equation
    y3 = subs(y3, t, s); %sub s
    
    %pag lipat ng values
    yn = y3;
    n = n+1;
end
fprintf("Answer: %f\n",subs(y3,s,t_end)); %display answer