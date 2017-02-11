import eg
import cPickle
import os.path 
import codecs
import sys

eg.RegisterPlugin(
    name = "pVar",
    author = "HN",
    version = "1.0.0",
    kind = "other",
    description = 	(
						"<p>Plugin to make eg.globals.xyz persistent "
						"between EventGhost sessions</p>"
						"<p>Action SetGlobalsVar has 2 parameters, key & value.</p>"
						"<p>Example:\n"
						"eg.plugins.pVar.SetGlobalVar('SunIsUp', True)</p>"
						"<p>This will set eg.globals.SunIsUp = True and also store "
						"this value in the pVar file.</p>"
						"<p>The pVar file is evaluated when plugin is loaded, and "
						"all variables in file will be set to it's last value.</p>"
					)
)

class Text:
	restoreHeader = "Restoring persistent variables"
	restoreRemoved = "removed, no longer used in config"
	restore = "restore"
	save = "save"
	configShowRestore = "Log restored variables at startup"
	configShowSave = "Log on variable save"
	unnamedConfig = "pVar plugin can not be loaded in unnamed config!"


		
class pVar(eg.PluginBase):
    text = Text

    def __init__(self):
		self.AddAction(SetGlobalsVar)
	
    def __start__(self, showRestore, showSave):
		if eg.document.filePath==None:
			print self.text.unnamedConfig
		else:
			self.showRestore = showRestore
			self.showSave = showSave
			self.varDict = {}
			configfile = eg.document.filePath
			self.pvarfile = configfile.replace(".xml", ".pvar")
			if os.path.exists(self.pvarfile):
				file = open(self.pvarfile, 'r')
				self.varDict = cPickle.load(file)
				file.close
				file = codecs.open(configfile, encoding='utf-8')
				configdata = file.read()
				file.close
				if self.showRestore:
					print "------------------------------------------------------------------------------"
					print "pVar: Restoring persistent variables"
					print "------------------------------------------------------------------------------"
				for dKey, dValue in self.varDict.items():
					searchStr1="SetGlobalsVar(\\'"+str(dKey)+"\\'"
					searchStr1.encode('utf-8')
					searchStr2="SetGlobalsVar('"+str(dKey)+"'"
					searchStr2.encode('utf-8')
					searchStr3="SetGlobalsVar(u'"+str(dKey)+"'"
					searchStr3.encode('utf-8')
					if configdata.find(searchStr1) == -1 \
					and configdata.find(searchStr2) == -1 \
					and configdata.find(searchStr3) == -1:
						if self.showRestore:
							print "pVar restore: eg.globals.%s  (removed, no longer used in config)" %(dKey)
						del self.varDict[dKey]
						file = open(self.pvarfile, 'w')
						cPickle.dump(self.varDict, file)
						file.close
					else:
						if self.showRestore:
							print "pVar restore: eg.globals.%s=%s" %(dKey, dValue)
						exec "eg.globals.%s=dValue" %(dKey)

				if self.showRestore:
					print "------------------------------------------------------------------------------"

			
    def Configure(
        self,
        showRestore = False,
        showSave = False
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer = wx.GridBagSizer(3, 5)

        showRestoreCtrl = wx.CheckBox(panel, -1, "")
        showRestoreCtrl.SetValue(showRestore)
        mySizer.Add(wx.StaticText(panel, -1, self.text.configShowRestore), (1,0))
        mySizer.Add(showRestoreCtrl, (1,1))

        showSaveCtrl = wx.CheckBox(panel, -1, "")
        showSaveCtrl.SetValue(showSave)
        mySizer.Add(wx.StaticText(panel, -1, self.text.configShowSave), (3,0))
        mySizer.Add(showSaveCtrl, (3,1))

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        while panel.Affirmed():
            showRestore = showRestoreCtrl.GetValue()
            showSave = showSaveCtrl.GetValue()
            
            panel.SetResult(
                        showRestore,
                        showSave
            )
			
			
class SetGlobalsVar(eg.ActionBase):

    def __call__(self, dKey, dValue):
	if self.plugin.showSave:
		print "pVar save: ", dKey, "=", dValue
	exec "eg.globals.%s=dValue" %(dKey)
	self.plugin.varDict[dKey] = dValue
	file = open(self.plugin.pvarfile, 'w')
	cPickle.dump(self.plugin.varDict, file)
	file.close

    def Configure(self, dKey="", dValue=""):
            
        panel = eg.ConfigPanel(self)
       
        # Create a textfield for Variable name
        keyCtrl = wx.TextCtrl(panel, -1, dKey)

        staticBox = wx.StaticBox(panel, -1, "Variable name")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(keyCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for Variable value
        valueCtrl = wx.TextCtrl(panel, -1, dValue)

        staticBox = wx.StaticBox(panel, -1, "Value")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(valueCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                keyCtrl.GetValue(), 
                valueCtrl.GetValue(),
            )      


      
