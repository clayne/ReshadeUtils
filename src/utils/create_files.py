#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
#|*****************************************************
# # -*- coding: utf-8 -*-

from src.utils import constants, utilities
import requests


class CreateFiles:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    @staticmethod
    def create_reshade_preset_ini_file():
        dst_path = constants.RESHADE_PRESET_FILENAME
        preset_remote_file = constants.PRESET_REMOTE_FILENAME

        try:
            req = requests.get(preset_remote_file)
            with open(dst_path, "wb") as outfile:
                outfile.write(req.content)
        except requests.HTTPError:
            file = open(constants.RESHADE_PRESET_FILENAME, encoding="UTF-8", mode="w")
            file.write(
"""PreprocessorDefinitions=
Techniques=LumaSharpen@LumaSharpen.fx,DPX@DPX.fx,Levels@Levels.fx
TechniqueSorting=LumaSharpen@LumaSharpen.fx,DPX@DPX.fx,Levels@Levels.fx

[DPX.fx]
Colorfulness=2.500000
Contrast=0.100000
RGB_C=0.360000,0.360000,0.340000
RGB_Curve=8.000000,8.000000,8.000000
Saturation=1.500000
Strength=0.200000

[Levels.fx]
BlackPoint=5
HighlightClipping=0
WhitePoint=245

[LumaSharpen.fx]
offset_bias=1.000000
pattern=1
sharp_clamp=1.000000
sharp_strength=1.200000
show_sharpen=0
""")
            file.close()


    @staticmethod
    def create_reshade_ini_file(dst_res_ini_path, screenshot_path):
        reshade_config_remote_file = constants.RESHADE_REMOTE_FILENAME

        try:
            req = requests.get(reshade_config_remote_file)
            with open(dst_res_ini_path, "wb") as outfile:
                outfile.write(req.content)

            utilities.set_file_settings(dst_res_ini_path, "GENERAL", "EffectSearchPaths",
                                        f"{constants.PROGRAM_PATH}\\Reshade - shaders\\Shaders")
            utilities.set_file_settings(dst_res_ini_path, "GENERAL", "TextureSearchPaths",
                                        f"{constants.PROGRAM_PATH}\\Reshade - shaders\\Textures")
            utilities.set_file_settings(dst_res_ini_path, "GENERAL", "PresetPath",
                                        f".\\{constants.RESHADE_PRESET_INI}")
            utilities.set_file_settings(dst_res_ini_path, "SCREENSHOTS", "SavePath",
                                        f"{screenshot_path}")
        except requests.HTTPError:
            file = open(dst_res_ini_path, encoding="utf-8", mode="w")
            file.write(
f"""[D3D11]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
UseAspectRatioHeuristics=1

[D3D12]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
UseAspectRatioHeuristics=1

[D3D9]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
DisableINTZ=0
UseAspectRatioHeuristics=1

[GENERAL]
PerformanceMode=1
PreprocessorDefinitions=RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=1000.0,RESHADE_DEPTH_INPUT_IS_UPSIDE_DOWN=0,RESHADE_DEPTH_INPUT_IS_REVERSED=1,RESHADE_DEPTH_INPUT_IS_LOGARITHMIC=0
PresetTransitionDelay=1000
SkipLoadingDisabledEffects=1
EffectSearchPaths={constants.PROGRAM_PATH}\\Reshade-shaders\\Shaders
TextureSearchPaths={constants.PROGRAM_PATH}\\Reshade-shaders\\Textures
PresetPath=.\\{constants.RESHADE_PRESET_INI}

[INPUT]
ForceShortcutModifiers=1
InputProcessing=2
KeyEffects=145,0,0,0
KeyNextPreset=0,0,0,0
KeyOverlay=119,0,1,0
KeyPerformanceMode=0,0,0,0
KeyPreviousPreset=0,0,0,0
KeyReload=0,0,0,0
KeyScreenshot=44,0,0,0

[OVERLAY]
ClockFormat=1
FPSPosition=1
NoFontScaling=1
SaveWindowState=0
ShowClock=0
ShowForceLoadEffectsButton=1
ShowFPS=0
ShowFrameTime=0
ShowScreenshotMessage=1
TutorialProgress=4
VariableListHeight=300.000000
VariableListUseTabs=1

[SCREENSHOTS]
ClearAlpha=1
FileFormat=1
FileNamingFormat=0
JPEGQuality=100
SaveBeforeShot=0
SaveOverlayShot=0
SavePresetFile=0
SavePath={screenshot_path}

[STYLE]
Alpha=1.000000
ChildRounding=12.000000
ColFPSText=1.000000,1.000000,0.784314,1.000000
EditorFont=ProggyClean.ttf
EditorFontSize=13
EditorStyleIndex=0
Font=ProggyClean.ttf
FontSize=13
FPSScale=1.000000
FrameRounding=12.000000
GrabRounding=12.000000
PopupRounding=12.000000
ScrollbarRounding=12.000000
StyleIndex=0
TabRounding=12.000000
WindowRounding=12.000000
""")
            file.close()


    @staticmethod
    def create_style_file():
        dst_path = constants.STYLE_QSS_FILENAME
        css_remote_file = constants.CSS_REMOTE_FILENAME

        try:
            req = requests.get(css_remote_file)
            with open(dst_path, "wb") as outfile:
                outfile.write(req.content)
        except requests.HTTPError as e:
            file = open(constants.STYLE_QSS_FILENAME, encoding="UTF-8", mode="w")
            file.write(
"""QWidget {
   background-color: #222222;
}

QWidget:disabled {
    color: #f5f5f5;
    background-color: #222222;
}

QLabel:disabled,
QCheckBox:disabled,
QRadioButton:disabled,
QGroupBox:disabled,
QTabBar:disabled
{
    color: #828282;
    padding: 3px;
    outline: none;
    background-color: transparent;
}

QLineEdit,
QLabel,
QCheckBox,
QRadioButton,
QGroupBox,
QtWidgets  {
    color: #FFFFFF;
}

QDialogButtonBox {
    button-layout: 0;
}

QTextEdit {
    color: #FFFFFF;
    background-color: #222222;
    border: 1px transparent #FFFFFF;
    padding: 0px;
    margin: 0px;
}

QPlainTextEdit {
    color: #FFFFFF;
    background-color: #222222;
    border-radius: 2px;
    border: 1px solid #b6b6b6;
    padding: 0px;
    margin: 0px;
}

/* QPushButton */

QPushButton {
   background-color: #8b0000;
   color: #000000;
   border-radius: 5px;
   border-style: none;
   height: 25px;
   font-weight: bold;
}

QPushButton:hover {
   background-color: #8b0000;
   color: #ffffff;
}

QPushButton:pressed {
   background-color: #000000;
   color: #8b0000;
   border-radius: 5px;
   border-style: none;
   height: 25px;
   font-weight: bold;
}

/* QTabWidget */

QTabWidget::pane {
    border: 1px transparent #222222;
}

QTabWidget:focus {
    border: 1px transparent #000000;
}

QTabWidget::tab-bar {
    alignment: left;
    border: 1px transparent #000000;
}

/* QTabBar */

QTabBar::tab {
    background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #cccccc, stop: 1.0 #FFFFFF);
    border: 1px transparent #000000;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    padding:4px;
}

QTabBar::tab:selected {
    border-bottom: 1px transparent #FFFFFF;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #8b0000, stop: 1.0 #FFFFFF);
}

/* QRadioButton */

QRadioButton::indicator:checked {
    background-color:#8b0000;
    border:1px solid black;
    border-radius: 8px;
}

QRadioButton::indicator:unchecked {
    background-color:#ffffff;
    border:1px solid black;
    border-radius: 8px;
}

/* QCheckBox */

QCheckBox::indicator:checked {
    background-color:#8b0000;
    border:1px solid black;
}

QCheckBox::indicator:unchecked {
    background-color:#ffffff;
    border:1px solid black;
}

/* QScrollBar */

QScrollBar:horizontal {
    height: 15px;
    margin: 3px 15px 3px 15px;
    border: 1px transparent #3A3939;
    border-radius: 4px;
    background-color: #3A3939;
}

QScrollBar::handle:horizontal {
    background-color: #b6b6b6;
    min-width: 5px;
    border-radius: 4px;
}

QScrollBar::add-line:horizontal {
    margin: 1px 3px 0px 3px;
    width: 6px;
    height: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    margin: 1px 3px 0px 3px;
    height: 10px;
    width: 6px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::up-arrow:horizontal,
QScrollBar::down-arrow:horizontal {
    background: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

QScrollBar:vertical {
    background-color: #3A3939;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px transparent #3A3939;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #b6b6b6;
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 1px;
    height: 6px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 1px;
    height: 6px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

/* QProgressBar */

QProgressBar,
QProgressBar:horizontal {  
    border: 1px solid #b6b6b6;
    border-radius: 4px;
    text-align: center;
    padding: 1px;
    background: #bdc1c9;
    background-color: #8b0000;
}

QProgressBar::chunk,
QProgressBar::chunk:horizontal {
    background-color: qlineargradient(spread:pad, x1:1, y1:0.545, x2:1, y2:0, stop:0 #3874f2, stop:1 #5e90fa);
    border-radius: 3px;
}

/* QTableWidget */

QTableWidget::item {
    background-color: #8b0000;
}

QHeaderView::section {
    background-color: rgba(128, 128, 128, 128);
}

QTableCornerButton::section {
    background: rgba(128, 128, 128, 128);
    border: 1px transparent rgba(128, 128, 128, 128);
}
""")
            file.close()
