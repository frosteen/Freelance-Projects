clear all; close all; clc;
recorder = audiorecorder(16000,8,2); %set audio recorder to 16000 sampling, 8-bit, 2 channels
disp('Say something...');
recordblocking(recorder, 3); %record upto 3s
data=getaudiodata(recorder); %convert audio to data
load database %load database file in the same folder, must exist first
f=FindPitch(data); %find pitch again.

%% Classify
D=[];
for i=1:size(F,1) 
    d=sum(abs(F(i)-f)); %subtract both pitch
    D=[D d]; %add to the array
end
%% Smallest distance
sm=inf;
ind=-1;
for i=1:length(D)
    if(D(i)<sm) %check if it is the smallest
        sm=D(i); %set sm to previous D(i)
        ind=i; %know the position of word in the array
    end
end
detected_class=C(ind); %word found in database
disp('The detected word is: ' + string(detected_class)); %output the word
