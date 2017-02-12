version="0.1" 

# Plugins/TMT/__init__.py

eg.RegisterPlugin(
    name = "TMT",
    author = "Brett Stottlemyer",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control TotalMedia Theater.'
    ),
    createMacrosOnAdd = False,
)

from win32gui import SendMessage, PostMessage
FindTMT = eg.WindowMatcher(u'uDigital{*}', None, None, None, None, 1, False, 0.0, 0)

class wmAction(eg.ActionClass):
    
    def __call__(self):
        hwnds = FindTMT()
        if len(hwnds) != 0:
            PostMessage(hwnds[0], 0x8D52, self.value, 0)
            print self.value
        else:
            self.PrintError("Error")
            return

class hotKeys(eg.ActionClass):
    
    def __call__(self):
        hwnds = FindTMT()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, False)
        else:
            self.PrintError("Error")
            return
			
ACTIONS = (
  #(wmAction, 'Play', 'Play', 'PLAY', 0),
  #(wmAction, 'Pause', 'Pause', 'Pause', 1),
  #(wmAction, 'Stop', 'Stop', 'Stop', 2),
  #(wmAction, 'Previous', 'Previous Track', 'Previous Track', 8),
  #(wmAction, 'Next', 'Next Track', 'Next Track', 7),
  #(wmAction, 'Forward', 'Fast Forward', 'Fast Forward', 3),
  #(wmAction, 'Rewind', 'Rewind', 'Rewind', 4),
  (hotKeys, 'Play', 'Play', 'Play', u'{Space}'),
  (hotKeys, 'Esc', 'Normal Window', 'In full screen mode, it will resume playing in normal window mode.', u'{Esc}'),
  (hotKeys, 'Pause', 'Pause', 'Pause/Play', u'{Space}'),
  (hotKeys, 'Stop', 'Stop', 'Stop', u'{O}'),
  (hotKeys, 'Resume', 'Resume', 'Resume', u'{Ctrl+Enter}'),
  (hotKeys, 'Forward', 'Forward', 'Play forward', u'{F}'),
  (hotKeys, 'Rewind', 'Rewind', 'Play backward', u'{R}'),
  (hotKeys, 'Previous', 'Previous Chapter', 'Previous Chapter', u'{PgUp}'),
  (hotKeys, 'Next', 'Next Chapter', 'Next Chapter', u'{PgDown}'),
  (hotKeys, 'Exit', 'Exit', 'Exit', u'{Ctrl+X}'),
  (hotKeys, 'Open', 'Select Source', 'Open the Select Source menu', u'{Ctrl+O}'),
  (hotKeys, 'Eject', 'Eject/Insert Disc', 'Eject/Insert disc', u'{E}'),
  (hotKeys, 'Settings', 'Settings Dialog', 'Open Settings dialog', u'{Ctrl+S}'),
  (hotKeys, 'Mute', 'Mute', 'Mute On/Off', u'{Q}'),
  (hotKeys, 'VolumeUp', 'Volume Up', 'Increase volume', u'{Shift+Up}'),
  (hotKeys, 'VolumeDown', 'Volume Down', 'Decrease volume', u'{Shift+Down}'),
  (hotKeys, 'Panel', 'Hide/Show Panel', 'Hide/Show Main Control Panel', u'{H}'),
  (hotKeys, 'SubPanel', 'Hide/Show SubPanel', 'Show/Hide Sub Control Panel', u'{Ctrl+F}'),
  (hotKeys, 'Menu', 'Show Menu', 'Show the Menu buttons', u'{Ctrl+G}'),
  (hotKeys, 'FullScreen', 'Toggle Full Screen', 'Full screen/Normal window', u'{Z}'),
  (hotKeys, 'Help', 'Help', 'Help', u'{F1}'),
  (hotKeys, 'Information', 'Toggle Information', 'Open the ArcSoft Information Center window', u'{Ctrl+I}'),
  (hotKeys, 'Effects', 'Open Effects', 'Open the "Effect and Utilities" menu', u'{Ctrl+A}'),
  (hotKeys, 'Minimize', 'Minimize Window', 'Minimize window', u'{Ctrl+N}'),
  (hotKeys, 'Bookmark', 'Add Bookmark', 'Add bookmark', u'{K}'),
  (hotKeys, 'Capture', 'Capture Picture', 'Capture picture', u'{P}'),
  (hotKeys, 'ABRepeat', 'A-B Repeat', 'A-B repeat', u'{Ctrl + R}'),
  (hotKeys, 'Title', 'Open Title List', 'Open the title list', u'{T}'),
  (hotKeys, 'Chapter', 'Open Chapter List', 'Open the chapter list', u'{Ctrl+C}'),
  (hotKeys, 'Popup', 'Show/Hide Popup', 'Show/Hide Popup Menu (for Blu-ray Disc Playback)', u'{Ctrl+U}'),
  (hotKeys, 'EffectCenter', 'Show/Hide Effect Center', 'Show/Hide Effect Center', u'{Ctrl+E}'),
  (hotKeys, 'Utilities', 'Show/Hide Utilities', 'Show/Hide Utilities window', u'{Ctrl+J}'),
  (hotKeys, 'Angle', 'Change Angle', 'Change Angle', u'{G}'),
  (hotKeys, 'Audio', 'Change Audio', 'Change (Primary) Audio Stream', u'{L}'),
  (hotKeys, 'SubTitle', 'Change Subtitle', 'Change Subtitle', u'{S}'),
  (hotKeys, 'JumpTitle', 'Jump to Title Menu', 'Jump to Title Menu', u'{Ctrl+T}'),
  (hotKeys, 'RightMenu', 'Open Right-Click Menu', 'Open Right-Click menu', u'{M}'),
  (hotKeys, 'JumpRoot', 'Jump to Root Menu', 'Jump to Root Menu', u'{Ctrl+M}'),
  (hotKeys, 'Num0', 'Number 0', '0', u'{0}'),
  (hotKeys, 'Num1', 'Number 1', '1', u'{1}'),
  (hotKeys, 'Num2', 'Number 2', '2', u'{2}'),
  (hotKeys, 'Num3', 'Number 3', '3', u'{3}'),
  (hotKeys, 'Num4', 'Number 4', '4', u'{4}'),
  (hotKeys, 'Num5', 'Number 5', '5', u'{5}'),
  (hotKeys, 'Num6', 'Number 6', '6', u'{6}'),
  (hotKeys, 'Num7', 'Number 7', '7', u'{7}'),
  (hotKeys, 'Num8', 'Number 8', '8', u'{8}'),
  (hotKeys, 'Num9', 'Number 9', '9', u'{9}'),
  (hotKeys, 'Red', 'Red', 'Red key', u'{F9}'),
  (hotKeys, 'Green', 'Green', 'Green key', u'{F10}'),
  (hotKeys, 'Yellow', 'Yellow', 'Yellow key', u'{F11}'),
  (hotKeys, 'Blue', 'Blue', 'Blue key', u'{F12}'),
  (hotKeys, 'Up', 'Up', 'Up', u'{Up}'),
  (hotKeys, 'Down', 'Down', 'Down', u'{Down}'),
  (hotKeys, 'Left', 'Left', 'Left', u'{Left}'),
  (hotKeys, 'Right', 'Right', 'Right', u'{Right}'),
)

class TMT(eg.PluginClass):
    
    def __init__(self):
        self.AddActionsFromList(ACTIONS)