version="0.1" 

# Plugins/MulticastTV/__init__.py

eg.RegisterPlugin(
    name = "MulticastTV",
    author = "Brett Stottlemyer",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control MulticastTV - IPTV client app.'
    ),
    createMacrosOnAdd = True,
)

from win32gui import PostMessage

windowMatch = u'NAME OF PROGRAM FROM TASK MANAGER'
myExe = windowMatch + u'.exe'
FindMulticast = eg.WindowMatcher(myExe, None, None, None, None, 1, False, 0.0, 0)

class wmAction(eg.ActionClass):    
    def __call__(self):
        hwnds = FindMulticast()
        if len(hwnds) != 0:
            PostMessage(hwnds[0], 34952, self.value, 0)
        else:
            self.PrintError("Multicast is not running.")
            return

class Multicast(eg.PluginClass):
    def __init__(self):
        self.windowMatch = windowMatch
        self.AddActionsFromList(ACTIONS)

ACTIONS = (
  (wmAction,"Previous", "Previous", "Previous", 65536),
  (wmAction,"1","1","1",1),
  (wmAction,"2","2","2",2),
  (wmAction,"3","3","3",3),
  (wmAction,"4","4","4",4),
  (wmAction,"5","5","5",5),
  (wmAction,"6","6","6",6),
  (wmAction,"7","7","7",7),
  (wmAction,"8","8","8",8),
  (wmAction,"9","9","9",9),
  (wmAction,"0","0","0",0),
  (wmAction,"Volume Down","Volume Down","Volume Down",11),
  (wmAction,"Volume Up","Volume Up","Volume Up",12),
  (wmAction,"Channel Up","Channel Up","Channel Up",13),
  (wmAction,"Channel Down","Channel Down","Channel Down",14),
  (wmAction,"Record","Record","Record",15),
  (wmAction,"Back","Back","Back",16),
  (wmAction,"OSD Channel","OSD Channel","OSD Channel",18),
  (wmAction,"Full Screen","Full Screen","Full Screen",19),
  (wmAction,"Table","Table","Table",20),
  (wmAction,"Mute","Mute","Mute",21),
  (wmAction,"Pause","Pause","Pause",22),
  (wmAction,"Play Faster","Play Faster","Play Faster",23),
  (wmAction,"Play Slower","Play Slower","Play Slower",24),
  (wmAction,"Snapshot","Snapshot","Snapshot",25),
  (wmAction,"Recall","Recall","Recall",26),
  (wmAction,"Aspect Ratio","Aspect Ratio","Aspect Ratio",27),
  (wmAction,"Crop","Crop","Crop",28),
  (wmAction,"Left","Left","Left",102),
  (wmAction,"Right","Right","Right",103),
  (wmAction,"Up","Up","Up",100),
  (wmAction,"Down","Down","Down",101),
  (wmAction,"PIP","PIP","PIP",29),
  (wmAction,"Epg scroll up","Epg scroll up","Epg scroll up",30),
  (wmAction,"Epg scroll down","Epg scroll down","Epg scroll down",31),
  (wmAction,"Epg zoom in","Epg zoom in","Epg zoom in",32),
  (wmAction,"Epg zoom out","Epg zoom out","Epg zoom out",33),
  (wmAction,"Epg Show","Epg Show","Epg Show",34),
  (wmAction,"Teletext","Teletext","Teletext",35),
  (wmAction,"Epg background toggle","Epg background toggle","Epg background toggle",36),
  (wmAction,"Exit","Exit","Exit",99),
  (wmAction,"Stop","Stop","Stop",37),
  (wmAction,"Audio track","Audio track","Audio track",38),
)