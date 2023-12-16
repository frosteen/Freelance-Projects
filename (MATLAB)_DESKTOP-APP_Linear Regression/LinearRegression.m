linearRegression(); %Call lang natin yung function ng linearRegression
function linearRegression()
    clc; %Clear lang po natin yung terminal
    disp("SIMPLE LINEAR REGRESSION"); %TITLE LANG BESHY
    disp("");
    x = input('X POINTS: '); %Input nung mga x points
    xLabel = input('Label for x points: ', 's'); %Label lang nung x intercept
    y = input('Y POINTS: '); %Input nung mga y points
    yLabel = input('Label for y points: ', 's'); %Label lang nung y intercept
    titleData = input('Label for data: ', 's'); %Label lang nung Data

    b1 = x\y; %Computation ng slope b1

    yCalc1 = b1*x; %Formula nung y = b1*x
    scatter(x,y); %Scatter lang yung mga points sa graph
    hold on; %Para di mabura yung unang graph
    plot(x,yCalc1); %Plot natin beshy yung y = b1*x
    xlabel(xLabel); %label lang natin idol
    ylabel(yLabel);
    title(titleData); %title lang din
    grid on; %May grid yung graph

    X = [ones(length(x),1) x];
    b = X\y; %Computation naman eto ng both b0 and b1 sa y = b0 + b1*x

    yCalc2 = X*b; %Bale eto yung y = b0 + b1*x beshy
    plot(x,yCalc2,'--'); %Graph lang natin yung y = b0 + b1*x lodi

    %Lagyan lang ng label yung mga graphs para di malito bes hahahahah
    title(legend('DATA',"y = " + b(2,1) + "x","y = " + b(1,1) + " + " + b(2,1) + "x",'location','best'),'LEGENDS');
    
    % IF ELSE STATEMENTS LANG IF GUSTO MO UMULIT
    againInput = input('Again(y/n)? ', 's');
    if againInput == 'y' || againInput == 'Y'
        linearRegression()
    else
        disp("Exits")
        quit
    end
end
