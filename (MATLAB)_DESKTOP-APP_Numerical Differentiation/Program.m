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

% Last Modified by GUIDE v2.5 23-Apr-2020 15:08:27

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

global choice
choice = 1;
system('Matlab.scr&');


% --- Outputs from this function are returned to the command line.
function varargout = Program_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function editEquation_Callback(hObject, eventdata, handles)
% hObject    handle to editEquation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editEquation as text
%        str2double(get(hObject,'String')) returns contents of editEquation as a double


% --- Executes during object creation, after setting all properties.
function editEquation_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editEquation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editXi_Callback(hObject, eventdata, handles)
% hObject    handle to editXi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editXi as text
%        str2double(get(hObject,'String')) returns contents of editXi as a double


% --- Executes during object creation, after setting all properties.
function editXi_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editXi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in editH.
function editH_Callback(hObject, eventdata, handles)
% hObject    handle to editH (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function editH_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editH (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes on button press in pbCompute.
function pbCompute_Callback(hObject, eventdata, handles)
global choice
format long g;
% hObject    handle to pbCompute (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%Truncated Version
str = "@(x)"+getObj('editEquation','String');
f = str2func(str);
xi = str2num(getObj('editXi','String'));
h = 0.125

%Forward Finite Divided Difference
if choice == 1
    hcol = [];
    xicol = [];
    fxicol = [];
    fxiplus1col = [];
    n = [];
    initial = 1;
    while 1
        hcol = [hcol;initial];
        xicol = [xicol;xi];
        fxicol = [fxicol;f(xi)];
        initial = initial/2;
        if initial == h/2
            break
        end
    end
    for i=1:numel(hcol) n=[n;2]; end
    xiplus1 = xicol+1*hcol;
    for i = 1:numel(hcol)
        fxiplus1col = [fxiplus1col;f(xiplus1(i))];
    end
    fprimex1 = (fxiplus1col-fxicol)./hcol;
    setObj('uitable1','Data',[hcol,xicol,fxicol,xiplus1,fxiplus1col,fprimex1]);
    
    %Richardson Extrapolation
    k = 2;
    oh2 = [];
    for i = 1:numel(hcol)+1-k
        oh2 = [oh2;fprimex1(i+1)+(fprimex1(i+1)-fprimex1(i))/(2^k-1)];
    end
    oh2 = [oh2;zeros(numel(hcol)-numel(oh2),1)]
    
    k = 3;
    oh4 = [];
    for i = 1:numel(hcol)+1-k
        oh4 = [oh4;oh2(i+1)+(oh2(i+1)-oh2(i))/(2^k-1)];
    end
    oh4 = [oh4;zeros(numel(hcol)-numel(oh4),1)];
    
    k = 4;
    oh6 = [];
    for i = 1:numel(hcol)+1-k
        oh6 = [oh6;oh4(i+1)+(oh4(i+1)-oh4(i))/(2^k-1)];
    end
    oh6 = [oh6;zeros(numel(hcol)-numel(oh6),1)];
    setObj('uitable2','Data',[n,hcol,fprimex1,oh2,oh4,oh6]);
    
%Backward Finite Divided Difference
elseif choice == 2
    hcol = [];
    xicol = [];
    fxicol = [];
    fximinus1col = [];
    n = [];
    initial = 1;
    while 1
        hcol = [hcol;initial];
        xicol = [xicol;xi];
        fxicol = [fxicol;f(xi)];
        initial = initial/2;
        if initial == h/2
            break
        end
    end
    for i=1:numel(hcol) n=[n;2]; end
    ximinus1 = xicol-1*hcol;
    for i = 1:numel(hcol)
        fximinus1col = [fximinus1col;f(ximinus1(i))];
    end
    fprimex1 = (fxicol-fximinus1col)./hcol;
    setObj('uitable3','Data',[hcol,xicol,fxicol,ximinus1,fximinus1col,fprimex1]);
    
    %Richardson Extrapolation
    k = 2;
    oh2 = [];
    for i = 1:numel(hcol)+1-k
        oh2 = [oh2;fprimex1(i+1)+(fprimex1(i+1)-fprimex1(i))/(2^k-1)];
    end
    oh2 = [oh2;zeros(numel(hcol)-numel(oh2),1)]
    
    k = 3;
    oh4 = [];
    for i = 1:numel(hcol)+1-k
        oh4 = [oh4;oh2(i+1)+(oh2(i+1)-oh2(i))/(2^k-1)];
    end
    oh4 = [oh4;zeros(numel(hcol)-numel(oh4),1)]
    
    k = 4;
    oh6 = [];
    for i = 1:numel(hcol)+1-k
        oh6 = [oh6;oh4(i+1)+(oh4(i+1)-oh4(i))/(2^k-1)];
    end
    oh6 = [oh6;zeros(numel(hcol)-numel(oh6),1)]
    setObj('uitable4','Data',[n,hcol,fprimex1,oh2,oh4,oh6]);
    
%Center Finite Divided Difference
elseif choice == 3
    hcol = [];
    xicol = [];
    fxicol = [];
    fximinus1col = [];
    fxiplus1col = [];
    n = [];
    initial = 1;
    while 1
        hcol = [hcol;initial];
        xicol = [xicol;xi];
        fxicol = [fxicol;f(xi)];
        initial = initial/2;
        if initial == h/2
            break
        end
    end
    for i=1:numel(hcol) n=[n;2]; end
    ximinus1 = xicol-1*hcol;
    xiplus1 = xicol+1*hcol;
    for i = 1:numel(hcol)
        fximinus1col = [fximinus1col;f(ximinus1(i))];
        fxiplus1col = [fxiplus1col;f(xiplus1(i))];
    end
    fprimex1 = ((fxiplus1col-fximinus1col)./hcol)*0.5;
    setObj('uitable6','Data',[hcol,ximinus1,xiplus1,fximinus1col,fxiplus1col,fprimex1]);
    
    %Richardson Extrapolation
    k = 2;
    oh2 = [];
    for i = 1:numel(hcol)+1-k
        oh2 = [oh2;fprimex1(i+1)+(fprimex1(i+1)-fprimex1(i))/(2^k-1)];
    end
    oh2 = [oh2;zeros(numel(hcol)-numel(oh2),1)]
    
    k = 3;
    oh4 = [];
    for i = 1:numel(hcol)+1-k
        oh4 = [oh4;oh2(i+1)+(oh2(i+1)-oh2(i))/(2^k-1)];
    end
    oh4 = [oh4;zeros(numel(hcol)-numel(oh4),1)]
    
    k = 4;
    oh6 = [];
    for i = 1:numel(hcol)+1-k
        oh6 = [oh6;oh4(i+1)+(oh4(i+1)-oh4(i))/(2^k-1)];
    end
    oh6 = [oh6;zeros(numel(hcol)-numel(oh6),1)]
    setObj('uitable5','Data',[n,hcol,fprimex1,oh2,oh4,oh6]);
end

% --- Executes on button press in pbFF.
function pbFF_Callback(hObject, eventdata, handles)
% hObject    handle to pbFF (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choice
choice = 1;
setObj("uipanel1","visible","on");
setObj("uipanel2","visible","off");
setObj("uipanel3","visible","off");


% --- Executes on button press in pbBF.
function pbBF_Callback(hObject, eventdata, handles)
% hObject    handle to pbBF (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choice
choice = 2;
setObj("uipanel1","visible","off");
setObj("uipanel2","visible","on");
setObj("uipanel3","visible","off");


% --- Executes on button press in pbCF.
function pbCF_Callback(hObject, eventdata, handles)
% hObject    handle to pbCF (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choice
choice = 3;
setObj("uipanel1","visible","off");
setObj("uipanel2","visible","off");
setObj("uipanel3","visible","on");
