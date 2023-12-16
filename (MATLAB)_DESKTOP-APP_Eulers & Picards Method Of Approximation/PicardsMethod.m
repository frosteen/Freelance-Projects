clc
syms phi y s t;
disp("Calculating Distance(x) with given (v, t)");
disp("");
disp("Warning: Initial condition is x(0) = 0"); %picards iteration uses initial t = 0 & y = 0
f_e = input('dx/dt = v = ', 's');%input v
yn = 0; n = 0;
t_end = input('tf = ');%input final time
n_ctr = 1;%first order linear equation
clc
while n < n_ctr
    y1 = subs(eval(f_e), t, s); %sub yung s sa t
    y2 = subs(y1, y, yn); %sub yung yn sa y
    y3 = int(y2, s, 0, t);
    fprintf('PHI(%d) = ', n+1); %display yung sagot ng PHI(1)
    disp(expand(y3)); %expand yung answer
    y3 = subs(y3, t, s); %sub yung s sa t
    yn = y3; %new value ng yn is yung y3
    n = n+1;
end
fprintf("The distance(x) is %f\n", subs(y3, s, t_end)); %display values