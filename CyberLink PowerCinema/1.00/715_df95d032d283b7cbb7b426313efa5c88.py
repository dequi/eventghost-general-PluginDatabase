import eg

eg.RegisterPlugin(
    name="CyberLink PowerCinema",
    author="Drazen Kozic",
    version="1.00",
    kind="program",
    description="Adds actions to control CyberLink PowerCinema 5.",
    createMacrosOnAdd = True,
)

ACTIONS = [
    ("TV", "TV", None, "{CTRL+T}"),
    ("Radio", "Radio", None, "{CTRL+A}"),
    ("Music", "Music", None, "{CTRL+M}"),
    ("Picture", "Picture", None, "{CTRL+I}"),
    ("Video", "Video", None, "{CTRL+E}"),
    ("Movie", "Movie", None, "{CTRL+N}"),
    ("Home", "Home", None, "{CTRL+ALT+SHIFT+HOME}"),
    ("Help", "Help", None, "{F1}"),
    ("Escape", "Escape", None, "{ESC}"),
    ("Back", "Back", None, "{BACK}"),
    ("Up", "Up", None, "{UP}"),
    ("Down", "Down", None, "{DOWN}"),
    ("Left", "Left", None, "{LEFT}"),
    ("Right", "Right", None, "{RIGHT}"),
    ("Enter", "Enter", None, "{ENTER}"),
    ("PageUp", "Page Up", None, "{PAGEUP}"),
    ("PageDown", "Page Down", None, "{PAGEDOWN}"),
    ("Begin", "Begin", None, "{HOME}"),
    ("End", "End", None, "{END}"),
    ("Paste", "Paste", None, "{CTRL+V}"),
    ("Delete", "Delete", None, "{DEL}"),
    ("Mute", "Mute", None, "{F8}"),
    ("VolumeUp", "Volume Up", None, "{F10}"),
    ("VolumeDown", "Volume Down", None, "{F9}"),
    ("Play", "Play", None, "{CTRL+SHIFT+P}"),
    ("Pause", "Pause", None, "{CTRL+P}"),
    ("Stop", "Stop", None, "{CTRL+S}"),
    ("Previous", "Previous", None, "{CTRL+B}"),
    ("Next", "Next", None, "{CTRL+F}"),
    ("Rewind", "Rewind", None, "{CTRL+SHIFT+D}"),
    ("Fastforward", "Fastforward", None, "{CTRL+SHIFT+F}"),
    ("Shuffle", "Shuffle", None, "{CTRL+SHIFT+H}"),
    ("Repeat", "Repeat", None, "{CTRL+SHIFT+R}"),
    ("PlaybackInfo", "Playback Info", None, "{CTRL+D}"),
    ("ChannelUp", "Channel Up", None, "{PAGEUP}"),
    ("ChannelDown", "Channel Down", None, "{PAGEDOWN}"),
    ("Record", "Record", None, "{CTRL+R}"),
    ("LastChannel", "Last Channel", None, "{CTRL+L}"),
    ("ProgramGuide", "Program Guide", None, "{CTRL+G}"),
    ("TeleText", "TeleText", None, "{CTRL+SHIFT+T}"),
    ("TTGreen", "TeleText Green", None, "{CTRL+SHIFT+G}"),
    ("TTYellow", "TeleText Yellow", None, "{CTRL+SHIFT+Y}"),
    ("TTBlue", "TeleText Blue", None, "{CTRL+SHIFT+B}"),
    ("TTRed", "TeleText Red", None, "{CTRL+SHIFT+R}"),
    ("Snapshot", "Snapshot", None, "{CTRL+SHIFT+Z}"),
    ("Subtitle", "Subtitle", None, "{CTRL+SHIFT+S}"),
    ("Audio", "Audio", None, "{CTRL+SHIFT+L}"),
    ("Angle", "Angle", None, "{CTRL+SHIFT+A}"),
    ("Menu", "Menu", None, "{CTRL+V}"),
    ("ClosedCaption", "Closed Caption", None, "{CTRL+SHIFT+T}"),
    ("CLEV", "CLEV", None, "{CTRL+SHIFT+E}"),
    ("CLPV", "CLPV", None, "{CTRL+SHIFT+X}"),
    ("ChangeAudioMode", "Change Audio Mode", None, "{CTRL+SHIFT+C}"),
    ("VizUp", "Viz Up", None, "{PAGEUP}"),
    ("VizDown", "Viz Down", None, "{PAGEDOWN}"),
    ("NumPad0", "NumPad 0", None, "{0}"),
    ("NumPad1", "NumPad 1", None, "{1}"),
    ("NumPad2", "NumPad 2", None, "{2}"),
    ("NumPad3", "NumPad 3", None, "{3}"),
    ("NumPad4", "NumPad 4", None, "{4}"),
    ("NumPad5", "NumPad 5", None, "{5}"),
    ("NumPad6", "NumPad 6", None, "{6}"),
    ("NumPad7", "NumPad 7", None, "{7}"),
    ("NumPad8", "NumPad 8", None, "{8}"),
    ("NumPad9", "NumPad 9", None, "{9}"),
]

gWindowMatcher = eg.WindowMatcher('PowerCinema{*}.exe', '{*}PowerCinema{*}')


class ActionPrototype(eg.ActionBase):
    
    def __call__(self):
        hwnds = gWindowMatcher()
        if hwnds:
            eg.SendKeys(hwnds[0], self.value)
        else:
            raise self.Exceptions.ProgramNotRunning
        
        
        
class PowerCinema(eg.PluginBase):
    
    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)