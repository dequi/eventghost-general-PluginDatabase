version="0.1.0" 

# Plugins/MV2Player/__init__.py
#
# Copyright (C)  2009 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ==============================================================================

eg.RegisterPlugin(
    name = "MV2Player",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://mv2.czweb.org/">'
        'MV2Player</a> (version 07 RC2) .'
    ),
    createMacrosOnAdd = True,    
    url = "http://www.eventghost.org/forum/viewtopic.php?XXXXXXXXX",
    
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUA//+ws7ioq7Km"
        "qbClqK+4u8Kio6hoa3BQU1hAQ0gwMzg2OUA4OEBbYGatsriRlJleYWhJSVF7e4OtsLfB"
        "wcnIy9DFyMxHSE2ZnKH3+PqfoqmtsLVzc3vo6/D5+fnz8/vv9PdvcHRPUlmmpq7W2eC1"
        "try0ubzIzM/g4+jn6Oq9wMTZ3ODQ09i/wMS+wcbo6evAwcXf4OKMkJM0ODvP0dTIyc3X"
        "2Nqcn6SJjZJVWV1HSk8AAABaXF2Hi444OT5xcXTR0tbQ1NdmamuJio2XmJ2EhIXY2dvg"
        "4eM8QEGpqq5LTFFAQUaQkZZRUVKgpKVDR0h5en7w8fPt7vC4ub1tbW5JSU2dnZ6wsbVk"
        "ZWr49veytrcvMDT8+vphYmaEhYqfn6cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////////////"
        "//////////////////////////////////////////////////////////////////9h"
        "ZgTTv/wANKz/////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "//////////////////////////////////////////////////////////88xkobAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAkJJREFUeNqFkl1z0kAUhjeZ"
        "hgCmxXQ2C5RmU/wgQLakwEJbU2lsIQEpWkQErdVf6L03+g/qT3CmjjPiTW8cL5TO6IaP"
        "Qiodn92d7M777tnNngPAf+B8C451bugz8LNpQBTFIBuh5ZVFESLcpcB5XKz8+bXMcd98"
        "cdYS65IcUDHWVHVjQ00sh5P+m/B3pLuadk/g7nOplKCnM1xIzs7rtyUDk5SwuQlzOZjN"
        "CtDMRaNzBpHpUIBQh4g1iLZgNp+Vgld6ochjBBVF0RGiOlJKJYpQeTu8gyeG3QfxPERU"
        "QdaejnSdlkolpFMiShP9YSUQh4RSxWLsU0ptatuK/Yi/NQ4ROJC1DCGkTK0RhzYlNikT"
        "isTQKEBVrmFCHIe4Y4MV5p0yccoGKYzPKNQb2DEMw5kaLOuxw8iTbakxeuMixIbrOm7a"
        "muG6eddYala9ZGVAEiTOWVJE3+Oic1D7eOEZfitDluQvA588AIOf6x9W1kaXrCdwOmOa"
        "pnp1QIutMqoTqTzxDEtPj3H7mWm2zYlc6bS9VVypNUfROs+7Gm57jPUXbKayofX60VFF"
        "vfv8/RJ8AmesMcJfh0EQZHV2tvr+x6T4XgX3MCsV1qxkG7/EXmf09qe5AEcnAp7xevxR"
        "jqT1aTbBgWzga9gRuTv327vSlnZN73YBnhkCciWmzuR0Z0cOdfxl2z855Z2M2tbUtNOJ"
        "iZUguE4kWuwfNhp8o7p62pSONfyPA8Ra9bDUlCrN1huAF+gevcDbGDv7BpXBNmJ8s7yQ"
        "v1q+eWdCw61rAAAAAElFTkSuQmCC"
    ),    
)

# Changelog:
# ==============================================================================
# 2009-06-20 Pako
#     * initial (beta) version 0.1.0
#===============================================================================

import os.path
import subprocess
from eg.WinApi.Dynamic import PostMessage
from win32gui import MessageBox
import _winreg

WM_COMMAND = 273
#===============================================================================

class Text:
    label1 = "Folder with Mv2PlayerPlus.exe:"
    text1 = "Couldn't find MV2Player window !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    boxMessage1 = 'Missing file %s !'
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================
            
def HandleMV2():
    FindMV2 = eg.WindowMatcher(
        u'Mv2PlayerPlus.exe',
        u'MV2Player',
        u'MV2 Player',
        None,
        None,
        None,
        True,
        0.0,
        0
    )

    res = None
    hwnds = FindMV2()
    if len(hwnds)>0:
        res = hwnds[0]
    return res

#===============================================================================

class MV2Player(eg.PluginClass):
    text=Text
    MV2Path = u''


    def __init__(self):
        text=Text
        self.AddActionsFromList(Actions)

    def __start__(self, path):
        self.MV2Path = path
                   
    def Configure(self, path = None):
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        mv2PathCtrl = MyDirBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )        
        mv2PathCtrl.GetTextCtrl().SetEditable(False)


        if path is None:
            try:
                mv2_reg = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Classes\\MV2_INI_File\\DefaultIcon"
                )
                self.MV2Path = unicode(os.path.split(_winreg.EnumValue(mv2_reg,0)[1])[0])
                _winreg.CloseKey(mv2_reg)
                mv2PathCtrl.SetValue(self.MV2Path)
            except:
                self.MV2Path = unicode(eg.folderPath.ProgramFiles)+"\\Mv2Player"
                mv2PathCtrl.SetValue("")

        else:
            mv2PathCtrl.SetValue(path)
            self.MV2Path = path
        mv2PathCtrl.startDirectory = self.MV2Path
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0, wx.TOP,15)
        sizerAdd(mv2PathCtrl,0,wx.TOP,3)

        def Validation():
            flag = os.path.exists(mv2PathCtrl.GetValue()+"\\Mv2PlayerPlus.exe")
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)
       
        def OnPathChange(event = None):
            path = mv2PathCtrl.GetValue()
            flag = os.path.exists(path+"\\Mv2PlayerPlus.exe")
            if event and not flag:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'Mv2PlayerPlus.exe',
                    self.text.boxTitle % path,
                    0
                )
            if path != "":
                mv2PathCtrl.startDirectory = path
            Validation()
        mv2PathCtrl.Bind(wx.EVT_TEXT,OnPathChange)
        OnPathChange()        

        while panel.Affirmed():
            panel.SetResult(
                mv2PathCtrl.GetValue(),
            )           
#===============================================================================
#cls types for Actions list:
#===============================================================================

class Run(eg.ActionClass):

    def __call__(self):
        hwnd = HandleMV2()        
        if hwnd is None:
            mv2 = self.plugin.MV2Path+'\\Mv2PlayerPlus.exe'
            if os.path.isfile(mv2):        
                wx.CallAfter(subprocess.Popen,[mv2])
            else:
                self.PrintError(self.text.text2 % 'Mv2PlayerPlus.exe')
                return self.text.text2 % 'Mv2PlayerPlus.exe'
                   
    class text:
        text2 = "Couldn't find file %s !"
#===============================================================================

class SendMessage(eg.ActionClass):
    def __call__(self):
        hwnd = HandleMV2()
        if hwnd:
            PostMessage(hwnd, WM_COMMAND, self.value, 2025)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

Actions = (
    (Run,"Run","Run MV2Player","Run MV2Player.",None),
    (eg.ActionGroup, 'OSD', 'OSD', 'OSD',(    
        (SendMessage,"OSDmenu","OSD menu","OSD menu.", 40290),
        (SendMessage,"OSDInfo","OSD Info","OSD info.", 40300),
        (SendMessage,"OSD_Up","OSD Up","OSD Up.",40291),
        (SendMessage,"OSD_Down","OSD Down","OSD Down.",40292),
        (SendMessage,"OSD_Left","OSD Left","OSD Left.",40293),
        (SendMessage,"OSD_Right","OSD Right","OSD Right.",40294),
        (SendMessage,"OSD_Select","OSD Select","OSD Select.",40295),
        (SendMessage,"OSD_Cancel","OSD Cancel","OSD Cancel.",40296),
    )),
    (eg.ActionGroup, 'General', 'General', 'General',(    
        (SendMessage,"Capture_Frame","Capture Frame","Capture Frame.",40363),
        (SendMessage,"Options","Options","Options.",40270),
        (SendMessage,"PlaylistEditor","Playlist editor","Playlist editor.",40271),
        (SendMessage,"Catalog","Catalog","Catalog.",40274),
        (SendMessage,"BookmarksEditor","Bookmarks editor","Bookmarks editor.",40276),
        (SendMessage,"FilesInfo","File(s) info","File(s) info.",40275),
        (SendMessage,"Exit","Exit","Exit.",40280),
        (SendMessage,"SwitchMinimize","Switch Minimize","Switch Minimize.",40281),
        (SendMessage,"RunStartupFile","Run Startup File","Run Startup File.",40282),
        (SendMessage,"ClearBookmarks","Clear Bookmarks","Clear Bookmarks.",40364),
    )),
    (eg.ActionGroup, 'Open_Save', 'Open/Save', 'Open/Save',(    
        (SendMessage,"OpenFile","Open File","Open File.",40260),
        (SendMessage,"OpenFolder","Open Folder","Open Folder.",40264),
        (SendMessage,"OpenCD","Open CD","Open CD.",40261),
        (SendMessage,"OpenAudioCDforceMCI","Open Audio CD (force MCI)","Open Audio CD (force MCI).",40265),
        (SendMessage,"SaveTitlesAsPlaylist","Save Titles As Playlist","Save Titles As Playlist.",40262),
        (SendMessage,"SaveTitlesAsMV2","Save Titles As MV2","Save Titles As MV2.",40263),
        (SendMessage,"SaveMenu","Save Menu","Save Menu.",40266),
    )),
    (eg.ActionGroup, 'Skin', 'Skin', 'Skin',(    
        (SendMessage,"NextSkin","Next Skin","Next Skin.",40283),
        (SendMessage,"PreviousSkin","Previous Skin","Previous Skin.",40286),
        (SendMessage,"SwitchSkinSize","Switch Skin Size","Switch Skin Size.",40330),
        (SendMessage,"HidePanel","Hide Panel","Hide Panel.",40360),
        (SendMessage,"ShowPanel","Show Panel","Show Panel.",40361),
        (SendMessage,"PanelOn_Off","Panel On/Off","Panel On/Off.",40362),
        (SendMessage,"Pad1On_Off","Pad1 On/Off","Pad1 On/Off.",40450),
        (SendMessage,"Pad2On_Off","Pad2 On/Off","Pad2 On/Off.",40451),
        (SendMessage,"Pad3On_Off","Pad3 On/Off","Pad3 On/Off.",40452),
        (SendMessage,"Pad4On_Off","Pad4 On/Off","Pad4 On/Off.",40453),
        (SendMessage,"Cover1On_Off","Cover1 On/Off","Cover1 On/Off.",40454),
        (SendMessage,"Cover2On_Off","Cover2 On/Off","Cover2 On/Off.",40455),
        (SendMessage,"Cover3On_Off","Cover3 On/Off","Cover3 On/Off.",40456),
        (SendMessage,"Cover4On_Off","Cover4 On/Off","Cover4 On/Off.",40457),
    )),
    (eg.ActionGroup, 'Volume', 'Volume', 'Volume',(    
        (SendMessage,"MuteOn","Mute On","Mute On.",40140),
        (SendMessage,"MuteOff","Mute Off","Mute Off.",40141),
        (SendMessage,"SwitchMute","Switch Mute","Switch Mute.",40142),
        (SendMessage,"VolumeP","Volume +","Volume +.",40143),
        (SendMessage,"VolumeM","Volume -","Volume -.",40144),
    )),
    (eg.ActionGroup, 'TTS', 'TTS', 'TTS',(    
        (SendMessage,"TTSon","TTS On","TTS On.",40150),
        (SendMessage,"TTSoff","TTS Off","TTS Off.",40151),
        (SendMessage,"SwitchTTS","Switch TTS","Switch TTS.",40152),
        (SendMessage,"TTS_Volume +","TTS Volume +","TTS Volume +.",40145),
        (SendMessage,"TTS_Volume -","TTS Volume -","TTS Volume -.",40146),
    )),
    (eg.ActionGroup, 'VideoSize', 'Video Size', 'Video Size',(    
        (SendMessage,"ZoomP","Zoom +","Zoom +.",40155),
        (SendMessage,"ZoomM","Zoom -","Zoom -.",40156),
        (SendMessage,"MoveLeft","Move Left","Move Left.",40157),
        (SendMessage,"MoveRight","Move Right","Move Right.",40158),
        (SendMessage,"MoveUp","Move Up","Move Up.",40159),
        (SendMessage,"MoveDown","Move Down","Move Down.",40160),
        (SendMessage,"CenterVideo","Center Video","Center Video.",40161),
        (SendMessage,"WindowMode","Window Mode","Window Mode.",40234),
        (SendMessage,"DesktopMode","Desktop Mode","Desktop Mode.",40237),
        (SendMessage,"FullscreenOn","Fullscreen On","Fullscreen On.",40180),
        (SendMessage,"SwitchFullscreen","Switch Fullscreen","Switch Fullscreen.",40182),
        (SendMessage,"NextFullscreenMode","Next Fullscreen Mode","Next Fullscreen Mode.",40179),
        (SendMessage,"FitToWindow","Fit to Window","Fit to Window.",40170),
        (SendMessage,"FullHeight","Full Height","Full Height.",40171),
        (SendMessage,"Scan1_55_1","Scan 1,55:1","Scan 1,55:1.",40172),
        (SendMessage,"Scan16_9","Scan 16:9","Scan 16:9.",40173),
        (SendMessage,"Scan2_1","Scan 2:1","Scan 2:1.",40174),
        (SendMessage,"FullWidth","Full Width","Full Width.",40175),
        (SendMessage,"ScanPixel_Pixel","Scan Pixel:Pixel","Scan Pixel:Pixel.",40176),
        (SendMessage,"ResetScan","Reset Scan","Reset Scan.",40178),
        (SendMessage,"SwitchScan","Switch Scan","Switch Scan.",40177),
        (SendMessage,"AspectRatioP","Aspect Ratio +","Aspect Ratio +.",40162),
        (SendMessage,"AspectRatioM","Aspect Ratio -","Aspect Ratio -.",40163),
        (SendMessage,"FreeaspectRatio","Free aspect ratio","Free aspect ratio.",40206),
        (SendMessage,"AspectRatio4_3","Aspect ratio 4:3","Aspect ratio 4:3.",40207),
        (SendMessage,"AspectRatio16_9","Aspect ratio 16:9","Aspect ratio 16:9.",40208),
        (SendMessage,"PrefferedAspectRatio","Preffered aspect ratio","Preffered aspect ratio.",40209),
        (SendMessage,"TopmostOn","Topmost On","Topmost On.",40167),
        (SendMessage,"TopmostOff","Topmost Off","Topmost Off.",40168),
        (SendMessage,"SwitchTopmost","Switch Topmost","Switch Topmost.",40169),
        (SendMessage,"WindowBorderOn_Off","Window border On/Off","Window border On/Off.",40153),
    )),
    (eg.ActionGroup, 'MV2_MVDmenu', 'MV2/MVD menu', 'MV2/MVD menu',(    
        (SendMessage,"PageMenu","Page Menu","Page Menu.",40210),
        (SendMessage,"PageChapters","Page Chapters","Page Chapters.",40211),
        (SendMessage,"PageSpecials","Page Specials","Page Specials.",40212),
        (SendMessage,"PageLanguages","Page Languages","Page Languages.",40213),
        (SendMessage,"PageSubtitles","Page Subtitles","Page Subtitles.",40214),
        (SendMessage,"PageCast","Page Cast","Page Cast.",40215),
        (SendMessage,"MainMovie","Main Movie","Main Movie.",40216),
        (SendMessage,"GenerateMenu","Generate Menu","Generate Menu.",40218),
        (SendMessage,"RemoveMenu","Remove Menu","Remove Menu.",40219),
    )),
    (eg.ActionGroup, 'PlayGeneral', 'Play General', 'Play General',(    
        (SendMessage,"Play","Play","Play.",40101),
        (SendMessage,"Pause","Pause","Pause.",40102),
        (SendMessage,"Stop","Stop","Stop.",40104),
        (SendMessage,"SwitchPause","Switch Pause","Switch Pause.",40103),
        (SendMessage,"PrevChapter_Title_Set","Prev Chapter/Title/Set","Prev Chapter/Title/Set.",40200),
        (SendMessage,"NextChapter_Title_Set","Next Chapter/Title/Set","Next Chapter/Title/Set",40201),
        (SendMessage,"PrevTitle_Set","Prev Title/Set","Prev Title/Set.",40203),
        (SendMessage,"NextTitle_Set","Next Title/Set","Next Title/Set.",40202),
        (SendMessage,"PrevSet","Prev Set","Prev Set.",40204),
        (SendMessage,"NextSet","Next Set","Next Set.",40205),
        (SendMessage,"JumpToTime","Jump To Time","Jump To Time.",40272),
        (SendMessage,"RepeatOff","Repeat Off","Repeat Off.",40105),
        (SendMessage,"RepeatTitle","Repeat Title","Repeat Title.",40106),
        (SendMessage,"RepeatAll","Repeat All","Repeat All.",40107),
        (SendMessage,"RandomMode","Random Mode","Random Mode.",40108),
        (SendMessage,"RandomModeInPlaylistOnly","Random mode in playlist only","Random mode in playlist only.",40284),
        (SendMessage,"RepeatAllInPlaylistOnly","Repeat All in Playlist Only","Repeat All in Playlist Only.",40285),
        (SendMessage,"NextRepeatMode","Next Repeat Mode","Next Repeat Mode.",40109),
        (SendMessage,"SetBookmark","Set Bookmark","Set Bookmark.",40133),
    )),
    (eg.ActionGroup, 'PlaySeek', 'Play Seek', 'Play Seek',(    
        (SendMessage,"JumpToNext keyframe","Jump to next keyframe","Jump to next keyframe.",40134),
        (SendMessage,"JumpToPreviousKeyframe","Jump to previous keyframe","Jump to previous keyframe.",40135),
        (SendMessage,"CustomJumpForward","Custom Jump forward","Custom Jump forward.",40136),
        (SendMessage,"CustomJumpBackward","Custom Jump backward","Custom Jump backward.",40137),
        (SendMessage,"Jump5sec","Jump 5 sec","Jump 5 sec.",40120),
        (SendMessage,"Jump-5sec","Jump - 5 sec","Jump - 5 sec.",40123),
        (SendMessage,"Jump10sec","Jump 10 sec","Jump 10 sec.",40121),
        (SendMessage,"Jump-10sec","Jump - 10 sec","Jump - 10 sec.",40124),
        (SendMessage,"Jump30sec","Jump 30 sec","Jump 30 sec.",40122),
        (SendMessage,"Jump-30sec","Jump - 30 sec","Jump - 30 sec.",40125),
        (SendMessage,"Step1frame","Step 1 frame","Step 1 frame.",40126),
        (SendMessage,"Step-1frame","Step - 1 frame","Step - 1 frame.",40127),
        (SendMessage,"Rewind","Rewind","Rewind.",40128),
    )),
    (eg.ActionGroup, 'PlaySpeed', 'Play Speed', 'Play Speed',(    
        (SendMessage,"Rate0_1x","Rate 0.1x","Rate 0.1x.",40110),
        (SendMessage,"Rate0_25x","Rate 0.25x","Rate 0.25x.",40111),
        (SendMessage,"Rate0_5x","Rate 0.5x","Rate 0.5x.",40112),
        (SendMessage,"Rate0_75x","Rate 0.75x","Rate 0.75x.",40113),
        (SendMessage,"Rate1x","Rate 1x","Rate 1x.",40114),
        (SendMessage,"Rate1_25x","Rate 1.25x","Rate 1.25x.",40115),
        (SendMessage,"Rate1_5x","Rate 1.5x","Rate 1.5x.",40116),
        (SendMessage,"Rate2x","Rate 2x","Rate 2x.",40117),
        (SendMessage,"Rate2_5x","Rate 2.5x","Rate 2.5x.",40118),
        (SendMessage,"RateP","Rate +","Rate +.",40147),
        (SendMessage,"RateM","Rate -","Rate -.",40148),
        (SendMessage,"DialogRate","Dialog Rate","Dialog Rate.",40149),
    )),
    (eg.ActionGroup, 'PlayLoop', 'Play Loop', 'Play Loop',(    
        (SendMessage,"LoopStart","Loop Start","Loop Start.",40130),
        (SendMessage,"LoopStop","Loop Stop","Loop Stop.",40131),
        (SendMessage,"LoopClear","Loop Clear","Loop Clear.",40132),
        (SendMessage,"LoopAdjust","Loop Adjust","Loop Adjust.",40273),
        (SendMessage,"ABRepeat","AB Repeat","AB Repeat.",40138),
    )),
    (eg.ActionGroup, 'Languages', 'Languages', 'Languages',(    
        (SendMessage,"NextSubtitles 1","Next Subtitles 1","Next Subtitles 1.",40190),
        (SendMessage,"Subtitles1Up","Subtitles1 Up","Subtitles1 Up.",40196),
        (SendMessage,"Subtitles1Down","Subtitles1 Down","Subtitles1 Down.",40197),
        (SendMessage,"Subtitles1SizeP","Subtitles1 Size +","Subtitles1 Size +.",40220),
        (SendMessage,"Subtitles1SizeM","Subtitles1 Size -","Subtitles1 Size -.",40221),
        (SendMessage,"OffsetSubtitles1P","Offset subtitles1 +","Offset subtitles1 +.",40183),
        (SendMessage,"OffsetSubtitles1M","Offset subtitles1 -","Offset subtitles1 -.",40184),
        (SendMessage,"OffsetSubtitles1reset","Offset subtitles1 reset","Offset subtitles1 reset.",40185),
        (SendMessage,"NextSubtitles2","Next Subtitles 2","Next Subtitles 2.",40191),
        (SendMessage,"Subtitles2Up","Subtitles2 Up","Subtitles2 Up.",40198),
        (SendMessage,"Subtitles2Down","Subtitles2 Down","Subtitles2 Down.",40199),
        (SendMessage,"Subtitles2SizeP","Subtitles2 Size +","Subtitles2 Size +.",40222),
        (SendMessage,"Subtitles2SizeM","Subtitles2 Size -","Subtitles2 Size -.",40223),
        (SendMessage,"OffsetSubtitles2P","Offset subtitles2 +","Offset subtitles2 +.",40186),
        (SendMessage,"OffsetSubtitles2M","Offset subtitles2 -","Offset subtitles2 -.",40187),
        (SendMessage,"OffsetSubtitles2reset","Offset subtitles2 reset","Offset subtitles2 reset.",40188),
        (SendMessage,"ClosedCaptionsOn","Closed captions on","Closed captions on.",40224),
        (SendMessage,"ClosedCaptionsOff","Closed captions off","Closed captions off.",40225),
        (SendMessage,"ClosedCaptionsOn_Off","Closed captions on/off","Closed captions on/off.",40226),
        (SendMessage,"NextAudio","Next Audio","Next Audio.",40192),
        (SendMessage,"AudioOffsetP","Audio Offset +","Audio Offset +.",40194),
        (SendMessage,"AudioOffsetM","Audio Offset -","Audio Offset -.",40193),
        (SendMessage,"AudioOffsetReset","Audio Offset reset","Audio Offset reset.",40195),
    )),
    (eg.ActionGroup, 'Time', 'Time', 'Time',(    
        (SendMessage,"ElapsedTime","Elapsed Time","Elapsed Time.",40250),
        (SendMessage,"RemainTime","Remain Time","Remain Time.",40251),
        (SendMessage,"CurrentTime","Current Time","Current Time.",40252),
        (SendMessage,"SwitchTimeMode","Switch Time Mode","Switch Time Mode.",40253),
        (SendMessage,"SwitchModeFrames/Time","Switch mode Frames/Time","Switch mode Frames/Time.",40254),
    )),
    (eg.ActionGroup, 'ColorControls', 'Color Controls', 'Color Controls',(    
        (SendMessage,"OverlayMixerOn","OverlayMixer On","OverlayMixer On.",40305),
        (SendMessage,"OverlayMixerOff","OverlayMixer Off","OverlayMixer Off.",40306),
        (SendMessage,"BrightnessMoverlay","Brightness - (overlay)","Brightness - (overlay).",40310),
        (SendMessage,"BrightnessPoverlay","Brightness + (overlay)","Brightness + (overlay).",40311),
        (SendMessage,"ContrastMoverlay","Contrast - (overlay)","Contrast - (overlay).",40312),
        (SendMessage,"ContrastPoverlay","Contrast + (overlay)","Contrast + (overlay).",40313),
        (SendMessage,"HueMoverlay","Hue - (overlay)","Hue - (overlay).",40314),
        (SendMessage,"HuePoverlay","Hue + (overlay)","Hue + (overlay).",40315),
        (SendMessage,"SaturationMoverlay","Saturation - (overlay)","Saturation - (overlay).",40316),
        (SendMessage,"SaturationPoverlay","Saturation + (overlay)","Saturation + (overlay).",40317),
        (SendMessage,"SharpnessMoverlay","Sharpness - (overlay)","Sharpness - (overlay).",40318),
        (SendMessage,"SharpnessPoverlay","Sharpness + (overlay)","Sharpness + (overlay).",40319),
        (SendMessage,"GammaMoverlay","Gamma - (overlay)","Gamma - (overlay).",40320),
        (SendMessage,"GammaPoverlay","Gamma + (overlay)","Gamma + (overlay).",40321),
        (SendMessage,"QualityM","Quality -","Quality -.",40340),
        (SendMessage,"QualityP","Quality +","Quality +.",40341),
        (SendMessage,"BrightnessM","Brightness -","Brightness -.",40342),
        (SendMessage,"BrightnessP","Brightness +","Brightness +.",40343),
        (SendMessage,"ContrastM","Contrast  -","Contrast  -.",40344),
        (SendMessage,"ContrastP","Contrast  +","Contrast  +.",40345),
        (SendMessage,"SaturationM","Saturation -","Saturation -.",40346),
        (SendMessage,"SaturationP","Saturation +","Saturation +.",40347),
        (SendMessage,"GammaM","Gamma -","Gamma -.",40348),
        (SendMessage,"GammaP","Gamma +","Gamma +.",40349),
        (SendMessage,"DefaultBrightness","Default Brightness","Default Brightness.",40380),
        (SendMessage,"DefaultContrast","Default Contrast","Default Contrast.",40381),
        (SendMessage,"DefaultSaturation","Default Saturation","Default Saturation.",40382),
        (SendMessage,"DefaultNoise","Default Noise","Default Noise.",40383),
        (SendMessage,"DefaultSharpness","Default Sharpness","Default Sharpness.",40384),
        (SendMessage,"DefaultGamma","Default Gamma","Default Gamma.",40385),
    )),
    (eg.ActionGroup, 'Filters', 'Filters', 'Filters',(    
        (SendMessage,"OverlayMixerOn_Off","OverlayMixer On/Off","OverlayMixer On/Off.",40307),
        (SendMessage,"DedynamicFilterOn_Off","Dedynamic Filter On/Off","Dedynamic Filter On/Off.",40350),
        (SendMessage,"TFM_AudioFilterOn_Off","TFM Audio Filter On/Off","TFM Audio Filter On/Off.",40351),
        (SendMessage,"VideodecoderProperties","Videodecoder Properties","Videodecoder Properties.",40230),
        (SendMessage,"AudiodecoderProperties","Audiodecoder Properties","Audiodecoder Properties.",40231),
        (SendMessage,"VideorendererProperties","Videorenderer Properties","Videorenderer Properties.",40232),
        (SendMessage,"AudiorendererProperties","Audiorenderer Properties","Audiorenderer Properties.",40233),
    )),
    (eg.ActionGroup, 'Shutdown', 'Shutdown', 'Shutdown',(    
        (SendMessage,"ShutdownOn","Shutdown On","Shutdown On.",40240),
        (SendMessage,"ShutdownOff","Shutdown Off","Shutdown Off.",40241),
        (SendMessage,"ShutdownNow","Shutdown Now","Shutdown Now.",40242),
        (SendMessage,"ShutdownCancel","Shutdown Cancel","Shutdown Cancel.",40243),
    )),
    (eg.ActionGroup, 'Extra Controls', 'Extra Controls', 'Extra Controls',(    
        (SendMessage,"CDtrayOpen","CD tray open","CD tray open.",40405),
        (SendMessage,"CDtrayClose","CD tray close","CD tray close.",40406),
        (SendMessage,"ComicsCreator","Comics Creator","Comics Creator.",40401),
        (SendMessage,"ExportGXR","Export GXR","Export GXR.",40440),
        (SendMessage,"ExportGML","Export GML","Export GML.",40441),
        (SendMessage,"Homepage","Homepage","Homepage.",40287),
        (SendMessage,"TitleButton0","Title button 0","Title button 0.",40540),
        (SendMessage,"TitleButton1","Title button 1","Title button 1.",40541),
        (SendMessage,"TitleButton2","Title button 2","Title button 2.",40542),
        (SendMessage,"TitleButton3","Title button 3","Title button 3.",40543),
        (SendMessage,"TitleButton4","Title button 4","Title button 4.",40544),
        (SendMessage,"TitleButton5","Title button 5","Title button 5.",40545),
        (SendMessage,"TitleButton6","Title button 6","Title button 6.",40546),
        (SendMessage,"TitleButton7","Title button 7","Title button 7.",40547),
        (SendMessage,"TitleButton8","Title button 8","Title button 8.",40548),
        (SendMessage,"TitleButton9","Title button 9","Title button 9.",40549),
        (SendMessage,"TitleButton_10","Title button +10","Title button +10.",40550),
        (SendMessage,"SaveSlot1","Save Slot 1","Save Slot 1.",40560),
        (SendMessage,"SaveSlot2","Save Slot 2","Save Slot 2.",40562),
        (SendMessage,"SaveSlot3","Save Slot 3","Save Slot 3.",40564),
        (SendMessage,"SaveSlot4","Save Slot 4","Save Slot 4.",40566),
        (SendMessage,"SaveSlot5","Save Slot 5","Save Slot 5.",40568),
        (SendMessage,"LoadSlot1","Load Slot 1","Load Slot 1.",40561),
        (SendMessage,"LoadSlot2","Load Slot 2","Load Slot 2.",40563),
        (SendMessage,"LoadSlot3","Load Slot 3","Load Slot 3.",40565),
        (SendMessage,"LoadSlot4","Load Slot 4","Load Slot 4.",40567),
        (SendMessage,"LoadSlot5","Load Slot 5","Load Slot 5.",40569)
    )),
)
#===============================================================================
