clc;
eq = input('Enter Equation: ','s');
low = input('Enter low value of x: ');
high = input('Enter high value of x: ');
tolerance = input('Enter tolerance: ');
syms x;
eq = diff(eval(eq));
eq = string(eq);
clear x;

my_fun = @(x) eval(eq);
x = doBisection(my_fun, low, high, tolerance);

function  m = doBisection(f, low, high, tol)
fprintf('\n')
disp('-=BISECTION METHOD=-'); 

% Evaluate both ends of the interval
y1 = feval(f, low);
y2 = feval(f, high);
i = 0; 

% Display error and finish if signs are not different
if y1 * y2 > 0
   disp('Have not found a change in sign. Will not continue...');
   m = 'Error'
   return
end 

% Work with the limits modifying them until you find
% a function close enough to zero.
fprintf('\n')
disp('Iter  x-low       x-high        x0         e(%)        f(x)');
old_m = 0;
while (abs(high - low) >= tol)
    i = i + 1;
    % Find a new value to be tested as a root
    m = (high + low)/2;
    y3 = feval(f, m); 
    fprintf('%2i \t %.5f \t %.5f \t %.5f \t %.5f \t %.5f \n', i, low, high, m, abs((m - old_m)/m)*100, y3);  

    % Update the limits
    if y1 * y3 > 0
        low = m;
        y1 = y3;
    else
        high = m;
    end
    old_m = m;
end
fprintf('\nRoot at x = %f \n\n', m);
end