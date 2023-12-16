clear all; close all; clc; %Clear some data
global name recordTime;
repeat = 0; %how many 
recordTime = 3; %how long is the record
name=input('Enter the word: ', 's'); %input word
name = string(name); %convert to string
disp('Say something...');
doRecord(); %record voice function
counter = 0; %set counter to zero

%repetition
while counter < repeat
    disp('Again.')
    doRecord()
    counter = counter + 1;
end

disp('Voice successfully registered.') %voice registered. program terminates.

%record function
function doRecord()
    global name recordTime;
    recorder = audiorecorder(16000,8,2); %set audio recorder to 16000 sampling, 8-bit, 2 channels
    recordblocking(recorder, recordTime); %do the recording
    data=getaudiodata(recorder); %convert audio to data
    f=FindPitch(data); %find pitch function
    plot(data)
    %try & catch block
    %try write data if database exist
    try
        load database
        F=[F;f];
        C=[C;name];
        save database F C %save data
    %if missing then create a database file
    catch
        F=f;
        C=name;
        save database F C %save data
    end
end