# -*- coding: utf-8 -*-
# $LastChangedDate: 2009-05-22 19:37:21 +0200 (Fr, 22 Mai 2009) $
# $LastChangedRevision: 1001 $
# $LastChangedBy: Bitmonster $

"""
    Webserver
    ~~~~~~~~~
    
    This plugin implements a small webserver, that can be used to generate
    events through HTML-pages.
"""

import eg

eg.RegisterPlugin(
    name = "Webserver",
    author = "Bitmonster",
    version = "1.1." + "$LastChangedRevision: 1001 $".split()[1],
    description = (
        "Implements a small webserver, that you can use to generate events "
        "through HTML-pages."
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH1gEECzsZ7j1DbAAAAu1JREFUOMul"
        "kztsW3UUxn////Xb1684NXbzsOskA6UiklWCCOmCCiKwsCDBjBShThVCDICYgCIxMHgC"
        "BhYYkbJAhaIoIBCKKvUBhArHGLexaar4/bj2ffjey0CboagTZ/l0jo5+Ovp0PvifJR4c"
        "5F64NOMX7kcoyrppOwmBwOcRHTGZXBk7YuPW5bfrDwWcWv/gdSFlcWEp55mZyxCJhBGA"
        "ruvcqd+lXKpOsMxLpW/ffe8/gNz6h6/FYuFP184VlNO5E8yfTJEKu2QSQbojk51rt7nx"
        "Z4Pr124Sks7HP3918S0ACfDJlz+ueBRZfPaZJ5R3Xinw3HKKx7MRCgtTzCaDRAMKwjJo"
        "N1qcWX6Uu93xm/nn358/Bmzt7r+RX8wG4kGFdm+MGo3h93lojaCnO5RrbZpjQXYmSSrq"
        "Y2EpJ7zC/QLAA1Ctt5568lxeDHULTYaYQtLUwCOh3dX47Osr9EcG0qOgjUzyi1lq1drK"
        "MWBs2ul4LMLiXJxkSHLQNvB5PWiWzfZuid5wjGnZGMMxXr+faFTFmNihY4DANXyK9L28"
        "NkejM6J5NET4VSa2jaqGkIrEtWxsx0EfaAC47r/my3vN3mg4sAcjk0wyTLvR4vL31zls"
        "9FG8Pp5eXWZm9hEmtoMQgn5/iILbPr4AIbaq1b+Xd/ZmQ/WDO5QPWmSmIzQ6A8aWjTY2"
        "SSdVMoVTBFSVq7/XXOHY3wEoAPGl8+VWq3fBDai+W0ea2K8c0hxa5OdPoOAQUCRnl6bZ"
        "eKnASLf49ZdSM51OvvrH7mZXAeiWtweR3FrvqNF7Mb8wh5QSfzjEYVujdtRnYtuczk4x"
        "HQ3gdQwrEZxs39j6fKdSqbSU+5/Y++uHsieateuHg9VYPCpTqSSp6QSJmIqhm+z9VnJu"
        "V6o9Jv2beq++WywWf3IcZ/hgmNKh9JnVk4+d31CCyRXDljEAx9T6zrC+dzYrribCcn9z"
        "c/ObTqdzALjiIQmNArF76gcMYAB0gT7g3l/+ByWIP9hU8ktfAAAAAElFTkSuQmCC"
    ),
)

import wx
import os
import posixpath
import httplib
import base64
import time
from threading import Thread, Event
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from urllib import unquote, unquote_plus

import jinja2


class FileLoader(jinja2.BaseLoader):
    """Loads templates from the file system."""

    def get_source(self, environment, filename):
        try:
            f = open(filename, "rb")
        except IOError:
            raise jinja2.TemplateNotFound(filename)
        try:
            contents = f.read().decode("utf-8")
        finally:
            f.close()

        mtime = os.path.getmtime(filename)
        def uptodate():
            try:
                return os.path.getmtime(filename) == mtime
            except OSError:
                return False
        return contents, filename, uptodate
 


class MyServer(ThreadingMixIn, HTTPServer):
    
    def __init__(self, address, handler, basepath, authRealm, authString):
        HTTPServer.__init__(self, address, handler)
        self.basepath = basepath
        self.authRealm = authRealm
        self.authString = authString
        self.env = jinja2.Environment(
            loader=FileLoader()
        )
        self.env.globals = eg.globals.__dict__
        
        
    #def handle_error(self, request, client_address):
    #    eg.PrintError("HTTP Error")



class HttpRequestHandler(SimpleHTTPRequestHandler):

    def Authenticate(self):
        # only authenticate, if set
        if not self.server.authString:
            return True
        
        # do Basic HTTP-Authentication
        authHeader = self.headers.get('authorization')
        if authHeader is not None:
            authType, authString = authHeader.split(' ', 2)
            if authType.lower() == 'basic':
                if authString == self.server.authString:
                    return True
                
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 
            'Basic realm="%s"' % self.server.authRealm
        )
        self.end_headers()
        return False

        
    def SendContent(self, path):
        fsPath = self.translate_path(path)
        if os.path.isdir(fsPath):
            if not path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(fsPath, index)
                if os.path.exists(index):
                    fsPath = index
                    break
            else:
                return self.list_directory(path)
        extension = posixpath.splitext(fsPath)[1].lower()
        if extension not in (".htm", ".html"):
            f = self.send_head()
            if f:
                self.wfile.write(f.read())
                f.close()
            return
        try:
            template = self.server.env.get_template(fsPath)
        except jinja2.TemplateNotFound:
            self.send_error(404, "File not found")
            return
        content = template.render()
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        #fs = os.fstat(f.fileno())
        self.send_header("Content-Length", len(content))
        #self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        self.wfile.write(content)


    @eg.LogIt
    def do_HEAD(self):
        SimpleHTTPRequestHandler.do_HEAD(self)
        
        
    @eg.LogItWithReturn
    def do_GET(self):
        """Serve a GET request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return
        
        path, dummy, remaining = self.path.partition("?")
        if remaining:
            queries = remaining.split("#", 1)[0].split("&")
            queries = [unquote_plus(part).decode("latin1") for part in queries]
            if len(queries) > 0:
                event = queries.pop(0).strip()
                if "withoutRelease" in queries:
                    queries.remove("withoutRelease")
                    event = self.TriggerEnduringEvent(event, queries)
                    while not event.isEnded:
                        time.sleep(0.05)
                elif event == "ButtonReleased":
                    self.EndLastEvent()
                else:
                    event = self.TriggerEvent(event, queries)
                    while not event.isEnded:
                        time.sleep(0.05)

        try:
            self.SendContent(path)
        except Exception, exc:
            self.EndLastEvent()
            eg.PrintError("Webserver socket error", self.path)
            eg.PrintError(Exception, exc)
            if exc.args[0] == 10053: # Software caused connection abort
                pass
            elif exc.args[0] == 10054: # Connection reset by peer
                pass
            else:
                raise


    def log_message(self, format, *args):
        # suppress all messages
        pass


    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # stolen from SimpleHTTPServer.SimpleHTTPRequestHandler
        # but changed to handle files from a defined basepath instead
        # of os.getcwd()
        path = posixpath.normpath(unquote(path))
        words = [word for word in path.split('/') if word]
        path = self.server.basepath
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): 
                continue
            path = os.path.join(path, word)
        return path

    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map['.ico'] = 'image/x-icon'



class Webserver(eg.PluginBase):
    canMultiLoad = True

    class text:
        generalBox = "General Settings"
        port = "TCP/IP port:"
        documentRoot = "HTML documents root:"
        eventPrefix = "Event prefix:"
        authBox = "Basic Authentication"
        authRealm = "Realm:"
        authUsername = "Username:"
        authPassword = "Password:"


    def __start__(
        self, 
        prefix=None, 
        port=80, 
        basepath=None, 
        authRealm="Eventghost", 
        authUsername="", 
        authPassword=""
    ):
        self.info.eventPrefix = prefix
        self.port = port
        self.abort = False
        
        class RequestHandler(HttpRequestHandler):
            TriggerEvent = self.TriggerEvent
            TriggerEnduringEvent = self.TriggerEnduringEvent
            EndLastEvent = self.EndLastEvent

        authString = None
        if authUsername or authPassword:
            authString = base64.b64encode(authUsername + ':' + authPassword)

        def ThreadLoop():
            server = MyServer(
                ('', port), RequestHandler, basepath, authRealm, authString
            )
            # Handle one request at a time until stopped
            while not self.abort:
                server.handle_request()
        self.httpdThread = Thread(name="WebserverThread", target=ThreadLoop)
        self.httpdThread.start()


    def __stop__(self):
        if self.httpdThread:
            self.abort = True
            conn = httplib.HTTPConnection("127.0.0.1:%d" % self.port)
            conn.request("QUIT", "/")
            conn.getresponse()
            self.httpdThread = None


    def Configure(
        self, 
        prefix="HTTP", 
        port=80, 
        basepath="", 
        authRealm="EventGhost", 
        authUsername="", 
        authPassword=""
    ):
        text = self.text
        panel = eg.ConfigPanel()

        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        filepathCtrl = panel.DirBrowseButton(basepath)
        editCtrl = panel.TextCtrl(prefix)
        authRealmCtrl = panel.TextCtrl(authRealm)
        authUsernameCtrl = panel.TextCtrl(authUsername)
        authPasswordCtrl = panel.TextCtrl(authPassword)

        labels = (
            panel.StaticText(text.port),
            panel.StaticText(text.documentRoot),
            panel.StaticText(text.eventPrefix),
            panel.StaticText(text.authRealm),
            panel.StaticText(text.authUsername),
            panel.StaticText(text.authPassword),
        )
        eg.EqualizeWidths(labels)

        acv = wx.ALIGN_CENTER_VERTICAL
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[0], 0, acv)
        sizer.Add(portCtrl)
        sizer.Add(labels[1], 0, acv)
        sizer.Add(filepathCtrl)
        sizer.Add(labels[2], 0, acv)
        sizer.Add(editCtrl)
        staticBox = wx.StaticBox(panel, label=text.generalBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[3], 0, acv)
        sizer.Add(authRealmCtrl)
        sizer.Add(labels[4], 0, acv)
        sizer.Add(authUsernameCtrl)
        sizer.Add(labels[5], 0, acv)
        sizer.Add(authPasswordCtrl)
        staticBox = wx.StaticBox(panel, label=text.authBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP, 10)

        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
                portCtrl.GetValue(),
                filepathCtrl.GetValue(),
                authRealmCtrl.GetValue(),
                authUsernameCtrl.GetValue(),
                authPasswordCtrl.GetValue()
            )
