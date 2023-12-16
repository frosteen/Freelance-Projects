BAGUHIN = 2% BAGUHIN NALANG THIS kapag 1-1st column, 2-2nd column

r = readtable('latest-data-sample-motion.xlsx');
r = r{:,BAGUHIN}; 
cntr = 0;
while true
    cntr = cntr + 1;
    if ~isnan(r(cntr))
        r(cntr) = r(cntr);
    else
         break;
    end
end
r(isnan(r)) = 0;
Fs = 55;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(r);            % Length of signal
t = (0:L-1)*T;        % Time vector
X = r;
Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
plot(f,P1) 
xlabel('f (Hz)')
ylabel('Amplitude (Unit)')