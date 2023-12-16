
function varargout = ControlGUI(varargin)
% CONTROLGUI MATLAB code for ControlGUI.fig
%      CONTROLGUI, by itself, creates a new CONTROLGUI or raises the existing
%      singleton*.
%
%      H = CONTROLGUI returns the handle to a new CONTROLGUI or the handle to
%      the existing singleton*.
%
%      CONTROLGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CONTROLGUI.M with the given input arguments.
%
%      CONTROLGUI('Property','Value',...) creates a new CONTROLGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ControlGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ControlGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ControlGUI

% Last Modified by GUIDE v2.5 04-Jan-2019 12:47:33

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ControlGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @ControlGUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before ControlGUI is made visible.
function ControlGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ControlGUI (see VARARGIN)

% Choose default command line output for ControlGUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ControlGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);
clear all;
if ~isempty(instrfind)
    fclose(instrfind);
    delete (instrfind);
end
global S;
S = serial(seriallist);
fclose(S);
fopen(S);

% --- Outputs from this function are returned to the command line.


function graph(hObject, eventdata, handles, x, y)
bar(y)
set(handles.axesHumidity,'xticklabel',x.')
set(handles.axesHumidity,'XTickLabelRotation',45)
ylabel('Humidity (%)');


function doReading(hObject, eventdata, handles)
global isReading;
global mode;
global humidityVal;
global S;
isReading = true;
mode = 1;
counter = 0;
y = [];
x = [];
maxData = 20; %change the maximum data to shift
while isReading == true
   humidityVal = fscanf(S);
   set(findobj(0, 'tag', "textHumidityValue"), 'String', humidityVal);
   y = [y, uint8(str2double(humidityVal))];
   c = fix(clock);
   x = [x, c(4)+":"+c(5)+":"+c(6)];
   if length(y) > maxData
       y(1) = [];
       x(1) = [];
   end
   if mode == 1
       if str2double(get(findobj(0, 'tag', "editValue"), 'String')) > str2double(humidityVal)
           fprintf(S, '%s', 'a');
           pause(1)
           fprintf(S, '%s', 'b');
           pause(str2double(get(findobj(0, 'tag', "editTime"), 'String')));
       end
       graph(hObject, eventdata, handles, x, y);
   else
       graph(hObject, eventdata, handles, x, y);
   end
   pause(1);
   counter = counter + 1;
end

function varargout = ControlGUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
doReading(hObject, eventdata, handles)

% --- Executes on button press in pushbuttonAutomatic.
function pushbuttonAutomatic_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonAutomatic (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global mode;
mode = 1;
global isUsing;
isUsing = false;
set(findobj(0, 'tag', "pushbuttonSpray"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonOn"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonOff"), 'Enable', 'off');
set(findobj(0, 'tag', "editValue"), 'Enable', 'on')
set(findobj(0, 'tag', "textStatus"), 'String', 'Automatic');

% --- Executes on button press in pushbuttonManual.
function pushbuttonManual_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonManual (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global mode;
mode = 2;
global isUsing;
isUsing = false;
set(findobj(0, 'tag', "editValue"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonSpray"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonOn"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonOff"), 'Enable', 'on');
set(findobj(0, 'tag', "textStatus"), 'String', 'Manual');



% --- Executes on button press in pushbuttonOn.
function pushbuttonOn_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonOn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global mode;
global S
global isUsing;
isUsing = true;
set(findobj(0, 'tag', "pushbuttonOn"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonOff"), 'Enable', 'on');
while mode==2 && isUsing==true
    fprintf(S, '%s', 'a');
    pause(1)
    fprintf(S, '%s', 'b');
    pause(3);
end

% --- Executes on button press in pushbuttonOff.
function pushbuttonOff_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonOff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global mode;
global isUsing;
set(findobj(0, 'tag', "pushbuttonOn"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonOff"), 'Enable', 'off');
if mode==2 && isUsing == true
    isUsing = false;
end
% --- Executes on button press in pushbuttonSpray.
function pushbuttonSpray_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonSpray (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global S;
global isUsing;
isUsing = false;
set(findobj(0, 'tag', "pushbuttonSpray"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonOn"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonOff"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonManual"), 'Enable', 'off');
set(findobj(0, 'tag', "pushbuttonAutomatic"), 'Enable', 'off');
fprintf(S, '%s', 'a');
pause(1)
fprintf(S, '%s', 'b');
set(findobj(0, 'tag', "pushbuttonSpray"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonSpray"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonOn"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonOff"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonManual"), 'Enable', 'on');
set(findobj(0, 'tag', "pushbuttonAutomatic"), 'Enable', 'on');


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
delete(hObject);
global isReading;
isReading = false;
global S
fprintf(S, '%s', 'b');
fclose(S);



function editValue_Callback(hObject, eventdata, handles)
% hObject    handle to editValue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editValue as text
%        str2double(get(hObject,'String')) returns contents of editValue as a double


% --- Executes during object creation, after setting all properties.
function editValue_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editValue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editTime_Callback(hObject, eventdata, handles)
% hObject    handle to editTime (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editTime as text
%        str2double(get(hObject,'String')) returns contents of editTime as a double


% --- Executes during object creation, after setting all properties.
function editTime_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editTime (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
