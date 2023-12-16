function varargout = DifferentialEquations(varargin)
% DIFFERENTIALEQUATIONS MATLAB code for DifferentialEquations.fig
%      DIFFERENTIALEQUATIONS, by itself, creates a new DIFFERENTIALEQUATIONS or raises the existing
%      singleton*.
%
%      H = DIFFERENTIALEQUATIONS returns the handle to a new DIFFERENTIALEQUATIONS or the handle to
%      the existing singleton*.
%
%      DIFFERENTIALEQUATIONS('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DIFFERENTIALEQUATIONS.M with the given input arguments.
%
%      DIFFERENTIALEQUATIONS('Property','Value',...) creates a new DIFFERENTIALEQUATIONS or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before DifferentialEquations_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to DifferentialEquations_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help DifferentialEquations

% Last Modified by GUIDE v2.5 13-Jan-2019 01:20:13

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @DifferentialEquations_OpeningFcn, ...
                   'gui_OutputFcn',  @DifferentialEquations_OutputFcn, ...
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


function tabMode(handles, num)

if num == 1
    set(findobj(0, 'tag', 'uipanel1'), 'Visible', 'On');
    set(findobj(0, 'tag', 'uipanel2'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel3'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel4'), 'Visible', 'Off');
elseif num == 2
    set(findobj(0, 'tag', 'uipanel1'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel2'), 'Visible', 'On');
    set(findobj(0, 'tag', 'uipanel3'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel4'), 'Visible', 'Off');
elseif num == 3
    set(findobj(0, 'tag', 'uipanel1'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel2'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel3'), 'Visible', 'On');
    set(findobj(0, 'tag', 'uipanel4'), 'Visible', 'Off');
elseif num ==4
    set(findobj(0, 'tag', 'uipanel1'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel2'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel3'), 'Visible', 'Off');
    set(findobj(0, 'tag', 'uipanel4'), 'Visible', 'on');
end

% --- Executes just before DifferentialEquations is made visible.
function DifferentialEquations_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to DifferentialEquations (see VARARGIN)

% Choose default command line output for DifferentialEquations
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes DifferentialEquations wait for user response (see UIRESUME)
% uiwait(findobj(0, 'tag', 'figure1);

ah = axes('unit','normalized','position',[0 0 1 1]);
bg = imread('bg.jpg'); imagesc(bg);
set(ah, 'handlevisibility', 'off', 'visible', 'off');
uistack(ah, 'bottom');

tabMode(handles, 1);

% --- Outputs from this function are returned to the command line.
function varargout = DifferentialEquations_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
clc;


function doReset()
format long;
clc;



% --- Executes on button press in pushbuttonTab1.
function pushbuttonTab1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonTab1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% --- Executes on button press in pushbuttonTab2.
tabMode(handles,1)

function pushbuttonTab2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonTab2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
tabMode(handles,2)


% --- Executes on button press in pushbuttonTab3.
function pushbuttonTab3_Callback(~, eventdata, handles)
% hObject    handle to pushbuttonTab3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
tabMode(handles,3)


% --- Executes on button press in pushbuttonTab4.
function pushbuttonTab4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonTab4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
tabMode(handles,4)



function edityequation_Callback(hObject, eventdata, handles)
% hObject    handle to edityequation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edityequation as text
%        str2double(get(hObject,'String')) returns contents of edityequation as a double


% --- Executes during object creation, after setting all properties.
function edityequation_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edityequation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edity0_Callback(hObject, eventdata, handles)
% hObject    handle to edity0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edity0 as text
%        str2double(get(hObject,'String')) returns contents of edity0 as a double


% --- Executes during object creation, after setting all properties.
function edity0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edity0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editt0_Callback(hObject, eventdata, handles)
% hObject    handle to editt0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editt0 as text
%        str2double(get(hObject,'String')) returns contents of editt0 as a double


% --- Executes during object creation, after setting all properties.
function editt0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editt0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edittf_Callback(hObject, eventdata, handles)
% hObject    handle to edittf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edittf as text
%        str2double(get(hObject,'String')) returns contents of edittf as a double


% --- Executes during object creation, after setting all properties.
function edittf_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edittf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edith_Callback(hObject, eventdata, handles)
% hObject    handle to edith (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edith as text
%        str2double(get(hObject,'String')) returns contents of edith as a double


% --- Executes during object creation, after setting all properties.
function edith_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edith (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonECalculate.
function pushbuttonECalculate_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonECalculate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
doReset();

m = str2num(get(findobj(0, 'tag', 'edity0'),'String'));
r = str2num(get(findobj(0, 'tag', 'editt0'),'String'));
vesc = sqrt((2*(6.67*10^-11)*m)/r);
data = [];
h = 1000;
for x = r/10:h:r
   data = [data, sqrt((2*(6.67*10^-11)*m)/x)]; 
end
plot(r/10:h:r,  data);
xlabel('r (radius)');
ylabel('Vesc');
set(findobj(0, 'tag', 'text65'), 'String', sprintf('%.6f',vesc));



function editp0_Callback(hObject, eventdata, handles)
% hObject    handle to editp0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editp0 as text
%        str2double(get(hObject,'String')) returns contents of editp0 as a double


% --- Executes during object creation, after setting all properties.
function editp0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editp0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editk_Callback(hObject, eventdata, handles)
% hObject    handle to editk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editk as text
%        str2double(get(hObject,'String')) returns contents of editk as a double


% --- Executes during object creation, after setting all properties.
function editk_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editr_Callback(hObject, eventdata, handles)
% hObject    handle to editr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editr as text
%        str2double(get(hObject,'String')) returns contents of editr as a double


% --- Executes during object creation, after setting all properties.
function editr_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editlt_Callback(hObject, eventdata, handles)
% hObject    handle to editlt (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editlt as text
%        str2double(get(hObject,'String')) returns contents of editlt as a double


% --- Executes during object creation, after setting all properties.
function editlt_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editlt (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonlcalculate.
function pushbuttonlcalculate_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonlcalculate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
doReset();
p0 = str2double(get(findobj(0, 'tag', 'editp0'),'String'));
k = str2double(get(findobj(0, 'tag', 'editk'),'String'));
r = str2double(get(findobj(0, 'tag', 'editr'),'String'));
t = str2double(get(findobj(0, 'tag', 'editlt'),'String')) ;
p = (p0*k)/(p0+(k-p0)*exp(-r*t));
data = [];
h = 0.001;
for x = 0:h:20
   data = [data,(p0*k)/(p0+(k-p0)*exp(-r*(x)))]; 
end
axes(findobj(0, 'tag', 'axeslogistic'))
plot(0:h:20,  data);
xlabel('t');
ylabel('P(t)');
set(findobj(0, 'tag', 'texpt'), 'String', "P = "+sprintf('%.6f',p));



function editm_Callback(hObject, eventdata, handles)
% hObject    handle to editm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editm as text
%        str2double(get(hObject,'String')) returns contents of editm as a double


% --- Executes during object creation, after setting all properties.
function editm_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonncalculate.
function pushbuttonncalculate_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonncalculate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
m = str2double(get(findobj(0, 'tag', 'editm'),'String'));
v0 = str2double(get(findobj(0, 'tag', 'editv0'),'String'));
v = str2double(get(findobj(0, 'tag', 'editv'),'String'));
t0 = str2double(get(findobj(0, 'tag', 'editnt0'),'String'));
t = str2double(get(findobj(0, 'tag', 'editnt'),'String'));
F = m*((v-v0)/(t-t0));
data = [];
data1 = [];
h = 0.1;
for x = t0:h:20
   data = [data, m*((v-v0)/(x-t0))]; 
end
for x = t0:h:20
   data1 = [data1,((v-v0)/(x-t0))];
end
axes(findobj(0, 'tag', 'axesnewtons'))
plot(t0:h:20,  data);
xlabel('Time (sec)');
ylabel('Force (N)');
set(findobj(0, 'tag', 'textf'), 'String', "F = "+sprintf('%.6f',F));



function editct_Callback(hObject, eventdata, handles)
% hObject    handle to editct (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editct as text
%        str2double(get(hObject,'String')) returns contents of editct as a double


% --- Executes during object creation, after setting all properties.
function editct_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editct (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editck_Callback(hObject, eventdata, handles)
% hObject    handle to editck (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editck as text
%        str2double(get(hObject,'String')) returns contents of editck as a double


% --- Executes during object creation, after setting all properties.
function editck_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editck (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit69r_Callback(hObject, eventdata, handles)
% hObject    handle to edit69r (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit69r as text
%        str2double(get(hObject,'String')) returns contents of edit69r as a double


% --- Executes during object creation, after setting all properties.
function edit69r_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit69r (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit69m_Callback(hObject, eventdata, handles)
% hObject    handle to edit69m (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit69m as text
%        str2double(get(hObject,'String')) returns contents of edit69m as a double


% --- Executes during object creation, after setting all properties.
function edit69m_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit69m (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonccalculate.
function pushbuttonccalculate_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonccalculate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
doReset();
T0 = str2double(get(findobj(0, 'tag', 'edittemp0'), 'String'));
Ts = str2double(get(findobj(0, 'tag', 'edittemps'), 'String'));
k = str2double(get(findobj(0, 'tag', 'editck'), 'String'));
t = str2double(get(findobj(0, 'tag', 'editct'), 'String'));
T = Ts + (T0 - Ts)*exp(-k*t);
data = [];
h = 0.001;
for x = 0:h:20
   data = [data, Ts + (T0 - Ts)*exp(-k*x)]; 
end
axes(findobj(0, 'tag', 'axescooling1'));
plot(0:h:20,  data);
xlabel('t (s)');
ylabel('T(t) Kelvinn');
set(findobj(0, 'tag', 'texttemp'), 'String', "T = "+sprintf('%.6f',T));
