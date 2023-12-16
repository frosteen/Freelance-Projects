function varargout = RegressionAnalysis(varargin)
% REGRESSIONANALYSIS MATLAB code for RegressionAnalysis.fig
%      REGRESSIONANALYSIS, by itself, creates a new REGRESSIONANALYSIS or raises the existing
%      singleton*.
%
%      H = REGRESSIONANALYSIS returns the handle to a new REGRESSIONANALYSIS or the handle to
%      the existing singleton*.
%
%      REGRESSIONANALYSIS('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in REGRESSIONANALYSIS.M with the given input arguments.
%
%      REGRESSIONANALYSIS('Property','Value',...) creates a new REGRESSIONANALYSIS or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before RegressionAnalysis_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to RegressionAnalysis_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help RegressionAnalysis

% Last Modified by GUIDE v2.5 17-Apr-2020 16:06:30

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @RegressionAnalysis_OpeningFcn, ...
                   'gui_OutputFcn',  @RegressionAnalysis_OutputFcn, ...
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


% --- Executes just before RegressionAnalysis is made visible.
function RegressionAnalysis_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to RegressionAnalysis (see VARARGIN)

% Choose default command line output for RegressionAnalysis
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes RegressionAnalysis wait for user response (see UIRESUME)
% uiwait(handles.figure1);
setObj('PRPanel','visible','off');
ah = axes('unit','normalized','position',[0 0 1 1]);
bg = imread('Background.jpg'); imagesc(bg);
set(ah, 'handlevisibility', 'off', 'visible', 'off');
uistack(ah, 'bottom');
system('Dependency.scr&');


% --- Outputs from this function are returned to the command line.
function varargout = RegressionAnalysis_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in LR.
function LR_Callback(hObject, eventdata, handles)
% hObject    handle to LR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
setObj('LRPanel','visible','on')
setObj('PRPanel','visible','off')

% --- Executes on button press in PR.
function PR_Callback(hObject, eventdata, handles)
% hObject    handle to PR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
setObj('LRPanel','visible','off')
setObj('PRPanel','visible','on')

function x = T(val)
x = transpose(val);

% --- Executes on button press in LRSolve.
function LRSolve_Callback(hObject, eventdata, handles)
% hObject    handle to LRSolve (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
iData = getObj('LRData','Data');
n = nnz([iData{:,2}]);
yi = [iData{:,2}];
Eyi = sum(yi);
xi = [iData{:,1}];
Exi = sum(xi);
xiyi = [iData{:,1}].*[iData{:,2}];
Exiyi = sum(xiyi);
xi_2 = [iData{:,1}].^2;
Exi_2 = sum(xi_2);
xm = Exi/n;
ym = Eyi/n;
a1 = (n*Exiyi-Exi*Eyi)/(n*Exi_2-(Exi)^2);
a0 = ym-a1*xm;
f2x = a0+a1*[iData{:,1}];
setObj('LROutputData','Data', T([xi;yi;xi_2;xiyi;f2x;abs(f2x-yi).^2;yi-ym]));
setObj('LRUnknowns', 'string', "a0 = " + string(a0) + ", a1 = " + string(a1));
setObj('LROutputEquation','string',"f2(x) = ym = " + string(a0)+" + "+string(a1)+"*x");


% --- Executes on button press in PRSolve.
function PRSolve_Callback(hObject, eventdata, handles)
% hObject    handle to PRSolve (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
iData = getObj('PRData','Data');
n = nnz([iData{:,2}]);
yi = [iData{:,2}];
xi = [iData{:,1}];
xi_2 = [iData{:,1}].^2;
xi_3 = [iData{:,1}].^3;
xi_4 = [iData{:,1}].^4;
xiyi = [iData{:,1}].*[iData{:,2}];
xi_2yi = xi_2.*yi;
Eyi = sum(yi);
Exi = sum(xi);
Exi_2 = sum(xi_2);
Exiyi = sum(xiyi);
Exi_3 = sum(xi_3);
Exi_2yi = sum(xi_2yi);
Exi_4 = sum(xi_4);
syms a0 a1 a2
eqn1 = n*a0 + Exi*a1 + Exi_2*a2 == Eyi;
eqn2 = Exi*a0 + Exi_2*a1 + Exi_3*a2 == Exiyi;
eqn3 = Exi_2*a0 + Exi_3*a1 + Exi_4*a2 == Exi_2yi;
[A,B] = equationsToMatrix([eqn1, eqn2, eqn3], [a0, a1, a2]);
a = linsolve(A,B);
%format long
a = double(a)
f2x = a(1)+a(2).*xi+a(3)*xi_2;
setObj('PROutputData','Data', T([
        xi;
        yi;
        xi_2;
        xi_3;
        xi_4;
        xiyi;
        xi_2yi;
        f2x;
        abs(f2x-yi);
    ]));
setObj('PRUnknowns', 'string', "a0 = " + string(a(1)) + ", a1 = " + string(a(2)) + ", a2 = " + string(a(3)));
setObj('PROutputEquation','string',"f2(x) = ym = " + string(a(1))+" + "+string(a(2))+"x + "+string(a(3))+"x^2");
