# -*- coding: utf-8 -*-
version = "0.2.16"

# plugins/PushBullet/__init__.py
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
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
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# The BSD 3-Clause License (applies to parts of the code obtained from gcm.py)
# Copyright (c) <YEAR>, <OWNER>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2.16  by Pako 2016-06-05 06:39 GMT+1
#     - removed address and list pushes which have been deprecated for forever
# 0.2.15  by Pako 2016-02-07 19:04 GMT+1
#     - bugfix (sometime 'sender_email' parameter is missing)
# 0.2.14  by Pako 2015-12-24 20:38 GMT+1
#     - bugfix
# 0.2.13  by Pako 2015-12-12 20:39 GMT+1
#     - bugfixes
# 0.2.12  by Pako 2015-11-51 12:09 GMT+1
#     - 'sms_changed' handler added
#     - bugfixes
# 0.2.11  by Pako 2015-10-08 12:27 GMT+1
#     - icon (in mirrored notification) is now correctly displayed 
# 0.2.10  by Pako 2015-10-04 11:00 GMT+1
#     - now can be dismissed also a push (not only mirror)
# 0.2.9  by Pako 2015-10-03 13:07 GMT+1
#     - plugin now reacts to push of type 'dismissal'.
#     - added action "Dismiss"
#     - when you close a mirrored notification (using right click), 
#       push of type 'dismissal' is sent
# 0.2.8  by Pako 2015-09-24 12:43 GMT+1
#     - added opt. "Use the complete original push as last part of the payload"
# 0.2.7  by Pako 2015-09-15 12:36 GMT+1
#     - added "End to end encryption" support
#     - uses the first word out of the body as the event suffix (optionaly)
#     - added response to ping message
# 0.2.6  by Pako 2015-03-27 14:53 GMT+1
#     - photo of the sender is clipped into the shape of a circle
# 0.2.5  by Pako 2015-02-13 20:35 GMT+1
#     - bugfix - upload of non-ascii named file
# 0.2.4  by Pako 2015-01-28 20:35 GMT+1
#     - added action "Send bulk SMS to list from file"
# 0.2.3  by Pako 2015-01-25 13:06 GMT+1
#     - bugfix - missing getNmNr() function
# 0.2.2  by Pako 2015-01-23 09:06 GMT+1
#     - added action "Push to a single"
# 0.2.1  by Pako 2015-01-20 09:09 GMT+1
#     - bugfix (actions "Push reply" and "Push to everything" - GUI problem)
# 0.2.0  by Pako 2015-01-11 18:38 GMT+1
#     - code adapted to use the pycurl library instead of requests library
#     - (this was necessary because of changes pushbullet server certificate)
# 0.1.10  by Pako 2015-01-01 14:21 GMT+1
#     - added recipients groups (push and SMS)
#     - added WebSocketOpened and WebSocketClosed events
# 0.1.9  by Pako 2014-12-15 16:12 GMT+1
#     - bugfix (action "Send SMS to multiple recipients")
# 0.1.8  by Pako 2014-12-08 18:08 GMT+1
#     - added action "Send SMS to multiple recipients"
# 0.1.7  by Pako 2014-11-07 06:00 GMT+1
#     - bugfix
# 0.1.6  by Pako 2014-11-06 20:43 GMT+1
#     - bugfix
#     - multiload of plugin enabled
#     - added action "Send SMS"
# 0.1.5  by Pako 2014-10-22 12:43 GMT+1
#     - added option to push an image, obtained as clipboard content
# 0.1.4  by Pako 2014-10-03 19:38 GMT+1
#     - bugfixes
#     - better synchronization with the time of server
# 0.1.3  by Pako 2014-10-02 20:09 GMT+1
#     - quick bugfix
# 0.1.2  by Pako 2014-10-01 19:24 GMT+1
#     - added action "Push reply"
#     - added support of channels
# 0.1.1  by Pako 2014-09-29 09:58 GMT+1
#     - added action "Push screenshot"
# 0.1.0  by Pako 2014-08-30 08:40 GMT+1
#     - "websocket-client (websocket)" library used instead of "Tornado" library
#     - Reply dialog improved
# 0.0.25 by Pako 2014-08-22 10:48 GMT+1
#     - bugfix
# 0.0.24 by Pako 2014-08-21 20:00 GMT+1
#     - push type 'clip' is now supported
# 0.0.23 by Pako 2014-08-10 09:12 GMT+1
#     - event payload contains "push dictionary" always
#                                             (if it is a mirrored notification) 
# 0.0.22 by Pako 2014-08-02 17:19 GMT+1
#     - bugfix (action "Set popups") 
#     - fixed bug - when decoding escape sequences (mirrored notifications)
#     - fixed bug - when 'body' parameter is missing in push (type 'note')
# 0.0.21 by Pako 2014-07-11 12:44 GMT+1
#     - checkbox "Disable popping up of mirrored notification" changed to 
#                "Enable popping up of mirrored notification"
#     - added action "Set popups" (enables, disables or toggles popups)
#     - added action "Get states of popups"
#     - action Push - added "smart" button "Apply, push and close"
#     - an image of the sender (on "Quick-Reply" dialogue) is now better
#     - reply buttons are now accompanied by an icon
# 0.0.20 by Pako 2014-06-25 13:39 GMT+1
#     - better text wrapping of mirrored notification
#     - the ability to copy text from an incoming message in the Reply dialogue
#     - disabling / enabling of mirroring for each application works again
# 0.0.19 by Pako 2014-06-22 12:21 GMT+1
#     - first version for release r1669 and later (no need to install libraries)
#     - mirror notifications are customizable now (colour, monitor, alignment)
#     - introduced a new event "ReplyAllowingMirror"
#     - added an action "Send reply to mirror"
#     - if there is a possibility to send a reply,
#                        then on the mirror notification is a new button "Reply"
# 0.0.18 by Pako 2014-05-30 18:45 GMT+1
#     - bugfix (when the 'title' parameter is missing in the received "Mirror")
# 0.0.17 by Pako 2014-05-30 11:53 GMT+1
#     - http://www.eventghost.net/forum/viewtopic.php?f=9&t=5709&p=31230#p31226
# 0.0.16 by Pako 2014-05-27 12:57 GMT+1
#     - bugfix (when friend is not "active")
# 0.0.15 by Pako 2014-05-25 12:51 GMT+1
#     - "Mirror" as kind of Push now exists only in action "Push to everything"
# 0.0.14 by Pako 2014-05-25 10:01 GMT+1
#     - incoming "Mirror" is processed differently (enforced by the new API)
# 0.0.13 by Pako 2014-05-21 06:17 GMT+1
#     - forced change of url, used to test connectivity
# 0.0.12 by Pako 2014-05-19 10:55 GMT+1
#     - added option to delete pushes, sent using this plugin
# 0.0.11 by Pako 2014-05-19 07:55 GMT+1
#     - pyPushBullet module from Azelphur no longer needed
#     - fixed issue with sending pushes to friends
# 0.0.10 by Pako 2014-05-17 10:58 GMT+1
#     - changes induced by introducing a new API
#     - added action "Delete push"
# 0.0.9 by Pako 2014-05-01 14:24 GMT+1
#     - added new action "Push to everything"
#     - optional message for push types "Link" 
#                                            and "File/Picture" is now supported
# 0.0.8 by Pako 2014-04-18 17:04 GMT+1
#     - a pushed file can be defined using a variables now
# 0.0.7 by Pako 2014-04-15 16:43 GMT+1
#     - popping up of mirrored notification can now be disabled
# 0.0.6 by Pako 2014-04-13 09:20 GMT+1
#     - bugfix
#     - icons size 96x96 (if possible) are now using also when sending mirrors
# 0.0.5 by Pako 2014-04-11 11:25 GMT+1
#     - new SSL certificate for tornado lib 3.2 is valid
#     - icon with size 96x96 is now supported (mirroring)
# 0.0.4 by Pako 2014-03-26 10:04 GMT+1
#     - automatic opening of pictures is now optional feature
#     - added actions "Open file" and "Jump according to file extension"
#     - with the api_key is treated as with a password for more security
# 0.0.3 by Pako 2014-03-14 12:35 GMT+1
#     - 'not_user' excluded from friends
# 0.0.2 by Pako 2014-02-26 16:02 GMT+1
#     - added support for push to "All of my devices" (Tasker integration)
# 0.0.1 by Pako 2014-02-21 08:04 GMT+1
#     - websocket.py is no longer needed
#     - support url inserted
# 0.0.0 by Pako 2014-02-07 20:00 GMT+1
#     - first public version
#===============================================================================

eg.RegisterPlugin(
    name = "PushBullet",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{C92AD47A-B959-44D5-A849-9FCCCAAC9572}",
    createMacrosOnAdd = False,
    canMultiLoad = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACyUlEQVRYw+1XPUxUQRD+"
        "Zt/eu4M7ThQSiBgVvWgM2Jmo0YKCxIaChPgvFhTaohV2WkmnMTaaUBj0REiMhkQLCyuJ"
        "BitpTMSQIBoi4AXuwb2/3bEgHMcdx1+QZ8Ekr5ndN/vt983OzgLbFrARAOzuPFMfO1Td"
        "As76G7TWXcNnu58uOKpet9bFfdEkiCILPmYuFtfTWg8p3x8cufh8fEUA+x4075XlJUkj"
        "ap7KG+OZ6fTp8baXAwCQ6Gv9KAzjOOVOKA4AABiApRyvWzt+D0rkwMiFpMqfJMI1O2JG"
        "1CxfDpwkHM5OJErQ+tktE6a8LqPhJ0R0eX/yfKQAwEoRhCAjX651a0xkkCFqDWk8kiHz"
        "YaL3SmzNADY32ShCQrRqwrU9Ly6Fc5jNGvK/f5DxpkF0i+3J5i1nYFESUVFaVt1e2nY0"
        "FAgAAERMJypPHjx3oO8qiaAKkLkz3gTomAiwAh6zrYlEYAAArhIqVBsgAxQLl8SPSJ6v"
        "p1y0mK699K4/GaWQgTHAANhTHFwOKK112rEDA+D/yaRdy/0qA9n8jA1/OjNBrH/IVYXa"
        "RNHZU/AmZ6FmMiApPpMph6X2NUgQSBRePnrWzTYQrDSTNDa0tvYUVGoOKu2CXX++ZUpl"
        "+s2auCWd75MwoibkrtKlP7kKM9N2FoD724KMR5YFWrBZBuApaMeHshYXzXIREp9So1N9"
        "dud7ltAMlXag57ylQbReCshy4VoOaA19CYMBVaS0EKYcTt23k188AJA5FBdpWXOzh+eD"
        "b9xcNvRd9sSrBcdWngIbpvFMSOPxZMcHZ20A9BJaNrp1xYxRhOk2s9v78+Y7O3dQkqQ0"
        "a6SguVDKdGY4R45vACrXdfAEWdrX3fBUD5eVDPxqf6uWVbnqTmO9KUMtWLxsGliKrrGO"
        "N9mHScW9xrpSO9QExZFVrhiQgMdSDLEUg2M3+se333//tf0FeVUoa3993xsAAAAASUVO"
        "RK5CYII="
    ),
    description = ur'''<rst>
Sends/receives notifications (and links, pictures and files) 
to/from your Android device or browser (Chrome, Firefox) via PushBullet_.

Google account and PushBullet account (free) are required to use PushBullet_.

| Plugin uses libraries websocket-client_ and pyCurl_.
| Plugin also incorporates the majority of code from the file pbkdf2.py_
  and **gcm.py**.
| The file **gcm.py** is part of a project iphone-dataprotection_, 
  which is protected by a license `The BSD 3-Clause License`_.

Plugin version: %s

.. _PushBullet:                 https://www.pushbullet.com/
.. _websocket-client:           https://pypi.python.org/pypi/websocket-client
.. _pyCurl:                     http://pycurl.sourceforge.net/
.. _pbkdf2.py:                  https://www.dlitz.net/software/python-pbkdf2/
.. _iphone-dataprotection:      https://code.google.com/p/iphone-dataprotection/
.. _`The BSD 3-Clause License`: http://opensource.org/licenses/BSD-3-Clause
''' % version,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5709",
)

import wx.grid as gridlib
from time import sleep, strftime, time as ttime
from urllib2 import urlopen, URLError
from urllib import urlencode
from threading import Thread, currentThread
from base64 import b64encode, b64decode
from PIL import Image
from StringIO import StringIO
from os import urandom, startfile, remove as os_remove
from os.path import join, split, splitext, isdir, isfile
from os.path import abspath, dirname, basename, exists
from eg.WinApi.Dynamic import BringWindowToTop
from copy import deepcopy as cpy
from datetime import datetime as dt
from json import dumps, loads
from mimetypes import guess_type as mimetype
from socket import gethostname
from wx.lib.buttons import GenButton
from eg.WinApi.Utils import GetMonitorDimensions
from textwrap import fill
from wx.combo import ComboCtrl, ComboPopup
import pycurl
from ssl import CERT_NONE
from websocket import WebSocketApp
from ImageGrab import grab, grabclipboard
from locale import setlocale, strcoll, LC_ALL
from encodings import aliases
from codecs import open as openFile
from tempfile import mktemp
from shutil import copyfileobj, copy as sh_copy
from math import sqrt
from wx.lib.statbmp import GenStaticBitmap
from Crypto.Hash import HMAC, SHA256, SHA as SHA1
from Crypto.Cipher import AES
from Crypto.Util import strxor
from struct import pack, unpack
from binascii import b2a_hex
from hashlib import sha256
import logging

logging.basicConfig()
setlocale(LC_ALL, "")
SEP = "   <#>   "
ICON_DIR      = join(abspath(dirname(__file__.decode('mbcs'))), "icons")
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ACV           = wx.ALIGN_CENTER_VERTICAL
AVATAR        = (
    "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAIAAABt+uBvAAAACXBIWXMAAAsSAAALEgHS"
    "3X78AAAI2klEQVR42u2biVMTVxzH/bcEjyCorUen2mlnrHXs1E47ApH7KGC9piKgSBFU"
    "KgkhCVg71UFH6zE63If/Q0jCYRGBETw4w6bf9367myWxDCR5S1Z35jeZPd6R/ezv/d77"
    "/d5vNzm6g6asIps2/B8kuJiATEAmIBOQCSiBxQRkAjIBmYBMQAksJiATkAnIBPRpA2rq"
    "iubWxw+oqUuiX4i9UxYbF/WU7qqFPwlAyjPLXPDr7Am29AdbB4I3n4cEp7iIW2oxqqI/"
    "KT0BhdQBz4yDloGgqy949cnSb3+/L2qaTq+fPFbzCoIDnOIibqEAiqGwgom0ST9M+gEi"
    "g8LRSFCQxvZAqXvmUPm/Owv9W04MQpKtIaEruIUCpa6ZG+2BVoZJJoumdDNPegDSKo67"
    "L9jcLRXYX+8pGUq2ekAhJdeXlu9PK4iQfD9ubWXgPJ+XDKEKAKG6rVNXwyQckIbOMrTg"
    "4r25g6dHkzI9lhwvgUjN9+/Ig/gihN2iMiiMKqiI6mgETenGSCcNgu7gwUqcM9tzfNuy"
    "vcRFi4ZOtaLFRKRQEdXRCGekk8EWCIgmHYitYxlTUp7tNbQAz5zGH15FEIkmEhMdUEU0"
    "gqZa+4NoVu3CkIBIbHxkFTfPbM70pOb7tA+8OpowTBpYPjSFBtEsGBlbg8gqV7bNYnTQ"
    "s0VBJ4xRKse0NWuwom3W3S98rIkCxGdieXztPzkCQNFx+T9SaHBf2YhmlBkNkIMtedjg"
    "ymqYgtWAiY1adz6oR2gQzaJxmtQMpkH0Vpt7pGtPl3YV+i25Pq31iV2DaLSiWawk0QU6"
    "EmeqRWkQbDNcqtzG16Q+Kbne2NFoBQ2SEqELdGQTpkQiNahb+urM6LYs7xpn9PUrkR+N"
    "owuhfqwIQJK9axlO5uX785Zcb3zRRGJCF+gI3aFTEU5s/AFhQsHU2zIgnXS/gavFXSpv"
    "3BmhQTbK8pmjW+aeQXd8vjeIBtk6JNiFjPpJ+JmpBQI1CI2ji+N1E8wMdQgJg4jQINnz"
    "OnppPNk6KAKNVtDF95fGxXln8QeEVYm9S3L1Bg9fGMN6V10BidAgNI4u0BG6s/OAgSEA"
    "sTdJgLac8IoGhC4IkBqoTHRATV3LzEj3B49UvUzmRlr0EENHLbJTZgQNUo30T7UToo10"
    "Gox0pgcdGclIO9gyGkZaKnJM4/XSNC8CEDWLLood060DQsaXKA3Cmo1HOeaYEy94oYgu"
    "qu7OuQ20UGRmiM0mbE754uTIdoVR/F2NPB8aRxd88pKaxLhjonwxCiSm108mZQqZ6eWI"
    "h3UQXbDQohLGNwYgCC2Fah4sWHK82r2KeKmP7IjleNEFLYIEPYgoDXLwBRFm32OXX2Eu"
    "i2/Eg2IdMM8/VI/TBO8QtgUkLuTKbFBzj1T/ZJHTiSkgreqO8utj240FfjSOLuzCxpdA"
    "QFxYQBoGotT1JskqR11jD7kq1seDZpWNDQMG7TV6xAbaz7UTmzNCjKLb1VDpoCk02CJ+"
    "S0MsIG0GkKtXOnpxXMto7WNNuylGdNAUGtQne0i4BjmUjA5nr/RjzSt5c5VtPftW2Xde"
    "qTWsMJFFdTSCprTJNEbVIIWRSoqNNfgfeE5MQAomeXteq1AalWGnhIaqoDoa0dAR++f1"
    "ABQ21mBWrzya/65ibGuWF89s4XO/muahinoFBVAMhVGl9uG8NjBm+OSFSEaUAYV1HbSg"
    "qm3uWPX47qIhSp3CL0/eYIID9SIKoBgKowpbEOpLRz9AigapB5Kb5yU2PFs699c767Wp"
    "I5Uvvz734sCpEQgOcIqLuIUCKIbC2o0dPTMVNyCJUz2AOjTzDM6bzxmC5tCGGjvFRdxC"
    "Ae1c/nEncX5gxDFMoTzWFQVYJrCSErshaDYSUMS4k9RUKE1OlKQpsGGiKyDKiVF1RxW7"
    "okcr5APIggq1jwiQCiXEojM0pmBinL0sW9rdx+xOCxc3SR+btpw9ciMR6fehtaLxAClQ"
    "FAVRHszZG0qqx/M3dS03PAvUPV6qebBQdXfuwp3Z8tuQ9+V3ZnFafX/+yqPF608DcEfB"
    "EbVIUNHRHVQtl+gk/DgDCvvSQJ2n8GAs9PF48fzt94X2abgLh8rHvvx15LPiIcr0YSug"
    "bLYCIsEpLmLpvKvQv79s+JtzL+B/Wa9Pnbr5FuAa2wPA1MoT9R3KTpzab4IC0rqO6pcG"
    "eIyGp0tnb709Xjdx8MzozgI5qR6CxTEopOSG+2JpEe4YSPGlo5cqWnK8+0qHj1SMFdin"
    "L92bo9W5qy/8q44EAhSGxsmHg60jcPrPt3jt6loZD5mStyKpfu2xjpW1mLqBb5KVZaMf"
    "ODV64vpUNc+AITctvl91xApIi4YsRf2TRfzjPSVD9MIpPEqfFmjDOusKLZLXqnX9Q7Cy"
    "uU+X4z10fgyqylzigaA99M5iXUDFBCjMC4VbkF4/CRBJ/B+nacaLHNmIR6JrKGiv8Wxx"
    "Su8DCnX21juaASnM4ohtkRklIHX9xhWHJUMXN8/sKhpKyvTQxykU7oklAr32WJqqYuh0"
    "W5Z3i3Xw2/KxK48W4vJVR0waZON54n88WzpcMaZ+n8L+br5wNJE6pbnCtAm/Ze6Z1v4V"
    "JlInQGT88HJA5/d/5veWDrMsDjlIuNaPMMRhoq86oMh4Z5lXJ92xMVo3IOrD1rns6pVq"
    "Hy7sLvLT1zv6E1k9gJ3KMW3O9GTUT/HwfpRbQ9FoELM73dKN9sC+smGe5RvrhpcgRpTE"
    "CD36xSl/+aKTBtFODlbDyfH7xkAMI3Yc4xbj+gDRfikGF5awWIDs0GWqipEU36T2ZFyd"
    "pIEmXIPQB1Zi6XWTLDkqHpulwlWJ5zjAoaM9WOEaRFMY+8YgO2R9Ell2KPao5sG8s3fd"
    "SrRuQPht7FjeUzrM81oSd3CFGSP828q2WXefYA0iI2frDOwtHdqem9BowjBZsgcr2+Zc"
    "/eteCkWjQRjMWBzCpU5NYPO8EhBp0BxFRcQD6mSALMbRIAgBcuukQSYgE5AJyARkAjIB"
    "mYBMQIkjJiATkAnIBGQCSmAxAZmATEAmIEMC+g+GT7SO/uKwgAAAAABJRU5ErkJggg=="
)
#===============================================================================

BODY = {
    'type': 'stream',
    'manufacturer': 'EventGhost',
    'model': 'plugin by Pako',
    'icon': 'system',
    'app_version': int(version.replace(".","")),
    'key_fingerprint': None
    }
API  = 'https://api.pushbullet.com/v2/'
API3 = 'https://api.pushbullet.com/v3/'
DEFAULT_WAIT = 35.0
false = False
true = True
null = None
#===============================================================================

def getKeyFingerprint(key):
    if key is not None:
        hash = sha256()
        hash.update(key)
        return b64encode(hash.digest())


# obtained from gcm.py --- start
def inc32(block):
    counter, = unpack('>L', block[12:])
    counter += 1
    return block[:12] + pack('>L', counter)


def gcm_rightshift(vec):
    for x in range(15, 0, -1):
        c = vec[x] >> 1
        c |= (vec[x-1] << 7) & 0x80
        vec[x] = c
    vec[0] >>= 1
    return vec


def gcm_gf_mult(a, b):
    mask = [ 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01 ]
    poly = [ 0x00, 0xe1 ]
    Z = [0] * 16
    V = [c for c in a]
    for x in range(128):
        if b[x >> 3] & mask[x & 7]:
            Z = [V[y] ^ Z[y] for y in range(16)]
        bit = V[15] & 1
        V = gcm_rightshift(V)
        V[0] ^= poly[bit]
    return Z


def ghash(h, data):
    u = (16 - len(data)) % 16
    x = data + chr(0) * u
    x += pack('>QQ', 0, len(data) * 8)
    y = [0] * 16
    vec_h = [ord(c) for c in h]
    for i in range(0, len(x), 16):
        block = [ord(c) for c in x[i:i+16]]
        y = [y[j] ^ block[j] for j in range(16)]
        y = gcm_gf_mult(y, vec_h)
    return ''.join(chr(c) for c in y)


def gctr(k, icb, plaintext):
    y = ''
    if len(plaintext) == 0:
        return y
    aes = AES.new(k)
    cb = icb
    for i in range(0, len(plaintext), aes.block_size):
        cb = inc32(cb)
        encrypted = aes.encrypt(cb)
        plaintext_block = plaintext[i:i+aes.block_size]
        y += strxor.strxor(plaintext_block, encrypted[:len(plaintext_block)])
    return y


def gcm_decrypt(k, msg):   
    bmsg=b64decode(msg)
    version = bmsg[0]
    tag = bmsg[1:17] # 128 bits
    iv = bmsg[17:29] # 96 bits
    encrypted = bmsg[29:]
    if version != "1":
        return
    aes = AES.new(k)
    y0 = iv + "\x00\x00\x00\x01"
    decrypted = gctr(k, y0, encrypted)
    return decrypted


def gcm_encrypt(k, plaintext):
    aes = AES.new(k)
    h = aes.encrypt(chr(0) * aes.block_size)
    iv = urandom(12)
    y0 = iv + "\x00\x00\x00\x01"
    encrypted = gctr(k, y0, plaintext)
    s = ghash(h, encrypted)
    t = aes.encrypt(y0)
    tag = strxor.strxor(s, t)
    res = "1"+tag+iv+encrypted
    return b64encode(res)
# obtained from gcm.py --- end
#-------------------------------------------------------------------------------

# part of pbkdf2.py --- start 
_0xffffffffL = long(1) << 32
def isunicode(s):
    return isinstance(s, unicode)
def isbytes(s):
    return isinstance(s, str)
def isinteger(n):
    return isinstance(n, (int, long))
def b(s):
    return s
def binxor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

class PBKDF2(object):
    """PBKDF2.py : PKCS#5 v2.0 Password-Based Key Derivation

    This implementation takes a passphrase and a salt (and optionally an
    iteration count, a digest module, and a MAC module) and provides a
    file-like object from which an arbitrarily-sized key can be read.

    If the passphrase and/or salt are unicode objects, they are encoded as
    UTF-8 before they are processed.

    The idea behind PBKDF2 is to derive a cryptographic key from a
    passphrase and a salt.

    PBKDF2 may also be used as a strong salted password hash.  The
    'crypt' function is provided for that purpose.

    Remember: Keys generated using PBKDF2 are only as strong as the
    passphrases they are derived from.
    """

    def __init__(self, passphrase, salt, iterations=1000,
                 digestmodule=SHA1, macmodule=HMAC):
        self.__macmodule = macmodule
        self.__digestmodule = digestmodule
        self._setup(passphrase, salt, iterations, self._pseudorandom)

    def _pseudorandom(self, key, msg):
        """Pseudorandom function.  e.g. HMAC-SHA1"""
        return self.__macmodule.new(key=key, msg=msg,
            digestmod=self.__digestmodule).digest()

    def read(self, bytes):
        """Read the specified number of key bytes."""
        if self.closed:
            raise ValueError("file-like object is closed")

        size = len(self.__buf)
        blocks = [self.__buf]
        i = self.__blockNum
        while size < bytes:
            i += 1
            if i > _0xffffffffL or i < 1:
                # We could return "" here, but
                raise OverflowError("derived key too long")
            block = self.__f(i)
            blocks.append(block)
            size += len(block)
        buf = b("").join(blocks)
        retval = buf[:bytes]
        self.__buf = buf[bytes:]
        self.__blockNum = i
        return retval

    def __f(self, i):
        # i must fit within 32 bits
        assert 1 <= i <= _0xffffffffL
        U = self.__prf(self.__passphrase, self.__salt + pack("!L", i))
        result = U
        for j in xrange(2, 1+self.__iterations):
            U = self.__prf(self.__passphrase, U)
            result = binxor(result, U)
        return result

    def hexread(self, octets):
        """Read the specified number of octets. Return them as hexadecimal.

        Note that len(obj.hexread(n)) == 2*n.
        """
        return b2a_hex(self.read(octets))

    def _setup(self, passphrase, salt, iterations, prf):
        # Sanity checks:
        # passphrase and salt must be str or unicode (in the latter
        # case, we convert to UTF-8)
        if isunicode(passphrase):
            passphrase = passphrase.encode("UTF-8")
        elif not isbytes(passphrase):
            raise TypeError("passphrase must be str or unicode")
        if isunicode(salt):
            salt = salt.encode("UTF-8")
        elif not isbytes(salt):
            raise TypeError("salt must be str or unicode")

        # iterations must be an integer >= 1
        if not isinteger(iterations):
            raise TypeError("iterations must be an integer")
        if iterations < 1:
            raise ValueError("iterations must be at least 1")

        # prf must be callable
        if not callable(prf):
            raise TypeError("prf must be callable")

        self.__passphrase = passphrase
        self.__salt = salt
        self.__iterations = iterations
        self.__prf = prf
        self.__blockNum = 0
        self.__buf = b("")
        self.closed = False

    def close(self):
        """Close the stream."""
        if not self.closed:
            del self.__passphrase
            del self.__salt
            del self.__iterations
            del self.__prf
            del self.__blockNum
            del self.__buf
            self.closed = True
 # part of pbkdf2.py --- end
#-------------------------------------------------------------------------------

def check(num):
    num = num.replace(" ", "").replace("(", "").replace(")","").replace("-","")
    if num[0] == "+":
        front = "+"
        num = num[1:]
    else:
        front = ""
    tmp = [c for c in num if c >= "0" and c <= "9"]
    if len(tmp) != len(num):
        return
    return front + num


def getNmNr(recip):
    return ("", recip.strip()) if SEP not in recip else \
        (recip.split(SEP)[0].strip(),recip.split(SEP)[1].strip())


def AlignLeft(width, offset):
    return offset


def AlignCenter(width, offset):
    return (width / 2) + offset


def AlignRight(width, offset):
    return width - offset


ALIGNMENT_FUNCS = (
    (AlignLeft, AlignLeft), # Top Left
    (AlignRight, AlignLeft), # Top Right
    (AlignLeft, AlignRight), # Bottom Left
    (AlignRight, AlignRight), # Bottom Right
    (AlignCenter, AlignCenter), # Screen Center
    (AlignCenter, AlignRight), # Bottom Center
    (AlignCenter, AlignLeft), # Top Center
    (AlignLeft, AlignCenter), # Left Center
    (AlignRight, AlignCenter), # Right Center
)


def pilToBitmap(pil):
    img = wx.EmptyImage(pil.size[0], pil.size[1])
    img.SetData( pil.convert( "RGB").tostring())
    if pil.mode in ('RGBA', 'LA') or \
        (pil.mode == 'P' and 'transparency' in pil.info):
            img.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    return img.ConvertToBitmap()


def imageToPil(img):
    w, h = img.GetWidth(), img.GetHeight()
    data = img.GetData()
    pil = Image.new('RGB', (w, h))
    pil.fromstring(data)
    if img.HasAlpha():
        aPil = Image.new("L", (w, h))
        aPil.fromstring(img.GetAlphaData())
        pil = Image.merge('RGBA', pil.split() + (aPil,))
    return pil
        

def resize(pil, newSize):
    w, h = pil.size
    if w > newSize or h > newSize:
        factor = max(w, h) / float(newSize)
        m = int(min(w, h) / factor) 
        w, h = (newSize, m) if w >= h else (m, newSize)     
        pil = pil.resize((w, h), Image.ANTIALIAS)
    image = Image.new('RGBA', (newSize, newSize))
    image.paste(pil, ((newSize - w) / 2, (newSize - h) / 2))
    return image


def grayed(bmp):
    img = bmp.ConvertToImage()
    pilImg = Image.new( 'RGB', (img.GetWidth(), img.GetHeight()) )
    pilImg.fromstring(img.GetData())
    pilImg = pilImg.convert("L")
    m = pilImg.load()
    s = pilImg.size
    for x in xrange(s[0]):
        for y in xrange(s[1]):
            g = m[x, y] 
            if g > 0xf0:
                g = 0xf0
            elif g < 0xc0:
                g = 0xc0
            m[x, y] = g
    return pilToBitmap(pilImg)


def grdnt(r, d):
    w = 0.20
    if d/r < 1 - w:
        return 255
    elif d > r:
        return 0
    return int(0.5 + 255*(r - d)/(r*w))


def FluffyCircleMask(sz):
    r = sz/2
    data = []
    for x in range(sz):
        tmp = sz*[chr(0)]
        for y in range(sz):
            dist = sqrt((x - r)**2 + (y - r)**2)
            alph = grdnt(r, dist)
            tmp[y] = chr(alph)
        row = "".join(tmp)
        data.append(row)
    strng = "".join(data)
    return strng


def getIcon(err, icon = None):
    icon = icon if icon else join(eg.Icons.IMAGES_PATH, "logo.png")
    if isfile(icon):
        try:
            pil = Image.open(icon)
        except:
            eg.PrintError(err % icon)
            pil = Image.open(join(eg.Icons.IMAGES_PATH, "logo.png"))
    else:
        try:
            pil = Image.open(StringIO(b64decode(icon)))
        except:
            eg.PrintError(err % icon[:128])
            pil = Image.open(join(eg.Icons.IMAGES_PATH, "logo.png"))
    w, h = pil.size
    if w > 96 or h > 96:
        factor = max(w, h) / 96.0
        x = int(min(w, h) / factor) 
        size = (96, x) if w >= h else (x, 96)     
        pil = pil.resize(size, Image.ANTIALIAS)
        image = Image.new('RGBA', (96, 96))
        image.paste(pil, ((96 - size[0]) / 2, (96 - size[1]) / 2))
        pil = image
    io_file = StringIO()
    #pil.save(io_file, format = 'PNG')
    pil.save(io_file, format = 'JPEG')
    io_file.seek(0)
    data = io_file.read()
    return b64encode(data)


def connectivity():
    try:
        response = urlopen('http://www.google.com', timeout = 1)
        return True
    except URLError as err:
        pass
    return False


def wrap(txt, width):
    txt = txt.rstrip()
    lst = txt.splitlines()
    for i, item in enumerate(lst):
        lst[i] = fill(item, width)
    txt = "\n".join(lst)
    return txt
 #===============================================================================

class StaticBitmap(GenStaticBitmap):
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        if self._bitmap:
            dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
            dc.Clear()
            dc.DrawBitmap(self._bitmap, 0, 0, True)
#===============================================================================

class PushGroupDialog(wx.Frame):
    oldSel = 0

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name="Push group dialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.groups = cpy(self.panel.pushGroups)


    def ShowPushGroupsDlg(self):
        text = self.plugin.text
        self.SetTitle(text.pushGroupsTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer = wx.FlexGridSizer(4, 2, 2, 8)
        leftSizer.AddGrowableCol(0)
        leftSizer.AddGrowableRow(1)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(self, -1, text.groupsList)
        listBoxCtrl = wx.ListBox(
            self,-1,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(self, -1, text.groupLabel)
        labelCtrl=wx.TextCtrl(self, -1, '')
        leftSizer.Add(previewLbl, 0, wx.TOP, 5)
        leftSizer.Add((1, 1))
        leftSizer.Add(listBoxCtrl, 1, wx.TOP|wx.EXPAND, 1)
        leftSizer.Add(topMiddleSizer, 0, wx.TOP, 1)
        leftSizer.Add(labelLbl, 0, wx.TOP, 3)
        leftSizer.Add((1, 1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1, 1))

        w1 = self.GetTextExtent(text.delete)[0]
        w2 = self.GetTextExtent(text.insert)[0]
        w = max(w1,w2)+24
        btnApp=wx.Button(self,-1,text.insert,size = (w, -1))
        btnDEL=wx.Button(self,-1,text.delete,size = (w, -1))
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnApp)
        topMiddleSizer.Add(btnDEL, 0, wx.TOP, 5)

        tmp = []
        for t in self.plugin.targets:
            tmp.append([t[0], t[1], t[2], False])
        items = [n[0] for n in tmp]
        tsCtrl = wx.CheckListBox(
            self,
            -1,
            choices = items,
        )
        rightSizer.Add(tsCtrl, 1, wx.EXPAND)

        def EvtCheckListBox(event):
            index = event.GetSelection()
            label = tsCtrl.GetString(index)
            tmp = [list(itm) for itm in self.plugin.targets]
            for i, item in enumerate(tmp):
                tmp[i].append(tsCtrl.IsChecked(i))
            self.groups[self.oldSel][1] = tmp
            tsCtrl.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
            validation()

        tsCtrl.Bind(wx.EVT_CHECKLISTBOX, EvtCheckListBox)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)    
        mainSizer.Add(leftSizer, 1, wx.EXPAND)
        mainSizer.Add(rightSizer, 1, wx.EXPAND|wx.LEFT, 10)        
        sizer.Add(mainSizer, 1, wx.ALL|wx.EXPAND, 10)
        line = wx.StaticLine(self, -1, size=(20,-1), style = wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,5))
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())


        def setValue(item):
            labelCtrl.ChangeValue(item[0])
            ts = item[1]
            tmp = []
            lst_1 = [i[1] for i in ts]
            for ix, t in enumerate(self.plugin.targets):
                tmp.append(list(t))
                if t[1] in lst_1:
                    iy = lst_1.index(t[1])
                    tmp[ix].append(ts[iy][3])
                else:
                    tmp[ix].append(False)
                tsCtrl.Check(ix, tmp[ix][3])
            tsCtrl.Enable(True)

        if len(self.groups) > 0:
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(0)
            setValue(self.groups[0])
            self.oldSel = 0
            btnDEL.Enable(True)
        else:
            labelLbl.Enable(False)
            labelCtrl.Enable(False)
            btn1.Enable(False)
            tsCtrl.Enable(False)
  
        sizer.Layout()
        self.MakeModal(True)
        self.SetFocus()
        self.Center()
        self.Show()

        def onClose(evt):
            self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
        
        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)
        
        def onOK(evt):
            self.panel.pushGroups = self.groups
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)
        
        def validation():
            while True:
                flag = True
                label = labelCtrl.GetValue()
                if label == '':
                    flag = False
                if len(self.groups) > 0:
                    strings = listBoxCtrl.GetStrings()
                    for lbl in strings:
                        if lbl == '':
                            flag = False
                            break
                    if strings.count(label) != 1:
                        flag = False
                        break
                sel = self.oldSel
                break
            btn1.Enable(flag)
            btnApp.Enable(flag)

        def OnTxtChange(evt):
            if self.groups<>[]:
                sel = self.oldSel
                label = labelCtrl.GetValue()
                self.groups[sel][0]=label
                listBoxCtrl.Set([n[0] for n in self.groups])
                listBoxCtrl.SetSelection(sel)
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            if self.oldSel != sel:
                self.oldSel = sel
                item = self.groups[sel]
                setValue(item)
                listBoxCtrl.SetSelection(self.oldSel)
                listBoxCtrl.SetFocus()
            #evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonDelete(evt):
            lngth=len(self.groups)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.groups=[]
                listBoxCtrl.Set([])
                item = ['', []]
                setValue(item)
                labelLbl.Enable(False)
                labelCtrl.Enable(False)
                tsCtrl.Enable(False)
                btn1.Enable(True)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.groups.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(sel)
            item = self.groups[sel]
            setValue(item)
            validation()
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            labelLbl.Enable(True)
            labelCtrl.Enable(True)
            tsCtrl.Enable(False)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['', []]
            self.groups.insert(sel, item)
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)
#===============================================================================

class SmsGroupDialog(wx.Frame):
    oldSel = 0

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name="SMS group dialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.groups = cpy(self.panel.smsGroups)


    def ShowSmsGroupsDlg(self):
        text = self.plugin.text
        self.SetTitle(text.smsGroupsTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer = wx.FlexGridSizer(4, 2, 2, 8)
        leftSizer.AddGrowableCol(0)
        leftSizer.AddGrowableRow(1)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(self, -1, text.groupsList)
        listBoxCtrl = wx.ListBox(
            self,-1,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(self, -1, text.groupLabel)
        labelCtrl=wx.TextCtrl(self, -1, '')
        leftSizer.Add(previewLbl, 0, wx.TOP, 5)
        leftSizer.Add((1, 1))
        leftSizer.Add(listBoxCtrl, 1, wx.TOP|wx.EXPAND, 1)
        leftSizer.Add(topMiddleSizer, 0, wx.TOP, 1)
        leftSizer.Add(labelLbl, 0, wx.TOP, 3)
        leftSizer.Add((1, 1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1, 1))

        w1 = self.GetTextExtent(text.delete)[0]
        w2 = self.GetTextExtent(text.insert)[0]
        w = max(w1,w2)+24
        btnApp=wx.Button(self,-1,text.insert,size = (w, -1))
        btnDEL=wx.Button(self,-1,text.delete,size = (w, -1))
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnApp)
        topMiddleSizer.Add(btnDEL, 0, wx.TOP, 5)

        try:
            choices = list(self.plugin.getSMSdevices().iterkeys())
        except:
            choices = []
        ctrlDev = wx.Choice(self, -1, choices = choices)
        lblDev = wx.StaticText(self, -1, text.device)
        staticBox = wx.StaticBox(self, -1, "")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        bottomSizer = wx.FlexGridSizer(2, 2, 10, 10)
        bottomSizer.AddGrowableCol(1)
        listCtrl = Table(
            self,
            text.header,
            3,
            ("DevName","Recipient name","XXXXXXXXXXXXXXXX")
        )
        lblRec = wx.StaticText(self, -1, text.recip)
        ctrlRec = PhonebookChoice(
            self,
            -1,
            [],
            self.plugin,
            "",
        )
        btnAdd = wx.Button(self, -1, text.insert)
        btnDel = wx.Button(self, -1, text.delete)
        btnDel.Enable(False)
        btnSizer.Add(btnAdd)
        btnSizer.Add(btnDel, 0, wx.TOP, 10)
        topSizer.Add(listCtrl, 1, wx.EXPAND)
        topSizer.Add(btnSizer, 0, wx.LEFT, 10)
        staticBoxSizer.Add(topSizer, 1, wx.EXPAND)
        bottomSizer.Add(lblDev, 0, ACV)
        bottomSizer.Add(ctrlDev, 0, wx.EXPAND)
        bottomSizer.Add(lblRec, 0, ACV)
        bottomSizer.Add(ctrlRec, 0, wx.EXPAND)
        staticBoxSizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP, 10)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND)        
        mainSizer.Add(leftSizer, 1, wx.EXPAND)
        mainSizer.Add(rightSizer, 2, wx.EXPAND|wx.LEFT, 10)        
        sizer.Add(mainSizer, 1, wx.ALL|wx.EXPAND, 10)
        line = wx.StaticLine(self, -1, size=(20,-1), style = wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,5))
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())

        def setRow():
            dev = ctrlDev.GetStringSelection()
            nm, nr = getNmNr(ctrlRec.GetSel())
            listCtrl.SetRow((dev, nm, nr))
            self.groups[self.oldSel][1] = listCtrl.GetData()
            validation()

        def onDev(evt):
            dev = ctrlDev.GetStringSelection()
            phbook = self.plugin.getPhonebook(dev)
            rcp = ctrlRec.GetValue()
            ctrlRec.Set(phbook)
            if rcp:
                ctrlRec.SetValue(rcp)
            setRow()
            evt.Skip()
        ctrlDev.Bind(wx.EVT_CHOICE, onDev)

        def onRec(evt):
            setRow()
            evt.Skip()
        ctrlRec.Bind(wx.EVT_COMBOBOX, onRec)

        def onSelect(evt):
            dev, nm, nr = listCtrl.GetRow()
            if dev != ctrlDev.GetStringSelection():
                if dev in ctrlDev.GetStrings():
                    ctrlDev.SetStringSelection(dev)
                    phbook = self.plugin.getPhonebook(dev)
                    ctrlRec.Set(phbook)
            ctrlRec.SetValue(nm + SEP + nr if nr != "" and nm != "" else nr)
            evt.Skip()
        listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, onSelect)

        def enablePart(enable = None):
            selCnt = listCtrl.GetSelectedItemCount()
            enable = selCnt > 0 if enable is None else enable
            if not enable:
                ctrlRec.SetValue("")
            btnDel.Enable(enable)
            ctrlRec.Enable(enable)
            ctrlDev.Enable(enable)
            lblRec.Enable(enable)
            lblDev.Enable(enable)

        def onChange(evt = None):
            enablePart()
            if evt:
                evt.Skip()
        listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, onChange)
        listCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, onChange)
        onChange()

        def onDelete(evt):
            listCtrl.DeleteItem(listCtrl.GetSelectedIndex())
            setRow()
            validation()
            evt.Skip()
        btnDel.Bind(wx.EVT_BUTTON, onDelete)

        def onAdd(evt):
            listCtrl.AddRow()
            if ctrlDev.GetStringSelection():
                setRow()
            evt.Skip()
        btnAdd.Bind(wx.EVT_BUTTON, onAdd)

        def enableBox(enable):
            listCtrl.Enable(enable)
            btnAdd.Enable(enable)
            if enable:
                enablePart()
            else:
                enablePart(False)

        def setValue(item):
            labelCtrl.ChangeValue (item[0])
            listCtrl.SetData(item[1])
            enableBox(True)

        if len(self.groups) > 0:
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(0)
            setValue(self.groups[0])
            self.oldSel = 0
            btnDEL.Enable(True)
        else:
            labelLbl.Enable(False)
            labelCtrl.Enable(False)
            btn1.Enable(False)
            enableBox(False)
  
        sizer.Layout()
        self.MakeModal(True)
        self.SetFocus()
        self.Center()
        self.Show()

        def onClose(evt):
            self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
        
        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)
        
        def onOK(evt):
            self.panel.smsGroups = self.groups
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)
        
        def validation():
            while True:
                flag = True
                label = labelCtrl.GetValue()
                if label == '':
                    flag = False
                if len(self.groups) > 0:
                    strings = listBoxCtrl.GetStrings()
                    for lbl in strings:
                        if lbl == '':
                            flag = False
                            break
                if strings.count(label) != 1:
                    flag = False
                    break
                sel = self.oldSel
                data = listCtrl.GetData()
                if len(data) == 0: 
                    flag = False
                    break
                else:
                    for rowData in data:
                        if rowData[2] == "":
                            flag = False
                break
            btn1.Enable(flag)
            btnApp.Enable(flag)

        def OnTxtChange(evt):
            if self.groups<>[]:
                sel = self.oldSel
                label = labelCtrl.GetValue()
                self.groups[sel][0]=label
                listBoxCtrl.Set([n[0] for n in self.groups])
                listBoxCtrl.SetSelection(sel)
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            if self.oldSel != sel:
                self.oldSel = sel
                item = self.groups[sel]
                setValue(item)
                listBoxCtrl.SetSelection(self.oldSel)
                listBoxCtrl.SetFocus()
            #evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonDelete(evt):
            lngth=len(self.groups)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.groups=[]
                listBoxCtrl.Set([])
                item = ['', []]
                setValue(item)
                labelLbl.Enable(False)
                labelCtrl.Enable(False)
                enableBox(False)
                btn1.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.groups.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(sel)
            item = self.groups[sel]
            setValue(item)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            labelLbl.Enable(True)
            labelCtrl.Enable(True)
            enableBox(False)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['', []]
            self.groups.insert(sel, item)
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)
#===============================================================================

class CheckListComboBox(ComboCtrl):

    class CheckListBoxComboPopup(ComboPopup):

        def __init__(self, values, helpText):
            ComboPopup.__init__(self)
            self.values = values
            self.helpText = helpText

        def OnDclick(self, evt):
            self.Dismiss()
            self.SetHelpText()

        def Init(self):
            self.curitem = None
            self.data = None

        def Create(self, parent):
            self.lb = wx.CheckListBox(parent, -1, (80, 50), wx.DefaultSize)
            self.itemHeight = self.lb.GetItemHeight()
            self.SetValue(self.values)
            self.SetHelpText()
            self.lb.Bind(wx.EVT_MOTION, self.OnMotion)
            self.lb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.lb.Bind(wx.EVT_LEFT_DCLICK, self.OnDclick)

        def SetHelpText(self, helpText = None):
            self.helpText = helpText if helpText is not None else self.helpText
            combo = self.GetCombo()
            combo.SetText(self.helpText)
            combo.TextCtrl.SetEditable(False)

        def SetValue(self, values):
            self.lb.Set(values[0])
            self.data = values[2] if len(values) == 3 else None
            for i in range(len(values[1])):
                self.lb.Check(i, int(values[1][i]))

        def GetValue(self):
            strngs = self.lb.GetStrings()
            flags = [self.lb.IsChecked(i) for i in range(len(strngs))]
            return [strngs, flags] if self.data is None else [
                strngs, flags, self.data
            ]

        def GetControl(self):
            return self.lb

        def OnPopup(self):
            if self.curitem:
                self.lb.EnsureVisible(self.curitem)
                self.lb.SetSelection(self.curitem)

        def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
            return wx.Size(
                minWidth,
                min(self.itemHeight*(0.5+len(self.lb.GetStrings())), maxHeight)
            )

        def OnMotion(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.lb.SetSelection(item)
                self.curitem = item
            evt.Skip()

        def OnLeftDown(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.curitem = item
            evt.Skip()


    def __init__(self, parent, id=-1, values=[[],[]], **kwargs):
        if 'helpText' in kwargs:
            helpText = kwargs['helpText']
            del kwargs['helpText']
        else:
            helpText = ""
        ComboCtrl.__init__(self, parent, id, **kwargs)
        self.popup = self.CheckListBoxComboPopup(values, helpText)
        self.SetPopupControl(self.popup)
        self.popup.lb.Bind(wx.EVT_CHECKLISTBOX, self.onCheck)


    def onCheck(self, evt):
        wx.PostEvent(self, evt)
        evt.StopPropagation()


    def GetValue(self):
        return self.popup.GetValue()


    def SetValue(self, values):
        self.popup.SetValue(values)


    def SetHelpText(self, helpText = None):
        self.popup.SetHelpText(helpText)
#===============================================================================

class FlatButton(GenButton):

    def __init__(
        self,
        parent = None,
        id = -1,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        idleBmp = None,
        activeBmp = None,
        label = None,
        radius = 5,
        idleTextClr = "#FFFFFF",
        activeTextClr = "#FFFFFF",
        idleBackClr = "#27ae60",
        activeBackClr = "#2ecc71",
        font = None,
        bmpIndent = None,
        lblIndent = None
    ):
        GenButton.__init__(self, parent, -1, "", pos, size, 0)
        self.font = font
        self.radius = radius
        self.idleTextClr = idleTextClr
        self.activeTextClr = activeTextClr
        self.idleBackClr = idleBackClr
        self.activeBackClr = activeBackClr
        self.idleBmp = idleBmp
        self.activeBmp = activeBmp if activeBmp else idleBmp
        self.label = label
        self.bmpIndent = bmpIndent
        self.lblIndent = lblIndent
        self.state = False
        self.mouse = False
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)


    def onPaint(self, evt):
        if self.state:
            backClr = self.activeBackClr
            textClr = self.activeTextClr
            bmp = self.activeBmp
        else:
            backClr = self.idleBackClr
            textClr = self.idleTextClr
            bmp = self.idleBmp
        width, height = self.GetSize()
        if bmp:
            if exists(bmp):
                try:
                    wxBmp = wx.Image(bmp, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                    bw, bh = wxBmp.GetWidth(), wxBmp.GetHeight()
                except:
                    wxBmp = None
            else:
                try:
                    pil = Image.open(StringIO(b64decode(bmp)))
                    hasAlpha = (pil.mode in ('RGBA', 'LA') \
                        or (pil.mode == 'P' and 'transparency' in pil.info))
                    image = wx.EmptyImage(*pil.size)
                    rgbPil = pil.convert('RGB')
                    if hasAlpha:
                        image.SetData(rgbPil.tostring())
                        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
                    else:
                        new_image = rgbPil
                        data = new_image.tostring()
                        image.SetData(data)
                    wxBmp = image.ConvertToBitmap()                                        
                    bw, bh = wxBmp.GetWidth(), wxBmp.GetHeight()
                except:
                    wxBmp = None
            if self.bmpIndent is None:
                tmpy = (bh+2*self.radius-height)/2
                self.bmpIndent = self.radius-sqrt(self.radius**2-tmpy**2) \
                    if (tmpy > 0 and self.radius > tmpy) else 0
                self.bmpIndent = max(5, self.bmpIndent)
                if not self.label:
                    self.bmpIndent = (width-bw)/2
        else:
            wxBmp = None

        if self.label:
            if self.font is None:
                self.font = wx.Font(
                    12,
                    wx.FONTFAMILY_SWISS,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    False,
                    u'Arial'
                )
            self.SetFont(self.font)
            tw, th = self.GetTextExtent(self.label)
            if self.lblIndent is None:
                if wxBmp:
                    self.lblIndent = (width-tw-bw-self.bmpIndent)/2
                else:
                    self.lblIndent = (width-tw)/2
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        path = gc.CreatePath()
        path.AddRoundedRectangle(0, 0, width, height, self.radius)
        path.CloseSubpath()
        gc.SetBrush(wx.Brush(backClr))
        gc.FillPath(path)
        dc.SetTextForeground(textClr)
        if wxBmp:
            dc.DrawBitmap(wxBmp, self.bmpIndent, (height-bh)/2)
        if self.label:
            dc.SetFont(self.font)
            lblPos = self.lblIndent if not wxBmp \
                else bw+self.bmpIndent+self.lblIndent
            dc.DrawText(self.label, lblPos, (height-th)/2)


    def onMouseDown(self, evt):
        if self.mouse:
            self.state = False
        self.Refresh()
        evt.Skip()


    def onMouseUp(self, evt):
        if self.mouse:
            self.state = True
        self.Refresh()
        evt.Skip()


    def onEnter(self, evt):
        self.mouse = True
        self.state = True
        self.Refresh()
        evt.Skip()


    def onLeave(self, evt):
        self.mouse = False
        self.state = False
        self.Refresh()
        evt.Skip()
#===============================================================================

class WebSocketClient(WebSocketApp):
    def __init__(self, url, plugin):
        WebSocketApp.__init__(
            self,
            url,
            on_open = plugin.on_open,
            on_message = plugin.on_message,
            on_error = self.on_error,
            on_close = self.on_close
        )
        self.plugin = plugin
        

    def on_error(self, _, error):
        eg.PrintError(self.plugin.text.wsError % error)
        self.plugin.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.plugin.watcher)


    def on_close(self, _):
        self.plugin.TriggerEvent(self.plugin.text.wsClosedEvt)


    def start(self):
        #self.run_forever(sslopt = {"cert_reqs": CERT_NONE})
        self.run_forever()
#===============================================================================

class FakeLbl():
    def GetSize(self):
        return (0,0)
    def GetTextExtent(self, s):
        return (0,0)
    def SetFont(self, font):
        pass
    def GetPosition(self):
        return (0,0)
    def SetPosition(self, pos):
        pass
    def Bind(self, *args, **kwargs):
        pass
    def SetToolTipString(self, s):
        pass
    def SetBackgroundColour(self, clr):
        pass
#===============================================================================

class EnableDialog(wx.Frame):
    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="PushBulletEnableDialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.disabled = cpy(self.plugin.disabled)
        self.enabled = []
        self.SetIcon(self.plugin.info.icon.GetWxIcon())


    def GetItems(self):
        pl = self.plugin
        return [pl.GetDevice(i[1]) for i in self.disabled]


    def ShowEnabDialog(self):
        pl = self.plugin
        text = pl.text
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(text.title3)
        panel = wx.Panel(self)
        line = wx.StaticLine(
            panel,
            -1,
            style = wx.LI_HORIZONTAL
        )
        btn4 = wx.Button(panel, wx.ID_DELETE,text.delete)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, wx.ID_OK,text.ok)
        btnsizer.Add(btn1)
        btnsizer.Add((5,-1))
        btn2 = wx.Button(panel, wx.ID_CANCEL,text.cancel)
        btnsizer.Add(btn2)
        lbl1 = wx.StaticText(panel, -1, text.enabLbl)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        listBoxCtrl.Set(self.GetItems())
        btn4.Disable()

        def OnClick(evt):
            btn4.Enable(True)
            sel =  evt.GetSelection()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)

        def OnButtonDelete(evt):
            lngth = listBoxCtrl.GetCount()
            sel = listBoxCtrl.GetSelection()
            item = self.disabled.pop(sel)
            self.enabled.append(item)
            listBoxCtrl.Set(self.GetItems())
            if listBoxCtrl.GetCount():
                if sel >= listBoxCtrl.GetCount():
                    sel = listBoxCtrl.GetCount() - 1
                listBoxCtrl.SetSelection(sel)
            else:
                btn4.Disable()
            evt.Skip()
        btn4.Bind(wx.EVT_BUTTON, OnButtonDelete)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(lbl1)
        leftSizer.Add(listBoxCtrl,1,wx.EXPAND)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add((-1,10))
        rightSizer.Add(btn4,0,wx.ALL,5)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(leftSizer,1,wx.ALL|wx.EXPAND,5)
        topSizer.Add(rightSizer,0,wx.TOP,2)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.BOTTOM,5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        mainSizer.Add((1,6))
        panel.SetSizer(mainSizer)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onOk(evt):
            wx.CallAfter(self.plugin.EnableMirroringMany, self.enabled)
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOk)


        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Fit(self)
        mainSizer.Layout()
        self.Raise()
        self.MakeModal(True)
        self.Show()
#===============================================================================

class Table(wx.ListCtrl):

    def __init__(self, parent, header, minRows, dummyData = None):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES| \
                wx.LC_VRULES|wx.LC_SINGLE_SEL,
        )
        self.cols = len(header)
        for i, colLabel in enumerate(header):
            self.InsertColumn(
                i,
                colLabel,
                format = wx.LIST_FORMAT_LEFT
            )
            if dummyData:
                if i:
                    self.SetStringItem(0, i, dummyData[i])
                else:
                    self.InsertStringItem(0, dummyData[i])
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        self.DeleteAllItems()
        self.w0 = self.GetColumnWidth(0)
        self.w1 = self.GetColumnWidth(1)
        self.w2 = self.GetColumnWidth(2)
        self.wk = SYS_VSCROLL_X + self.GetWindowBorderSize()[0] + self.w0 \
            + self.w1 + self.w2
        width = self.wk
        hh = rect[1] #header height
        hi = rect[3] #item height
        self.SetMinSize((width, 4 + hh + minRows * hi))
        self.SetSize((width, 4 + hh + minRows * hi))
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def SetWidth(self):
        w = (self.GetSize().width - self.wk)
        w0_ = w/3 + self.w0
        w1_ = w/3 + self.w1
        w2_ = w - 2*w/3 + self.w2
        self.SetColumnWidth(0, w0_)
        self.SetColumnWidth(1, w1_)
        self.SetColumnWidth(2, w2_)


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()


    def GetSelectedIndex(self):
        itemIndex = -1
        return self.GetNextItem(
            itemIndex,
            wx.LIST_NEXT_ALL,
            wx.LIST_STATE_SELECTED
        )


    def AddRow(self):
        row = self.GetItemCount()
        self.InsertStringItem(row, "")
        self.SetItemState(row, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.SetFocus()


    def SetRow(self, rowData, row = None):
        row = self.GetSelectedIndex() if row is None else row
        if row > -1:
            for col, colData in enumerate(rowData):
                self.SetStringItem(row, col, colData)
        

    def GetRow(self, row = None):
        row = self.GetSelectedIndex() if row is None else row
        rowData = []
        for col in range(self.cols):
            rowData.append(self.GetItem(row, col).GetText())
        return rowData


    def GetData(self):
        data = []
        for row in range(self.GetItemCount()):
            rowData = self.GetRow(row)
            data.append(rowData)
        return data


    def SetData(self, data):
        self.DeleteAllItems()
        for row, rowData in enumerate(data):
            self.InsertStringItem(row, rowData[0])
            for col, colData in enumerate(rowData[1:]):
                self.SetStringItem(row, col + 1, colData)
#===============================================================================

class ListGrid(gridlib.Grid):

    def __init__(self, parent, id, items, width):
        gridlib.Grid.__init__(
            self,
            parent,
            id,
            size = (width-5, -1),
            style = wx.BORDER_RAISED
        )
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetDefaultRowSize(19)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(True)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(True)
        self.SetColMinimalAcceptableWidth(8)
        self.CreateGrid(len(items), 1)
        self.SetColSize(0, width-6-SYS_VSCROLL_X)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0, attr)
        self.SetSelectionMode(gridlib.Grid.wxGridSelectRows)
        self.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetValue(items)
        self.oldW=self.GetSize()[0]
        self.Show(True)


    def SetWidth(self):
        width = self.GetSize()[0]
        if width != self.oldW:
            self.SetColSize(0, width-6-SYS_VSCROLL_X)
            self.oldW = width


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()


    def onGridSelectCell(self, event):
        rows = self.GetNumberRows()
        row = event.GetRow()
        self.SelectRow(row)
        if rows-1 == row:
            self.AppendRows(1)
        if not self.IsVisible(row, 0):
            self.MakeCellVisible(row, 0)
        event.Skip()


    def GetValue(self):
        items = []
        for r in range(self.GetNumberRows()):
            item = self.GetCellValue(r, 0)
            if item.strip():
                items.append(item)
        return items


    def SetValue(self, items):
        self.ClearGrid()
        for i in range(len(items)):
            self.SetCellValue(i,0,items[i])
#===============================================================================

class ReplyDialog(wx.Frame):

    def __init__(
        self,
        parent,
        plugin,
        title,
        body,
        img,
        app,
        pushDict
    ):
        wx.Frame.__init__(
        self,
        parent,
        -1,
        style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
        name="PushBulletReplyDialog"
    )
        self.SetBackgroundColour(wx.NullColour)
        self.plugin = plugin
        self.title = title
        self.body = body
        self.img = img
        self.app = app
        self.pushDict = pushDict
        self.SetIcon(self.plugin.info.icon.GetWxIcon())


    def ShowReplyDialog(self):
        pl = self.plugin
        self.SetTitle(pl.text.title4 % self.title)
        panel = wx.Panel(self)
        panel.SetBackgroundColour(self.GetBackgroundColour())
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(10, 10)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(3)
        self.SetSizer(mainSizer)
        intBrdr = 10
        mainSizer.Add(sizer,1,wx.ALL|wx.EXPAND, intBrdr)
        bmp = StaticBitmap(
            self,
            -1,
            self.img,
            size = (self.img.GetWidth(), self.img.GetHeight())
        )
        ttl = wx.StaticText(
            self,
            -1,
            self.title,
        )
        font = wx.Font(
            14,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            False,
            u'Ariel'
        )
        ttl.SetFont(font)        
        dsc = wx.StaticText(
            self,
            -1,
            "Via %s" % self.app,
        )
        font = wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_LIGHT,
            False,
            u'Ariel'
        )
        dsc.SetFont(font)  
        btn = FlatButton(
            self,
            -1,
            size = (90, 50),
            idleBmp = join(ICON_DIR, "Reply.png"),
            label = pl.text.reply,
            radius = 5,
            bmpIndent = 5
        )
        sizer.Add(bmp, (0,0),(2,1))
        sizer.Add(ttl, (0, 1))
        sizer.Add(btn, (0, 2), (2,1), flag = wx.ALIGN_RIGHT)
        sizer.Add(dsc, (1, 1))
        bd = wx.TextCtrl(
            self,
            -1,
            self.body,
            style = wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE|wx.TE_RICH 
        )
        bd.SetBackgroundColour(self.GetBackgroundColour())
        bd.SetFont(font)
        sizer.Add(bd, (2, 0), (1,3), flag = wx.EXPAND)
        msg = wx.TextCtrl(
            self,
            -1,
            style = wx.TE_MULTILINE| wx.TE_RICH
        )
        msg.ChangeValue(pl.text.replyPrompt)

        fnt = msg.GetFont()
        fnt.SetPointSize(10)
        msg.SetFont(fnt)
        def GetMultiLineTextExtent(ctrl, txt):
            slices = [ctrl.GetTextExtent(item)[0] for item in txt.split("\n")]
            return max(slices)
        msgW = GetMultiLineTextExtent(msg, pl.text.replyPrompt)
        extBrdr = self.GetSize()[0] - self.GetClientSize()[0]
        brdrs = 10 + extBrdr + 2 * intBrdr
        msg.SetForegroundColour(wx.GREEN)
        sizer.Add(msg, (3, 0), (1,3), flag = wx.EXPAND)        


        def onFrameCharHook(evt):
            kc = evt.GetKeyCode()
            if kc in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and evt.ControlDown():
                pl.sendReply(self.pushDict, msg.GetValue())
                self.Close()                    
            else:
                evt.Skip()
        self.Bind(wx.EVT_CHAR_HOOK, onFrameCharHook)


        def onFocus(evt):
            if msg.GetValue() == pl.text.replyPrompt:
                msg.SetForegroundColour(self.GetForegroundColour())
                msg.ChangeValue("")
        msg.Bind(wx.EVT_SET_FOCUS, onFocus)


        def onClose(evt):
            self.MakeModal(False)
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onReply(evt):
            pl.sendReply(self.pushDict, msg.GetValue())
            self.Close()
        btn.Bind(wx.EVT_BUTTON, onReply)

        mainSizer.Fit(self)
        mainSizer.Layout()
        self.Raise()
        self.MakeModal(True)
        w, h = self.GetSize()
        self.SetSize((max(w, msgW + brdrs), 320))
        self.SetMinSize((min(w, msgW + brdrs), min(h, 290)))
        self.Show()
#===============================================================================

class MirrorNote(wx.Frame):

    def __init__(
        self,
        parent,
        plugin,
        dev,
        title,
        body,
        icon,
        app,
        wav,
        pushDict
    ):
        flag = self.flag = pushDict.has_key('type') and pushDict['type']=='sms' and pushDict['recip'] != "MULTI"
        self.plugin = plugin
        self.pushDict = pushDict
        repl = self.pushDict.has_key('conversation_iden')
        dev = dev.rstrip()
        title = title.replace("&","&&").rstrip()
        body = body.replace("&","&&")
        body = body if body == body[:1000] else "%s ...." % body[:1000]
        body = wrap(body, 80)

        if icon:
            sbuf = StringIO(b64decode(icon))
        else:
            sbuf = StringIO(b64decode(AVATAR))
        wximg = wx.ImageFromStream(sbuf)
        W = wximg.GetWidth()
        H = wximg.GetHeight()
        K = 96
        if W > K or H > K:
            factor = max(W, H)/float(K)
            x = int(min(W, H) / factor) 
            size = (K, x) if W >= H else (x, K)
            wximg = wximg.Scale(size[0],size[1], wx.IMAGE_QUALITY_HIGH)
            W = wximg.GetWidth()
            H = wximg.GetHeight()
     
        if repl and W == H:
            mask = FluffyCircleMask(wximg.GetWidth())
            wximg.SetAlphaData(mask)
        img = wx.BitmapFromImage(wximg)

        if W < 72 and H < 72:
            W, H = (72, 72)            
            
        wx.Frame.__init__(
            self,
            parent,
            -1,
            '',
            size = (400, H + 8),
            style = wx.STAY_ON_TOP | wx.SIMPLE_BORDER
        )
        bc = plugin.clr
        self.SetBackgroundColour(bc)
        self.delta = (0, 0)
        bmp = StaticBitmap(
            self, 
            -1,
            img,
            (3, 3),
            (img.GetWidth(),
            img.GetHeight())
        )
        app = app if (not plugin.hideBtn and not flag) else ""
        lbl = plugin.text.disable % app if app else ""
        label0 = wx.StaticText(self, -1, dev, (W + 10,2)) if dev else FakeLbl()
        label1 = wx.StaticText(self, -1, title) if title else FakeLbl()
        label2 = wx.StaticText(self, -1, body) if body else FakeLbl()
        label3 = wx.StaticText(self, -1, lbl) if app else FakeLbl()
        label4 = wx.StaticText(self, -1, strftime('     %H:%M:%S'))

        font = label0.GetFont()
        size = font.GetPointSize()
        font.SetPointSize(size*1.4)
        label2.SetFont(font)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label1.SetFont(font)
        font = label0.GetFont()
        font.SetStyle(wx.FONTSTYLE_ITALIC)
        label3.SetFont(font)

        w0, h0 = label0.GetSize()
        w1, h1 = label1.GetSize()
        w2, h2 = label2.GetSize()
        w3, h3 = label3.GetSize()
        w4, h4 = label4.GetSize()
        _, e0 = label0.GetTextExtent("X")
        _, e1 = label1.GetTextExtent("X")
        _, e2 = label2.GetTextExtent("X")
        label1.SetPosition((W+10, 19-e0+h0))
        label2.SetPosition((W+10, 38-e0-e1+h0+h1))
        x0, y0 = label0.GetPosition()
        x1, y1 = label1.GetPosition()
        x2, y2 = label2.GetPosition()

        if app:
            def onClick(event):
                wx.CallAfter(plugin.DisableMirroring, self.pushDict, app)
                #self.OnCloseWindow(event)
                if flag:
                    self.plugin.smsDismiss()
                else:
                    self.plugin.dismiss(self.pushDict)
                self.Close()
                event.Skip()
            h = max(y0 + h0, y1 + h1, y2 + h2)
            png = wx.Bitmap(
                join(eg.Icons.IMAGES_PATH, "disabled.png"),
                wx.BITMAP_TYPE_PNG
            )
            gr = png.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()
            hh = max(H + 8, h + 32 if repl else h + 22)
            b = wx.BitmapButton(
                self,
                -1,
                gr,
                pos = (W + 10, hh - 20),
                size = (16, 16),
                style = wx.BORDER_NONE
            )

            label0.SetBackgroundColour(bc)
            label1.SetBackgroundColour(bc)
            label2.SetBackgroundColour(bc)
            label3.SetBackgroundColour(bc)
            label4.SetBackgroundColour(bc)
            b.SetBackgroundColour(bc)
            b.SetBitmapHover(png)
            b.SetBitmapSelected(png)
            b.Bind(wx.EVT_BUTTON, onClick)
            label3.SetPosition((W + 32, hh - 18))
        else:
            hh = None
        if repl:
            def onBtn(event):
                if flag:
                    self.plugin.smsDismiss()
                else:
                    self.plugin.dismiss(cpy(self.pushDict))
                dlg = ReplyDialog(
                    parent,
                    plugin,
                    title if title else "",
                    body if body else "",
                    img,
                    app,
                    self.pushDict
                )
                self.Show(False)
                self.Close()
                dlg.Centre()
                dlg.ShowReplyDialog()
                event.Skip()

            idleImg = wx.Image(join(ICON_DIR, "Reply.png"), wx.BITMAP_TYPE_ANY)
            pil = imageToPil(idleImg)
            if pil:
                pil = resize(pil, 16)
                io_file = StringIO()
                pil.save(io_file, format = 'PNG')
                io_file.seek(0)
                data = io_file.read()
                idleBmp = b64encode(data)
            else:
                idleBmp = None

            btn = FlatButton(
                self,
                -1,
                idleBmp = idleBmp,
                label = plugin.text.reply,
                radius = 5,
                bmpIndent = 3
            )
            btn.Bind(wx.EVT_BUTTON, onBtn)
            wb, hb = btn.GetSize()
            hh = hh if hh is not None else 8 + max(H, y0 + h0 + hb, y1 + h1 + hb, y2 + h2 + hb)
            w = max(w0 + w4, w1, w2, w3 + wb + 37)
            btn.SetPosition((W + 18 + w - wb - 5, hh - hb - 5))
        else:
            w = max(w0 + w4, w1, w2, w3 + 22)
        self.SetSize((W + 18 + w, hh))
        label4.SetPosition((W+10 + w0 if w == w0 + w4 else W+10 + w - w4, 2))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)      

        for win in (self, label0, label1, label2, label3, label4, bmp):
            win.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            win.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            win.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            win.Bind(wx.EVT_MOTION, self.OnMouseMove)
            win.SetToolTipString(plugin.text.tooltip)   

        self.timer = wx.Timer(self)
        if plugin.hide:
            self.timer.Start(1000*plugin.hide)
            self.Bind(wx.EVT_TIMER, self.OnCloseWindow)

        width, height = self.GetSize()
        monitorDimensions = GetMonitorDimensions()
        try:
            displayRect = monitorDimensions[plugin.dspl]
        except IndexError:
            displayRect = monitorDimensions[0]
        xOffset, yOffset = plugin.offset
        xFunc, yFunc = ALIGNMENT_FUNCS[plugin.alignment]
        x = displayRect.x + xFunc((displayRect.width - width), xOffset)
        y = displayRect.y + yFunc((displayRect.height - height), yOffset)

        self.SetPosition((x, y))
        if wav:
            self.sound = wx.Sound(wav)
            if self.sound.IsOk():
                self.sound.Play(wx.SOUND_ASYNC)
        else:
            self.sound = None
        self.Show(True)
        plugin.notification_ids[self.pushDict['notification_id']] = self
        BringWindowToTop(self.GetHandle())


    def OnCloseWindow(self, event):
        id = self.pushDict['notification_id']
        if id in self.plugin.notification_ids:
            del self.plugin.notification_ids[id]
        if hasattr(self, 'timer'):
            self.timer.Stop()
            del self.timer
        if self.sound:
            self.sound.Stop()
        self.Destroy()


    def OnRightClick(self, evt):
        if self.flag:
            self.plugin.smsDismiss()
        else:
            self.plugin.dismiss(self.pushDict)
        self.Show(False)
        self.Close()


    def OnLeftDown(self, evt):
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(win, (
            wx._controls.StaticText, 
            eg.CorePluginModule.PushBullet.StaticBitmap
            )):
            childX, childY = win.GetPosition()
            x += childX
            y += childY
        self.CaptureMouse()
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()


    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)
#===============================================================================

class Text:
    recips = "Recipients:"
    device = "Device:"
    recip = "Recipient:"
    header = (
        "Device",
        "Name",
        "Phone number"
    )
    file = "File:"
    ext = "List of file extensions:"
    notLbl = " not"
    ifExt = "if extension"
    inLbl = "in"
    autoOpen = "Automatically open downloaded pictures"
    firstWord = """If title of push (type Note) is missing, 
use the first word out of the body as the event suffix"""
    enabMirr = "Enable popping up of mirrored notification"
    nLabel = 'Nickname of this "device":'
    apiLabel = 'API key:'
    password = "Encryption password:"
    prefix = 'Event prefix:'
    mode = 'The title of the push to use as:'
    modes = ("event suffix", "payload[0]")
    complPush = "Use the complete original push as last part of the payload"
    folder =  'Directory for file download:'
    timeout = 'Timeout for auto-hide [s]:'
    pTimeout = 'Picture hide timeout [s]:'
    timeout2 = "(0 = not to hide)"
    err = 'Failed to open file "%s"'
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    hideBtn = "Hide disable button on mirrored notifications"
    title3 = "Unmute a disabled application"
    title4 = "PushBullet - quick replying to: %s"
    enabLbl = "Disabled application:"
    cancel = "Cancel"
    ok = "OK"
    delete = "Unmute"
    reenab = "Re-enable mirroring for an app ..."
    tooltip = "Right mouse button closes this window"
    disable = 'Mute "%s"'
    clipFilter = 'Filter of clipboard change monitoring '\
        '(device checked = notifying disabled)'
    filterToolTip = "This combo is enabled only if the devices are synced !"
    wavs = "Alerting sounds location:"
    reconnect = "Haven't seen a nop lately, reconnecting"
    waiting = "Haven't seen a nop lately, waiting for connectivity"
    waiting2 = "PushBullet: No connectivity, waiting ..."
    uplFld = u'Failed to upload the file "%s"'
    uplSucc = u'The file "%s" was uploaded successfully'
    addLstnr = 'Adding push messaging listener'
    wsMssg = "WebSocket message: %s"
    dcrptdMssg = "Decrypted message: %s"
    rspnsr = "Response = %s"
    fTriggMute = 'Failed to trigger mute of app %s'
    triggMute = "Triggered mute of app %s"
    fPong = 'Failed to send pong'
    pong = "Pong was sent"
    fTriggUnmute = 'Failed to trigger unmute of app %s'
    triggUnmute = "Triggered unmute of app %s"
    gettPshs = "Getting pushes, modified_after = %.7f"
    fLoadPshs = "Failed to load pushes"
    thrReqRes = "Threads request response = %s"
    fLoadThrds = "Failed to load threads"
    e2eMssg1 = 'End to end encryption: Invalid version'
    e2eMssg2 = 'End to end encryption: Decrypted message is not a dictionary'
    e2eMssg3 = 'End to end encryption: Decryption failed'
    smsSent = 'SMS sent successfuly to device "%s"'
    smsSentF = 'SMS sent to device "%s" failed'
    fRetrTmstmp = "Failed to retrieve timestamp"
    mdfdUpd = "modified_after updated: %.7f"
    wsOpenedEvt = "WebSocketOpened"
    wsClosedEvt = "WebSocketClosed"
    wsError = u"PushBullet: WebSocket error: %s"
    idenSaved = 'New iden "%s" automatically saved'
    dsbldUpdated = 'List of disabled app automatically updated'
    emlObtained = "Email address obtained"
    accReqFailed = "Account request failed"
    noApi = "No API key"
    noNick = "No nickname"
    devRcvd = "Devices received: %s"
    devReqFailed = "Device request failed"
    bookRcvd = 'Phonebook from device "%s" received'
    thrdsRcvd = 'SMS threads from device "%s" received'
    bookReqFailed = 'Phonebook request from device "%s" failed'
    noDev = "No devices"
    pcMssng = "This EventGhost is missing in the device list. "\
        "Request for creating device sent."
    devCrtd = "Device created: %s"
    crDevFld = "Creating device failed"
    pushDelted = "Push deleted"
    pushDelFld = 'Push deleting failed: "%s"'
    forwRep = "Forwarding reply to extension in %s"
    forwRepFld = "Failed to forward reply to extension in %s"
    dismissNote = 'Notification "%s" dismissed'
    dismissNoteFld = 'Dismiss of notification "%s" failed'
    dismissPush = 'Push "%s" dismissed'
    dismissPushFld = 'Dismiss of push "%s" failed'
    dismissSms = 'Triggered remote sms dismissal'
    dismissSmsFld = 'Failed to trigger remote sms dismissal'  
    notIdMissing = 'Parameter "notification_id" is missing!'
    notDismiss = 'Push "%s" is marked as "not dismissable" ! '\
        "Still, I'll try it."
    reply = "Reply"
    replyPrompt = "Type your reply here.\n"\
        "You can use the Enter (or Return) key to make new line.\n"\
        "You can use Ctrl-Enter (Ctrl-Return) to send the message.\n"\
        "The dialog can be resized.\n"\
        "You can even copy a text from the incoming messages !"
    frndsRcvd = "Friends received: %s"
    chnnlsRcvd = "Channels received: %s"
    trgtsDrvd = "Targets derived: %s"
    pushRslt = "Push results: %s"
    dwnldFailed = 'Download of "%s" failed (code %i)'
    nicknameUsed = 'PushBullet: Chosen nickname "%s" is already used for '\
        'other device, than the "EventGhost"  !!!'
    wavFldr = "Select the folder that stores sounds ..."
    toolWav = '''Here you can select the folder, where you saved the alerting
sounds. If the field is left blank, this feature will not be used. 
Sounds must be in "wav" format and must have the same name, 
as the corresponding push type (for example, "note.wav", for "note" push). 
If some sound is missing, this feature will not be used (for the corresponding 
push type).'''
    kinds = (
        "Note",
        "Link",
        "File",
        "Mirror",
    )    
    choices = [
        "the file extension is one of the listed extension",
        "the file extension is not one of the listed extension",
    ]
    mirroring = "Mirroring"
    bcgColour = "Background Colour:"
    alignment = "Alignment:"
    alignmentChoices = [
        "Top Left",
        "Top Right",
        "Bottom Left",
        "Bottom Right",
        "Screen Center",
        "Bottom Center",
        "Top Center",
        "Left Center",
        "Right Center",
    ]
    display = "Show on display:"
    xOffset = "Horizontal offset X:"
    yOffset = "Vertical offset Y:"
    pushGroupsTitle = 'Push recipient groups'
    smsGroupsTitle = 'SMS recipient groups'
    groupsList = "List of groups:"
    groupLabel = "Group name:"
    delete = 'Delete'
    insert = 'Add new'
    tsLabel = "Push targets:"
    unknStream = 'PushBullet: Unknown stream push type: "%s"'
    reqErr = "PushBullet: Request error: %s"
    noKey = '''Pushbullet: Encrypted data received.
            You must enter the encryption password,
            or turn off the End to end encryption on your other devices.'''
#===============================================================================

class PushBullet(eg.PluginClass):
    api_key = None
    iden = None
    ct = None
    wsC = None
    pb = None
    lastMessage = 0
    msgWait = DEFAULT_WAIT
    modified_after = 0
    devices = []
    friends = []
    channels = []
    targets = []
    disabled = []
    notification_ids = {}
    sms_trds = {}
    watchdog = None
    debug = 1
    email = None
    updtDvcs = None
    connFlag = False
    autoUpdate = False
    source_user_iden = None
    text = Text
    flag1 = False
    flag2 = False

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def __start__(
        self,
        nickname = None,
        api_key = "",
        iden = "",
        prefix = "PushBullet",
        mode = 0,
        fldr = "",
        debug = 3,
        hide = 15,
        pHide = 15,
        disabled = [],
        hideBtn = False,
        wavs = "",
        autoOpen = True,
        dummy = "",
        enabMirr = True,
        clr = (255, 255, 255),
        alignment = 0,
        dspl = 0,
        offset = (0, 0),
        filtered = [],
        pushGroups = [],
        smsGroups = [],
        password = "",
        firstWord = True,
        complPush = False
    ):
        self.source_user_iden = None
        self.notification_ids = {}
        self.pushGroups = pushGroups
        self.smsGroups = smsGroups
        if filtered and isinstance(filtered[0], list):  # backward compatibility
            tmp = []
            for i, item in enumerate(filtered[0]):
                if filtered[1][i]:
                    tmp.append(item)
            filtered = tmp
        self.filtered = filtered

        if self.autoUpdate:
            self.autoUpdate = False
            return
        if isinstance(api_key, eg.Password):
            api_key = api_key.Get()    
        self.api_key = api_key
        self.pssd = password
        self.key = None
        self.info.eventPrefix = prefix
        self.nickname = nickname
        self.iden = iden
        self.prefix = prefix
        self.mode = mode
        self.fldr = fldr if isdir(fldr) else eg.folderPath.TemporaryFiles
        self.debug = debug
        self.hide = hide
        self.pHide = pHide

        self.disabled = []
        for item in disabled:                           # backward compatibility
            self.disabled.append(item if len(item)==2 else item[1:])
        self.hideBtn = hideBtn
        self.wavs = wavs
        self.autoOpen = autoOpen
        self.firstWord = firstWord
        self.complPush = complPush
        self.enabMirr = enabMirr
        self.clr = clr
        self.alignment = alignment
        self.dspl = dspl
        self.offset = offset
        self.connFlag = False
        self.sms_trds = {}
        self.updtDvcs = eg.scheduler.AddTask(2.0, self.updateDevices)


    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass


    def stopUpdtDvcs(self):
        fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
        if self.updateDevices in fcs:
            try:
                eg.scheduler.CancelTask(self.updtDvcs)
            except:
                pass


    def OnComputerResume(self, dummy):
        self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
        self.watchdog = eg.scheduler.AddTask(15.0, self.watcher)


    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
        self.stopUpdtDvcs()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None
        self.devices = []
        self.friends = []
        self.channels = []
        self.targets = []
    

    def __stop__(self):
        if self.autoUpdate:
            return
        self.stopWatchdog()
        self.stopUpdtDvcs()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None
        self.watchdog = None
        self.devices = []
        self.friends = []
        self.channels = []
        self.targets = []
        self.sms_trds = {}
        self.email = None


    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.name, message)


    def parseArgument(self, arg):
        try:
            arg = eg.ParseString(arg)
        except:
            pass
        try:
            arg = eval(arg)
        except:
            pass
        return arg


    def watcher(self):
        if not self.info.isStarted:
            return
        if self.api_key and (ttime() - self.lastMessage) > self.msgWait:
            if connectivity():
                self.connFlag = True
                self.TriggerEvent("InternetConnection.Restored")
                self.Log(self.text.reconnect, 2)
                self.msgWait = min(600000, self.msgWait * 2)
                self.refreshWebSocket()
            elif self.connFlag:
                self.Log(self.text.waiting, 1)
                self.connFlag = False
                self.TriggerEvent("InternetConnection.Broken")
        elif not self.connFlag:
            if connectivity():
                self.connFlag = True
                self.TriggerEvent("InternetConnection.Restored")
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)


    def on_open(self, _):
        self.TriggerEvent(self.text.wsOpenedEvt)
        res,flag = self.request("GET",API + 'pushes?limit=1&modified_after=0.0')
        if not flag or not isinstance(res, dict) or not 'pushes' in res: 
            self.Log(self.text.fRetrTmstmp, 1)
            return
        pushes = res['pushes']
        for push in pushes:
            try:
                self.modified_after = max(self.modified_after, push['modified'])
                self.Log(self.text.mdfdUpd % self.modified_after, 4)
            except:
                self.Log(self.text.fRetrTmstmp, 1)


    def establishSubscriber(self): 
        if self.wsC: 
            return
        self.flag1 = False
        url = 'wss://stream.pushbullet.com/websocket/' + self.api_key
        self.wsC = WebSocketClient(url, self)
        self.ct = Thread(target = self.wsC.start)
        self.ct.start()
        self.lastMessage = ttime()      
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(0.01, self.watcher)
        self.Log(self.text.addLstnr, 4)


    def refreshWebSocket(self):
        self.msgWait = DEFAULT_WAIT
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.establishSubscriber()



    def requestThreads(self, iden):
        res, flag = self.request(
            "POST",
            API3 + 'get-permanent',
            data = {'key': iden + '_threads'}
        )

        self.Log(self.text.thrReqRes % repr(res), 4)
        if not flag or not isinstance(res, dict) or not res.has_key('data'): 
            self.Log(self.text.fLoadThrds, 1)
            return []
        data = res['data']
        if data.has_key('encrypted') and data['encrypted']:
            if self.key:
                decrypted = gcm_decrypt(self.key, data[u'ciphertext'])
                try:
                    data = loads(decrypted)
                    if not isinstance(data, dict):
                        self.Log(self.text.e2eMssg2, 2)
                        return []
                except:
                    self.Log(self.text.e2eMssg3, 2)
                    return []
            else:
                eg.PrintNotice(self.text.noKey)
                return []
        self.Log(self.text.thrdsRcvd % self.GetDevice(iden), 4)
        return data['threads'] if data.has_key(u'threads') else []


    def on_message(self, _, m):
        if not self.info.isStarted:
            if self.wsC:
                self.wsC.close()
        if self.targets == []:
            if self.flag1:
                self.flag2 = True
            else:
                self.updtDvcs = eg.scheduler.AddTask(5.00, self.updateDevices)
            return
        if m is None:
            return
        try:
            m = loads(m)
            self.Log(self.text.wsMssg % repr(m), 5)
            self.lastMessage = ttime()
            self.msgWait = DEFAULT_WAIT
        except:
            eg.PrintTraceback()
            self.refreshWebSocket()
            return
        if m['type'] == 'nop':
            pass
        elif m['type'] == 'alert':
            if m.target_device_iden != self.iden:
                return
            self.TriggerEvent(
                'Alert',
                m['title'] or "Empty",
                payload = m['body']
            )
        elif m['type'] == 'push':
            push = m['push']
            if push.has_key('encrypted') and push['encrypted']:
                if self.key:
                    decrypted = gcm_decrypt(self.key, push['ciphertext'])
                    if decrypted is None:
                        self.Log(self.text.e2eMssg1, 2)
                        return
                    try:
                        push = loads(decrypted)
                        self.Log(self.text.dcrptdMssg % repr(push), 5)
                        if not isinstance(push, dict):
                            self.Log(self.text.e2eMssg2, 2)
                            return
                    except:
                        self.Log(self.text.e2eMssg3, 2)
                        return
                else:
                    eg.PrintNotice(self.text.noKey)
                    return
            if push['type'] == 'mirror':
                try:
                    self.processMirror(push)
                except:
                    eg.PrintTraceback()
            elif push['type'] == 'clip':
                dev = push['device_iden'] if 'device_iden' in push else None
                dev = push['source_device_iden'] \
                    if 'source_device_iden' in push else dev
                if dev not in self.filtered:
                        try:
                            self.processPush(push)
                        except:
                            eg.PrintTraceback()
            elif push['type'] == 'dismissal':
                notification_id = push['notification_id']
                if notification_id in self.notification_ids:
                    win = self.notification_ids[notification_id]
                    win.Close()
            elif push['type'] == 'messaging_extension_reply':
                pass 
            elif push['type'] == 'mute':
                pass
            elif push['type'] == 'unmute':
                pass
            elif push['type'] == 'pong':
                pass
            elif push['type'] == 'ping':
                pong = {
                    'type': 'pong',
                    "device_iden": self.iden,
                }
                res, flag = self.request(
                    "POST",
                    API + 'ephemerals',
                    data = {"type": "push", "push":pong}
                )
                self.Log(self.text.rspnsr % repr(res), 4)
                if not flag:
                    self.Log(self.text.fPong, 1)
                    return
                self.Log(self.text.pong, 3)
            elif push['type'] == 'sms_changed':
                id = push[u'source_device_iden']
                trds = self.requestThreads(id)
                for trd in trds:            
                    cid = trd[u'id']
                    if not trd.has_key(u'latest'):
                        continue
                    if  trd[u'latest']['direction'] != 'incoming':
                        continue
                    if cid in self.sms_trds[id]:
                        if trd['latest']['timestamp'] <= self.sms_trds[id][cid][0] and trd['latest']['id'] <= self.sms_trds[id][cid][1]:
                            continue
                    self.sms_trds[id][cid] = [trd['latest']['timestamp'],trd['latest']['id']] # timestamp and id update
                    dev = self.GetDevice(id) 
                    try:
                        trd_recs = trd['recipients']
                        if len(trd_recs) == 1:
                            suffix = "ReplyAllowingMirror"
                            rec = trd_recs[0]
                            name = rec['name']
                            icon = self.urlretrieve(rec['image_url']) if rec.has_key('image_url') else None
                        else:
                            suffix = "Mirror"
                            icon = None
                            name = ", ".join([i['name'] for i in trd_recs])
                        self.TriggerEvent(
                            "%s.%s" % (
                                suffix,
                                name.replace(" ", "").replace(".",":")
                            ),
                            payload = [
                                trd['latest']['body'],
                                dev,
                                icon,
                                trd if self.complPush else trd['latest']
                            ]
                        )
                        if self.enabMirr:
                            pushDict = cpy(trd['latest'])
                            pushDict['dev'] = dev
                            pushDict['recip'] = rec['number'] if len(trd_recs) == 1 else "MULTI"
                            notification_id = 0
                            pushDict['notification_id'] = notification_id
                            pushDict['conversation_iden'] = cid
                            if notification_id in self.notification_ids:
                                win = self.notification_ids[notification_id]
                                win.Close()
                            body = trd['latest']['body']
                            wx.CallAfter(
                                MirrorNote,
                                None,
                                self,
                                dev,
                                name,
                                body if body else " ",
                                icon,
                                "sms",
                                self.getSound('mirror'),
                                pushDict
                            )
                    except:
                        eg.PrintTraceback()
            else:
                eg.PrintNotice(unknStream % push['type'])
        elif m['type'] == 'tickle' and m['subtype'] == 'push':
            self.requestPushes()
        elif m['type'] == 'tickle' and m['subtype'] == 'device':
            self.devices = []
            fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
            if not self.updateDevices in fcs:
                if self.flag1:
                    self.flag2 = True
                else:
                    self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
        elif m['type'] == 'tickle' and m['subtype'] == 'contact':
            self.friends = []
            fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
            if not self.updateDevices in fcs:
                if self.flag1:
                    self.flag2 = True
                else:
                    self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
        elif m['type'] == 'tickle' and m['subtype'] == 'channel':
            self.channels = []
            fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
            if not self.updateDevices in fcs:
                if self.flag1:
                    self.flag2 = True
                else:
                    self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)


    def EventTrigger(self, part1, part2, part3, part4, part5, dev, ts):
        if self.mode:
            self.TriggerEvent(
                part1,
                payload = [part2, part3, part4, part5, dev, ts]
            )
        else:
            self.TriggerEvent(
                "%s.%s"% (part1,part2.title().replace(" ","").replace(".",":")),
                payload = [part3, part4, part5, dev, ts]
            )


    def urlretrieve(self, remote, flpth = None):
        headers = {}
        def header_function(header_line):
            if ':' not in header_line:
                return
            name, value = header_line.split(':', 1)
            name = name.strip()
            value = value.strip()
            name = name.lower()
            headers[name] = value
        buff = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, remote)
        c.setopt(c.HTTPHEADER, ['Accept: */*', 'User-Agent: EventGhost'])
        c.setopt(c.WRITEDATA, buff)
        c.setopt(c.HEADERFUNCTION, header_function)
        c.perform()
        status_code = c.getinfo(c.RESPONSE_CODE)
        c.close()
        if status_code == 200:
            if flpth is not None:
                ct = headers['content-type']
                fo = open(flpth, 'wb')
                buff.seek(0)
                copyfileobj(buff, fo)
                fo.close()
                self.TriggerEvent("FileDownloaded", payload = flpth)
                if self.autoOpen and ct.split(r"/")[0] == u'image':
                    eg.plugins.System.DisplayImage(
                        flpth, 3, 1, True, False, 0, True, 4,
                        self.pHide,
                        0, 5, 5, 640, 480, (51, 51, 51), False, True, True, u''
                    )
            else:
                return b64encode(buff.getvalue())
        else:
            self.Log(self.text.dwnldFailed % (flpth, status_code), 1)


    def getSound(self, tp):
        if self.wavs:
            if isfile(join(self.wavs, "%s.wav" % tp)):
                return join(self.wavs, "%s.wav" % tp)


    def deletePush(self, iden):
        res, flag = self.request("DELETE", API + 'pushes/%s' % iden)
        if flag:
            self.Log(self.text.pushDelted, 4)
        else: 
            self.Log(self.text.pushDelFld % res, 2)


    def sendReply(self, push, msg):
        if push.has_key('type') and push['type'] == 'sms':
            return self.sendSMS(push['dev'], push['recip'], msg)
        push['type'] = 'messaging_extension_reply'
        push['target_device_iden'] = push['source_device_iden']
        push['message'] = msg
        package_name = push['package_name']
        if 'source_device_iden' in push:
            del push['source_device_iden']
        if 'dismissible' in push:
            del push['dismissible']
        if 'notification_id' in push:
            del push['notification_id']
        if 'notification_tag' in push:
            del push['notification_tag']
        push = push if self.key is None else \
            {
                'encrypted': True,
                'ciphertext': gcm_encrypt(self.key, dumps(push))
            }
        body = {'type':'push', 'push': push}
        res, flag = self.request("POST", API + 'ephemerals', data = body)
        if flag:
            self.Log(self.text.forwRep % package_name, 4)
        else: 
            self.Log(self.text.forwRepFld % package_name, 2)


    def smsDismiss(self):
        dismissal = {
            'type': 'dismissal',
            'source_user_iden': self.source_user_iden,
            'package_name': 'sms',
            'notification_id': 0
        }
        body = {
            'type': 'push',
            'push': dismissal,
            'targets': ['stream', 'android']
        }
        res, flag = self.request("POST", API + 'ephemerals', data = body)
        if flag:
            self.Log(self.text.dismissSms, 4)
        else: 
            self.Log(self.text.dismissSmsFld, 2)


    def dismiss(self, oldpush):
        if isinstance(oldpush, dict):
            if not 'notification_id' in oldpush:
                self.Log(self.text.notIdMissing, 2)
                return
            notification_id = oldpush['notification_id']
            push = {
                'notification_id': notification_id, 
                'notification_tag': None if not oldpush.has_key('notification_tag') else oldpush['notification_tag'], 
                'type': u'dismissal', 
                'source_user_iden': self.source_user_iden, 
                'package_name': oldpush['package_name']
            }
            push = push if self.key is None else \
                {
                    'encrypted': True,
                    'ciphertext': gcm_encrypt(self.key, dumps(push))
                }
            body = {
                'type':'push',
                'push': push,
                'targets': [u'stream', u'android', u'ios']
            }
            res, flag = self.request("POST", API + 'ephemerals', data = body)
            if flag:
                self.Log(self.text.dismissNote % notification_id, 4)
            else: 
                self.Log(self.text.dismissNoteFld % notification_id, 2)
        else:
            body = {"dismissed":True}
            res, flag=self.request("POST", API + 'pushes/%s' % oldpush, data=body)
            if flag:
                self.Log(self.text.dismissPush % oldpush, 4)
            else: 
                self.Log(self.text.dismissPushFld % oldpush, 2)


    def processMirror(self, push):
        body = push[u'body'] if 'body' in push and push['body'] else ""
        title = push['title'] if 'title' in push and push['title'] else ""
        dev = self.GetDevice(push['source_device_iden']) \
                if 'source_device_iden' in push else "Unknown"
        pushDict = {
            'package_name': push['package_name'] \
                if 'package_name' in push else None,
            'source_user_iden': push['source_user_iden'] \
                if 'source_user_iden' in push else None,
            'source_device_iden': push['source_device_iden'] \
                if 'source_device_iden' in push else None,
            'dismissible': push['dismissible'] \
                if 'dismissible' in push else None,
            'notification_id': push['notification_id'] \
                if 'notification_id' in push else None,
            'notification_tag': push['notification_tag'] \
                if 'notification_tag' in push else None                
        }
        try:
            if "conversation_iden" in push:
                pushDict["conversation_iden"] = push['conversation_iden']
                suffix = "ReplyAllowingMirror"
            else:
                suffix = "Mirror"
            self.TriggerEvent(
                "%s.%s" % (
                    suffix,
                    title.title().replace(" ", "").replace(".",":") \
                        if title else suffix,
                ),
                payload = [
                    body,
                    dev,
                    push[u'icon'],
                    push if self.complPush else pushDict
                ]
            )
            if self.enabMirr:
                title = title if title else body
                notification_id = pushDict['notification_id']
                if notification_id in self.notification_ids:
                    win = self.notification_ids[notification_id]
                    win.Close()
                wx.CallAfter(
                    MirrorNote,
                    None,
                    self,
                    dev,
                    title,
                    body if body and body != title else "",
                    push[u'icon'],
                    push['application_name'] if 'application_name' \
                        in push and push['application_name'] else "",
                    self.getSound(push['type']),
                    pushDict
                )
        except:
            eg.PrintTraceback()


    def processPush(self, push):
        if ('active' in push and not push['active'])\
            or 'dismissed' in push and push['dismissed']:
            return
        if 'target_device_iden' in push\
            and push['target_device_iden'] != self.iden:
            return
        friend = False
        if 'receiver_email' in push:
            if push['receiver_email'] != self.email:
                return
            elif 'sender_email' in push and push['sender_email'] != self.email:
                friend = True
                dev = self.GetDevice(push['sender_email'])
        if not friend:
            dev = self.GetDevice(push['source_device_iden']) \
                if 'source_device_iden' in push else push['sender_name']
        if 'modified' in push:
            ts = push['modified']
            if ts > self.modified_after:
                self.modified_after = ts
                self.Log(self.text.mdfdUpd % self.modified_after, 4)
        else:
            ts = ttime()
        ts = str(dt.fromtimestamp(ts))[:19]
        wav = self.getSound(push['type'])
        if wav:
            sound = wx.Sound(wav)
            if sound.IsOk():
                sound.Play(wx.SOUND_ASYNC)     
        body = push[u'body'] if ('body' in push and push['body']) else ""
        part1 = push['type'].capitalize()
        part2 = push['title'] if ('title' in push and push['title']) else part1
        if self.firstWord and part1 == "Note" and part2 == 'Note':
            tmpBody = body.strip(' \t\n\r').replace("\n"," ")
            part2 = tmpBody.split(" ")[0].replace(",","") if tmpBody else part1
        part3 = None
        part4 = None
        part5 = push[u'iden'] if 'iden' in push else None
        if push['type'] == u'link':
            part3 = push[u'url']
            part4 = body
        elif push['type'] == u'note':
            part3 = body
        elif push['type'] == 'clip':
            part3 = body
            part2 = dev if dev else part2
        if push['type'] in (u'link', u'note', u'clip'):
            self.EventTrigger(part1, part2, part3, part4, part5, dev, ts)
        elif push['type'] == u'file':
            image = push[u'file_type'].split(r"/")[0] == u'image'
            self.TriggerEvent(
                "Image" if image else "File",
                payload = [
                    push[u'file_name'],
                    push[u'file_type'],
                    push[u'file_url'],
                    body,
                    dev,
                    ts
                ]
            )
            flpth = join(self.fldr, push[u'file_name'])
            self.urlretrieve(push[u'file_url'], flpth = flpth)


    def DisableMirroring(self, pushDict, app):
        push = {
            'type': 'mute',
            'source_user_iden': pushDict['source_user_iden'],
            "source_device_iden": self.iden,
            'package_name': pushDict['package_name']
        }
        push = push if self.key is None else \
            {
                'encrypted': True,
                'ciphertext': gcm_encrypt(self.key, dumps(push))
            }
        res, flag = self.request(
            "POST",
            API + 'ephemerals',
            data = {"type": "push", "push":push}
        )
        self.Log(self.text.rspnsr % repr(res), 4)
        if not flag:
            self.Log(self.text.fTriggMute % app, 1)
            return
        self.Log(self.text.triggMute % app, 3)
        self.updateConfig(disabled = (
            {'source_user_iden':pushDict['source_user_iden'],
            'package_name': pushDict['package_name']},
            app
        ))


    def EnableMirroring(self, push, app):
        push['type'] = 'unmute'
        push['source_device_iden'] = self.iden
        push = push if self.key is None else \
            {
                'encrypted': True,
                'ciphertext': gcm_encrypt(self.key, dumps(push))
            }
        res, flag = self.request(
            "POST",
            API + 'ephemerals',
            data = {"type": "push", "push":push}
        )
        self.Log(self.text.rspnsr % repr(res), 4)
        if not flag:
            self.Log(self.text.fTriggUnmute % app, 1)
            return
        self.Log(self.text.triggUnmute % app, 3)


    def EnableMirroringMany(self, lst):    
        for item in lst:
            self.EnableMirroring(*item)
        self.updateConfig(enabled = lst)


    def EnableDisablePopupsTsk(self, trItem, args):
        eg.actionThread.Func(trItem.SetArguments)(args) # __stop__ / __start__        
        eg.document.SetIsDirty()
        eg.document.Save()
 

    def EnableDisablePopups(self, pic, mirr, save):
        if not self.info.isStarted:
            return
        if pic == 2 and mirr == 2:
            return
        if (pic < 2 and self.autoOpen == pic) or pic == 3:
            self.autoOpen = not self.autoOpen
        if (mirr < 2 and self.enabMirr == mirr) or mirr == 3:
            self.enabMirr = not self.enabMirr
        if save:
            flag = False
            trItem = self.info.treeItem
            args = list(trItem.GetArguments())
            if args[12] != self.autoOpen:
                flag = True
                args[12] = self.autoOpen
            if args[14] != self.enabMirr:
                flag = True
                args[14] = self.enabMirr
            if flag:
                self.autoUpdate = True
                ct = currentThread()
                if ct == eg.actionThread._ThreadWorker__thread:
                    trItem.SetArguments(args) #automatically __stop__/__start__      
                    eg.document.SetIsDirty()
                    eg.document.Save()
                else:
                    eg.scheduler.AddTask(
                        0.01,
                        self.EnableDisablePopupsTsk,
                        trItem,
                        args
                    )


    def GetDevice(self, iden):
        tmp = [t[1] for t in self.targets]
        if iden in tmp:
            return [t[0] for t in self.targets][tmp.index(iden)]
        else:
            return iden


    def GetTargets(self, nick):
        tmp = [list(item) for item in self.targets if item[0] == nick]
        for item in tmp:
            item.append(True)
        return tmp


    def GetSingle(self, id):
        if id in [itm[1] for itm in self.targets]:
            return [itm for itm in self.targets if itm[1] == id]
        if id in [itm[0] for itm in self.targets]:
            return [itm for itm in self.targets if itm[0] == id]
        elif id in [itm['tag'] for itm in self.channels if itm['active']]:
            return [
                [itm['name'],itm['tag'],'channel'] for \
                itm in self.channels if itm['active'] and itm['tag'] == id]


    def requestPushes(self):        
        self.Log(self.text.gettPshs % self.modified_after, 4)
        res, flag = self.request("GET", API +  \
            'pushes?modified_after=%.7f&active=true' % self.modified_after)
        self.Log(self.text.rspnsr % repr(res), 4)
        if not flag or not isinstance(res, dict) or not 'pushes' in res: 
            self.Log(self.text.fLoadPshs, 1)
            return
        pushes = res['pushes']
        for push in pushes:
            try:
                self.processPush(push)
            except:
                eg.PrintTraceback()


    def uploadFile(self, filepath):

        def guess_type(filepath):
            return mimetype(filepath)[0] or 'application/octet-stream'
        
        baseName = basename(filepath)
        params = {
            "file_name": baseName.encode("utf-8"), 
            "file_type": guess_type(baseName)
        }
        resp, flag = self.request(
            "GET",
            API + "upload-request",
            params = params
        )
        if flag:
            if not isfile(filepath.encode("utf-8")):
                tmpfile = mktemp(".tmp", prefix = '_eg_')
                sh_copy(filepath, tmpfile)
            else:
                tmpfile = None
            local_file = tmpfile if tmpfile is not None else filepath
            data = [("file", (pycurl.FORM_FILE, local_file.encode("utf-8")))]
            c = pycurl.Curl()
            c.setopt(pycurl.URL, resp["upload_url"])
            c.setopt(pycurl.POST, 1)
            c.setopt(c.HTTPPOST, data)
            c.perform()
            response_code = c.getinfo(pycurl.RESPONSE_CODE)
            c.close()
            if tmpfile is not None:
                os_remove(tmpfile)
            if response_code == 204:
                return (resp["file_name"], resp["file_type"], resp["file_url"])


    def request(self, method, url, **kwargs):
        hdrs = [
            "X-User-Agent:EventGhost",
            "Authorization:Basic " + b64encode(self.api_key+":"),
            'Accept:application/json',
            "Content-type:application/json",
        ] if not 'headers' in kwargs else kwargs['headers']

        c = pycurl.Curl()
        if 'params' in kwargs:
            url = url + '?' + urlencode(kwargs['params'])
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, hdrs)
        if method == "POST":
            post_data = kwargs['data'] if 'data' in kwargs else {}
            postfields = dumps(post_data)
            c.setopt(pycurl.POST, 1)
            c.setopt(c.POSTFIELDS, postfields)
        elif method == 'DELETE': #rv = self.app.delete('/subscription?uuid=%s&service=%s' % (self.uuid, public))
            c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
        b = StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.perform()
        status_code = c.getinfo(c.RESPONSE_CODE)
        c.close()
        resp = b.getvalue()
        if status_code == 200:
            if method == "DELETE":
                return (resp, True)
            else:
                return (loads(resp), True)
        else:
            eg.PrintError(self.text.reqErr % str(resp))
            return (status_code, False)


    def updateConfig(self, iden = None, disabled = None, enabled = None):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        if iden:
            args[2] = iden
            self.Log(self.text.idenSaved % iden, 2)
            self.iden = args[2]
        elif disabled and disabled not in args[9]:
            args[9].append(disabled)
            self.Log(self.text.dsbldUpdated, 2)
            self.disabled = cpy(args[9])
        elif enabled:
            for item in enabled:
                del item[0]['type']
                del item[0]['source_device_iden']
                if item in args[9]:
                    args[9].remove(item)
            self.Log(self.text.dsbldUpdated, 2)
            self.disabled = cpy(args[9])
        self.autoUpdate = True
        eg.actionThread.Func(trItem.SetArguments)(args)       
        eg.document.SetIsDirty()
        eg.document.Save()


    def getAccount(self):
        account, flag = self.request("GET", API + 'users/me')
        if flag and isinstance(account, dict) and "email" in account:
            self.email = account["email"]
            self.source_user_iden = account["iden"]
            self.Log(self.text.emlObtained, 4)
        else:
            self.Log(self.text.accReqFailed, 1)


    def getSMSdevices(self):
        sms_devs = {}
        for dev in self.devices:
            if 'has_sms' in dev and dev['has_sms'] and dev['active']:
                sms_devs[dev['nickname']] = dev['iden']
        return sms_devs


    def getPhonebook(self, dev):
        sms_devs = self.getSMSdevices()
        if dev in list(sms_devs.iterkeys()):
            ph_book, flag = self.request(
                'GET',
                API + 'permanents/phonebook_' + sms_devs[dev])
            if flag:
                if ph_book.has_key('encrypted') and ph_book['encrypted']:
                    if self.key:
                        decrypted = gcm_decrypt(self.key, ph_book['ciphertext'])
                        try:
                            ph_book = loads(decrypted)
                            if not isinstance(ph_book, dict):
                                self.Log(self.text.e2eMssg2, 2)
                                return []
                        except:
                            self.Log(self.text.e2eMssg3, 2)
                            return []
                    else:
                        eg.PrintNotice(self.text.noKey)
                        return []
                self.Log(self.text.bookRcvd % dev, 4)
                phbook = ph_book['phonebook']
                choices = []
                for item in phbook:
                    choices.append(item['name'] + SEP + item['phone'])
                choices.sort(cmp = strcoll)
                return choices
            else:
                self.Log(self.text.bookReqFailed % dev, 2)
        return []


    def sendSMS(self, dev, recip, msg):
        sms_devs = self.getSMSdevices()
        if dev in list(sms_devs.iterkeys()):
            iden = sms_devs[dev]
            recip = recip.strip() if SEP not in recip else \
                recip.split(SEP)[1].strip()
            push = {
                "type":               "messaging_extension_reply",
                "package_name":       "com.pushbullet.android",
                "source_user_iden":   self.source_user_iden,
                "target_device_iden": iden,
                "source_device_iden": self.iden,
                "conversation_iden":  recip,
                "message":            msg,
            }
            push = push if self.key is None else \
                {
                    'encrypted': True,
                    'ciphertext': gcm_encrypt(self.key, dumps(push))
                }
            res, flag = self.request(
                "POST",
                API + 'ephemerals',
                data = {"type": "push", "push":push}
            )

            if flag:
                self.Log(self.text.smsSent % dev, 4)
            else:
                self.Log(self.text.smsSentF % dev, 2)


    def sendSMSmulti(self, recips, msg, dev = None):
        if dev is not None:
            for recip in recips:
                self.sendSMS(dev, recip, msg)
        else:
            for recip in recips:
                self.sendSMS(recip[0], recip[2], msg)


    def updateDevices(self):
        if self.flag1:
            return
        fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2],tuple)]
        if self.updateDevices in fcs:
            try:
                eg.scheduler.CancelTask(self.updtDvcs)
                return
            except:
                pass
        if not self.info.isStarted:
            return
        if not connectivity():
            self.stopWatchdog()
            self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)
            return
        if not self.api_key:
            self.Log(self.text.noApi, 1)
            return
        if not self.nickname:
            self.Log(self.text.noNick, 1)
            return
        self.flag1 = True
        self.flag2 = False

        if not self.email:
            self.getAccount()

        pssd = self.pssd.Get() if isinstance(self.pssd, eg.Password) else None
        if self.key is None and pssd and self.source_user_iden:
            self.key = PBKDF2(
                pssd,
                self.source_user_iden,
                30000,
                digestmodule = SHA256,
                macmodule = HMAC
            ).read(32)

        if not self.devices:
            devices, flag = self.request("GET", API + "devices?active=true")
            if flag and isinstance(devices, dict) and "devices" in devices:
                self.devices = devices["devices"]
                self.Log(self.text.devRcvd % repr(self.devices), 3)

                self.flagDev = True
                


                for dev in self.devices:
                    if not dev['active']: # ignore deleted device
                        continue
                    if not 'nickname' in dev or not dev['nickname']:
                        nick = dev['manufacturer'].capitalize() + ' ' + dev['model']
                        dev['nickname'] = nick
                nicknames = dict([(dev['nickname'], dev) for dev \
                    in self.devices if dev['active']])
                key_fingerprint = getKeyFingerprint(self.key)
                BODY['key_fingerprint'] = key_fingerprint
                if self.nickname in nicknames.iterkeys():
                    dev = nicknames[self.nickname]
                    if dev['manufacturer'] == u'EventGhost':
                        if self.iden != dev['iden']:
                            self.iden = dev['iden']
                            self.updateConfig(iden = self.iden)
                    else:
                        eg.PrintNotice(self.text.nicknameUsed % self.nickname)
                        if self.flag2:
                            self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
                            self.flag2 = False
                        self.flag1 = False
                        return
                    if self.key:
                        if not dev.has_key('key_fingerprint') or key_fingerprint != dev['key_fingerprint']:
                            me, flag = self.request("POST", API + 'devices/%s' % self.iden, data = BODY)
                else:
                    BODY['nickname'] = self.nickname
                    me, flag = self.request("POST", API + 'devices', data = BODY)
                    self.Log(self.text.pcMssng, 2)
                    if flag and isinstance(me, dict) and me:
                        self.Log(self.text.devCrtd % repr(me), 3)
                        self.iden = me['iden']
                        self.updateConfig(iden = self.iden)
                        if self.flag2:
                            self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
                            self.flag2 = False
                        self.flag1 = False
                        return
                    else:
                        self.Log(self.text.crDevFld, 1)
                        self.flag1 = False
                        if self.flag2:
                            self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
                            self.flag2 = False
                        return
            else:
                self.Log(self.text.devReqFailed, 1)
                self.flag1 = False
                self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
                self.flag2 = False
                return
        if not self.friends:
            friends, flag = self.request("GET", API + "contacts?active=true")
            if flag and isinstance(friends, dict) and "contacts" in friends:
                self.friends = friends["contacts"]
                self.Log(self.text.frndsRcvd % repr(self.friends), 3)
        if not self.channels:
            channels, flag = self.request("GET", API + "channels")
            if flag and isinstance(channels, dict) and "channels" in channels:
                self.channels = channels["channels"]
                self.Log(self.text.chnnlsRcvd % repr(self.channels), 3)
        self.targets = []
        for dev in self.devices:
            if not dev['active']:
                continue
            droid = 'android' if 'android_version' in dev\
                and dev['android_version'] is not None else 'pc'
            self.targets.append((dev['nickname'], dev['iden'], droid))
            if dev.has_key('has_sms') and dev['has_sms']:
                trds = self.requestThreads(dev['iden'])
                if trds:
                    self.sms_trds[dev['iden']] = dict([(i[u'id'],[i[u'latest'][u'timestamp'],i[u'latest'][u'id']]) for i in trds if i.has_key(u'latest') and i[u'latest'][u'direction'] == u'incoming'])
               
                
        for fr in self.friends:
            if not fr['active'] or fr['status'] == 'not_user':
                continue
            name = fr['name'] if 'name' in fr and fr['name'] else fr['email']
            self.targets.append((name, fr['email'], 'user'))
        for ch in self.channels:
            if not ch['active']:
                continue
            name = ch['name']
            self.targets.append((name, ch['tag'], 'channel'))
        self.Log(self.text.trgtsDrvd % repr(self.targets), 3)
        self.establishSubscriber()
        self.flag1 = False
        if self.flag2:
            self.updtDvcs = eg.scheduler.AddTask(5.0, self.updateDevices)
            self.flag2 = False


    def push(self, kind, trgts, data, suff = None):
        if not self.wsC:
            eg.actionThread.Call(eg.PrintNotice, self.text.waiting2)
            return
        kinds = [i.lower() for i in self.text.kinds]
        payload = {'type' : kinds[kind]}
        results = []
        ok = True
        if kind == 2: #file
            payload['body'] = data[0] if data[0] else None
            fl = data[1]
            fileInfo = self.uploadFile(fl)
            if not fileInfo: 
                eg.actionThread.Call(
                    self.Log,
                    self.text.uplFld % basename(fl),
                    1
                )
                return
            eg.actionThread.Call(
                self.Log,
                self.text.uplSucc % basename(fl),
                4
            )
            payload["file_name"] = fileInfo[0]
            payload["file_type"] = fileInfo[1]
            payload["file_url"]  = fileInfo[2]
            for trgt in trgts:
                if not trgt[3]:
                    continue
                dev = trgt[0]
                #check, if trgt is valid ?
                tmp = {'nickname':dev}
                if trgt[2] == 'user':
                    iden = 'email'
                    tmp['type']='friend'
                    if 'device_iden' in payload:
                        del payload['device_iden']
                    if 'channel_tag' in payload:
                        del payload['channel_tag']
                elif trgt[2] == 'channel':
                    iden = 'channel_tag'
                    tmp['type']='channel'
                    if 'device_iden' in payload:
                        del payload['device_iden']
                    if 'email' in payload:
                        del payload['email']
                else:
                    iden = 'device_iden'
                    tmp['type'] ='device'
                    if 'channel_tag' in payload:
                        del payload['channel_tag']
                    if 'email' in payload:
                        del payload['email']
                tmp[iden] = trgt[1]
                payload[iden] = trgt[1]
                res, flag = self.request("POST", API + "pushes", data = payload)
                if flag:
                    tmp['push_iden'] = res['iden']
                else:
                    ok = False
                tmp['ok'] = flag
                results.append(tmp)
            level = 4 if ok else 1
            eg.actionThread.Call(
                self.Log,
                self.text.pushRslt % repr(results),
                level
            )
            if suff:
                self.TriggerEvent("PushSent.%s" % suff, payload = results)
            return

        else: #if kind in (0, 1, 3):
            payload['title'] = data[0]
        if kind in (0, 3):
            payload['body'] = data[1]
        elif kind == 1:
            payload['url'] = data[1]
            payload['body'] = data[2] if data[2] else None
        payload[u'source_device_iden'] = self.iden
        for trgt in trgts:
            if not trgt[3]:
                continue
            dev = trgt[0]
            tmp = {'nickname':dev}
            if trgt[2] == 'user':
                iden = 'email'
                tmp['type']='friend'
                if 'device_iden' in payload:
                    del payload['device_iden']
                if 'channel_tag' in payload:
                    del payload['channel_tag']
            elif trgt[2] == 'channel':
                iden = 'channel_tag'
                tmp['type']='channel'
                if 'device_iden' in payload:
                    del payload['device_iden']
                if 'email' in payload:
                    del payload['email']
            else:
                iden = 'device_iden'
                tmp['type'] ='device'
                if 'email' in payload:
                    del payload['email']
                if 'channel_tag' in payload:
                    del payload['channel_tag']
            tmp[iden] = trgt[1]
            payload[iden] = trgt[1]
            #check, if trgt is valid ?
            if kind != 3:
                res, flag = self.request("POST", API + "pushes", data = payload) 
            else: # mirror
                payload['icon'] = getIcon(self.text.err, data[2])
                payload[u'application_name'] = eg.event.prefix if \
                    eg.event else 'EventGhost'

                payload = payload if self.key is None else \
                    {
                        'encrypted': True,
                        'ciphertext':gcm_encrypt(self.key, dumps(payload))
                    }
                
                res, flag = self.request(
                    "POST",
                    API + "ephemerals",
                    data = {
                        "type":"push",
                        "push":payload,
                        'targets': ['stream', 'android']
                    }
                )
            if flag:
                if 'iden' in res:
                    tmp['push_iden'] = res['iden']
            else:
                ok = False
            tmp['ok'] = flag
            results.append(tmp)
        level = 4 if ok else 1
        eg.actionThread.Call(self.Log, self.text.pushRslt % repr(results),level)
        if suff:
            self.TriggerEvent("PushSent.%s" % suff, payload = results)
        return


    def GetActiveDevices(self):
        actDevs = {}
        for device in self.devices:
            if device['active']:
                actDevs[device['iden']] = device['nickname']
        return actDevs


    def Configure(
        self,
        nickname = None,
        apiKey = "",
        iden = "",
        prefix = "PushBullet",
        mode = 0,
        fldr = "",
        debug = 3,
        hide = 15,
        pHide = 15,
        disabled = [],
        hideBtn = False,
        wavs = "",
        autoOpen = True,
        dummy = "",
        enabMirr = True,
        clr = (255, 255, 255),
        alignment = 0,
        dspl = 0,
        offset = (0, 0),
        filtered = [],
        pushGroups = [],
        smsGroups = [],
        password = "",
        firstWord = True,
        complPush = False
    ):
        self.disabled = []
        for item in disabled:                           # backward compatibility
            self.disabled.append(item if len(item)==2 else item[1:])

        if nickname is None:
            nickname = "EG-%s" % gethostname()
        if not isinstance(apiKey, eg.Password):
            api_key = eg.Password(None)
            api_key.Set(apiKey)
        else:
            api_key = apiKey
        if not isinstance(password, eg.Password):
            passw = eg.Password(None)
            passw.Set(password)
        else:
            passw = password
                
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.pushGroups = cpy(pushGroups)
        panel.smsGroups = cpy(smsGroups)
        if not fldr:
            fldr = eg.folderPath.TemporaryFiles
        nLabel = wx.StaticText(panel, -1, text.nLabel)
        nickCtrl = wx.TextCtrl(panel,-1,nickname)
        apiLabel = wx.StaticText(panel, -1, text.apiLabel)
        passwLabel = wx.StaticText(panel, -1, text.password)
        apiCtrl = wx.TextCtrl(panel, -1, api_key.Get(), style = wx.TE_PASSWORD)
        passwCtrl = wx.TextCtrl(panel, -1, passw.Get(), style = wx.TE_PASSWORD)
        prefixLabel = wx.StaticText(panel, -1, text.prefix)
        prefixCtrl = panel.TextCtrl(prefix)
        modeLabel = wx.StaticText(panel, -1, text.mode)
        rb0=panel.RadioButton(mode==0,self.text.modes[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode==1, self.text.modes[1])
        fldrLabel = wx.StaticText(panel, -1, text.folder)
        fldrCtrl = panel.DirBrowseButton(fldr)
        wavLabel = wx.StaticText(panel, -1, text.wavs)
        wavCtrl= eg.DirBrowseButton(
            panel,
            -1,
            toolTip = self.text.toolWav,
            dialogTitle = self.text.wavFldr,
            buttonText = eg.text.General.browse,
            startDirectory = join(
                abspath(dirname(__file__.decode('mbcs'))), 
                "sounds"
            ),
        )
        wavCtrl.SetValue(wavs)
        debugLabel = wx.StaticText(panel, -1, text.debug)
        debugLabel2 = wx.StaticText(panel, -1, text.debug2)
        debugCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            debug,
            min = 1,
            max = 5
        )
        button = wx.Button(panel, -1, self.text.reenab)
        hideBtnCtrl = wx.CheckBox(panel, 0, self.text.hideBtn)
        hideBtnCtrl.SetValue(hideBtn)
        hideLabel = wx.StaticText(panel, -1, text.timeout)
        hideLabel2 = wx.StaticText(panel, -1, text.timeout2)
        hideCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            hide,
            min = 0,
            max = 999
        )
        autoOpenCtrl = panel.CheckBox(autoOpen, self.text.autoOpen)
        firstWordCtrl = panel.CheckBox(firstWord, self.text.firstWord)
        complPushCtrl = panel.CheckBox(complPush, self.text.complPush)
        enabMirrCtrl = panel.CheckBox(enabMirr, self.text.enabMirr)
        pHideLabel = wx.StaticText(panel, -1, text.pTimeout)
        pHideLabel2 = wx.StaticText(panel, -1, text.timeout2)
        pHideCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            pHide,
            min = 0,
            max = 999
        )
        clipFilterCtrl = CheckListComboBox(
            panel,
            -1,
            values = [[],[],[]],
            helpText = text.clipFilter
        )
        if self.devices:
            actDevs = self.GetActiveDevices()
            items = list(self.GetActiveDevices().iterkeys())
            values = [
                [actDevs[item] for item in items],
                [item in filtered for item in items],
                actDevs
            ]
            def Sorted(lst):
                tmp = zip(lst[0], lst[1], lst[2])
                tmp.sort()
                return [
                    [item[0] for item in tmp],
                    [item[1] for item in tmp],
                    [item[2] for item in tmp]
                ]            
            clipFilterCtrl.SetValue(Sorted(values))
        else:
            clipFilterCtrl.Enable(False)
        clipFilterCtrl.SetToolTipString(text.filterToolTip) 
        clrLabel = wx.StaticText(panel, -1, text.bcgColour)
        algLabel = wx.StaticText(panel, -1, text.alignment)
        dspLabel = wx.StaticText(panel, -1, text.display)
        xOfLabel = wx.StaticText(panel, -1, text.xOffset)
        yOfLabel = wx.StaticText(panel, -1, text.yOffset)

        clrCtrl = panel.ColourSelectButton(clr)
        algCtrl = panel.Choice(
            alignment, choices=text.alignmentChoices
        )
        dspCtrl = eg.DisplayChoice(panel, dspl)
        xOfCtrl = panel.SpinIntCtrl(offset[0], -32000, 32000)
        yOfCtrl = panel.SpinIntCtrl(offset[1], -32000, 32000)

        pHideSizer = wx.BoxSizer(wx.HORIZONTAL)
        pHideSizer.Add(pHideCtrl, 0, wx.RIGHT, 5)
        pHideSizer.Add(pHideLabel2, 0, flag = ACV)        
        gridSizer = wx.GridBagSizer(10, 10)
        gridSizer.AddGrowableCol(1)
        gridSizer.Add(nLabel, (0,0), flag = ACV)
        gridSizer.Add(nickCtrl, (0, 1), flag = wx.EXPAND)
        gridSizer.Add(apiLabel, (1, 0), flag = ACV)
        gridSizer.Add(apiCtrl, (1, 1), flag = wx.EXPAND)
        gridSizer.Add(passwLabel, (2, 0), flag = ACV)
        gridSizer.Add(passwCtrl, (2, 1), flag = wx.EXPAND)
        gridSizer.Add(prefixLabel, (3, 0), flag = ACV)
        gridSizer.Add(prefixCtrl, (3, 1), flag = wx.EXPAND)
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        gridSizer.Add(modeLabel, (4, 0), flag = ACV)
        gridSizer.Add(modeSizer, (4, 1),flag = wx.EXPAND)
        gridSizer.Add(fldrLabel, (5, 0), flag = ACV)
        gridSizer.Add(fldrCtrl, (5, 1), flag = wx.EXPAND)
        debugSizer = wx.BoxSizer(wx.HORIZONTAL)
        debugSizer.Add(debugCtrl, 0, wx.RIGHT, 5)
        debugSizer.Add( debugLabel2, 0, flag = ACV)        
        gridSizer.Add(debugLabel, (6,0), flag = ACV)
        gridSizer.Add(debugSizer, (6, 1))
        gridSizer.Add(firstWordCtrl, (7, 0), (1, 2))
        gridSizer.Add(autoOpenCtrl, (8, 0), (1, 2))
        gridSizer.Add(pHideLabel, (9, 0), flag = ACV)
        gridSizer.Add(pHideSizer, (9, 1))
        gridSizer.Add(clipFilterCtrl, (10, 0), (1, 2), flag = wx.EXPAND)
        gridSizer.Add(wavLabel, (11, 0), flag = ACV)
        gridSizer.Add(wavCtrl, (11, 1), flag = wx.EXPAND)

        mSizer = wx.GridBagSizer(10, 5)
        mSizer.AddGrowableCol(2)
        mSizer.Add(enabMirrCtrl, (0, 0), (1, 3))
        mSizer.Add(clrLabel, (1, 0), flag = ACV)
        mSizer.Add(clrCtrl, (1, 1), flag = ACV)
        mSizer.Add(algLabel, (2, 0), flag = ACV)
        mSizer.Add(algCtrl, (2, 1), (1, 2), flag = ACV)
        mSizer.Add(dspLabel, (3, 0), flag = ACV)
        mSizer.Add(dspCtrl, (3, 1), (1, 2), flag = ACV)
        mSizer.Add(xOfLabel, (4, 0), flag = ACV)
        mSizer.Add(xOfCtrl, (4, 1), (1, 2), flag = ACV)
        mSizer.Add(yOfLabel, (5, 0), flag = ACV)
        mSizer.Add(yOfCtrl, (5, 1), (1, 2), flag = ACV)
        mSizer.Add(hideLabel, (6, 0), flag = ACV)
        mSizer.Add(hideCtrl, (6, 1))
        mSizer.Add(hideLabel2, (6, 2), flag = ACV)
        mSizer.Add(hideBtnCtrl, (7, 0), flag = ACV)
        mSizer.Add(complPushCtrl, (8, 0), flag = ACV)
        mSizer.Add(button, (9, 0))
        staticBox = wx.StaticBox(panel, -1, label = text.mirroring)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(mSizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(gridSizer, 0, wx.RIGHT|wx.EXPAND, 10)
        mainSizer.Add(staticBoxSizer, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer,0, wx.EXPAND|wx.ALL,10)

        def enableHidePicture(enable):
            pHideLabel.Enable(enable)
            pHideCtrl.Enable(enable)
            pHideLabel2.Enable(enable)
        enableHidePicture(autoOpen)


        def onAutoOpen(evt):
            enableHidePicture(evt.Checked())
            evt.Skip()
        autoOpenCtrl.Bind(wx.EVT_CHECKBOX, onAutoOpen)


        def disableMirrPopUp(disable):
            hideLabel.Enable(disable)
            hideCtrl.Enable(disable)
            hideLabel2.Enable(disable)
            hideBtnCtrl.Enable(disable)
            complPushCtrl.Enable(disable)
            button.Enable(disable)
            clrLabel.Enable(disable)
            algLabel.Enable(disable)
            dspLabel.Enable(disable)
            xOfLabel.Enable(disable)
            yOfLabel.Enable(disable)
            clrCtrl.Enable(disable)
            algCtrl.Enable(disable)
            dspCtrl.Enable(disable)
            xOfCtrl.Enable(disable)
            yOfCtrl.Enable(disable)
        disableMirrPopUp(enabMirr)


        def onDisMirr(evt):
            disableMirrPopUp(evt.Checked())
            evt.Skip()
        enabMirrCtrl.Bind(wx.EVT_CHECKBOX, onDisMirr)

        def onButton(evt):
            dlg = EnableDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowEnabDialog,
            )
            evt.Skip()
        button.Bind(wx.EVT_BUTTON, onButton)

        pushGroupBtn = wx.Button(panel.dialog, -1, text.pushGroupsTitle)

        def onPushGroupBtn(evt):
            dlg = PushGroupDialog(
                parent = panel,
                plugin = self,
            )
            wx.CallAfter(
                dlg.ShowPushGroupsDlg,
            )
            evt.Skip()
        pushGroupBtn.Bind(wx.EVT_BUTTON, onPushGroupBtn)
        panel.dialog.buttonRow.Add(pushGroupBtn)

        smsGroupBtn = wx.Button(panel.dialog, -1, text.smsGroupsTitle)

        def onSmsGroupBtn(evt):
            dlg = SmsGroupDialog(
                parent = panel,
                plugin = self,
            )
            wx.CallAfter(
                dlg.ShowSmsGroupsDlg,
            )
            evt.Skip()
        smsGroupBtn.Bind(wx.EVT_BUTTON, onSmsGroupBtn)
        panel.dialog.buttonRow.Add(smsGroupBtn)

        while panel.Affirmed():
            values = clipFilterCtrl.GetValue()
            actDevs = self.GetActiveDevices()
            idens = []
            for iden in actDevs:
                if iden in values[2]:
                    ix = values[2].index(iden)
                    if values[1][ix]:
                        idens.append(iden)
            oldKey = api_key.Get()
            newKey = apiCtrl.GetValue()
            if oldKey != newKey:
                api_key.Set(newKey)
                dummy = str(ttime())

            oldPassw = passw.Get()
            newPassw = passwCtrl.GetValue()
            if oldPassw != newPassw:
                passw.Set(newPassw)
                dummy = str(ttime())
            panel.SetResult(
                nickCtrl.GetValue(),
                api_key,
                self.iden,
                prefixCtrl.GetValue(),
                int(rb1.GetValue()),
                fldrCtrl.GetValue(),
                debugCtrl.GetValue(),
                hideCtrl.GetValue(),
                pHideCtrl.GetValue(),
                self.disabled,
                hideBtnCtrl.GetValue(),
                wavCtrl.GetValue(),
                autoOpenCtrl.GetValue(),
                dummy,
                enabMirrCtrl.GetValue(),
                clrCtrl.GetValue(),
                algCtrl.GetValue(),
                dspCtrl.GetValue(),
                (xOfCtrl.GetValue(), yOfCtrl.GetValue()),
                idens,
                panel.pushGroups,
                panel.smsGroups,
                passw,
                firstWordCtrl.GetValue(),
                complPushCtrl.GetValue()
           )
#===============================================================================

class Push(eg.ActionBase):

    class text:
        limit = "Files must be smaller than 25 MB"
        lbls1 = (
            "Title:",
            "Link title:",
            "Message:",
            "Title:"
        )
        lbls2 = (
            "Message:",
            "Link (something like http://eventghost.net/forum):",
            "File:",
            "Message:"
        )
        lbl3 = "Icon (path to image or base64 string):"
        toolTipFile = '''Type filename or click browse to choose file
Files must be smaller than 25 MB'''
        toolTipIcon = '''Type filename or click browse to choose image
or enter base64 string'''
        browseFile = 'Choose a file'
        browseIcon = 'Choose a image file'
        cont = "Push contents:"
        fMask = "All files (*.*)|*.*"
        iMask = (
            "JPG files (*.jpg)|*.jpg"
            "|BMP files (*.bmp)|*.bmp"
            "|PNG files (*.png)|*.png"
            "|All files (*.*)|*.*"
        )
        ever = 'Everything'
        suffix = "Event suffix when completed:"
        toolTipSuff = '''If you fill out this field, then after sending 
of push(-es) it will be triggered an event, carrying  a result (as a payload). 
If the field is left blank, the event will not be triggered.'''
        smartLabel = "Apply, push and close"
        smartTip = "The changes are saved, push is sent and the dialog closes."
        grLabel = "Group:"
        target = "Push target:"
        toolTipSingle = """The target can be a device or a friend or channel.
You can use iden, (nick)name, email or channel tag.
You can also use variables - for example {eg.result} or {eg.event.payload} ."""

    def __call__(self, kind = 0, trgts = [], data = ["",""], suff=""):
        if self.value == "Everything":
            trgts = [['Everything', None, 'everything', True]]
        elif self.value == "Reply":
            trgts = self.plugin.GetTargets(eg.event.payload[-2])
            trgts = trgts if trgts else [['Everything',None,'everything',True]]
        elif self.value == "Gr":
            tmp = [itm[0] for itm in self.plugin.pushGroups]
            if trgts in tmp:
                ix = tmp.index(trgts)
                trgts = self.plugin.pushGroups[ix][1]
            else:
                return # no targets
        elif self.value == "Single":
            if not isinstance(trgts, (str, unicode)):
                return
            trgts = eg.ParseString(trgts)
            trgts = self.plugin.GetSingle(trgts)
            if not trgts:
                return
            else:
                trgts = list(trgts[0])
                trgts.append(True)
                trgts = [trgts]
        suff = eg.ParseString(suff)
        pdt = len(data) * [None]
        pdt[0] = eg.ParseString(data[0])
        pdt[1] = eg.ParseString(data[1])
        if len(data) > 2:
            pdt[2] = eg.ParseString(data[2])
        pushThread = Thread(
            target = self.plugin.push,
            args = (kind, trgts, pdt, suff)
        )
        pushThread.start()


    def GetLabel(self, kind, trgts, data, suff):
        k = self.plugin.text.kinds[kind]
        if self.value == "Everything":
            ts = self.text.ever
        elif self.value == "Reply":
            return "%s: %s" % (self.name, k)
        elif self.value in ("Gr", "Single"):
            ts = trgts
        else:
            ts = [i[0] for i in trgts if i[3]]
            ts = repr(ts) if len(ts) > 1 else '"%s"' % ts[0]
        return "%s: %s to %s" % (self.name, k.lower(), ts)
         

    def Configure(self, kind = 0, trgts = [], data = ["",""], suff = ""):
        text = self.text
        self.kind = kind
        panel = eg.ConfigPanel(self)
        self.ts = []
        if self.value == "Gr":
            tsLabel = wx.StaticText(panel, -1, self.text.grLabel)
            tsCtrl = wx.Choice(
                panel,
                -1,
                choices = [itm[0] for itm in self.plugin.pushGroups],
                size = ((-1, 200)),
            )
            if isinstance(trgts, (str, unicode)):
                tsCtrl.SetStringSelection(trgts)
        elif self.value == "Single":
            if not isinstance(trgts, (str, unicode)):
                trgts = ""
            tsLabel = wx.StaticText(panel, -1, self.text.target)
            tsCtrl = wx.TextCtrl(panel, -1, trgts, size = (200, -1))
            tsLabel.SetToolTipString(text.toolTipSingle)
            tsCtrl.SetToolTipString(text.toolTipSingle)
            
        elif not self.value:
            self.ts = cpy(trgts)
            for t in self.ts:
                if tuple(t[:3]) not in self.plugin.targets:
                    self.ts.remove(t)
            tmp = []
            for t in self.plugin.targets:
                tmp2 = [i[:3] for i in self.ts]
                if list(t) in tmp2:
                    tmp.append(list(self.ts[tmp2.index(list(t))]))
                else:
                    tmp.append([t[0], t[1], t[2], False])
            self.ts = tmp
            items = [n[0] for n in self.ts]
            tsLabel = wx.StaticText(panel, -1, self.plugin.text.tsLabel)
            tsCtrl = wx.CheckListBox(
                panel,
                -1,
                choices = items,
                size = ((-1, 200)),
            )
            for i, item in enumerate(self.ts):
                tsCtrl.Check(i, item[3])


            def removeTargets():
                for i, t in enumerate(self.ts):
                    if t[2] != 'pc':
                        self.ts[i][3] = False
                        tsCtrl.Check(i, False)
            
            def afterCheckListBox():
                tsCtrl.SetSelection(self.ix)
                if tsCtrl.IsChecked(self.ix):
                    if self.kind==3 and self.plugin.targets[self.ix][2] != 'pc':
                        tsCtrl.Check(self.ix, False)
                        self.ts[self.ix][3] = False
                    else:
                        self.ts[self.ix][3] = True
                else:
                    self.ts[self.ix][3] = False


            def onCheckListBox(evt):
                self.ix = evt.GetInt()
                wx.CallAfter(afterCheckListBox)
                evt.Skip()
            tsCtrl.Bind(wx.EVT_CHECKLISTBOX, onCheckListBox)
            
            def UpdateSize():
                h = leftSizer.GetSize()[1]
                tsCtrl.SetSize((-1, h - 17))

            def OnSize(event):
                wx.CallAfter(UpdateSize)
                event.Skip()
            panel.Bind(wx.EVT_SIZE, OnSize)


        def onClick(event):
            b = wx.FindWindowById(buttons[self.kind])
            b.SetBitmapLabel(grayed(bmps[self.kind])) # reset to gray
            id = event.GetId()
            self.kind = buttons.index(id)
            b = wx.FindWindowById(id)
            b.SetBitmapLabel(bmps[self.kind])         # selected -> color
            setDynCtrls()
            if not self.value and self.kind == 3:
                removeTargets()
            event.Skip()

        buttons = (
            wx.NewId(),wx.NewId(),wx.NewId(),
            wx.NewId(),wx.NewId(),wx.NewId()
        )
        buttonSizer = wx.GridBagSizer(0, 0)
        bmps = []
        kinds = self.plugin.text.kinds if self.value\
            else self.plugin.text.kinds[:-1]
        for i, icon in enumerate(kinds):
            id = buttons[i]
            bmp = wx.Bitmap(join(ICON_DIR, icon + ".png"), wx.BITMAP_TYPE_PNG)
            bmps.append(bmp)
            g = grayed(bmp)
            b = wx.BitmapButton(
                panel,
                id,
                g if i != kind else bmp,
                size = (32, 32),
                style = wx.NO_BORDER
            )
            b.SetBitmapHover(bmp)
            if i==2:
                b.SetToolTipString(text.limit)
            buttonSizer.Add(b,(0,2*i))
            if i < 3:
                buttonSizer.Add((18,-1),(0,2*i+1))
            buttonSizer.Add(wx.StaticText(panel,-1,icon),(1,2*i),(1,2))
            b.Bind(wx.EVT_BUTTON, onClick, id=id)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        if not self.value or self.value in ("Gr", "Single"):
            leftSizer.Add(tsLabel)
            leftSizer.Add(tsCtrl,0,wx.TOP|wx.EXPAND,2)
        mainSizer.Add(leftSizer,0,wx.EXPAND|wx.RIGHT, 10)
        
        sSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.VERTICAL
        )                
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        sSizer.Add(self.rightSizer,1,wx.EXPAND|wx.ALL,5)
        self.rightSizer.Add(buttonSizer)

        self.ids = [
            wx.NewId(),wx.NewId(),wx.NewId(),
            wx.NewId(),wx.NewId(),wx.NewId()
        ]

        def detachControl(id):
            cntrl = wx.FindWindowById(id)
            if cntrl:
                self.rightSizer.Detach(cntrl)
                cntrl.Destroy()

        def setDynCtrls(data = None, knd = None):
            rightSizer = self.rightSizer
            knd = self.kind if knd is None else knd
            for id in self.ids:
                detachControl(id)
            style = wx.TOP|wx.EXPAND
            flag = 0 if knd in (1, 2) else 1
            cntrl1 = wx.TextCtrl(
                panel,
                self.ids[0],
                data[0] if data and (knd != 2 or len(data) == 2) else ""
            )        # for backward compatibility ^^^^^^^^^^^^^^
            lbl1 = wx.StaticText(panel,self.ids[2],self.text.lbls1[knd]) 
            if knd == 2:
                if data and len(data) == 1: # for backward compatibility
                    data.insert(0, "")
                cntrl2 = eg.FileBrowseButton(
                    panel,
                    self.ids[1],
                    toolTip = text.toolTipFile,
                    dialogTitle = text.browseFile,
                    buttonText = eg.text.General.browse,
                    startDirectory = eg.folderPath.Documents,
                    initialValue = data[1] if data is not None else "",
                    fileMask = text.fMask,
                )  
            else:
                cntrl2 = wx.TextCtrl(
                    panel,
                    self.ids[1],
                    data[1] if data is not None else "",
                    style = wx.TE_MULTILINE if knd != 1 else 0
                )
            lbl2 = wx.StaticText(panel,self.ids[3],self.text.lbls2[knd])
            rightSizer.Add(lbl1,0,wx.TOP,10)
            rightSizer.Add(cntrl1,0,style,1)
            rightSizer.Add(lbl2,0,wx.TOP,10)
            rightSizer.Add(cntrl2,flag,style,1)                

            if knd in (1, 3):
                if knd == 1:
                    lbl3 = wx.StaticText(panel,self.ids[4],self.text.lbls2[0])
                    cntrl3 = wx.TextCtrl(
                        panel,
                        self.ids[5],
                        data[2] if data and len(data) > 2 else ""
                    )
                else:
                    lbl3 = wx.StaticText(panel,self.ids[4],self.text.lbl3)
                    cntrl3 = eg.FileBrowseButton(
                        panel,
                        self.ids[5],
                        toolTip = text.toolTipIcon,
                        dialogTitle = text.browseIcon,
                        buttonText = eg.text.General.browse,
                        startDirectory = eg.folderPath.Pictures,
                        initialValue = data[2] if data and len(data)>2 else "",
                        fileMask = text.iMask,
                    )                
                rightSizer.Add(lbl3,0,wx.TOP,10)
                rightSizer.Add(cntrl3,0,style,1)                    
            rightSizer.Layout()
        suffLbl = wx.StaticText(panel, -1, text.suffix)
        suffCtrl = wx.TextCtrl(panel, -1, suff)
        suffLbl.SetToolTipString(text.toolTipSuff)
        suffCtrl.SetToolTipString(text.toolTipSuff)
        suffSizer = wx.BoxSizer(wx.HORIZONTAL)
        suffSizer.Add(suffLbl, 0, ACV|wx.RIGHT, 8)
        suffSizer.Add(suffCtrl, 1, wx.EXPAND)
        rSizer = wx.BoxSizer(wx.VERTICAL)
        rSizer.Add(wx.StaticText(panel,-1,text.cont))
        rSizer.Add(sSizer, 1, wx.EXPAND|wx.TOP, -5)
        rSizer.Add(suffSizer, 0, wx.EXPAND|wx.TOP, 5)
        mainSizer.Add(rSizer,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,5)

        if not self.plugin.wsC:
            panel.Enable(False)

        smartButton = wx.Button(panel.dialog, -1, text.smartLabel)
        smartButton.SetToolTipString(text.smartTip)
        panel.dialog.buttonRow.Add(smartButton)

        def OnSmartButton(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)
        smartButton.Bind(wx.EVT_BUTTON, OnSmartButton)

        setDynCtrls(data = ("","",""), knd = 1) # dialog - size adjustment
        panel.GetParent().GetParent().Show()
        wx.CallAfter(setDynCtrls, data)

        while panel.Affirmed():
            data = []
            if self.value == "Gr":
                ts = tsCtrl.GetStringSelection()
            elif self.value == "Single":
                ts = tsCtrl.GetValue()
            else:
                ts = self.ts
            data.append(wx.FindWindowById(self.ids[0]).GetValue())
            data.append(wx.FindWindowById(self.ids[1]).GetValue())
            if self.kind in (1, 3):
                data.append(wx.FindWindowById(self.ids[5]).GetValue())
            panel.SetResult(
                self.kind,
                ts,
                data,
                suffCtrl.GetValue()
            )
#===============================================================================

class PushScreenshot(eg.ActionBase):

    class text:
        type = "Screenshot or clipboard options"
        types = ("Fullscreen", "Region", "Clipboard")
        descr = "Optional message:"
        suffix = "Event suffix when completed:"
        toolTipSuff = '''If you fill out this field, then after sending 
of push(-es) it will be triggered an event, carrying  a result (as a payload). 
If the field is left blank, the event will not be triggered.'''
        smartLabel = "Apply, push and close"
        smartTip = "The changes are saved, push is sent and the dialog closes."
        x_coord = "X-coordinate of the upper left corner:"
        y_coord = "Y-coordinate of the upper left corner:" 
        width = "The width of the region:" 
        height = "The height of the region:"
        noData = "PushBullet: The image can not be sent, there are no image datas"


    def __call__(
        self,
        trgts = [],
        region = (0,0,0,0),
        descr = "",
        suff = "",
        src = None
    ):
        src = int(region != (0, 0, 0, 0)) if src is None else src
        if self.value:
            trgts = [['Everything', None, 'everything', True]]
        if src == 2:
            im = grabclipboard()
            filename = "%s__clipboard.png"
        elif src == 1:
            im = grab(bbox = region) 
            filename = "%s__region.png"
        else:
            im = grab()
            filename = "%s__screenshot.png"
        filePath = join(
            eg.folderPath.TemporaryFiles,
            filename % self.plugin.nickname
        )
        if not im:
            eg.PrintError(self.text.noData)
            return
        im.save(filePath)
        descr = eg.ParseString(descr)
        suff = eg.ParseString(suff)
        pushThread = Thread(
            target = self.plugin.push,
            args = (2, trgts, (descr, filePath), suff)
        )
        pushThread.start()


    def GetLabel(self, trgts, region, descr, suff, src):
        src = int(region != (0, 0, 0, 0)) if src is None else src
        type_ = self.text.types[src]
        if self.value:
            return "%s: %s: %s" % (self.name, descr, type_)
        elif trgts:
            ts = [i[0] for i in trgts if i[3]]
            ts = repr(ts) if len(ts) > 1 else '"%s"' % ts[0]
            return "%s: %s: %s to %s" % (self.name, descr, type_, ts)
         

    def Configure(
        self,
        trgts = [],
        region = (0,0,0,0),
        descr = "",
        suff = "",
        src = None
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        if self.value:
            self.ts = []
        else:
            self.ts = cpy(trgts)
            for t in self.ts:
                if tuple(t[:3]) not in self.plugin.targets:
                    self.ts.remove(t)
            tmp = []
            for t in self.plugin.targets:
                tmp2 = [i[:3] for i in self.ts]
                if list(t) in tmp2:
                    tmp.append(list(self.ts[tmp2.index(list(t))]))
                else:
                    tmp.append([t[0], t[1], t[2], False])
            self.ts = tmp
            items = [n[0] for n in self.ts]
            tsLabel = wx.StaticText(panel, -1, self.plugin.text.tsLabel)
            tsCtrl = wx.CheckListBox(
                panel,
                -1,
                choices = items,
                size = ((-1, 200)),
            )
            for i, item in enumerate(self.ts):
                tsCtrl.Check(i, item[3])

            def afterCheckListBox():
                tsCtrl.SetSelection(self.ix)
                if tsCtrl.IsChecked(self.ix):
                    self.ts[self.ix][3] = True
                else:
                    self.ts[self.ix][3] = False

            def onCheckListBox(evt):
                self.ix = evt.GetInt()
                wx.CallAfter(afterCheckListBox)
                evt.Skip()
            tsCtrl.Bind(wx.EVT_CHECKLISTBOX, onCheckListBox)
            
            def UpdateSize():
                h = leftSizer.GetSize()[1]
                tsCtrl.SetSize((-1, h - 17))

            def OnSize(event):
                wx.CallAfter(UpdateSize)
                event.Skip()
            panel.Bind(wx.EVT_SIZE, OnSize)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        if not self.value:
            leftSizer = wx.BoxSizer(wx.VERTICAL)
            leftSizer.Add(tsLabel)
            leftSizer.Add(tsCtrl,0,wx.TOP|wx.EXPAND,2)
            mainSizer.Add(leftSizer,0,wx.EXPAND|wx.RIGHT, 10)
        
        sSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.type),
            wx.VERTICAL
        )                
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        sSizer.Add(rightSizer,1,wx.EXPAND|wx.ALL,5)

        src = int(region != (0, 0, 0, 0)) if src is None else src
        rb0 = panel.RadioButton(src == 0, text.types[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(src == 1, text.types[1])
        rb2 = panel.RadioButton(src == 2, text.types[2])
        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        rbSizer.Add(rb0)
        rbSizer.Add(rb1, 0, wx.LEFT|wx.RIGHT, 25)
        rbSizer.Add(rb2)
        rightSizer.Add(rbSizer)
        regionSizer = wx.FlexGridSizer(4, 2, 2, 15)
        xlbl = wx.StaticText(panel, 0, text.x_coord)
        ylbl = wx.StaticText(panel, 0, text.y_coord)
        wlbl = wx.StaticText(panel, 0, text.width)
        hlbl = wx.StaticText(panel, 0, text.height)
        xctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[0],
            min = 0,
            max = 10000
        )
        yctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[1],
            min = 0,
            max = 10000
        )
        wctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[2],
            min = 0,
            max = 10000
        )
        hctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[3],
            min = 0,
            max = 10000
        )

        def onRadioBox(evt = None):
            flg = rb1.GetValue()
            xlbl.Enable(flg)
            xctrl.Enable(flg)
            ylbl.Enable(flg)
            yctrl.Enable(flg)
            wlbl.Enable(flg)
            wctrl.Enable(flg)
            hlbl.Enable(flg)
            hctrl.Enable(flg)
            if not flg:
                xctrl.SetValue(0)
                yctrl.SetValue(0)
                wctrl.SetValue(0)
                hctrl.SetValue(0)
            if evt:
                evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb2.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        onRadioBox()

        desLbl = wx.StaticText(panel, -1, text.descr)
        desCtrl = wx.TextCtrl(panel, -1, descr)
        regionSizer.Add(xlbl, 0, ACV)
        regionSizer.Add(xctrl)
        regionSizer.Add(ylbl, 0, ACV)
        regionSizer.Add(yctrl)
        regionSizer.Add(wlbl, 0, ACV)
        regionSizer.Add(wctrl)
        regionSizer.Add(hlbl, 0, ACV)
        regionSizer.Add(hctrl)
        rightSizer.Add(regionSizer, 0, wx.TOP, 13)
        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        descSizer.Add(desLbl, 0, ACV|wx.RIGHT, 10)
        descSizer.Add(desCtrl, 1, wx.EXPAND)
        rightSizer.Add(descSizer, 0, wx.EXPAND|wx.TOP, 15)

        suffLbl = wx.StaticText(panel, -1, text.suffix)
        suffCtrl = wx.TextCtrl(panel, -1, suff)
        suffLbl.SetToolTipString(text.toolTipSuff)
        suffCtrl.SetToolTipString(text.toolTipSuff)
        suffSizer = wx.BoxSizer(wx.HORIZONTAL)
        suffSizer.Add(suffLbl, 0, ACV|wx.RIGHT, 8)
        suffSizer.Add(suffCtrl, 1, wx.EXPAND)
        rSizer = wx.BoxSizer(wx.VERTICAL)
        rSizer.Add(sSizer, 1, wx.EXPAND|wx.TOP, 0)
        rSizer.Add(suffSizer, 0, wx.EXPAND|wx.TOP, 5)
        mainSizer.Add(rSizer,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,5)

        if not self.plugin.wsC:
            panel.Enable(False)

        smartButton = wx.Button(panel.dialog, -1, text.smartLabel)
        smartButton.SetToolTipString(text.smartTip)
        panel.dialog.buttonRow.Add(smartButton)

        def OnSmartButton(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)
        smartButton.Bind(wx.EVT_BUTTON, OnSmartButton)

        while panel.Affirmed():
            data = []
            panel.SetResult(
                self.ts,
                (
                    xctrl.GetValue(),
                    yctrl.GetValue(),
                    wctrl.GetValue(),
                    hctrl.GetValue()
                ),
                desCtrl.GetValue(),
                suffCtrl.GetValue(),
                rb1.GetValue() + 2 * rb2.GetValue() 
            )
#===============================================================================

class DeletePush(eg.ActionBase):

    class text:
        lbl = "Push iden:"


    def __call__(self, iden = ""):
        iden = eg.ParseString(iden)
        self.plugin.deletePush(iden)


    def Configure(self, iden = ""):
        panel = eg.ConfigPanel()
        lbl = wx.StaticText(panel, -1, self.text.lbl)
        pushCtrl = wx.TextCtrl(panel, -1, iden)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(lbl, 0, ACV)
        mainSizer.Add(pushCtrl, 1, wx.EXPAND|wx.LEFT, 8)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        while panel.Affirmed():
            panel.SetResult(
                pushCtrl.GetValue(),
            )
#===============================================================================

class SendReply(eg.ActionBase):

    class text:
        lblPush = "Reply push:"
        lblMsg = "Reply message:"


    def __call__(self, push = "{eg.event.payload[3]}", msg = ""):
        push = self.plugin.parseArgument(push)
        msg = eg.ParseString(msg)
        self.plugin.sendReply(push, msg)


    def GetLabel(self, push, msg):
        msg = msg.replace("\n","<LF>")
        return "%s: %s" % (self.name, msg if len(msg)<13 else msg[:12]+" .....")


    def Configure(self, push = "{eg.event.payload[3]}", msg = ""):
        panel = eg.ConfigPanel()
        lblPush = wx.StaticText(panel, -1, self.text.lblPush)
        lblMsg = wx.StaticText(panel, -1, self.text.lblMsg)
        pushCtrl = wx.TextCtrl(panel, -1, push)
        msgCtrl = wx.TextCtrl(panel, -1, msg, style = wx.TE_MULTILINE)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 10)
        mainSizer.AddGrowableRow(0)    
        mainSizer.AddGrowableCol(1)    
        mainSizer.Add(lblMsg, 0, wx.TOP, 3)
        mainSizer.Add(msgCtrl, 1, wx.EXPAND)
        mainSizer.Add(lblPush, 0, ACV)
        mainSizer.Add(pushCtrl, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND|wx.ALL, 10)
        
        while panel.Affirmed():
            panel.SetResult(
                pushCtrl.GetValue(),
                msgCtrl.GetValue()
            )
#===============================================================================

class Dismiss(eg.ActionBase):

    class text:
        lblPush = "Push dictionary (for mirror) or push iden:"


    def __call__(self, pushDict = "{eg.event.payload[-1]}"):
        pushDict = self.plugin.parseArgument(pushDict)
        self.plugin.dismiss(pushDict)


    def GetLabel(self, pushDict):
        return "%s: %s" % (self.name, pushDict)


    def Configure(self, pushDict = "{eg.event.payload[-1]}"):
        panel = eg.ConfigPanel()
        lblPush = wx.StaticText(panel, -1, self.text.lblPush)
        pushCtrl = wx.TextCtrl(panel, -1, pushDict)
        mainSizer = wx.FlexGridSizer(1, 2, 10, 10)  
        mainSizer.AddGrowableCol(1)    
        mainSizer.Add(lblPush, 0, ACV)
        mainSizer.Add(pushCtrl, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND|wx.ALL, 10)
        
        while panel.Affirmed():
            panel.SetResult(
                pushCtrl.GetValue()
            )
#===============================================================================

class PhonebookChoice(wx.ComboBox):
    phbook = []

    def __init__(self, parent, id, phbook, plugin, val, pos=wx.DefaultPosition):
        wx.ComboBox.__init__(self, parent, id, pos = pos, choices = [])
        self.val = val
        self.plugin = plugin
        self.Set(phbook)


    def GetSel(self):
        return self.GetValue()


    def SetSel(self, val):
        strings = self.GetStrings()
        if val:
            if SEP in val:
                if val in strings:
                    self.SetStringSelection(val)
                else:
                    phone = val.split(SEP)[1].strip()
                    v = [itm for itm in strings if itm.split(SEP)[1].strip() \
                        == phone]
                    if v:
                        self.SetStringSelection(v[0])
                    else: 
                        self.SetStringSelection(phone)
            else:
                v = [itm for itm in strings if itm.split(SEP)[1].strip() == \
                    val.strip()]
                if v:
                    self.SetStringSelection(v[0])
                else: 
                    self.SetStringSelection(val)


    def Set(self, phbook):
        self.Clear()
        self.phbook = phbook
        self.SetItems(self.phbook)
        if self.val:
            self.SetSel(self.val)
#===============================================================================

class SendSMS(eg.ActionBase):

    class text:
        device = "Device:"
        recip = "Recipient:"
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."

    def __call__(self, dev = "", recip = "", msg = ""):
        dev = self.plugin.parseArgument(dev)
        recip = eg.ParseString(recip)
        msg = eg.ParseString(msg)
        self.plugin.sendSMS(dev, recip, msg)


    def GetLabel(self, dev, recip, msg):
        msg = msg.replace("\n","<LF>")
        return "%s: %s: %s: %s" % (
            self.name,
            dev,
            recip,
            msg if len(msg)<13 else msg[:12]+" ....."
        )


    def Configure(self, dev = "", recip = "", msg = ""):
        panel = eg.ConfigPanel()
        lblDev = wx.StaticText(panel, -1, self.text.device)
        lblRec = wx.StaticText(panel, -1, self.text.recip)
        lblMsg = wx.StaticText(panel, -1, self.text.message)
        try:
            choices = list(self.plugin.getSMSdevices().iterkeys())
        except:
            choices = []
        ctrlDev = wx.Choice(panel, -1, choices = choices)
        if choices:
            ctrlDev.SetStringSelection(dev)
        phbook = self.plugin.getPhonebook(dev)
        ctrlRec = PhonebookChoice(panel, -1, phbook, self.plugin, recip)
        ctrlMsg = wx.TextCtrl(panel, -1, msg, style = wx.TE_MULTILINE)
        mainSizer = wx.FlexGridSizer(3, 2, 10, 10)
        mainSizer.AddGrowableRow(2)    
        mainSizer.AddGrowableCol(1)    
        mainSizer.Add(lblDev, 0, ACV)
        mainSizer.Add(ctrlDev, 0, wx.EXPAND)
        mainSizer.Add(lblRec, 0, ACV)
        mainSizer.Add(ctrlRec, 0, wx.EXPAND)
        mainSizer.Add(lblMsg, 0,  wx.TOP,3)
        mainSizer.Add(ctrlMsg, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND|wx.ALL, 10)

        def onDev(evt = None):
            dev = ctrlDev.GetStringSelection()
            phbook = self.plugin.getPhonebook(dev)
            ctrlRec.Set(phbook)
            if evt:
                evt.Skip()
        ctrlDev.Bind(wx.EVT_CHOICE, onDev)
        onDev()

        smartButton = wx.Button(panel.dialog, -1, self.text.smartLabel)
        smartButton.SetToolTipString(self.text.smartTip)
        panel.dialog.buttonRow.Add(smartButton)

        def OnSmartButton(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)
        smartButton.Bind(wx.EVT_BUTTON, OnSmartButton)

        while panel.Affirmed():
            panel.SetResult(
                ctrlDev.GetStringSelection(),
                ctrlRec.GetSel(),
                ctrlMsg.GetValue()
            )
#===============================================================================

class SendSMS2list(eg.ActionBase):

    class text:
        device = "Device:"
        filepath = "File with list of numbers:"
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."
        fileMask = (
            "CSV files (*.csv)|*.csv"
            "|TXT files (*.txt)|*.txt"
            "|All files (*.*)|*.*"
        )
        msgMask = (
            "TXT files (*.txt)|*.txt"
            "|All files (*.*)|*.*"
        )
        toolTipFile = 'Type filename or click browse to choose file'
        browseFile = 'Choose a file'
        src = "Message source:"
        srcs = ("File", "Text box")
        encoding = "File encoding:"


    def __call__(self, dev = "", filepath = "", msg = "", src = 1, enc = 0):
        col = 0
        sep = "\t"
        filepath = eg.ParseString(filepath)
        msg = eg.ParseString(msg)
        if not src:      
            f = openFile(msg, 'r', enc, 'replace')
            msg = f.read()
            f.close()
        f = open(filepath, 'r')
        data = [item.split(sep) for item in f.readlines()]
        tmp = [item[col].strip() for item in data]
        numbers = []
        for item in tmp:
            num = check(item)
            if num:
                numbers.append(num)
        f.close()
        self.plugin.sendSMSmulti(numbers, msg, dev)


    def GetLabel(self, dev, filepath, msg, src, enc):
        msg = msg.replace("\n","<LF>")
        return "%s: %s: %s: %s" % (
            self.name,
            dev,
            filepath,
            msg if len(msg)<13 else msg[:12]+" ....."
        )


    def Configure(self, dev = "", filepath = "", msg = "", src = 1, enc = ""):
        self.enc = enc
        panel = eg.ConfigPanel()
        text = self.text
        ctrls = [wx.NewId(), wx.NewId()]
        lblDev = wx.StaticText(panel, -1, text.device)
        lblPath = wx.StaticText(panel, -1, text.filepath)
        try:
            choices = list(self.plugin.getSMSdevices().iterkeys())
        except:
            choices = []
        ctrlDev = wx.Choice(panel, -1, choices = choices)
        if choices:
            ctrlDev.SetStringSelection(dev)        
        
        fileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = text.toolTipFile,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Documents,
            initialValue = filepath,
            fileMask = text.fileMask
        )
        srcLabel = wx.StaticText(panel, -1, text.src)
        rb0=panel.RadioButton(src == 0, self.text.srcs[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(src == 1, self.text.srcs[1])

        srcSizer = wx.BoxSizer(wx.HORIZONTAL)
        srcSizer.Add(rb0)
        srcSizer.Add(rb1, 0, wx.LEFT, 10)
        mainSizer = wx.FlexGridSizer(0, 2, 10, 10)
        mainSizer.AddGrowableCol(1)    
        mainSizer.Add(lblDev, 0, flag=ACV)
        mainSizer.Add(ctrlDev, 0, flag=wx.EXPAND)
        mainSizer.Add(lblPath, 0, flag=ACV)
        mainSizer.Add(fileCtrl, 0, flag=wx.EXPAND)
        mainSizer.Add(srcLabel, 0, flag=ACV)
        mainSizer.Add(srcSizer,0)

        def onSource2(flag = False):
            if rb1.GetValue():
                lblMsg = wx.StaticText(panel, -1, text.message)
                ctrlMsg = wx.TextCtrl(
                    panel, 
                    ctrls[0], 
                    "", 
                    style = wx.TE_MULTILINE
                )
                if flag:
                    ctrlMsg.ChangeValue(msg)
                mainSizer.Add(lblMsg, 0,  wx.TOP,3)
                mainSizer.Add(ctrlMsg, 1, wx.EXPAND)
                mainSizer.AddGrowableRow(3)
            else:
                lblMsg = wx.StaticText(panel, -1, text.message)
                ctrlMsg = eg.FileBrowseButton(
                    panel,
                    ctrls[0],
                    toolTip = text.toolTipFile,
                    dialogTitle = text.browseFile,
                    buttonText = eg.text.General.browse,
                    startDirectory = eg.folderPath.Documents,
                    initialValue = "",
                    fileMask = text.msgMask
                )
                lblEnc = wx.StaticText(panel, -1, text.encoding)
                encTypes = []
                for key, value in aliases.aliases.items():
                    if value not in encTypes:
                        encTypes.append(value)
                        
                encTypes = sorted(encTypes)
                ctrlEnc = wx.Choice(panel, ctrls[1], choices = encTypes)
                if self.enc == "" and eg.systemEncoding in encTypes:
                    self.enc = eg.systemEncoding                
                if flag:
                    ctrlMsg.SetValue(msg)
                ctrlEnc.SetStringSelection(self.enc)
                mainSizer.Add(lblMsg, 0,  wx.TOP,3)
                mainSizer.Add(ctrlMsg, 1, wx.EXPAND)
                mainSizer.Add(lblEnc, 0,  wx.TOP,3)
                mainSizer.Add(ctrlEnc, 1, wx.EXPAND)
            mainSizer.Layout()
        onSource2(True)

        def onSource(evt):
            chldrns = list(mainSizer.GetChildren())
            cnt = len(chldrns)
            if cnt == 8:
                mainSizer.RemoveGrowableRow(3)
            for i in range(cnt - 1, 5, -1):
                win = chldrns[i].GetWindow()
                mainSizer.Detach(i)
                win.Destroy()
            onSource2()
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onSource)
        rb1.Bind(wx.EVT_RADIOBUTTON, onSource)

        panel.sizer.Add(mainSizer, 1, wx.EXPAND|wx.ALL, 10)

        smartButton = wx.Button(panel.dialog, -1, text.smartLabel)
        smartButton.SetToolTipString(text.smartTip)
        panel.dialog.buttonRow.Add(smartButton)

        def OnSmartButton(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)
        smartButton.Bind(wx.EVT_BUTTON, OnSmartButton)

        while panel.Affirmed():
            src = int(rb1.GetValue())
            ctrlEnc = wx.FindWindowById(ctrls[1])
            panel.SetResult(
                ctrlDev.GetStringSelection(),
                fileCtrl.GetValue(),
                wx.FindWindowById(ctrls[0]).GetValue(),
                src,
                ctrlEnc.GetStringSelection() if not src else "",              
            )
#===============================================================================

class SendSMSmulti(eg.ActionBase):
    phbook = None

    class text:
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."

    def __call__(self, dev = "", recips = [], msg = ""):
        dev = self.plugin.parseArgument(dev)
        msg = eg.ParseString(msg)
        self.plugin.sendSMSmulti(recips, msg, dev)


    def GetLabel(self, dev, recips, msg):
        msg = msg.replace("\n", "<LF>")
        return "%s: %s: %s" % (
            self.name,
            dev,
            msg if len(msg) < 13 else msg[:12] + " ....."
        )


    def Configure(self, dev = "", recips2 = [], msg = ""):
        text = self.text
        ptext = self.plugin.text

        recips = recips2
        if recips2: # for backward compatibility
            if dev is not None and isinstance(recips2[0], unicode):
                recips = []
                for recip in recips2:
                    tmp = [dev]
                    nm, nr = getNmNr(recip)
                    tmp.append(nm)
                    tmp.append(nr)
                    recips.append(tmp)

        panel = eg.ConfigPanel()
        lblDev = wx.StaticText(panel, -1, ptext.device)
        lblRecs = wx.StaticText(panel, -1, ptext.recips)
        lblMsg = wx.StaticText(panel, -1, text.message)
        try:
            choices = list(self.plugin.getSMSdevices().iterkeys())
        except:
            choices = []
        ctrlDev = wx.Choice(panel, -1, choices = choices)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 10)
        mainSizer.AddGrowableRow(0)    
        mainSizer.AddGrowableRow(1)    
        mainSizer.AddGrowableCol(1)    

        staticBox = wx.StaticBox(panel, -1, "")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        bottomSizer = wx.FlexGridSizer(2, 2, 10, 10)
        bottomSizer.AddGrowableCol(1)
        listCtrl = Table(
            panel,
            ptext.header,
            3,
            ("DevName","Recipient name","XXXXXXXXXXXXXXXX")
        )
        listCtrl.SetData(recips)
        lblRec = wx.StaticText(panel, -1, ptext.recip)
        ctrlRec = PhonebookChoice(
            panel,
            -1,
            [],
            self.plugin,
            "",
        )
        btnAdd=wx.Button(panel, -1, ptext.insert)
        btnDel=wx.Button(panel, -1, ptext.delete)
        btnDel.Enable(False)
        btnSizer.Add(btnAdd)
        btnSizer.Add(btnDel, 0, wx.TOP, 10)
        topSizer.Add(listCtrl, 1, wx.EXPAND)
        topSizer.Add(btnSizer, 0, wx.LEFT, 10)
        staticBoxSizer.Add(topSizer, 1, wx.EXPAND)
        bottomSizer.Add(lblDev, 0, ACV)
        bottomSizer.Add(ctrlDev, 0, wx.EXPAND)
        bottomSizer.Add(lblRec, 0, ACV)
        bottomSizer.Add(ctrlRec, 0, wx.EXPAND)
        staticBoxSizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP, 10)
        ctrlMsg = wx.TextCtrl(panel, -1, msg, style = wx.TE_MULTILINE)

        mainSizer.Add(lblRecs, 0, wx.TOP, 6)
        mainSizer.Add(staticBoxSizer, 1, wx.EXPAND)
        mainSizer.Add(lblMsg, 0,  wx.TOP,3)
        mainSizer.Add(ctrlMsg, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND|wx.ALL, 10)


        def setRow():
            dev = ctrlDev.GetStringSelection()
            nm, nr = getNmNr(ctrlRec.GetSel())
            listCtrl.SetRow((dev, nm, nr))

        def onDev(evt):
            dev = ctrlDev.GetStringSelection()
            phbook = self.plugin.getPhonebook(dev)
            rcp = ctrlRec.GetValue()
            ctrlRec.Set(phbook)
            if rcp:
                ctrlRec.SetValue(rcp)
            setRow()
            evt.Skip()
        ctrlDev.Bind(wx.EVT_CHOICE, onDev)

        def onRec(evt):
            setRow()
            evt.Skip()
        ctrlRec.Bind(wx.EVT_COMBOBOX, onRec)

        def onSelect(evt):
            dev, nm, nr = listCtrl.GetRow()
            if dev != ctrlDev.GetStringSelection():
                if dev in ctrlDev.GetStrings():
                    ctrlDev.SetStringSelection(dev)
                    phbook = self.plugin.getPhonebook(dev)
                    ctrlRec.Set(phbook)
            ctrlRec.SetValue(nm + SEP + nr if nr != "" and nm != "" else nr)
            evt.Skip()
        listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, onSelect)

        def onChange(evt = None):
            selCnt = listCtrl.GetSelectedItemCount()
            enable = selCnt > 0
            if not enable:
                ctrlRec.SetValue("")
            btnDel.Enable(enable)
            ctrlRec.Enable(enable)
            ctrlDev.Enable(enable)
            lblRec.Enable(enable)
            lblDev.Enable(enable)
            if evt:
                evt.Skip()
        listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, onChange)
        listCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, onChange)
        onChange()

        def onDelete(evt):
            listCtrl.DeleteItem(listCtrl.GetSelectedIndex())
            evt.Skip()
        btnDel.Bind(wx.EVT_BUTTON, onDelete)


        def onAdd(evt):
            listCtrl.AddRow()
            if ctrlDev.GetStringSelection():
                setRow()
            evt.Skip()
        btnAdd.Bind(wx.EVT_BUTTON, onAdd)

        smartButton = wx.Button(panel.dialog, -1, text.smartLabel)
        smartButton.SetToolTipString(text.smartTip)
        panel.dialog.buttonRow.Add(smartButton)

        def OnSmartButton(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)
        smartButton.Bind(wx.EVT_BUTTON, OnSmartButton)

        while panel.Affirmed():
            panel.SetResult(
                None,
                listCtrl.GetData(),
                ctrlMsg.GetValue()
            )
#===============================================================================

class SendSMSgroup(eg.ActionBase):

    class text:
        group = "Group:"
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."

    def __call__(self, group = "", msg = ""):
        group = eg.ParseString(group)
        msg = eg.ParseString(msg)
        tmp = [itm[0] for itm in self.plugin.smsGroups]
        if group in tmp:
            ix = tmp.index(group)
            self.plugin.sendSMSmulti(self.plugin.smsGroups[ix][1], msg, None)



    def GetLabel(self, group, msg):
        msg = msg.replace("\n","<LF>")
        return "%s: %s: %s" % (
            self.name,
            group,
            msg if len(msg) < 13 else msg[:12] + " ....."
        )


    def Configure(self, group = "", msg = ""):
        panel = eg.ConfigPanel()
        lblGrp = wx.StaticText(panel, -1, self.text.group)
        lblMsg = wx.StaticText(panel, -1, self.text.message)
        ctrlGroup = wx.Choice(
            panel,
            -1,
            choices = [itm[0] for itm in self.plugin.smsGroups],
        )
        ctrlGroup.SetStringSelection(group)
        ctrlMsg = wx.TextCtrl(panel, -1, msg, style = wx.TE_MULTILINE)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 10)
        mainSizer.AddGrowableRow(1)    
        mainSizer.AddGrowableCol(1)    
        mainSizer.Add(lblGrp, 0, ACV)
        mainSizer.Add(ctrlGroup, 0, wx.EXPAND)
        mainSizer.Add(lblMsg, 0,  wx.TOP,3)
        mainSizer.Add(ctrlMsg, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND|wx.ALL, 10)

        smartButton = wx.Button(panel.dialog, -1, self.text.smartLabel)
        smartButton.SetToolTipString(self.text.smartTip)
        panel.dialog.buttonRow.Add(smartButton)

        def OnSmartButton(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)
        smartButton.Bind(wx.EVT_BUTTON, OnSmartButton)

        while panel.Affirmed():
            panel.SetResult(
                ctrlGroup.GetStringSelection(),
                ctrlMsg.GetValue()
            )
#===============================================================================

class JumpIf(eg.ActionBase):
    #iconFile = "../EventGhost/icons/NewJumpIf"

    class text:
        text1 = "If:"
        text2 = "Jump to:"
        mesg1 = "Select the macro..."
        mesg2 = (
            "Please select the macro that should be executed, if the "
            "condition is/is not fulfilled."
        )
        tooltip = "Enter a list of file extensions, separated by a comma "\
            "(eg txt, pdf, mp3)"


    def __call__(self, link, kind = 0, fl="", exts = ""):
        fl = eg.ParseString(fl)
        exts = exts.replace(" ","").split(",")
        dummy, fExt = splitext(fl)
        flinexts = fExt.lower()[1:] in [item.lower() for item in exts]
        if flinexts != bool(kind):
            nextItem = link.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.indent += 1
            eg.programCounter = (nextItem, nextIndex)
        return flinexts != bool(kind)


    def GetLabel(self, link, kind, fl, exts):
        return "%s %s %s%s %s (%s)" % (
            self.text.text2,
            link.target.name,
            self.plugin.text.ifExt,
            ("", self.plugin.text.notLbl)[kind],
            self.plugin.text.inLbl,
            exts,
        )


    def Configure(self, link = None, kind = 0, fl = "", exts = ""):
        text = self.text
        panel = eg.ConfigPanel()
        lbl1 = wx.StaticText(panel, -1, self.plugin.text.file)
        lbl2 = wx.StaticText(panel, -1, self.plugin.text.ext)
        ctrl1 = wx.TextCtrl(panel, -1, fl)
        ctrl1.SetToolTipString(text.tooltip)
        ctrl2 = wx.TextCtrl(panel, -1, exts)
        ctrl2.SetToolTipString(text.tooltip)
        kindCtrl = panel.Choice(kind, choices = self.plugin.text.choices)
        linkCtrl = panel.MacroSelectButton(
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link
        )
        labels = (
            panel.StaticText(text.text1),
            panel.StaticText(text.text2),
        )
        eg.EqualizeWidths(labels)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(lbl1)
        mainSizer.Add(ctrl1, 0, wx.EXPAND)
        mainSizer.Add(lbl2, 0, wx.TOP, 12)
        mainSizer.Add(ctrl2, 0, wx.EXPAND)
        sizer = wx.FlexGridSizer(3, 2, 15, 5)
        sizer.AddGrowableCol(1, 1)
        sizer.Add(labels[0], 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(kindCtrl)
        sizer.Add(labels[1], 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(linkCtrl, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(sizer,0,wx.TOP|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)

        while panel.Affirmed():
            panel.SetResult(
                linkCtrl.GetValue(),
                kindCtrl.GetValue(),
                ctrl1.GetValue(),
                ctrl2.GetValue()
            )
#===============================================================================

class OpenFile(eg.ActionBase):
    
    class text:
        open = "Open the file if"
        stop = "and stop the macro" 
        tooltip = "Enter a list of file extensions, separated by a comma "\
            "(eg txt, pdf, mp3)"

    def GetLabel(self, fl, exts, kind, stop):
        return "%s: %s %s%s %s (%s) %s" % (
            self.name,
            fl,
            self.plugin.text.ifExt,
            ("", self.plugin.text.notLbl)[kind],
            self.plugin.text.inLbl,
            exts,
            ("", self.text.stop)[int(stop)]
        )

    def __call__(
        self,
        fl = "{eg.event.payload}",
        exts = "",
        kind = 0,
        stop = True
    ):
        fl = eg.ParseString(fl)
        exts = exts.replace(" ","").split(",")
        dummy, fExt = splitext(fl)
        flinexts = fExt.lower()[1:] in [item.lower() for item in exts]
        if flinexts:
            try:
                startfile(fl)
            except:
                pass
        if (kind == 1 and flinexts) or (kind == 2 and not flinexts):
            eg.programCounter = None
        return flinexts


    def Configure(
        self,
        fl = "{eg.event.payload}",
        exts = "",
        kind = 0,
        stop = True
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        lbl1 = wx.StaticText(panel, -1, self.plugin.text.file)
        lbl2 = wx.StaticText(panel, -1, self.plugin.text.ext)
        lbl3 = wx.StaticText(panel, -1, text.open)
        ctrl1 = wx.TextCtrl(panel, -1, fl)
        ctrl1.SetToolTipString(text.tooltip)
        ctrl2 = wx.TextCtrl(panel, -1, exts)
        ctrl2.SetToolTipString(text.tooltip)
        kindCtrl = panel.Choice(kind, choices = self.plugin.text.choices)
        ifSizer = wx.FlexGridSizer(2, 2, 12, 10)
        ifSizer.Add(lbl3, 0, wx.ALIGN_CENTER_VERTICAL)
        ifSizer.Add(kindCtrl,0)
        ifSizer.Add((-1,-1))
        stopCtrl = panel.CheckBox(stop, text.stop)
        ifSizer.Add(stopCtrl)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(lbl1)
        mainSizer.Add(ctrl1, 0, wx.EXPAND)
        mainSizer.Add(lbl2, 0, wx.TOP, 12)
        mainSizer.Add(ctrl2, 0, wx.EXPAND)
        mainSizer.Add(ifSizer, 0, wx.TOP, 14)
        panel.sizer.Add(mainSizer, 1, wx.ALL|wx.EXPAND, 10)
        
        while panel.Affirmed():
            panel.SetResult(
                ctrl1.GetValue(),
                ctrl2.GetValue(),
                kindCtrl.GetValue(),
                stopCtrl.GetValue()
            )
#===============================================================================

class EnableDisablePopups(eg.ActionBase):
    class text:
        rbLabel = "Persistence of change"
        choices = (
            "Make the change only temporarily", 
            "Make the change persistent (and automatically save the document)"
        )
        labels = ("temporarily", "persistent")
        modes = ("On", "Off", "No change", "Toggle")

    def __call__(
        self, 
        pic = 2,
        mirr = 2,
        save = 1
    ):
        self.plugin.EnableDisablePopups(pic, mirr, save)


    def GetLabel(self, pic, mirr, save):
        return "%s: %i, %i (%s)" % (self.name,pic,mirr,self.text.labels[save])


    def Configure(
        self, 
        pic = 2,
        mirr = 2,
        save = 1
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        picCtrl = wx.RadioBox(
            panel, 
            -1, 
            self.plugin.text.autoOpen,
            choices = text.modes,
            style = wx.RA_SPECIFY_COLS
        )
        picCtrl.SetSelection(pic)
        mirrCtrl = wx.RadioBox(
            panel, 
            -1, 
            self.plugin.text.enabMirr,
            choices = text.modes,
            style = wx.RA_SPECIFY_COLS
        )
        mirrCtrl.SetSelection(mirr)


        saveCtrl = wx.RadioBox(
            panel, 
            -1, 
            text.rbLabel,
            choices = text.choices,
            style = wx.RA_SPECIFY_ROWS
        )
        saveCtrl.SetSelection(save)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(picCtrl, 0, wx.EXPAND)
        mainSizer.Add(mirrCtrl, 0, wx.TOP|wx.EXPAND,10)
        mainSizer.Add(saveCtrl, 0, wx.TOP|wx.EXPAND, 20)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                picCtrl.GetSelection(),
                mirrCtrl.GetSelection(),
                saveCtrl.GetSelection()
            )
#===============================================================================

class GetPopups(eg.ActionBase):

    def __call__(self):
        return (bool(self.plugin.autoOpen), bool(self.plugin.enabMirr))
#===============================================================================

ACTIONS = (
    (
        Push,
        "Push",
        "Push",
        "Pushes to one (or more) of the device (or friend).",
        False
    ),
    (
        Push,
        "PushToGroup",
        "Push to group",
        "Pushes to recipient group.",
        "Gr"
    ),
    (
        Push,
        "PushToEverything",
        "Push to everything",
        "Pushes to all of your devices.",
        "Everything"
    ),
    (
        Push,
        "PushReply",
        "Push reply",
        "Pushes a reply to the device from which the original push was sent.",
        "Reply"
    ),
    (
        Push,
        "PushSingle",
        "Push to a single",
        "Pushes to just one recipient (specified by iden, email, nickname or channel tag).",
        "Single"
    ),
    (
        PushScreenshot,
        "PushScreenshot",
        "Grab and push image",
        "Pushes screenshot (or clipboard content) to one (or more) of the device (or friend).",
        False
    ),
    (
        PushScreenshot,
        "PushScreenshotToEverything",
        "Grab and push image to everything",
        "Pushes screenshot (or clipboard content) to all of your devices.",
        True
    ),
    (
        DeletePush,
        "DeletePush",
        "Delete push",
        "Deletes push.",
        None
    ),
    (
        OpenFile,
        'OpenFile',
        "Open file",
        "Opens (downloaded) file in the associated application.",
        None
    ),
    (
        JumpIf,
        'JumpIf',
        "Jump according to file extension",
        "Jumps if the file is/is not one of the listed extension.",
        None
    ),
    (
        SendSMS,
        'SendSMS',
        "Send SMS",
        "Sends SMS.",
        None
    ),
    (
        SendSMS2list,
        'SendSMS2list',
        "Send bulk SMS to list from file",
        "Sends bulk SMS to list, imported from specified file.",
        None
    ),
    (
        SendSMSmulti,
        'SendSMSmulti',
        "Send SMS to multiple recipients",
        "Sends SMS to multiple recipients.",
        None
    ),
    (
        SendSMSgroup,
        'SendSMSgroup',
        "Send SMS to recipient group",
        "Sends SMS to recipient group.",
        None
    ),
    (
        SendReply,
        'SendReply',
        "Send reply to mirror",
        "Sends a reply to application, whose notification was mirrored.",
        None
    ),
    (
        Dismiss,
        'Dismiss',
        "Dismiss the notification or push",
        "Dismisses the notification or push.",
        None
    ),
    (
        EnableDisablePopups,
        'EnableDisablePopups',
        "Set popups",
        "Enables, disables or toggles popups.",
        None
    ),
    (
        GetPopups,
        'GetPopups',
        "Get states of popups",
        "Gets states of popups (enabled or disabled).",
        None
    )
)
#===============================================================================
