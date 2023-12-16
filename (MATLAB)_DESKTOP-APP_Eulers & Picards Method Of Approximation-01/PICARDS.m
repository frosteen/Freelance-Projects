%PICARDS METHOD

picardsMethod(); %tawagin yung function ng picards method
function picardsMethod()
    clc %clear lang yung screen
    syms phi y s t; % mga symbolic variables
    disp("PICARD'S METHOD OF APPROXIMATION");
    disp("");
    disp("NOTE: Initial condition is y(0) = 0");
    f_e = input('dy/dt = f(t, y) = ', 's'); %input yung equation dito example is t + y + 1
    n_ctr = input('n = '); %input value ng n
    yn = 0; n = 0; %initials y(0) = 0

    while n < n_ctr
       y1 = subs(eval(f_e), t, s); %dito banda yung computation ng picards
       y2 = subs(y1, y, yn);
       y3 = int(y2, s, 0, t);
       fprintf('phi(%d) = ', n+1); %display yung values sa command window
       disp(expand(y3)); %dispaly niya yung equation na na-compute
       y3 = subs(y3, t, s); %dito yung paglipat ng values
       yn = y3;
       n = n+1; %iterate natin by 1
    end
    
    % if else statements lang dito, para kung gusto umulit ng user
    againInput = input('Again(y/n)? ');
    if againInput == 'y' || againInput == 'Y'
        picardsMethod();
    else
        disp("Exits"); %eto exits yung program kapag hindi nag 'y' or 'Y' yung user
    end
end