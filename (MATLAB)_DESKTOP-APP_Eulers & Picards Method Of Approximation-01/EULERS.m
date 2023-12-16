%EULERS METHOD

eulersMethod(); % tawagin yung function ng eulers method
function eulersMethod()
    clc
    syms y t; %clear lang yung screen
    disp("EULER'S METHOD OF APPROXIMATION");
    disp("");
    h = input('Step size = '); %input value ng step size
    f_e = input('dy/dt = f(t, y) = ', 's'); %input yung equation dito example is t + y + 1
    tn = input('t0 = '); %input value ng t0
    yn = input('y0 = '); %input value ng y0
    n = 0;
    t_end = input('last t = '); %input value ng t
    %Iteration

    fprintf('n\t\ttn\t\t\tyn\t\t\tyn+1\n'); %headings nung table
    for x = tn:h:t_end %dito nangyayare yung iteration
        y1 = yn + subs(eval(f_e), t, x) * h; %dito yung computation ng eulersMethod
        y2 = subs(y1, y, yn); %substitutions lang
        fprintf('%d\t %f\t %f\t %f\n', n, x, yn, y2); %print yung n, x, yn, y2
        yn = y2; %paglipat ng values
        n = n+1; %iterate lang natin by 1
    end
    
    % if else statements lang dito, para kung gusto umulit ng user
    againInput = input('Again(y/n)? ');
    if againInput == 'y' || againInput == 'Y'
        eulersMethod();
    else
        disp("Exits"); %eto exits yung program kapag hindi nag 'y' or 'Y' yung user
    end
end