repeat = 3; %how many 
recordTime = 3; %how long is the record
name=input('Enter a number for this word: ', 's'); %input word
name = string(name); %convert to string
disp('Say something...');
doRecord(name, recordTime); %record voice function
counter = 0; %set counter to zero

%repetition
while counter < repeat
    disp('Again.')
    doRecord(name, recordTime)
    counter = counter + 1;
end

disp('Voice successfully registered.') %voice registered. program terminates.

%record function
