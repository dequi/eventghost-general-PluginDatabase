# -*- coding: utf-8 -*-
version = "0.0.13"

# plugins/PushBullet/__init__.py
#
# Copyright (C) 2014  Pako <lubos.ruckl@gmail.com>
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
# ##############################################################################
# Acknowledgement
#
# This plugin is using Requests, the excellent Apache2 Licensed HTTP library,
# written in Python, for human beings, http://www.python-requests.org/en/latest/
# 
# Copyright 2013 Kenneth Reitz
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ##############################################################################
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.13a by Pako 2014-05-22 11:55 GMT+1
#     - test version
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
    canMultiLoad = False,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACjUlEQVRYw92Xz08TQRTH"
        "P9PfLeVXgVpKoAKGRjQY9AAhRkJMjNGoF/5CD5w4cDXxphxIMMaEy0ZUQGMoVlr6c3dn"
        "d8YDBi39RUxkjXPa2bx983mzb977jlhbW9N4OAIA2WzWk8UNw8CHx8NzgMDvE9O1cUVj"
        "Sggg5gufzZVW1LXs6FQAYRHEL3wXByg4VdaOX/PFOW4wSATiPO27QzaSxlKS9eIWO+bn"
        "zk6Fn+FAL5nQMLciGSbDye4AJ6rGW2uPmrIbDPZlnplQipnwKN+dCptVg6KqdY3sg51j"
        "q7bLVnCXB71zLMev42uxI41v2hxIU8k//sf7Ms/zwivWi1tYLfxcShJaWrJxss3GyTZK"
        "K49OgYAX5XdsVg3vjqGpJS8rOxyYee/qwHvrkDf1j94Woj0nf5YLngB8so44ckreARTd"
        "Kod20TsAqV1KP4uZZ81Ie9oNXY3fFd4BhOswRM/lA2itcUomg1aYZHTgcgGU5SBzFeTX"
        "EpOhEYbCfecEidJtu6FQZyGgXXWqOLommQYFynZQZQu3bKJMB5/wca1/rFkPaMtB5spI"
        "0agHtKPQKRuGQLsK+a2C1PWOEFppcDXacVG2i5YuQgiEECyOzrKUutlCkgmBUzKRst7s"
        "Mflra1TVRtar3ZufEE3PY/ERHo4vMBCKt9aE5z9sJ1KabC4w4qEojzOLzCWm2ovSv5T6"
        "ZPpHeZJZ4v7Y7faaUAiBr1VkQhMPRgHwCx/RQIQC5c4lTpz66wlEmBue5tHEIjcGr3YW"
        "peOxEVanltmv5BoMUrEEC1dmEUKQiiZYnbqHUTjAVk5bhmgwwkQ8yXRvmlQscRZARwC/"
        "38+zybtdd3QlPc9Kev7/uRn9G1czwzA8A/gBRJz9BTwIz5wAAAAASUVORK5CYII="
    ),
    description = ur'''<rst>
Sends/receives notifications (and addresses, lists, links, pictures and files) 
to/from your Android device or browser (Chrome, Firefox) via PushBullet_.

Google account and PushBullet account (free) are required to use PushBullet_.

Plugin is based on libraries Tornado_ and pushbullet.py_ .

.. _PushBullet:    https://www.pushbullet.com/
.. _Tornado:       http://www.tornadoweb.org/en/stable/
.. _pushbullet.py: https://github.com/Azelphur/pyPushBullet
''',
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5709",
)

import wx.grid as gridlib
from time import strftime, time as ttime
from urllib2 import urlopen, URLError
from threading import Thread
from base64 import b64encode, b64decode
from PIL import Image
from StringIO import StringIO
from os import startfile
from os.path import join,abspath,dirname,isdir,isfile,basename,splitext
from eg.WinApi.Dynamic import BringWindowToTop
from copy import deepcopy as cpy
from datetime import datetime as dt
fldr = dirname(__file__.decode('mbcs'))
ICON_DIR = join(abspath(fldr), "icons")
lib_dir  = join(abspath(fldr), "lib")
from sys import path as syspath
syspath.append(lib_dir)
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from requests import request
from json import dumps
from mimetypes import guess_type as mimetype

SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ACV = wx.ALIGN_CENTER_VERTICAL
#===============================================================================

BODY = {
    'type': 'windows',
    'manufacturer': 'EventGhost',
    'model': 'plugin by Pako',
    'app_version': 100,
    #'fingerprint': '{"cpu": "Python", "computer_name": "EventGhost"}'
}
API = 'https://api.pushbullet.com/v2/'
DEFAULT_WAIT = 35.0
false = False
true = True
null = None
#===============================================================================

def pilToWxImage(pil):
    img = wx.EmptyImage(pil.size[0], pil.size[1])
    img.SetData( pil.convert( "RGB").tostring())
    if pil.mode in ('RGBA', 'LA') or \
        (pil.mode == 'P' and 'transparency' in pil.info):
            img.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    return img.ConvertToBitmap()


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
    return pilToWxImage(pilImg)


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
    pil.save(io_file, format = 'PNG')
    io_file.seek(0)
    data = io_file.read()
    return b64encode(data)


def connectivity():
    try:
        response = urlopen('http://www.google.com', timeout=1)
        return True
    except URLError as err:
        pass
    return False
#===============================================================================

class WebSocketClient(object):
    ws_cc = None

    def __init__(self, url, plugin):
        self.url = url
        self.plugin = plugin


    def start(self):
        self.io_loop = IOLoop.instance()
        wsc = websocket_connect(self.url, self.io_loop)
        wsc.add_done_callback(self.ws_conn_cb)
        self.io_loop.start()


    def ws_conn_cb(self, ws_cc):
        try:
            self.ws_cc = ws_cc.result()
        except:
            self.close()
            self.start()
        else:
            self.plugin.on_open()
            self.ws_cc.on_message = self.plugin.on_message


    def close(self):
        if hasattr(self.ws_cc, "protocol") and self.ws_cc.protocol is not None:
            self.ws_cc.protocol.close()
            self.ws_cc.protocol = None
        self.ws_cc = None
        if hasattr(self, 'io_loop'):
            self.io_loop.stop()
        self.plugin.Log(self.plugin.text.wsClosed, 2)
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
        return ["%s - %s" % (pl.GetDevice(i[0]),i[2]) for i in self.disabled]


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

class ListGrid(gridlib.Grid):

    def __init__(self, parent, id, items, width):
        gridlib.Grid.__init__(
            self,
            parent,
            id,
            size=(width-5, -1),
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
        self.SetColAttr(0,attr)
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
        if not self.IsVisible(row,0):
            self.MakeCellVisible(row,0)
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
        wav
    ):
        dev = dev.rstrip()
        title = title.rstrip()
        body = body.rstrip()
        if icon:
            pil = Image.open(StringIO(b64decode(icon)))
        else:
            return
        W, H = pil.size
        if W > 96 or H > 96:
            factor = max(W, H)/96.0
            x = int(min(W, H) / factor) 
            size = (96, x) if W >= H else (x, 96)     
            pil = pil.resize(size, Image.ANTIALIAS)
            image = Image.new('RGBA', (96,96))
            image.paste(pil, ((96-size[0])/2, (96-size[1])/2))
            pil = image
            W, H = pil.size
        elif W < 72 and H < 72:
            W, H = (72, 72)
        wx.Frame.__init__(
            self,
            parent,
            -1,
            '',
            size = (400, H+8),
            style = wx.STAY_ON_TOP | wx.SIMPLE_BORDER
        )
        self.delta = (0,0)
        img = pilToWxImage(pil)
        bmp = wx.StaticBitmap(
            self, -1,
            img,
            (3, 3),
            (img.GetWidth(),
            img.GetHeight())
        )
        app = app if not plugin.hideBtn else None
        s = plugin.text.disable % app[2] if app else ""
        label0 = wx.StaticText(self, -1, dev, (W+10,2)) if dev else FakeLbl()
        label1 = wx.StaticText(self, -1, title) if title else FakeLbl()
        label2 = wx.StaticText(self, -1, body) if body else FakeLbl()
        label3 = wx.StaticText(self, -1, s) if app else FakeLbl()
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
        w = max(w0 + w4, w1, w2, w3 + 22)
        label1.SetPosition((W+10, 19-e0+h0))
        label2.SetPosition((W+10, 38-e0-e1+h0+h1))
        x0, y0 = label0.GetPosition()
        x1, y1 = label1.GetPosition()
        x2, y2 = label2.GetPosition()

        if app:
            def onClick(event):
                wx.CallAfter(plugin.DisableMirroring, *app)
                self.OnCloseWindow(event)
                event.Skip()
            h = max(y0+h0,y1+h1,y2+h2)
            png = wx.Bitmap(
                join(eg.Icons.IMAGES_PATH, "disabled.png"),
                wx.BITMAP_TYPE_PNG
            )
            gr = png.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()
            b = wx.BitmapButton(
                self,
                -1,
                gr,
                pos = (W+10, h+2),
                size = (16, 16),
                style = wx.BORDER_NONE
            )
            label3.SetPosition((W+32, h+4))
            bc = self.GetBackgroundColour()
            b.SetBackgroundColour(bc)
            b.SetBitmapHover(png)
            b.SetBitmapSelected(png)
            b.Bind(wx.EVT_BUTTON, onClick)        
            self.SetSize(((W+18+w, max(H+8, h+22))))
        else:
            self.SetSize((W+18+w, max(H+8,y0+h0,y1+h1,y2+h2)))
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

        self.SetPosition((10,10))
        if wav:
            self.sound = wx.Sound(wav)
            if self.sound.IsOk():
                self.sound.Play(wx.SOUND_ASYNC)
        else:
            self.sound = None
        self.Show(True)
        BringWindowToTop(self.GetHandle())


    def OnCloseWindow(self, event):
        self.timer.Stop()
        del self.timer
        if self.sound:
            self.sound.Stop()
        self.Destroy()


    def OnRightClick(self, evt):
        self.Show(False)
        self.Close()


    def OnLeftDown(self, evt):
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(win, (wx._controls.StaticText,wx._controls.StaticBitmap)):
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
    file = "File:"
    ext = "List of file extensions:"
    notLbl = " not"
    ifExt = "if extension"
    inLbl = "in"
    autoOpen = "Automatically open downloaded pictures"
    disMirr = "Disable popping up of mirrored notification"
    nLabel = 'Nickname of this PC:'
    apiLabel = 'API key:'
    prefix = 'Event prefix:'
    mode = 'The title of the push to use as:'
    modes = ("event suffix", "payload[0]")
    folder =  'Directory for file download:'
    timeout = 'Mirror hide timeout [s]:'
    pTimeout = 'Picture hide timeout [s]:'
    timeout2 = "(0 = not to hide)"
    err = 'Failed to open file "%s"'
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    hideBtn = "Hide disable button on mirrored notifications"
    title3 = "Re-enable a disabled application"
    enabLbl = "Disabled application:"
    cancel = "Cancel"
    ok = "OK"
    delete = "Re-enable"
    reenab = "Re-enable mirroring for an app ..."
    tooltip = "Right mouse button closes this window"
    disable = 'Disable mirroring of "%s"'
    wavs = "Folder of alerting sounds:"
    reconnect = "Haven't seen a nop lately, reconnecting"
    waiting = "Haven't seen a nop lately, waiting for connectivity"
    waiting2 = "PushBullet: No connectivity, waiting ..."
    uplFld = u'Failed to upload the file "%s"'
    uplSucc = u'The file "%s" uploaded successfully'
    addLstnr = 'Adding push messaging listener'
    wsMssg = "WebSocket message: %s"
    rspnsr = "Response = %s"
    fTriggMute = 'Failed to trigger mute of app %s'
    triggMute = "Triggered mute of app %s"
    fTriggUnmute = 'Failed to trigger unmute of app %s'
    triggUnmute = "Triggered unmute of app %s"
    gettPshs = "Getting pushes, modified_after = %.7f"
    fLoadPshs = "Failed to load pushes"
    mdfdUpd = "modified_after updated: %.7f"
    wsOpened = "WebSocket opened"
    wsClosed = "WebSocket closed"
    idenSaved = 'New iden "%s" automatically saved'
    dsbldUpdated = 'List of disabled app automatically updated'
    emlObtained = "Email address obtained"
    accReqFailed = "Account request failed"
    noApi = "No API key"
    noNick = "No nickname"
    devRcvd = "Devices received: %s"
    devReqFailed = "Device request failed"
    noDev = "No devices"
    pcMssng = "This PC is missing in the device list. "\
        "Request for creating device sent."
    devCrtd = "Device created: %s"
    crDevFld = "Creating device failed"
    pushDelted = "Push deleted"
    pushDelFld = 'Push deleting failed: "%s"'
    frndsRcvd = "Friends received: %s"
    trgtsDrvd = "Targets derived: %s"
    pushRslt = "Push results: %s"
    dwnldFailed = 'Download of "%s" failed (code %i)'
    nicknameUsed = 'PushBullet: Chosen nickname "%s" is already used for '\
        'other device, than the "EventGhost"  !!!'
    wavFldr = "Select the folder that stores sounds ..."
    toolWav = '''Here you can select the folder, where you saved the alerting
sounds. If the field is left blank, this feature will not be used. 
Sounds must be in "wav" format and must have the same name, 
as the corresponding push type (for example, "address.wav", for "address" push). 
If some sound is missing, this feature will not be used (for the corresponding 
push type).'''
    kinds = (
        "Note",
        "Link",
        "File",
        "List",
        "Address",
        "Mirror",
    )    
    choices = [
        "the file extension is one of the listed extension",
        "the file extension is not one of the listed extension",
    ]
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
    targets = []
    disabled = []
    watchdog = None
    debug = 1
    email = None
    updtDvcs = None
    connFlag = False

    text = Text


    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def OnComputerSuspend(self, dummy):
        self.__stop__()


    def OnComputerResume(self, dummy):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        self.__start__(*args)


    def __start__(
        self,
        nickname = "My PC",
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
        disMirr = False
    ):
        if isinstance(api_key, eg.Password):
            api_key = api_key.Get()    
        self.api_key = api_key
        self.info.eventPrefix = prefix
        self.nickname = nickname
        self.iden = iden
        self.prefix = prefix
        self.mode = mode
        self.fldr = fldr if isdir(fldr) else eg.folderPath.TemporaryFiles
        self.debug = debug
        self.hide = hide
        self.pHide = pHide
        self.disabled = disabled
        self.hideBtn = hideBtn
        self.wavs = wavs
        self.autoOpen = autoOpen
        self.disMirr = disMirr
        self.connFlag = False
        self.updtDvcs = eg.scheduler.AddTask(2.0, self.updateDevices)


    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass


    def stopUpdtDvcs(self):
        if self.updtDvcs:
            try:
                eg.scheduler.CancelTask(self.updtDvcs)
            except:
                pass
    

    def __stop__(self):
        self.stopWatchdog()
        self.stopUpdtDvcs()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None
        self.watchdog = None
        self.devices = []
        self.friends = []
        self.targets = []
        self.email = None

    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.name, message)


    def watcher(self):
        if ttime() - self.lastMessage > self.msgWait and self.api_key:
            if connectivity():
                self.connFlag = True
                self.Log(self.text.reconnect, 2)
                self.msgWait = min(600000, self.msgWait * 2)
                self.refreshWebSocket()
            elif self.connFlag:
                self.Log(self.text.waiting, 1)
                self.connFlag = False
        elif not self.connFlag:
            if connectivity():
                self.connFlag = True
        if self.info.isStarted:
            self.stopWatchdog()
            self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)


    def startWsc(self, wsc):
        wsc.start()


    def on_open(self):
        if not self.modified_after:
            self.modified_after = ttime()
        self.requestPushes()
        self.Log(self.text.wsOpened, 2)


    def establishSubscriber(self): 
        if self.wsC: 
            return
        url = 'wss://stream.pushbullet.com/websocket/' + self.api_key
        self.wsC = WebSocketClient(url, self)
        self.ct = Thread(
            target = self.startWsc,
            args = (self.wsC, )
        )
        self.ct.start()
        self.lastMessage = ttime()      
        if self.info.isStarted:
            self.stopWatchdog()
            self.watchdog = eg.scheduler.AddTask(0.01, self.watcher)
        self.Log(self.text.addLstnr, 4)


    def refreshWebSocket(self):
        self.msgWait = DEFAULT_WAIT
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.establishSubscriber()


    def on_message(self, m):
        try:
            if m is None:
                return
            self.Log(self.text.wsMssg % m, 5)
            self.lastMessage = ttime()
            self.msgWait = DEFAULT_WAIT
            m = eval(m)
        except:
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
            self.processPush(m['push'])
        elif m['type'] == 'tickle' and m['subtype'] == 'push':
            self.requestPushes()
        elif m['type'] == 'tickle' and m['subtype'] == 'device':
            self.devices = []
            if self.info.isStarted:
                self.stopUpdtDvcs()
                self.updtDvcs = eg.scheduler.AddTask(0.01, self.updateDevices)
        elif m['type'] == 'tickle' and m['subtype'] == 'contact':
            self.friends = []
            if self.info.isStarted:
                self.stopUpdtDvcs()
                self.updtDvcs = eg.scheduler.AddTask(0.01, self.updateDevices)


    def EventTrigger(self, part1, part2, part3, part4, part5, dev, ts):
        if self.mode:
            self.TriggerEvent(
                part1,
                payload = [part2, part3, part4, part5, dev, ts]
            )
        else:
            self.TriggerEvent(
                "%s.%s" % (part1, part2.replace(" ","")),
                payload = [part3, part4, part5, dev, ts]
            )


    def urlretrieve(self, remote, flpth):
        u = urlopen(remote)
        t = u.headers.getheader("Content-Type")
        code = u.getcode()
        if code == 200:
            fp = open(flpth, 'wb')
            fp.write(u.read())
            fp.close()
            self.TriggerEvent("FileDownloaded", payload = flpth)
            if self.autoOpen and t.split(r"/")[0] == u'image':
                eg.plugins.System.DisplayImage(
                    flpth, 3, 1, True, False, 0, True, 4,
                    self.pHide,
                    0, 5, 5, 640, 480, (51, 51, 51), False, True, True, u''
                )
        else:
            self.Log(self.text.dwnldFailed % (flpth, code), 1)


    def fromFriend(self, push):
        if push['receiver_email'] == self.email and \
            push['sender_email'] != self.email:
                return True


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



    def processPush(self, push):
        if not push['active'] or push['dismissed']:
            return
        if push['receiver_email'] != self.email:
            return
        if self.fromFriend(push):
            friend = True
            dev = self.GetDevice(push['sender_email'])
        else:                
            dev = self.GetDevice(push['source_device_iden']) \
                if 'source_device_iden' in push else ""
            trgt = push['target_device_iden'] \
                if 'target_device_iden' in push else None
            friend = False
        if not friend and not trgt in (self.iden, None):
            return
        ts = push['modified']
        if ts > self.modified_after:
            self.modified_after = ts
            self.Log(self.text.mdfdUpd % self.modified_after, 4)
        ts = str(dt.fromtimestamp(ts))[:19]
        wav = self.getSound(push['type'])
        if wav and push['type'] != 'mirror':
            sound = wx.Sound(wav)
            if sound.IsOk():
                sound.Play(wx.SOUND_ASYNC)                
        part1 = push['type'].capitalize()
        part2 = push['title'] if ('title' in push and push['title']) else part1
        part3 = None
        part4 = None
        part5 = push[u'iden']
        if push['type'] == u'link':
            part3 = push[u'url']
            part4 = push[u'body'] if ('body' in push and push['body']) else ""
        elif push['type'] == u'note':
            part3 = push[u'body']
        elif push['type'] == u'list':
            part3 = push[u'items']
        elif push['type'] == u'address':
            part2 = push[u'name']
            part3 = push[u'address']
        if push['type'] in (u'link', u'note', u'list', u'address'):
            self.EventTrigger(part1, part2, part3, part4, part5, dev, ts)
        elif push['type'] == u'file':
            image = push[u'file_type'].split(r"/")[0] == u'image'
            self.TriggerEvent(
                "Image" if image else "File",
                payload = [
                    push[u'file_name'],
                    push[u'file_type'],
                    push[u'file_url'],
                    push[u'body'] if ('body' in push and push['body']) else "",
                    dev,
                    ts
                ]
            )
            flpth = join(self.fldr, push[u'file_name'])
            self.urlretrieve(push[u'file_url'], flpth)
        elif push['type'] == u'mirror':
            ue = 'unicode-escape'
            if dev:
                self.TriggerEvent(
                    "Mirror.%s" % push['title'].decode(ue)\
                        if push['title'] else 'Mirror',
                    payload = [
                        push[u'body'].decode(ue),
                        dev,
                        push[u'icon']
                    ]
                )
                if not self.disMirr:
                    wx.CallAfter(
                        MirrorNote,
                        None,
                        self,
                        dev,
                        push['title'].decode(ue)\
                            if push['title'] else push[u'body'].decode(ue),
                        push[u'body'].decode(ue) if push['title'] else "",
                        push[u'icon'],
                        (push['source_device_iden'], push['package_name'],
                            push['application_name'].decode(ue))\
                            if push['package_name'] else None,
                        wav
                        )
        

    def DisableMirroring(self, iden, package, app):
        body = {
            'type': 'mute',
            'device_iden': iden,
            'package_name': package
        }
        res, flag = self.request("POST", API + 'pushes', data = body)
        self.Log(self.text.rspnsr % repr(res), 4)
        if not flag or not isinstance(res, dict) or res['type'] != 'mute': 
            self.Log(self.text.fTriggMute % app, 1)
            return
        self.Log(self.text.triggMute % app, 3)
        self.updateConfig(disabled = (iden, package, app))


    def EnableMirroring(self, iden, package, app):
        body = {
            'type': 'unmute',
            'device_iden': iden,
            'package_name': package
        }
        res, flag = self.request("POST", API + 'pushes', data = body)
        self.Log(self.text.rspnsr % repr(res), 4)
        if not flag or not isinstance(res, dict) or res['type'] != 'unmute': 
            self.Log(self.text.fTriggUnmute % app, 1)
            return
        self.Log(self.text.triggUnmute % app, 3)
        self.updateConfig(enabled = (iden, package, app))


    def EnableMirroringMany(self, lst):
        for item in lst:
            self.EnableMirroring(*item)


    def GetDevice(self, iden):
        tmp = [t[1] for t in self.targets]
        if iden in tmp:
            return [t[0] for t in self.targets][tmp.index(iden)]
        else:
            return iden


    def requestPushes(self):        
        self.Log(self.text.gettPshs % self.modified_after, 4)
        res, flag = self.request("GET", API + 'pushes?modified_after=%.7f' \
            % self.modified_after)
        self.Log(self.text.rspnsr % repr(res), 4)
        if not flag or not isinstance(res, dict) or not 'pushes' in res: 
            self.Log(self.text.fLoadPshs, 1)
            return
        pushes = res['pushes']
        for push in pushes:
            self.processPush(push)


    def uploadFile(self, filepath):
        def guess_type(filepath):
            return mimetype(filepath)[0] or 'application/octet-stream'
        baseName = basename(filepath)
        params = {"file_name": baseName, "file_type": guess_type(baseName)}
        resp, flag = self.request(
            "GET",
            API + "upload-request",
            params = params
        )
        if flag:
            fileobject = ''
            with open(filepath, "rb") as f:
                fileobject = f.read()            
            uplResp = request(
                "POST",
                resp["upload_url"],
                data = resp["data"],
                files = {"file": fileobject},
                headers = {"X-User-Agent":"EventGhost"}
            )
            if uplResp.ok:
                return (resp["file_name"], resp["file_type"], resp["file_url"])



    def request(self, method, url, **kwargs):

        kwargs['headers'] = {
            "X-User-Agent":"EventGhost",
            "Authorization":"Basic " + b64encode(self.api_key+":"),
            'Accept':'application/json',
            "Content-type":"application/json",
        }
        if 'data' in kwargs:
            kwargs['data'] = dumps(kwargs['data'])

        resp = request(method, url, **kwargs)
        if resp.ok:
            if method == "DELETE":
                return (resp, True)
            else:
                return (resp.json(), True)
        else:
            #resp.raise_for_status()
            return (resp.status_code, False)


    def updateConfig(self, iden = None, disabled = None, enabled = None):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        if iden:
            args[2] = iden
            self.Log(self.text.idenSaved % iden, 2)
        elif disabled and disabled not in args[9]:
            args[9].append(disabled)
            self.Log(self.text.dsbldUpdated, 2)
        elif enabled and enabled in args[9]:
            args[9].remove(enabled)
            self.Log(self.text.dsbldUpdated, 2)
        eg.actionThread.Func(trItem.SetArguments)(args)       
        eg.document.SetIsDirty()
        eg.document.Save()


    def getAccount(self):
        account, flag = self.request("GET", API + 'users/me')
        if flag and isinstance(account, dict) and "email" in account:
            self.email = account["email"]
            self.Log(self.text.emlObtained, 4)
        else:
            self.Log(self.text.accReqFailed, 1)


    def updateDevices(self):
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
        if not self.devices:
            devices, flag = self.request("GET", API + "devices")
            if flag and isinstance(devices, dict) and "devices" in devices:
                self.devices = devices["devices"]
                self.Log(self.text.devRcvd % repr(self.devices), 3)
            else:
                self.Log(self.text.devReqFailed, 1)
                if self.info.isStarted:
                    self.stopUpdtDvcs()
                    self.updtDvcs = eg.scheduler.AddTask(60, self.updateDevices)
                return
            if not self.devices:
                if self.info.isStarted:
                    self.stopUpdtDvcs()
                    self.updtDvcs = eg.scheduler.AddTask(60, self.updateDevices)
                self.Log(self.text.noDev, 2)
                return
            for dev in self.devices:
                if not dev['active']: # ignore deleted device
                    continue
                if not 'nickname' in dev or not dev['nickname']:
                    nick = dev['manufacturer'].capitalize() + ' ' + dev['model']
                    dev['nickname'] = nick
            nicknames = dict([(dev['nickname'], dev) for dev \
                in self.devices if dev['active']])
            if self.nickname in nicknames.iterkeys():
                dev = nicknames[self.nickname]
                if dev['manufacturer'] == u'EventGhost':
                    if self.iden != dev['iden']:
                        self.iden = dev['iden']
                        self.updateConfig(iden = self.iden)
                else:
                    eg.PrintNotice(self.text.nicknameUsed % self.nickname)
                    return
            else:
                BODY['nickname'] = self.nickname
                me, flag = self.request("POST", API + 'devices', data = BODY)
                self.Log(self.text.pcMssng, 2)
                if flag and isinstance(me, dict) and me:
                    self.Log(self.text.devCrtd % repr(me), 3)
                    self.iden = me['iden']
                    self.updateConfig(iden = self.iden)
                    return
                else:
                    self.Log(self.text.crDevFld, 1)
                    return
        if not self.friends:
            friends, flag = self.request("GET", API + "contacts")
            if flag and isinstance(friends, dict) and "contacts" in friends:
                self.friends = friends["contacts"]
                self.Log(self.text.frndsRcvd % repr(self.friends), 3)
        self.targets = []
        for dev in self.devices:
            if not dev['active']:
                continue
            droid = 'android' if 'android_version' in dev\
                and dev['android_version'] is not None else 'pc'
            self.targets.append((dev['nickname'], dev['iden'], droid))
        for fr in self.friends:
            if fr['status'] == 'not_user':
                continue
            name = fr['name'] if 'name' in fr and fr['name'] else fr['email']
            self.targets.append((name, fr['email'], 'user'))
        self.Log(self.text.trgtsDrvd % repr(self.targets), 3)
        if not self.email:
            self.getAccount()
        self.establishSubscriber()


    def push(self, kind, trgts, data, suff = None):
        if not self.wsC:
            eg.actionThread.Call(eg.PrintNotice, self.text.waiting2)
            return
        kinds = [i.lower() for i in self.text.kinds]
        payload = {'type' : kinds[kind]}
        results = []
        ok = True
        if kind == 2: #file
            payload['body'] = eg.ParseString(data[0]) if data[0] else None
            fl = eg.ParseString(data[1])
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
                else:
                    iden = 'device_iden'
                    tmp['type'] ='device'
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

        if kind in (0, 1, 3):
            payload['title'] = eg.ParseString(data[0])
        if kind == 0:
            payload['body'] = eg.ParseString(data[1])
        elif kind == 1:
            payload['url'] = eg.ParseString(data[1])
            payload['body'] = eg.ParseString(data[2]) if data[2] else None
        elif kind == 3:
            tmp = []
            for i in data[1]:
                tmp.append(eg.ParseString(i))
            payload['items'] = tmp
        elif kind == 4:
            payload['name'] = eg.ParseString(data[0])
            payload['address'] = eg.ParseString(data[1])
        elif kind == 5: #mirror
            payload['title']= eg.ParseString(data[0])
            payload['body'] = eg.ParseString(data[1])
            payload['icon'] = getIcon(self.text.err, eg.ParseString(data[2]))
            payload[u'application_name'] = eg.event.prefix if \
                eg.event else 'EventGhost'
            payload[u'notification_duration'] = -0x1

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
            else:
                iden = 'device_iden'
                tmp['type'] ='device'
                if 'email' in payload:
                    del payload['email']
            tmp[iden] = trgt[1]
            payload[iden] = trgt[1]
            #check, if trgt is valid ?
            res, flag = self.request("POST", API + "pushes", data = payload)  
            if ok:
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


    def Configure(
        self,
        nickname = "My PC",
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
        disMirr = False
    ):
        if not isinstance(apiKey, eg.Password):
            api_key = eg.Password(None)
            api_key.Set(apiKey)
        else:
            api_key = apiKey
                
        text = self.text
        panel = eg.ConfigPanel(self)
        if not fldr:
            fldr = eg.folderPath.TemporaryFiles
        nLabel = wx.StaticText(panel, -1, text.nLabel)
        nickCtrl = wx.TextCtrl(panel,-1,nickname)
        apiLabel = wx.StaticText(panel, -1, text.apiLabel)
        apiCtrl = wx.TextCtrl(panel, -1, api_key.Get(), style = wx.TE_PASSWORD)
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
        hideSizer = wx.BoxSizer(wx.HORIZONTAL)
        hideSizer.Add(hideCtrl, 0, wx.RIGHT, 5)
        hideSizer.Add(hideLabel2, 0, flag = ACV)
        autoOpenCtrl = panel.CheckBox(autoOpen, self.text.autoOpen)
        disMirrCtrl = panel.CheckBox(disMirr, self.text.disMirr)
        pHideLabel = wx.StaticText(panel, -1, text.pTimeout)
        pHideLabel2 = wx.StaticText(panel, -1, text.timeout2)
        pHideCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            pHide,
            min = 0,
            max = 999
        )
        pHideSizer = wx.BoxSizer(wx.HORIZONTAL)
        pHideSizer.Add(pHideCtrl, 0, wx.RIGHT, 5)
        pHideSizer.Add(pHideLabel2, 0, flag = ACV)        
        mainSizer = wx.GridBagSizer(10, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nLabel, (0,0), flag = ACV)
        mainSizer.Add(nickCtrl,(0,1),flag = wx.EXPAND)
        mainSizer.Add(apiLabel, (1,0), flag = ACV)
        mainSizer.Add(apiCtrl,(1,1),flag = wx.EXPAND)
        mainSizer.Add(prefixLabel, (2,0), flag = ACV)
        mainSizer.Add(prefixCtrl,(2,1),flag = wx.EXPAND)
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        mainSizer.Add(modeLabel, (3,0), flag = ACV)
        mainSizer.Add(modeSizer,(3,1),flag = wx.EXPAND)
        mainSizer.Add(fldrLabel, (4,0), flag = ACV)
        mainSizer.Add(fldrCtrl,(4,1),flag = wx.EXPAND)
        debugSizer = wx.BoxSizer(wx.HORIZONTAL)
        debugSizer.Add(debugCtrl, 0, wx.RIGHT, 5)
        debugSizer.Add( debugLabel2, 0, flag = ACV)        
        mainSizer.Add(debugLabel, (5,0), flag = ACV)
        mainSizer.Add(debugSizer,(5,1))
        mainSizer.Add(autoOpenCtrl,(6,0),(1,2))

        mainSizer.Add(pHideLabel, (7,0), flag = ACV)
        mainSizer.Add(pHideSizer,(7,1))
        mainSizer.Add(disMirrCtrl,(8,0),(1,2))
        mainSizer.Add(hideLabel, (9,0), flag = ACV)
        mainSizer.Add(hideSizer,(9,1))
        mainSizer.Add(wavLabel, (10,0), flag = ACV)
        mainSizer.Add(wavCtrl,(10,1),flag = wx.EXPAND)
        mirrorSizer = wx.BoxSizer(wx.HORIZONTAL)
        mirrorSizer.Add(hideBtnCtrl,0, flag = ACV)
        mirrorSizer.Add((-1,1),1,wx.EXPAND)
        mirrorSizer.Add(button, 0, wx.RIGHT)
        mainSizer.Add(mirrorSizer,(11,0), (1,2),flag = wx.EXPAND)
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
        disableMirrPopUp(not disMirr)


        def onDisMirr(evt):
            disableMirrPopUp(not evt.Checked())
            evt.Skip()
        disMirrCtrl.Bind(wx.EVT_CHECKBOX, onDisMirr)

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


        while panel.Affirmed():
            oldKey = api_key.Get()
            newKey = apiCtrl.GetValue()
            if oldKey != newKey:
                api_key.Set(newKey)
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
                disMirrCtrl.GetValue()
            )
#===============================================================================

class Push(eg.ActionBase):

    class text:
        limit = "Files must be smaller than 25 MB"
        lbls1 = (
            "Title:",
            "Link title:",
            "Message:",
            "List title:",
            "Address name:",
            "Title:"
        )
        lbls2 = (
            "Message:",
            "Link (something like http://eventghost.net/forum):",
            "File:",
            "Items:",
            "Street address, place or name of location:",
            "Message:"
        )
        lbl3 = "Icon (path to image or base64 string):"
        toolTipFile = '''Type filename or click browse to choose file
Files must be smaller than 25 MB'''
        toolTipIcon = '''Type filename or click browse to choose image
or enter base64 string'''
        browseFile = 'Choose a file'
        browseIcon = 'Choose a image file'
        tsLabel = "Push targets:"
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

    def __call__(self, kind = 0, trgts = [], data = ["",""], suff=""):
        if self.value:
            trgts=[['Everything',None,'everything',True]]
        pushThread = Thread(
            target = self.plugin.push,
            args = (kind, trgts, data, suff)
        )
        pushThread.start()


    def GetLabel(self, kind, trgts, data, suff):
        k = self.plugin.text.kinds[kind]
        if self.value:
            ts = self.text.ever
        else:
            ts = [i[0] for i in trgts if i[3]]
            ts = repr(ts) if len(ts) > 1 else '"%s"' % ts[0]
        return "%s %s to %s" % (self.name, k.lower(), ts)
         

    def Configure(self, kind = 0, trgts = [], data = ["",""], suff = ""):
        text = self.text
        self.kind = kind
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
            tsLabel = wx.StaticText(panel, -1, text.tsLabel)
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
                    if self.kind==5 and self.plugin.targets[self.ix][2] != 'pc':
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
            if not self.value and self.kind == 5:
                removeTargets()
            event.Skip()

        buttons = (
            wx.NewId(),wx.NewId(),wx.NewId(),
            wx.NewId(),wx.NewId(),wx.NewId()
        )
        buttonSizer = wx.GridBagSizer(0, 0)
        bmps = []
        for i, icon in enumerate(self.plugin.text.kinds):
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
            if i < 5:
                buttonSizer.Add((18,-1),(0,2*i+1))
            buttonSizer.Add(wx.StaticText(panel,-1,icon),(1,2*i),(1,2))
            b.Bind(wx.EVT_BUTTON, onClick, id=id)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        if not self.value:
            leftSizer = wx.BoxSizer(wx.VERTICAL)
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

        def setDynCtrls(data = None):
            rightSizer = self.rightSizer
            kind = self.kind
            for id in self.ids:
                detachControl(id)
            style = wx.TOP|wx.EXPAND
            flag = 0 if kind in (1, 2) else 1
            cntrl1 = wx.TextCtrl(
                panel,
                self.ids[0],
                data[0] if data and (kind != 2 or len(data) == 2) else ""
            )        # for backward compatibility ^^^^^^^^^^^^^^
            lbl1 = wx.StaticText(panel,self.ids[2],self.text.lbls1[kind]) 
            if kind not in (2, 3):
                cntrl2=wx.TextCtrl(
                    panel,
                    self.ids[1],
                    data[1] if data is not None else "",
                    style = wx.TE_MULTILINE if kind != 1 else 0
                )
            elif kind == 2:
                if data and len(data)==1: # for backward compatibility
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
            elif kind == 3:
                cntrl2=ListGrid(
                    panel,
                    self.ids[1],
                    data[1] if data is not None else ("", "", ""),
                    rightSizer.GetSize()[0]
                )
                if data is not None:
                    cntrl2.SetValue(data[1])
            lbl2 = wx.StaticText(panel,self.ids[3],self.text.lbls2[kind])
            rightSizer.Add(lbl1,0,wx.TOP,10)
            rightSizer.Add(cntrl1,0,style,1)
            rightSizer.Add(lbl2,0,wx.TOP,10)
            rightSizer.Add(cntrl2,flag,style,1)                

            if kind in (1, 5):
                if kind == 1:
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
        suffSizer.Add(suffCtrl)
        setDynCtrls(data)
        rSizer = wx.BoxSizer(wx.VERTICAL)
        rSizer.Add(wx.StaticText(panel,-1,text.cont))
        rSizer.Add(sSizer,1,wx.EXPAND|wx.TOP,-5)
        rSizer.Add(suffSizer,0,wx.TOP,5)

        mainSizer.Add(rSizer,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,5)



        if not self.plugin.wsC:
            panel.Enable(False)

        while panel.Affirmed():
            data = []
            data.append(wx.FindWindowById(self.ids[0]).GetValue())
            data.append(wx.FindWindowById(self.ids[1]).GetValue())
            if self.kind in (1, 5):
                data.append(wx.FindWindowById(self.ids[5]).GetValue())
            panel.SetResult(
                self.kind,
                self.ts,
                data,
                suffCtrl.GetValue()
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
        mainSizer.Add(lbl,0,ACV)
        mainSizer.Add(pushCtrl,1,wx.EXPAND|wx.LEFT, 8)
        panel.sizer.Add(mainSizer,0,wx.EXPAND|wx.ALL, 10)
        
        while panel.Affirmed():
            panel.SetResult(
                pushCtrl.GetValue(),
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


    def __call__(self, link, kind=0, fl="", exts = ""):
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


    def Configure(self, link=None, kind=0, fl="", exts = ""):
        text = self.text
        panel = eg.ConfigPanel()
        lbl1 = wx.StaticText(panel, -1, self.plugin.text.file)
        lbl2 = wx.StaticText(panel, -1, self.plugin.text.ext)
        ctrl1 = wx.TextCtrl(panel, -1, fl)
        ctrl1.SetToolTipString(text.tooltip)
        ctrl2 = wx.TextCtrl(panel, -1, exts)
        ctrl2.SetToolTipString(text.tooltip)
        kindCtrl = panel.Choice(kind, choices=self.plugin.text.choices)
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
        "PushToEverything",
        "Push to everything",
        "Pushes to all of your devices.",
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
)
#===============================================================================
