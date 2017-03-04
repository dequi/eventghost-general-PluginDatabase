import eg

eg.RegisterPlugin(
    name = "Amazon FireTV",
    author = "Eric Fetty",
    version = "0.0.1",
    kind = "other",
    description = "Issues controller commands to a FireTV using ADB.")

import subprocess
global adbPath
global aftvString

class AFTVPlugin(eg.PluginBase):
    def __init__(self):
        self.AddAction(HOME)
        self.AddAction(BACK)
        self.AddAction(UP)
        self.AddAction(DOWN)
        self.AddAction(LEFT)
        self.AddAction(RIGHT)
        self.AddAction(SELECT)
        self.AddAction(MENU)

    def __start__(self, aftvString, adbPath):
        self.adbPath=str(adbPath)
        self.aftvString=str(aftvString)
        subprocess.Popen([adbPath,'connect', aftvString],shell=True,creationflags=subprocess.SW_HIDE)

    def __stop__(self):
        subprocess.Popen([self.adbPath,'disconnect',self.aftvString],shell=True,creationflags=subprocess.SW_HIDE)

    def Configure(self, aftvString="",adbPath=""):
        panel = eg.ConfigPanel()
        aftvStringEdit=panel.TextCtrl(aftvString)
        #adbPathEdit=panel.TextCtrl(adbPath)
        adbPathEdit= MyFileBrowseButton(
            panel,
            buttonText = eg.text.General.browse,
            fileMask = '*.exe')
        panel.AddLine("Amazon FireTV IP : ",aftvStringEdit)
        panel.AddLine("ADB Executable Location : ",adbPathEdit)
        while panel.Affirmed():

            panel.SetResult(aftvStringEdit.GetValue(), adbPathEdit.GetValue())
class MENU(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','1'],shell=True,creationflags=subprocess.SW_HIDE)
class HOME(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','3'],shell=True,creationflags=subprocess.SW_HIDE)

class BACK(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','4'],shell=True,creationflags=subprocess.SW_HIDE)

class UP(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','19'],shell=True,creationflags=subprocess.SW_HIDE)

class DOWN(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','20'],shell=True,creationflags=subprocess.SW_HIDE)

class LEFT(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','21'],shell=True,creationflags=subprocess.SW_HIDE)

class RIGHT(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','22'],shell=True,creationflags=subprocess.SW_HIDE)

class SELECT(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath,'shell','input','keyevent','23'],shell=True,creationflags=subprocess.SW_HIDE)

class MyFileBrowseButton(eg.FileBrowseButton):
    def GetTextCtrl(self):
        return self.textControl