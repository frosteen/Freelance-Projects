clc
syms phi y s t;
disp("Picard's Method");
disp("");
disp("*Initial condition is y(0) = 0");
f_e = input('f(t, y) = ', 's'); %input yung equation dito example is t + y + 1
n_ctr = input('n = '); %input value ng n
yn = 0; n = 0; %initials y(0) = 0

while n < n_ctr
    y1 = subs(eval(f_e), t, s); %sub natin yung s sa t
    y2 = subs(y1, y, yn); %sub natin yung initial values sa y
    y3 = int(y2, s, 0, t); %integrate
    fprintf('phi(%d) = ', n+1); %display yung values sa cmd window
    disp(expand(y3)); %display ng nakaexpand yung equation
    y3 = subs(y3, t, s); %dito yung paglipat ng values
    yn = y3;
    n = n+1;
end