clc
syms y t;
disp("Euler's Method");
disp("");
h = input('h: '); %input value ng h
f_e = input('dy/dt =  ', 's');
tn = input('t0: '); %input value ng t0
yn = input('y0: '); %input value ng y0
n = 0;
t_end = input('tf: '); %input value ng tf

xPoints = [];
yPoints = []; %points

fprintf('n\t\ttn\t\t\tyn\t\t\tyn+1\n'); %headings nung table
for x = tn:h:t_end
    y1 = yn + subs(eval(f_e), t, x) * h; %equation ng eulers method
    y2 = subs(y1, y, yn); %sub ng yn
    fprintf('%d\t %f\t %f\t %f\n', n, x, yn, y2); %tabulate data
    xPoints = [xPoints, x];
    yPoints = [yPoints, yn];
    yn = y2; %exchange of values
    n = n+1;
end

xlabel('X-AXIS');
ylabel('Y-AXIS');
title('GRAPHICAL REPRESENTATION');
plot(xPoints, yPoints); %show graph
grid on