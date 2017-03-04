eg.RegisterPlugin(
    name = "ArcSoft TotalMedia Theatre",
    author = "landj9697",
    version = "0.1",
    kind = "program",
    createMacrosOnAdd = True,
)

from eg.WinApi import WM_COMMAND, SendMessageTimeout

gWindowMatcher = eg.WindowMatcher('uDigital Theatre.exe')

class ActionBase(eg.ActionClass):

    def SendCommand(self, msg, wParam, lParam):
        hwnd = gWindowMatcher()
	if hwnd:
            return SendMessageTimeout(hwnd, msg, wParam, lParam)
        else:
            raise self.Exceptions.ProgramNotRunning

class TMT(eg.PluginClass):

    def __init__(self):
        self.AddAction(Play)
        self.AddAction(Pause)
        self.AddAction(Stop)
        self.AddAction(PreviousTrack)
        self.AddAction(NextTrack)
        self.AddAction(FastForward)
        self.AddAction(FastRewind)

class Play(ActionBase):
    name = "Play"
    description = "Executes the PLAY command."
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 0, 0)
        else:
            raise self.Exceptions.ProgramNotRunning

class Pause(ActionBase):
    name = "Pause"
    description = "Executes the PAUSE command."
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 1, 0)
        else:
            raise self.Exceptions.ProgramNotRunning

class Stop(ActionBase):
    name = "Stop"
    description = "Executes the STOP command."
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 2, 0)
        else:
            raise self.Exceptions.ProgramNotRunning

class PreviousTrack(ActionBase):
    name = "PreviousTrack"
    description = "Skips BACK one chapter"
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 8, 0)
        else:
            raise self.Exceptions.ProgramNotRunning

class NextTrack(ActionBase):
    name = "NextTrack"
    description = "Skips FORWARD one chapter"
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 7, 0)
        else:
            raise self.Exceptions.ProgramNotRunning

class FastForward(ActionBase):
    name = "FastForward"
    description = "Engages the FAST FORWARD function (multiple presses increase speed)"
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 3, 0)
        else:
            raise self.Exceptions.ProgramNotRunning

class FastRewind(ActionBase):
    name = "FastRewind"
    description = "Engages the REWIND function (multiple presses increase speed)"
    
    def __call__(self):
        hwnd = gWindowMatcher()
	if hwnd:
            return self.SendCommand(0x8D52, 4, 0)
        else:
            raise self.Exceptions.ProgramNotRunning



