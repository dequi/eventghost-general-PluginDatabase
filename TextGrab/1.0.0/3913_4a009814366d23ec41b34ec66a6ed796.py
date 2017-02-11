import eg

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

    def __call__(self):
        eg.globals.grabbedText = eg.WinApi.GetWindowText(eg.lastFoundWindows[0]) 
        print "Text grabbed: "+ eg.globals.grabbedText


