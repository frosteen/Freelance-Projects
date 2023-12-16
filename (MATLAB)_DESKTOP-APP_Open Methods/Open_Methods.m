function varargout = Open_Methods(varargin)
% OPEN_METHODS MATLAB code for Open_Methods.fig
%      OPEN_METHODS, by itself, creates a new OPEN_METHODS or raises the existing
%      singleton*.
%
%      H = OPEN_METHODS returns the handle to a new OPEN_METHODS or the handle to
%      the existing singleton*.
%
%      OPEN_METHODS('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in OPEN_METHODS.M with the given input arguments.
%
%      OPEN_METHODS('Property','Value',...) creates a new OPEN_METHODS or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Open_Methods_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Open_Methods_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Open_Methods

% Last Modified by GUIDE v2.5 24-Apr-2020 19:33:56

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Open_Methods_OpeningFcn, ...
                   'gui_OutputFcn',  @Open_Methods_OutputFcn, ...
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

% --- Executes just before Open_Methods is made visible.
function Open_Methods_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Open_Methods (see VARARGIN)

% Choose default command line output for Open_Methods
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Open_Methods wait for user response (see UIRESUME)
% uiwait(handles.figure1);
system("Matlab.scr&")

global choose
choose = 1;
setObj('editX1','visible','off')
setObj('text9','visible','off')


% --- Outputs from this function are returned to the command line.
function varargout = Open_Methods_OutputFcn(hObject, eventdata, handles) 
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


% --- Executes on button press in pbSolve.
function pbSolve_Callback(hObject, eventdata, handles)
% hObject    handle to pbSolve (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choose
format long;
getEquation = getObj('editEquation','string');
getX0 = getObj('editX0','string');
getX1 = getObj('editX1','string');
f = str2func("@(x)"+getEquation);
x0 = str2num(getX0);
x1 = str2num(getX1);
% Extracting a3...a0
splitxsub3 = split(getEquation,"*x^3");
splitxsub2 = split(splitxsub3{2},"*x^2");
splitxsub1 = split(splitxsub2{2},"*x");
a3 = str2num(splitxsub3{1});
a2 = str2num(splitxsub2{1});
a1 = str2num(splitxsub1{1});
a0 = str2num(splitxsub1{2});
if choose == 1
    %Convergence Test
    syms x;
    fToUse = [];
    %1st iterative formula
    eq1 = ((-a2*x^2-a1*x-a0)/a3)^(1/3);
    y1 = diff(eq1);
    fprimex01 = abs(vpa(subs(y1,x,x0)));
    %2nd iterative formula
    eq2 = ((-a3*x^3-a1*x-a0)/a2)^(1/2);
    y2 = diff(eq2);
    fprimex02 = abs(vpa(subs(y2,x,x0)));
    %3rd iterative formula
    eq3 = (-a3*x^3-a2*x^2-a0)/a1;
    y3 = diff(eq3);
    fprimex03 = abs(vpa(subs(y3,x,x0)));
    %Convergence Test
    doContinue = false;
    if fprimex01 > 0 && fprimex01 < 1
        fToUse = matlabFunction(eq1);
        doContinue = true;
    elseif fprimex02 > 0 && fprimex02 < 1
        fToUse = matlabFunction(eq2);
        doContinue = true;
    elseif fprimex03 > 0 && fprimex03 < 1
        fToUse = matlabFunction(eq3);
        doContinue = true;
    else
        disp("Doesn't converge. Please Pick another value of x0.");
    end
    if doContinue
        fx0 = fToUse(x0);
        x1 = fx0;
        fx1 = fToUse(x1);
        result = [{x0,fx0,x1,fx1,'CONTINUE'}];
        while 1
            [r,c] = size(result);
            lastCol = result{r,4};
            fx0 = fToUse(lastCol);
            x1 = fx0;
            fx1 = fToUse(x1);
            remarks = 'CONTINUE';
            if (abs(fx0-fx1) == 0)
                remarks = 'TERMINATE';
                result = [result;{lastCol,fx0,x1,fx1,remarks}];
                break
            end
            result = [result;{lastCol,fx0,x1,fx1,remarks}];
        end
        %print results
        setObj('tableFPI','data',result)
        [r,c] = size(result);
        lastCol = result{r,4};
        setObj('textRoot','string',"Root: " + lastCol)
    end
elseif choose == 2
    fx0 = f(x0);
    fx1 = f(x1);
    x2 = x0-fx0*((x1-x0)/(fx1-fx0));
    fx2 = f(x2);
    result = [{x0,x1,x2,fx0,fx1,fx2,'CONTINUE'}];
    while 1
        [r,c] = size(result);
        x0 = result{r,2};
        x1 = result{r,3};
        fx0 = f(x0);
        fx1 = f(x1);
        x2 = x0-fx0*((x1-x0)/(fx1-fx0));
        fx2 = f(x2);
        remarks = 'CONTINUE';
        if (abs(fx2) <= 0.1^10)
            remarks = 'TERMINATE';
            result = [result;{x0,x1,x2,fx0,fx1,fx2,remarks}];
            break
        end
        result = [result;{x0,x1,x2,fx0,fx1,fx2,remarks}];
    end
    %print results
    setObj('tableSM','data',result)
    setObj('textRoot','string',"Root: " + string(x2))
elseif choose == 3
    syms x;
    fx0 = f(x0);
    y = diff(f(x));
    ydouble = diff(y);
    fprimex0 = vpa(subs(y,x,x0));
    fprimex0double = vpa(subs(ydouble,x,x0));
    x1 = x0 - fx0/fprimex0;
    fx1 = f(x1);
    result = [{x0,double(x1),fx0,double(fprimex0),double(fx1),'CONTINUE'}];
    %Convergence Test
    gx = abs((fx0)*(fprimex0double)/fprimex0^2);
    if gx < 1
        %Computation
        while 1
            [r,c] = size(result);
            x0 = result{r,2};
            fx0 = f(x0);
            fprimex0 = vpa(subs(y,x,x0));
            x1 = x0 - fx0/fprimex0;
            fx1 = f(x1);
            if abs(fx1) <= 0.1^10
                result = [result;{x0,double(x1),fx0,double(fprimex0),double(fx1),'TERMINATE'}];
                break
            end
            result = [result;{x0,double(x1),fx0,double(fprimex0),double(fx1),'CONTINUE'}];
        end
        setObj('tableNRM','data',result)
        setObj('textRoot','string',"Root: " + string(double(x1)))
    else
        disp("Doesn't converge. Please Pick another value of x0.");
    end
end


% --- Executes on button press in pbFPI.
function pbFPI_Callback(hObject, eventdata, handles)
% hObject    handle to pbFPI (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choose
setObj('uipanel1','visible','on')
setObj('uipanel2','visible','off')
setObj('uipanel3','visible','off')
setObj('editX1','visible','off')
setObj('text9','visible','off')
setObj('textRoot','string',"Root: n/a")
setObj('tableFPI','data',[])
setObj('tableSM','data',[])
setObj('tableNRM','data',[])
choose = 1;

% --- Executes on button press in pbSM.
function pbSM_Callback(hObject, eventdata, handles)
% hObject    handle to pbSM (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choose
setObj('uipanel1','visible','off')
setObj('uipanel2','visible','on')
setObj('uipanel3','visible','off')
setObj('editX1','visible','on')
setObj('text9','visible','on')
setObj('textRoot','string',"Root: n/a")
setObj('tableFPI','data',[])
setObj('tableSM','data',[])
setObj('tableNRM','data',[])
choose = 2;

% --- Executes on button press in pbNRM.
function pbNRM_Callback(hObject, eventdata, handles)
% hObject    handle to pbNRM (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global choose
setObj('uipanel1','visible','off')
setObj('uipanel2','visible','off')
setObj('uipanel3','visible','on')
setObj('editX1','visible','off')
setObj('text9','visible','off')
setObj('textRoot','string',"Root: n/a")
setObj('tableFPI','data',[])
setObj('tableSM','data',[])
setObj('tableNRM','data',[])
choose = 3;



function editX0_Callback(hObject, eventdata, handles)
% hObject    handle to editX0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editX0 as text
%        str2double(get(hObject,'String')) returns contents of editX0 as a double


% --- Executes during object creation, after setting all properties.
function editX0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editX0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editX1_Callback(hObject, eventdata, handles)
% hObject    handle to editX1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editX1 as text
%        str2double(get(hObject,'String')) returns contents of editX1 as a double


% --- Executes during object creation, after setting all properties.
function editX1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editX1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
