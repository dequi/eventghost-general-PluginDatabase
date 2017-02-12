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
  (wmAction, 'Play', 'Play', 'PLAY', 0),
  (wmAction, 'Pause', 'Pause', 'Pause', 1),
  (wmAction, 'Stop', 'Stop', 'Stop', 2),
  (wmAction, 'Previous', 'Previous Track', 'Previous Track', 8),
  (wmAction, 'Next', 'Next Track', 'Next Track', 7),
  (wmAction, 'Forward', 'Fast Forward', 'Fast Forward', 3),
  (wmAction, 'Rewind', 'Rewind', 'Rewind', 4),
  (hotKeys, 'Exit', 'Exit', 'Exit', u'{Ctrl+X}'),
)

class TMT(eg.PluginClass):
    
    def __init__(self):
        self.AddActionsFromList(ACTIONS)