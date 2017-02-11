# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

##############################################################################
# Revision history:
#
# 2013-01-10  Experimental with mapping to house/unit codes
##############################################################################

"""<rst>
Hardware plugin for X10 compatible RF remotes.

This includes remotes like:

* `ATI Remote Wonder
  <http://www.ati.com/products/remotewonder/index.html>`_
* `ATI Remote Wonder PLUS
  <http://www.ati.com/products/remotewonderplus/index.html>`_
* `SnapStream Firefly
  <http://www.snapstream.com/products/firefly/>`_
* `NVIDIA Personal Cinema Remote
  <http://www.nvidia.com/object/feature_PC_remote.html>`_
* `Marmitek PC Control
  <http://www.marmitek.com/>`_
* `Pearl Q-Sonic Master Remote 6in1
  <http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601&vid=916&curr=DEM>`_
* `Niveus PC Remote Control
  <http://www.niveusmedia.com/>`_
* Medion RF Remote Control
* Packard Bell RF MCE Remote Control OR32E
"""

import eg

eg.RegisterPlugin(
    name = "X10 Remote",
    author = "Bitmonster",
    version = "1.0.1",
    kind = "remote",
    hardwareId = "USB\\VID_0BC7&PID_0006",
    guid = "{C3E96757-E507-4CC3-A2E6-465D48B87D09}",
    canMultiLoad = True,
    description = __doc__,
    url = "http://www.eventghost.net/forum/viewtopic.php?t=1589",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)

import wx
from win32com.client import DispatchWithEvents

class Text:
    allButton = "&All"
    noneButton = "&None"
    remoteBox = "Remote type:"
    idBox = "Active IDs:"
    usePrefix = "Event prefix:"
    errorMesg = "No X10 receiver found!"


REMOTES = [
    [
        "ATI Remote Wonder",
        {
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
            'MouseUp': 'Mouse000',
            'MouseRightUp': 'Mouse045',
            'MouseRight': 'Mouse090',
            'MouseRightDown': 'Mouse135',
            'MouseDown': 'Mouse180',
            'MouseLeftDown': 'Mouse225',
            'MouseLeft': 'Mouse270',
            'MouseLeftUp': 'Mouse315',
            'MTAddDelete': 'Menu',
            'MTAB': 'Check',
        }
    ],
    [
        "Medion",
        {
            'MTTV': 'TV',
            'MTVCR': 'VCR',
            'Book': 'Music',
            'MTRadio': 'Radio',
            'Web': 'Photo',
            'MTPC': 'TVPreview',
            'MTChannelList': 'ChannelList',
            'D': 'Setup',
            'MTAlbum': 'VideoDesktop',
            'VolumeUp': 'VolumeDown',
            'VolumeDown': 'VolumeUp',
            'A': 'Mute',
            'MTArtist': 'Red',
            'MTGenre': 'Green',
            'MTTrack': 'Yellow',
            'MTUp': 'Blue',
            'MTAddDelete': 'TXT',
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
            'Bookmark': 'ChannelSearch',
            'Resize': 'Delete',
            'MTLeft': 'Rename',
            'MTAB': 'Snapshot',
            'MTDown': 'AcquireImage',
            'MTRight': 'EditImage',
            'E': 'PreviousTrack',
            'F': 'NextTrack',
            'C': 'DVDMenu',
            'MTPlaylist': 'DVDAudio',
            'MTEnter': 'Fullscreen',
        }
    ],
    [
        "Generic X10",
        {
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
        }
    ],
    [
        "SnapStream FireFly",
        {
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
            'MTTV': 'Maximize',
            'Power': 'Close',
            'MTAddDelete': 'Back',
            'MTAB': 'Enter',
            'VolumeDown': 'VolumeUp',
            'VolumeUp': 'VolumeDown',
            'A': 'FireFly',
            'MTRadio': 'Info',
            'MTPC': 'Option',
            'Bookmark': 'Menu',
            'Resize': 'Exit',
            'Input': 'PreviousTrack',
            'Zoom': 'NextTrack',
            'Book': 'Music',
            'Web': 'Photo',
            'Hand': 'Video',
            'B': 'Help',
            'MTVCR': 'Mouse',
            'C': 'A',
            'D': 'B',
            'E': 'C',
            'F': 'D',
        }
    ],
]

HOUSE_UNITS = {
        
    '0': 'A1', '1': 'A2', '2': 'A3', '3': 'A4', '4': 'A5', '5': 'A6', '6': 'A7', '7': 'A8', '8': 'A9', '9': 'A10', '10': 'A11', '11': 'A12', '12': 'A13', '13': 'A14', '14': 'A15', '15': 'A16',
    '16': 'B1', '17': 'B2', '18': 'B3', '19': 'B4', '20': 'B5', '21': 'B6', '22': 'B7', '23': 'B8', '24': 'B9', '25': 'B10', '26': 'B11', '27': 'B12', '28': 'B13', '29': 'B14', '30': 'B15', '31': 'B16',
    '32': 'C1', '33': 'C2', '34': 'C3', '35': 'C4', '36': 'C5', '37': 'C6', '38': 'C7', '39': 'C8', '40': 'C9', '41': 'C10', '42': 'C11', '43': 'C12', '44': 'C13', '45': 'C14', '46': 'C15', '47': 'C16',
    '48': 'D1', '49': 'D2', '52': 'D3', '51': 'D4', '52': 'D5', '53': 'D6', '54': 'D7', '55': 'D8', '56': 'D9', '58': 'D10', '58': 'D11', '59': 'D12', '60': 'D13', '61': 'D14', '62': 'D15', '63': 'D16',
	'64': 'E1', '65': 'E2', '66': 'E3', '67': 'E4', '68': 'E5', '69': 'E6', '70': 'E7', '71': 'E8', '72': 'E9', '73': 'E10', '74': 'E11', '75': 'E12', '76': 'E13', '77': 'E14', '78': 'E15', '79': 'E16',
	'80': 'F1', '81': 'F2', '82': 'F3', '83': 'F4', '84': 'F5', '85': 'F6', '86': 'F7', '87': 'F8', '88': 'F9', '89': 'F10', '90': 'F11', '91': 'F12', '92': 'F13', '93': 'F14', '94': 'F15', '95': 'F16',
	'96': 'G1', '97': 'G2', '98': 'G3', '99': 'G4', '100': 'G5', '101': 'G6', '102': 'G7', '103': 'G8', '104': 'G9', '105': 'G10', '106': 'G11', '107': 'G12', '108': 'G13', '109': 'G14', '110': 'G15', '111': 'G16',
	'112': 'H1', '113': 'H2', '114': 'H3', '115': 'H4', '116': 'H5', '117': 'H6', '118': 'H7', '119': 'H8', '120': 'H9', '121': 'H10', '122': 'H11', '123': 'H12', '124': 'H13', '125': 'H14', '126': 'H15', '127': 'H16',
	'128': 'I1', '129': 'I2', '130': 'I3', '131': 'I4', '132': 'I5', '133': 'I6', '134': 'I7', '135': 'I8', '136': 'I9', '137': 'I10', '138': 'I11', '139': 'I12', '140': 'I13', '141': 'I14', '142': 'I15', '143': 'I16',
	'144': 'J1', '145': 'J2', '146': 'J3', '147': 'J4', '148': 'J5', '149': 'J6', '150': 'J7', '151': 'J8', '152': 'J9', '153': 'J10', '154': 'J11', '155': 'J12', '156': 'J13', '157': 'J14', '158': 'J15', '159': 'J16',
	'160': 'K1', '161': 'K2', '162': 'K3', '163': 'K4', '164': 'K5', '165': 'K6', '166': 'K7', '167': 'K8', '168': 'K9', '169': 'K10', '170': 'K11', '171': 'K12', '172': 'K13', '173': 'K14', '174': 'K15', '175': 'K16', 
	'176': 'L1', '177': 'L2', '178': 'L3', '179': 'L4', '180': 'L5', '181': 'L6', '182': 'L7', '183': 'L8', '184': 'L9', '185': 'L10', '186': 'L11', '187': 'L12', '188': 'L13', '189': 'L14', '190': 'L15', '191': 'L16',
	'192': 'M1', '193': 'M2', '194': 'M3', '195': 'M4', '196': 'M5', '197': 'M6', '198': 'M7', '199': 'M8', '200': 'M9', '201': 'M10', '202': 'M11', '203': 'M12', '204': 'M13', '205': 'M14', '206': 'M15', '207': 'M16',
	'208': 'N1', '209': 'N2', '210': 'N3', '211': 'N4', '212': 'N5', '213': 'N6', '214': 'N7', '215': 'N8', '216': 'N9', '217': 'N10', '218': 'N11', '219': 'N12', '220': 'N13', '221': 'N14', '222': 'N15', '223': 'N16',
	'224': 'O1', '225': 'O2', '226': 'O3', '227': 'O4', '228': 'O5', '229': 'O6', '230': 'O7', '231': 'O8', '232': 'O9', '233': 'O10', '234': 'O11', '235': 'O12', '236': 'O13', '237': 'O14', '238': 'O15', '239': 'O16',
	'240': 'P1', '241': 'P2', '242': 'P3', '243': 'P4', '244': 'P5', '245': 'P6', '246': 'P7', '247': 'P8', '248': 'P9', '249': 'P10', '250': 'P11', '251': 'P12', '252': 'P13', '253': 'P14', '254': 'P15', '255': 'P16', 
	}


REMOTES_SORT_ORDER = [2, 0, 1, 3]

REMOTE_IDS = {
    192: 1,
    208: 2,
    224: 3,
    240: 4,
    32: 5,
    48: 6,
    0: 7,
    16: 8,
    64: 9,
    80: 10,
    96: 11,
    112: 12,
    160: 13,
    176: 14,
    128: 15,
    144: 16,
}


class X10Events:
    plugin = None

    #@eg.LogIt
    def OnX10Command(
        self,
        bszCommand,
        eCommand,
        lAddress,
        eKeyState,
        lSequence,
        eCommandType,
        varTimestamp
    ):
        if eKeyState == 3:
            return
        plugin = self.plugin
        remoteId = REMOTE_IDS[lAddress & 0xF0]
        house_unit = HOUSE_UNITS[str(lAddress)]
        if remoteId not in plugin.ids:
            return
        event = str(bszCommand)
        if eKeyState == 1:
            plugin.TriggerEnduringEvent(
                plugin.mappingTable.get(event, event),
                payload=house_unit
            )
        elif eKeyState == 2:
            plugin.EndLastEvent()



class X10ThreadWorker(eg.ThreadWorker):
    comInstance = None
    plugin = None
    eventHandler = None

    def Setup(self, plugin, eventHandler):
        self.plugin = plugin
        self.eventHandler = eventHandler
        self.comInstance = DispatchWithEvents(
            'X10net.X10Control.1',
            eventHandler
        )


    def Finish(self):
        if self.comInstance:
            self.comInstance.Close()
            del self.comInstance



class X10(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddEvents()


    def __start__(self, remoteType=None, ids=None, prefix=None):
        self.remoteType = remoteType
        self.ids = ids
        self.info.eventPrefix = prefix
        self.mappingTable = REMOTES[remoteType][1]

        class SubX10Events(X10Events):
            plugin = self
        self.workerThread = X10ThreadWorker(self, SubX10Events)
        try:
            self.workerThread.Start(20)
        except:
            raise self.Exception(self.text.errorMesg)


    def __stop__(self):
        self.workerThread.Stop(10)


    def GetLabel(self, remoteType, *dummyArgs):
        return "X10: " + REMOTES[remoteType][0]


    def Configure(self, remoteType=2, ids=None, prefix="X10"):
        panel = eg.ConfigPanel()
        text = self.text
        fbtypes = []
        selection = 0
        for i, remoteId in enumerate(REMOTES_SORT_ORDER):
            fbtypes.append(REMOTES[remoteId][0])
            if remoteId == remoteType:
                selection = i
        remoteTypeCtrl = panel.Choice(selection, fbtypes)
        prefixCtrl = panel.TextCtrl(prefix)

        btnsizer = wx.FlexGridSizer(4, 4)
        idBtns = []
        for i in xrange(16):
            btn = wx.ToggleButton(panel, -1, size=(35, 35), label=str(i + 1))
            if (ids is None) or ((i+1) in ids):
                btn.SetValue(True)
            btnsizer.Add(btn)
            idBtns.append(btn)

        selectAllButton = panel.Button(text.allButton, style=wx.BU_EXACTFIT)
        def OnSelectAll(event):
            for item in idBtns:
                item.SetValue(True)
            event.Skip()
        selectAllButton.Bind(wx.EVT_BUTTON, OnSelectAll)

        selectNoneButton = panel.Button(text.noneButton, style=wx.BU_EXACTFIT)
        def OnSelectNone(event):
            for item in idBtns:
                item.SetValue(False)
            event.Skip()
        selectNoneButton.Bind(wx.EVT_BUTTON, OnSelectNone)

        rightBtnSizer = eg.VBoxSizer(
            (selectAllButton, 0, wx.EXPAND),
            ((5, 5), 1),
            (selectNoneButton, 0, wx.EXPAND),
        )
        idSizer = eg.HBoxSizer(
            (btnsizer),
            ((10, 10), 0),
            (rightBtnSizer, 0, wx.EXPAND),
        )
        leftSizer = eg.VBoxSizer(
            (panel.StaticText(text.remoteBox), 0, wx.BOTTOM, 2),
            (remoteTypeCtrl, 0, wx.BOTTOM, 10),
            (panel.StaticText(text.usePrefix), 0, wx.BOTTOM, 2),
            (prefixCtrl),
        )
        rightSizer = eg.VBoxSizer(
            (panel.StaticText(text.idBox), 0, wx.BOTTOM, 2),
            (idSizer),
        )
        mainSizer = eg.HBoxSizer(
            (leftSizer),
            ((0, 0), 1, wx.EXPAND),
            (wx.StaticLine(panel, style=wx.LI_VERTICAL), 0, wx.EXPAND),
            ((0, 0), 1, wx.EXPAND),
            (rightSizer),
            ((0, 0), 1, wx.EXPAND),
        )
        panel.sizer.Add(mainSizer, 1, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                REMOTES_SORT_ORDER[remoteTypeCtrl.GetValue()],
                [i+1 for i, button in enumerate(idBtns) if button.GetValue()],
                prefixCtrl.GetValue()
            )

