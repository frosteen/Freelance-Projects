clc
syms y t;
disp("Calculating Distance(x) with given (v, t)");
disp("");
h = input('h = ');%step h
f_e = input('dx/dt = v = ', 's');%input velocity
yn = input('x0 = ');%input initial displacement(x)
tn = input('t0 = ');%input intial time
n = 0;
t_end = input('tf = ');%final time
clc
fprintf('n\t\ttn\t\t\tyn\n');%header table
yAnswer = 0;
for x = tn:h:t_end
    y1 = yn + subs(eval(f_e), t, x) * h;%equation ye = y0 + f(t,y) * h
    y2 = subs(y1, y, yn);%subs yn
    fprintf('%d\t %f\t %f\n', n, x, yn);%print values
    yAnswer = yn;
    yn = y2;%new value ng y0 is yung sagot ng ye
    n = n+1;
end
fprintf("The distance(x) is %f\n", yAnswer); %display yung sagot
