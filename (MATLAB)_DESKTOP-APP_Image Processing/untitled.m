
function varargout = untitled(varargin)
% untitled MATLAB code for untitled.fig
%      untitled, by itself, creates a new untitled or raises the existing
%      singleton*.
%
%      H = untitled returns the handle to a new untitled or the handle to
%      the existing singleton*.
%
%      untitled('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in untitled.M with the given input arguments.
%
%      untitled('Property','Value',...) creates a new untitled or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before untitled_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to untitled_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help untitled

% Last Modified by GUIDE v2.5 01-Oct-2018 00:41:17

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @untitled_OpeningFcn, ...
                   'gui_OutputFcn',  @untitled_OutputFcn, ...
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


% --- Executes just before untitled is made visible.
function untitled_OpeningFcn(hObject, eventdata, handles, varargin)
global value
global valueT
value = 0;
valueT = 0.5;
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to untitled (see VARARGIN)

% Choose default command line output for untitled
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes untitled wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = untitled_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbuttonBrowse.
function pushbuttonBrowse_Callback(hObject, eventdata, handles)
global fullFile;
% hObject    handle to pushbuttonBrowse (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

[file,path] = uigetfile({'*.jpg'; '*.png'; '*.bmp'; '*.gif'}, 'Select');
if ~isequal(file,0)
    axes(handles.axes1);
    imshow(imread(fullfile(path,file)));
    axes(handles.axes2);
    imshow(imread(fullfile(path,file)));
    
    fullFile = fullfile(path, file);
end

% --- Executes on button press in pushbuttonSave.
function pushbuttonSave_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonSave (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

[file,path] = uiputfile({'*.jpg'; '*.png'}, 'Save as');
if ~isequal(file,0) || ~isequal(path,0)
    F = getframe(handles.axes2);
    Image = frame2im(F);
    imwrite(Image, fullfile(path,file));
    disp(fullfile(path,file));
end


% --- Executes on button press in pushbuttonIC.
function pushbuttonIC_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonIC (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global fullFile
global value

if value < 0.9
    value = value + 0.1;
    axes(handles.axes2);
    img = imread(fullFile);
    img = imadjust(img, [0,1-value], [0.0,1]);
    imshow(img);
else
    disp('LIMIT');
end


% --- Executes on button press in pushbuttonDC.
function pushbuttonDC_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonDC (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
try
global fullFile
global value

if value > 0.1
    value = value - 0.1;
    axes(handles.axes2);
    img = imread(fullFile);
    img = imadjust(img, [0,1-value], [0.0,1]);
    imshow(img);
else
    disp('LIMIT');
end
catch e
    disp(e);
end

% --- Executes on button press in pushbuttonIT.
function pushbuttonIT_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonIT (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

try
global fullFile;
global valueT;
if valueT < 0.9
valueT = valueT + 0.1;
axes(handles.axes2);
img = (imread(fullFile));
img = im2bw((rgb2gray(img)), valueT);
imshow(img)
end
catch e
    disp(e);
end

 
% --- Executes on button press in pushbuttonDT.
function pushbuttonDT_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonDT (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global fullFile;
global valueT;
if valueT > 0.1
valueT = valueT - 0.1;
axes(handles.axes2);
img = (imread(fullFile));
img = im2bw((rgb2gray(img)), valueT);
imshow(img)
end

% --- Executes on button press in pushbuttonII.
function pushbuttonII_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonII (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
axes(handles.axes2);
imshow(getimage(handles.axes2)+5);


% --- Executes on button press in pushbuttonDI.
function pushbuttonDI_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonDI (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

axes(handles.axes2);
imshow(getimage(handles.axes2)-5);

% --- Executes on button press in pushbuttonGaussian.
function pushbuttonGaussian_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonGaussian (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
        img = imgaussfilt(imread(fullFile), 2);
        imshow(img);

% --- Executes on button press in pushbuttonGrayscale.
function pushbuttonGrayscale_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonGrayscale (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
        imshow(rgb2gray(imread(fullFile)));


% --- Executes on button press in pushbuttonNoiseRemove.
function pushbuttonNoiseRemove_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonNoiseRemove (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

        J = imnoise(imread(fullFile),'gaussian',0,0.025);
        imshow(J);

% --- Executes on button press in pushbuttonMedian.
function pushbuttonMedian_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonMedian (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

        J = imnoise(rgb2gray(imread(fullFile)),'salt & pepper',0.02);
        imshow(medfilt2(J));

% --- Executes on button press in pushbuttonSmooth.
function pushbuttonSmooth_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonSmooth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

        Ismooth = imguidedfilter(imread(fullFile));
        imshow(Ismooth);

% --- Executes on button press in pushbuttonBinary.
function pushbuttonBinary_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonBinary (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

        imshow(imbinarize(rgb2gray(imread(fullFile))));

% --- Executes on button press in pushbuttonEnhanceStructures.
function pushbuttonEnhanceStructures_Callback(hObject, eventdata, handles)
global fullFile
% hObject    handle to pushbuttonEnhanceStructures (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

        imshow(fibermetric(rgb2gray(imread(fullFile)), 7, 'ObjectPolarity', 'dark', 'StructureSensitivity', 7));

% --- Executes on button press in pushbuttonOrderStatistic.
function pushbuttonOrderStatistic_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonOrderStatistic (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        imshow(ordfilt2(rgb2gray(imread(fullFile)),25,true(5)));

% --- Executes on button press in pushbuttonBottomHat.
function pushbuttonBottomHat_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonBottomHat (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        imshow(bwmorph(rgb2gray(imread(fullFile)),'remove'));

% --- Executes on button press in pushbuttonReconstruct.
function pushbuttonReconstruct_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonReconstruct (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        mask = adapthisteq(rgb2gray(imread(fullFile)));
        se = strel('disk',5);
        marker = imerode(mask,se);
        imshow(marker);

% --- Executes on button press in pushbuttonDilate.
function pushbuttonDilate_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonDilate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        se = strel('line',11,90);
        imshow(imdilate(rgb2gray(imread(fullFile)),se));

% --- Executes on button press in pushbuttonFill.
function pushbuttonFill_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonFill (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        BW2 = imfill(imbinarize(rgb2gray(imread(fullFile))));
        imshow(BW2);

% --- Executes on button press in pushbuttonClose.
function pushbuttonClose_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonClose (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        se = strel('disk',10);
        imshow(imclose(rgb2gray(imread(fullFile)),se));

% --- Executes on button press in pushbuttonTopHat.
function pushbuttonTopHat_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonTopHat (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        %Top-Hat
        se = strel('disk',12);
        tophatFiltered = imtophat(rgb2gray(imread(fullFile)),se);
        imshow(tophatFiltered);

% --- Executes on button press in pushbuttonErode.
function pushbuttonErode_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonErode (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile
        se = strel('line',11,90);
        imshow(imerode(rgb2gray(imread(fullFile)),se));

% --- Executes on button press in pushbuttonOpen.
function pushbuttonOpen_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonOpen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fullFile

        se = strel('disk',5);
        afterOpening = imopen(rgb2gray(imread(fullFile)),se);
        imshow(afterOpening,[]);
