import eg
from ctypes import create_unicode_buffer
from eg.WinApi import GetWindowThreadProcessId,GetClassName,GetWindowText
from eg.WinApi.Dynamic import SendMessage,_kernel32

def GetStatusBarText(hwnd, buf_len = 128):
    """If success, return statusbar texts like list of strings.
    Otherwise return either '>>> No process ! <<<' or '>>> No parts ! <<<'.
    Mandatory argument: handle of statusbar.
    Option argument: length of text buffer."""
    
    
    PAGE_READWRITE            = 4
    PROCESS_VM_OPERATION      = 8
    PROCESS_VM_READ           = 16
    PROCESS_QUERY_INFORMATION = 1024
    SB_GETPARTS               = 1030
    SB_GETTEXTW               = 1037
    MEM_COMMIT                = 4096
    MEM_RELEASE               = 32768

    pid = GetWindowThreadProcessId(hwnd)[1]
    process = _kernel32.OpenProcess(PROCESS_VM_OPERATION|PROCESS_VM_READ|PROCESS_QUERY_INFORMATION, False, pid)
    res_val = ['>>> No process ! <<<',]
    if process <> 0:
        parts = SendMessage(hwnd, SB_GETPARTS, 0, 0)
        partList = []
        res_val = ['>>> No parts ! <<<',]
        if parts > 0:
            remBuf = _kernel32.VirtualAllocEx(process, None, buf_len, MEM_COMMIT, PAGE_READWRITE)
            locBuf = create_unicode_buffer(buf_len)
            for item in range(parts):
                SendMessage(hwnd, SB_GETTEXTW, item, remBuf)
                _kernel32.ReadProcessMemory(process, remBuf, locBuf, buf_len, None) #copy remBuf to locBuf
                partList.append(locBuf.value)
            res_val =  partList
            _kernel32.VirtualFreeEx(process, remBuf, 0, MEM_RELEASE)
    return res_val
        
eg.RegisterPlugin(
    name = "TextGrab",
    author = "Samcek",
    version = "1.0.0",
    kind = "other",
    description = """<rst>
    Grabs the text from any standard Windows graphic element (window title, static text (label), etc...) and stores it in the eg.globals.grabbedText variable.

    Works hand-in-hand with "Find a window" action. Usage:
    
    - first, create a macro
    
    - add a "Find a window" action, appropriately configured to find a graphic element containing the text you wish to grab. This action stores the result into the eg.lastFoundWindows variable.
    
    - add a GrabText action immediately following the "Find a window" action. No need to configure this one, it automatically grabs the text from the windows handle stored in the eg.lastFoundWindows[0] (if any) and stores it into a variable called "eg.globals.grabbedText".
    
    - add a postprocessing action that does something useful with the grabbed text stored in eg.globals.grabbedText. Good candidates are Speech action and Show OSD action. Just add {eg.globals.grabbedText} (curly braces included) in the text field of the configuration window of one of these actions.
    
    """
)



class TextGrabPlugin(eg.PluginBase):
    def __init__(self):
        self.AddAction(GrabText)




class GrabText(eg.ActionBase):

    class text:
        topLabel = """If the result has more parts (such as the status-bar),
you can choose, which part of the result you need.
If the result is only one part, the following settings are meaningless."""
        frontLabel = "Return only part number:"
        endLabel = "(0 = return the entire result as a list)"

    def __call__(self, item = 0):
        hwnd = eg.lastFoundWindows[0]
        clsName = GetClassName(hwnd)
        if clsName == 'TStatusBar' or clsName == 'msctls_statusbar32':
            result = GetStatusBarText(hwnd,1024)
            if item:
                result = result[item-1]
            elif len(result) == 1:
                result = result[0]
        else:
            result =  GetWindowText(hwnd) 
        return result

    def Configure(self, item = 0):
        panel = eg.ConfigPanel(self)
        mainSizer =wx.BoxSizer(wx.HORIZONTAL)
        labelTop = wx.StaticText(panel, -1, self.text.topLabel)
        labelTop.Enable(False)
        labelFront=wx.StaticText(panel, -1, self.text.frontLabel)
        itemCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            min=0,
            max=99,
        )
        itemCtrl.SetValue(item)
        labelEnd=wx.StaticText(panel, -1, self.text.endLabel)
        mainSizer.Add(labelFront,0,wx.TOP,4)
        mainSizer.Add(itemCtrl,0,wx.LEFT,5)
        mainSizer.Add(labelEnd,0,wx.LEFT|wx.TOP,4)
        panel.sizer.Add(labelTop)
        panel.sizer.Add(mainSizer,0,wx.TOP,15)
        
        while panel.Affirmed():
            panel.SetResult(
                itemCtrl.GetValue(),
            )           

        
        


