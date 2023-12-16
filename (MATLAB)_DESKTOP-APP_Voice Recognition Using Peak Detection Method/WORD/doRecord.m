function []=doRecord(name, recordTime)
    recorder = audiorecorder(16000,8,2); %set audio recorder to 16000 sampling, 8-bit, 2 channels
    recordblocking(recorder, recordTime); %do the recording
    data=getaudiodata(recorder); %convert audio to data
    f=FindPitch(data); %find pitch function
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