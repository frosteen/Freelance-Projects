function varargout = CONFIDENCEINTERVAL(varargin)
% CONFIDENCEINTERVAL MATLAB code for CONFIDENCEINTERVAL.fig
%      CONFIDENCEINTERVAL, by itself, creates a new CONFIDENCEINTERVAL or raises the existing
%      singleton*.
%
%      H = CONFIDENCEINTERVAL returns the handle to a new CONFIDENCEINTERVAL or the handle to
%      the existing singleton*.
%
%      CONFIDENCEINTERVAL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CONFIDENCEINTERVAL.M with the given input arguments.
%
%      CONFIDENCEINTERVAL('Property','Value',...) creates a new CONFIDENCEINTERVAL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before CONFIDENCEINTERVAL_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to CONFIDENCEINTERVAL_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help CONFIDENCEINTERVAL

% Last Modified by GUIDE v2.5 03-Apr-2019 12:45:42

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @CONFIDENCEINTERVAL_OpeningFcn, ...
                   'gui_OutputFcn',  @CONFIDENCEINTERVAL_OutputFcn, ...
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


% --- Executes just before CONFIDENCEINTERVAL is made visible.
function CONFIDENCEINTERVAL_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to CONFIDENCEINTERVAL (see VARARGIN)

% Choose default command line output for CONFIDENCEINTERVAL
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes CONFIDENCEINTERVAL wait for user response (see UIRESUME)
% uiwait(handles.figure1);

ah = axes('unit','normalized','position',[0 0 1 1]);
bg = imread('bg.jpg'); imagesc(bg);
set(ah, 'handlevisibility', 'off', 'visible', 'off');
uistack(ah, 'bottom');


% --- Outputs from this function are returned to the command line.
function varargout = CONFIDENCEINTERVAL_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

%EXTRA USEFUL FUNCTIONS
function setString(handles, text)
set(findobj(0, 'tag', handles), 'String', text);

function v = getVal(handles)
v = str2double(get(findobj(0, 'tag', handles), 'String'));

function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
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



function edit3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3 as text
%        str2double(get(hObject,'String')) returns contents of edit3 as a double


% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
sigma = getVal('edit1');
n = getVal('edit2');
mu = getVal('edit3');
z = getVal('edit4');
E = z*(sigma/sqrt(n));
lower = mu - E;
upper = mu + E;
setString('text5', 'INTERVAL: ('+string(lower)+', '+string(upper)+')')
x = [-n:.1:n];
y = normpdf(x,0,sigma);

%GRAPHING
alpha = getVal('edit5');          % significance level
cutoff1 = norminv(alpha, mu, sigma);
cutoff2 = norminv(1-alpha, mu, sigma);
x = [linspace(mu-4*sigma,cutoff1), ...
    linspace(cutoff1,cutoff2), ...
    linspace(cutoff2,mu+4*sigma)];
y = normpdf(x, mu, sigma);
plot(x,y)

xlo = [x(x<=cutoff1) cutoff1];
ylo = [y(x<=cutoff1) 0];
patch(xlo, ylo, 'b')

xhi = [cutoff2 x(x>=cutoff2)];
yhi = [0 y(x>=cutoff2)];
patch(xhi, yhi, 'b')

xlabel('Sample');
set(gca,'yticklabel',[])
set(gca,'ytick',[])

function edit4_Callback(hObject, eventdata, handles)
% hObject    handle to edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit4 as text
%        str2double(get(hObject,'String')) returns contents of edit4 as a double


% --- Executes during object creation, after setting all properties.
function edit4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit5_Callback(hObject, eventdata, handles)
% hObject    handle to edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit5 as text
%        str2double(get(hObject,'String')) returns contents of edit5 as a double


% --- Executes during object creation, after setting all properties.
function edit5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
