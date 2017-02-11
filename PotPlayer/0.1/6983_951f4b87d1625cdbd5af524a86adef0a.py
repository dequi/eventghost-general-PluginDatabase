#
# Plugins/PotPlayer/__init__.py
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


eg.RegisterPlugin(
    name = "PotPlayer",
    author = "Slack",
    version = "0.1",
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://en.wikipedia.org/wiki/PotPlayer">'
        'PotPlayer'
    ),
    help = """
        initial version of PotPlayer plugin by slack.
    """,
)
    
# changelog:
# - initial version



ACTIONS = (
(eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
    ('Exit', 'Quit Application', None, 57665),
    ('Play', 'Play', None, 20001),
    ('Pause', 'Pause', None, 20000),
    ('Stop', 'Stop', None, 20002),
    ('JumpForward5sec', 'Jump Forward 5 sec', None, 10060),
    ('JumpBackward5sec', 'Jump Backward 5 sec', None, 10059),
    ('JumpForward1min', 'Jump Forward 1 min', None, 10064),
    ('JumpBackward1min', 'Jump Backward 1 min', None, 10063),
    ('JumpForward5min', 'Jump Forward 5 min', None, 10066),
    ('JumpBackward5min', 'Jump Backward 5 min', None, 10065),
)),
(eg.ActionGroup, 'GroupViewModes', 'View modes', None, (
    ('Fullscreen', 'Fullscreen', None, 10013),
)),
(eg.ActionGroup, 'GroupExtendedControls', 'Extended controls', None, (
    ('OnOffSubtitle', 'On/Off Subtitle', None, 10126),
)),
)

from eg.WinApi import FindWindow, SendMessageTimeout, WM_COMMAND


class ActionPrototype(eg.ActionClass):
    
    def __call__(self):
        try:
            hWnd = FindWindow("PotPlayer")
            return SendMessageTimeout(hWnd, WM_COMMAND, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning
    


class PotPlayer(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)

