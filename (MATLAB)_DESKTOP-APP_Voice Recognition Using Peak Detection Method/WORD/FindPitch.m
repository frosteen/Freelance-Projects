function [xPitch]=FindPitch(data)
counter = 0;
for k = 1 : length(data)
    if data(k) ~= 0
        counter = counter + 1;
    end
end
xPitch = counter;
end