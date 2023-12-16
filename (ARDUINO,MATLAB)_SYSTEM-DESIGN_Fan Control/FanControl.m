function varargout = FanControl(varargin)
% FANCONTROL MATLAB code for FanControl.fig
%      FANCONTROL, by itself, creates a new FANCONTROL or raises the existing
%      singleton*.
%
%      H = FANCONTROL returns the handle to a new FANCONTROL or the handle to
%      the existing singleton*.
%
%      FANCONTROL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FANCONTROL.M with the given input arguments.
%
%      FANCONTROL('Property','Value',...) creates a new FANCONTROL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before FanControl_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to FanControl_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help FanControl

% Last Modified by GUIDE v2.5 19-Jan-2019 01:56:52

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @FanControl_OpeningFcn, ...
                   'gui_OutputFcn',  @FanControl_OutputFcn, ...
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


% --- Executes just before FanControl is made visible.
function FanControl_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to FanControl (see VARARGIN)

% Choose default command line output for FanControl
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes FanControl wait for user response (see UIRESUME)
% uiwait(handles.figure1);




function setObj(text1,text2,text3)
set(findobj(0, 'tag', text1), text2, text3);

function x=getObj(text1,text2)
x = get(findobj(0, 'tag', text1), text2);

function doReading()
global s;
global mode;
x = []; y = []; y1 = [];
maxData = 50; %change the maximum data to shift
counter = 0;
while mode == 'A' || mode == 'B'
   values = strsplit(fscanf(s),';');
   setObj('text6','string', 'Temperature: '+string(values{1})+' *C');
   setObj('text5','string', 'Fan Speed: '+string(str2num(values{2}))+' %');
   if str2num(values{2}) <= 0
    setObj('text8','string', 'Status: Off');
   else
    setObj('text8','string', 'Status: On'); 
   end
   y = [y, str2num(values{1})];
   x = [x, counter];
   y1 = [y1, str2num(values{2})];
   if length(y) > maxData
       y(1) = [];
       y1(1) = [];
       x(1) = [];
   end
   plot(x,y,x,y1)
   xlabel('Time (seconds)');
   legend({'Temperatre (*C)','Fan Speed (%)'},'Location','southwest')
   counter = counter + 1;
   pause(1);
 end
% --- Outputs from this function are returned to the command line.
function varargout = FanControl_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

clear all;
if ~isempty(instrfind)
    fclose(instrfind);
    delete (instrfind);
end
global s;
global mode;
mode = 'A';
s = serial(seriallist);
fclose(s);
fopen(s);
doReading();

% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global mode;
mode = 'A';
setObj('pushbutton1', 'enable', 'off');
setObj('pushbutton2', 'enable', 'on');
setObj('edit2', 'enable', 'off');
setObj('pushbutton3', 'enable', 'off');
global s;
fprintf(s, 'A');

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global mode;
mode = 'B';
setObj('pushbutton2', 'enable', 'off');
setObj('pushbutton1', 'enable', 'on');
setObj('edit2', 'enable', 'on');
setObj('pushbutton3', 'enable', 'on');


% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global s;
global mode;
if mode == 'B'
    fprintf(s,'%s','B'+string(getObj('edit2','string')));
end



function edit2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2 as text
%        str2double(get(hObject,'String')) returns contents of edit2 as a double


% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
delete(hObject);
global s;
global mode;
mode = 'C';
fprintf(s, '%s', 'B0');
fclose(s);
