# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
#
# $LastChangedDate: 2009-02-07 12:13:27 -0700 (Sat, 07 Feb 2009) $
# $LastChangedRevision: 831 $
# $LastChangedBy: Bitmonster $

"""<rst>
This plugin generates events on SIMULATED keypresses (i.e. from VNC).

**Notice:** If such a keyboard event is assigned to a macro, the plugin will 
block the key, so Windows or another application will not see it anymore. This 
is needed to permit remapping of keys as otherwise the old key would reach the 
target in conjunction of another action you might want to do and this is 
mostly not what you intend.

But this blocking only happens, if a macro would actually execute in 
succession of the event. So if the macro or any of its parents is disabled, 
the keypress will pass through.
"""


import eg

eg.RegisterPlugin(
    name = "SimKey",
    author = "Brett Stottlemyer",
    version = "1.0." + "$LastChangedRevision: 831 $".split()[1],
    kind = "remote",
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QQIDBMjdIFglwAAADV0RVh0Q29t"
        "bWVudAAoYykgMjAwNCBKYWt1YiBTdGVpbmVyCgpDcmVhdGVkIHdpdGggVGhlIEdJTVCQ"
        "2YtvAAABfklEQVQ4y6WSv0sCYRjHP2+IGlI0GOeN4WQJQnd/gENbRHtTji2NIkhTROLa"
        "EATh0hpE0OTmKNzgQUpDFEhdmosNVw3d2yB3+HYXRX3h5Xnf7/v8fh7BL1CrHywASSAN"
        "uMAAeK2Uq56IUFwFtoAH4BG4AZ6BJ+AF+KiUq55vE/sS7Ai4Ag6Bh0q5+vZTdqJWP1gD"
        "mj/oWYARwe/EgObG+qZMpxcFgBACKSVCKNUZ/t80ThsnxzEATcuIfr//bXjbtslmlxQu"
        "lZpTe2DbtqKgaRqDwUDhEokG7+8lEokGsKs6KBQKOI6Drus4jkMmk0FKGbxvb+/IZkt4"
        "nsR93WZ+kgAzvoNpY13XGY/HigSIx5Mkk7Pc390TGuO0cZQE6PV6of4EDjqdDgDD4TBS"
        "AuRyOSzLYnllOeCCEkzTxHVdTNNUDkA+n8d13ck8DYPudTecQavVUuQ02u32ZJssK7qE"
        "0WhEsVhESomUEiB09zwvWDKf9x3sX1ye7/E3nPFffAJVOqjtMbQazAAAAABJRU5ErkJg"
        "gg=="
    ),
)


from eg import HasActiveHandler
from eg.cFunctions import SetSimKeyCallback

modKeys = set(["Shift","LShift","RShift","Ctrl","LCtrl","RCtrl","Win","LWin","RWin","Alt","RAlt","LAlt"])
class SimKey(eg.PluginBase):
    
    def __init__(self):
        self.AddEvents()
        
    
    def __start__(self, *dummyArgs):
        SetSimKeyCallback(self.SimKeyCallback)
        
        
    def __stop__(self):
        SetSimKeyCallback(None)
        
    def SimKeyCallback(self, codes, info):
        if codes == "":
            self.EndLastEvent()
        else:
            keys = set(codes.split("+")).difference(modKeys)
            if len(keys) == 0: #All keys are modifiers
                return False
            shouldBlock = HasActiveHandler("SimKey." + codes)
            self.TriggerEnduringEvent(codes)
            return shouldBlock
