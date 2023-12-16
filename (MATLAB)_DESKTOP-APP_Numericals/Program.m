function varargout = Program(varargin)
% PROGRAM MATLAB code for Program.fig
%      PROGRAM, by itself, creates a new PROGRAM or raises the existing
%      singleton*.
%
%      H = PROGRAM returns the handle to a new PROGRAM or the handle to
%      the existing singleton*.
%
%      PROGRAM('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in PROGRAM.M with the given input arguments.
%
%      PROGRAM('Property','Value',...) creates a new PROGRAM or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Program_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Program_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Program

% Last Modified by GUIDE v2.5 13-Apr-2020 16:17:55

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Program_OpeningFcn, ...
                   'gui_OutputFcn',  @Program_OutputFcn, ...
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

function setObj(text1,text2,text3)
    set(findobj(0, 'tag', text1), text2, text3);

function x = getObj(text1,text2)
    x = get(findobj(0, 'tag', text1), text2);

% --- Executes just before Program is made visible.
function Program_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Program (see VARARGIN)

% Choose default command line output for Program
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Program wait for user response (see UIRESUME)
% uiwait(handles.figure1);
% Hide all panels
setObj('uipanel1','visible','off')
setObj('uipanel2','visible','off')
setObj('goBackBttn','visible','off')
% Set background
ah = axes('unit','normalized','position',[0 0 1 1]);
bg = imread('Background.png'); imagesc(bg);
set(ah, 'handlevisibility', 'off', 'visible', 'off');
uistack(ah, 'bottom');
% --- Outputs from this function are returned to the command line.
function varargout = Program_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
setObj('uipanel1','visible','on')
setObj('pushbutton1','visible','off')
setObj('pushbutton2','visible','off')
setObj('goBackBttn','visible','on')

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
setObj('uipanel2','visible','on')
setObj('pushbutton1','visible','off')
setObj('pushbutton2','visible','off')
setObj('goBackBttn','visible','on')

function rfmEquation_Callback(hObject, eventdata, handles)
% hObject    handle to rfmEquation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of rfmEquation as text
%        str2double(get(hObject,'String')) returns contents of rfmEquation as a double


% --- Executes during object creation, after setting all properties.
function rfmEquation_CreateFcn(hObject, eventdata, handles)
% hObject    handle to rfmEquation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function rfmx0_Callback(hObject, eventdata, handles)
% hObject    handle to rfmx0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of rfmx0 as text
%        str2double(get(hObject,'String')) returns contents of rfmx0 as a double


% --- Executes during object creation, after setting all properties.
function rfmx0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to rfmx0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function rfmx1_Callback(hObject, eventdata, handles)
% hObject    handle to rfmx1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of rfmx1 as text
%        str2double(get(hObject,'String')) returns contents of rfmx1 as a double


% --- Executes during object creation, after setting all properties.
function rfmx1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to rfmx1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in rfmSolve.
function rfmSolve_Callback(hObject, eventdata, handles)
% hObject    handle to rfmSolve (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str = "@(x)"+getObj('rfmEquation','String');
f = str2func(str);
x0 = str2double(getObj('rfmx0','String'));
x1 = str2double(getObj('rfmx1','String'));
fx0 = f(x0);
fx1 = f(x1);
err = str2double(getObj('rfmError','String'));
error = 1;
rows = {};
if (fx0>0 && fx1>0) || (fx0<0 && fx1<0)
    setObj("rfmRoot","String","Root: Error initial conditions");
else
    x2 = x0-(fx0*(x1-x0)/(fx1-fx0));
    fx2 = f(x2);
    rows = [rows;{x0, x1, x2, fx0, fx1, fx2, 'CONTINUE'}];
    while error > err
        fx0 = f(x0);
        fx1 = f(x1);
        x2 = x0-(fx0*(x1-x0)/(fx1-fx0));
        fx2 = f(x2);
        prevx2 = x2;
        if (fx2>0)
            x1 = x2;
            x0 = x0;
            fx0 = f(x0);
            fx1 = f(x1);
            x2 = x0-(fx0*(x1-x0)/(fx1-fx0));
            fx2 = f(x2);            
        elseif (fx2<0)
            x0 = x2;
            x1 = x1;
            fx0 = f(x0);
            fx1 = f(x1);
            x2 = x0-(fx0*(x1-x0)/(fx1-fx0));
            fx2 = f(x2);
        end
        error = abs(prevx2 - x2);
        if error > err
            rows = [rows;{x0, x1, x2, fx0, fx1, fx2, 'CONTINUE'}];
        elseif error < err || error == err
            rows = [rows;{x0, x1, x2, fx0, fx1, fx2, 'TERMINATE'}];
        end
    end
    setObj('rfmTable','Data',rows);
    setObj('rfmRoot','String',"Root: " + x2)
end

% --- Executes on button press in goBackBttn.
function goBackBttn_Callback(hObject, eventdata, handles)
% hObject    handle to goBackBttn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
setObj('uipanel1','visible','off')
setObj('uipanel2','visible','off')
setObj('pushbutton1','visible','on')
setObj('pushbutton2','visible','on')
setObj('goBackBttn','visible','off')



function rfmError_Callback(hObject, eventdata, handles)
% hObject    handle to rfmError (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of rfmError as text
%        str2double(get(hObject,'String')) returns contents of rfmError as a double


% --- Executes during object creation, after setting all properties.
function rfmError_CreateFcn(hObject, eventdata, handles)
% hObject    handle to rfmError (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bmEquation_Callback(hObject, eventdata, handles)
% hObject    handle to bmEquation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bmEquation as text
%        str2double(get(hObject,'String')) returns contents of bmEquation as a double


% --- Executes during object creation, after setting all properties.
function bmEquation_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bmEquation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bmx0_Callback(hObject, eventdata, handles)
% hObject    handle to bmx0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bmx0 as text
%        str2double(get(hObject,'String')) returns contents of bmx0 as a double


% --- Executes during object creation, after setting all properties.
function bmx0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bmx0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bmx1_Callback(hObject, eventdata, handles)
% hObject    handle to bmx1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bmx1 as text
%        str2double(get(hObject,'String')) returns contents of bmx1 as a double


% --- Executes during object creation, after setting all properties.
function bmx1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bmx1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in bmSolve.
function bmSolve_Callback(hObject, eventdata, handles)
% hObject    handle to bmSolve (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str = "@(x)"+getObj('bmEquation','String');
f = str2func(str);
x0 = str2double(getObj('bmx0','String'));
x1 = str2double(getObj('bmx1','String'));
fx0 = f(x0);
fx1 = f(x1);
err = str2double(getObj('bmerror','String'));
error = 1;
rows = {};
if (fx0>0 && fx1>0) || (fx0<0 && fx1<0)
    setObj("bmRoot","String","Root: Error initial conditions");
else
    x2 = (x0+x1)/2;
    fx2 = f(x2);
    rows = [rows;{x0, x1, x2, fx0, fx1, fx2, 'CONTINUE'}];
    while error > err
        fx0 = f(x0);
        fx1 = f(x1);
        x2 = (x0+x1)/2;
        fx2 = f(x2);
        prevx2 = x2;
        if fx2*fx1>0
            x1 = x2;
            x0 = x0;
            fx0 = f(x0);
            fx1 = f(x1);
            x2 = (x0+x1)/2;
            fx2 = f(x2);          
        elseif fx2*fx0>0
            x0 = x2;
            x1 = x1;
            fx0 = f(x0);
            fx1 = f(x1);
            x2 = (x0+x1)/2;
            fx2 = f(x2);
        end
        error = abs(prevx2 - x2);
        if error > err
            rows = [rows;{x0, x1, x2, fx0, fx1, fx2, 'CONTINUE'}];
        elseif error < err || error == err
            rows = [rows;{x0, x1, x2, fx0, fx1, fx2, 'TERMINATE'}];
        end
    end
    setObj('bmTable','Data',rows);
    setObj('bmRoot','String',"Root: " + x2)
end


function bmerror_Callback(hObject, eventdata, handles)
% hObject    handle to bmerror (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bmerror as text
%        str2double(get(hObject,'String')) returns contents of bmerror as a double


% --- Executes during object creation, after setting all properties.
function bmerror_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bmerror (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
