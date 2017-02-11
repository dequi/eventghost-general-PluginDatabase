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

# $LastChangedDate: 2015-08-06 3:30:00 +0100$
# $LastChangedRevision: 1 $
# $LastChangedBy: kdschlosser $



import eg
import ast

global DBase

DBase = {}

eg.RegisterPlugin(
    name = "System Database",
    description = "Dictionary Based Database System",
    version = "0." + "$LastChangedRevision: 0 $".split()[1],
    author = "kdschlosser",
    canMultiLoad = False,
    guid = '{2E4E12A0-826A-408F-92EA-B6E98595071B}'
)

class Text:
    keyword1 = "Keyword 1:"
    keyword2 = "Keyword 2:"
    keyword3 = "Keyword 3:"
    value = "Value:"
    filepath = "File Path:"
    filename = "File Name:"
    loadpath = "Load File Path"
    loadname = "Load File Name"
    savepath = "Save File Path"
    savename = "Save File Name"
    modifybox = "Modify Database Item"
    addbox = "Add Database Item"
    deletebox = "Delete Database Item"
    querybox = "Lookup Database Item"
    loadbox = "Load Database from File"
    savebox = "Save Database to File"
    confbox = "Default Database Load and Save"
    class ModifyItem:
        name = 'Modify Item'
        description = 'Modify Item'
    class AddItem:
        name = 'Add Item'
        description = 'Add Item'
    class DeleteItem:
        name = 'Delete Item'
        description = 'Delete Item'
    class QueryItem:
        name = 'Query Item'
        description = 'Query Item'
    class LoadFromFile:
        name = 'Load From File'
        description = 'Load From File'
    class SaveToFile:
        name = 'Save To File'
        description = 'Save To File'

class PrintDB(eg.ActionBase):

    name = 'Print Database'
    description = 'Print Database'

    def __call__(self):

        print DBase


class ModifyItem(eg.ActionWithStringParameter):

    text = Text

    def __call__(self, key1, key2=None, key3=None, val=None):

        return self.plugin.Modify(key1,key2,key3,val)

    def Configure(self, key1='', key2='', key3='', val=None):

        if val == None:
            val = ""
        text = self.text
        panel = eg.ConfigPanel()
        key1Ctrl = panel.TextCtrl(key1)
        key2Ctrl = panel.TextCtrl(key2)
        key3Ctrl = panel.TextCtrl(key3)
        valCtrl = panel.TextCtrl(val)
        
        modifyItemBox = panel.BoxedGroup(
                                    text.modifybox,
                                    (text.keyword1, key1Ctrl),
                                    (text.keyword2, key2Ctrl),
                                    (text.keyword3, key3Ctrl),
                                    (text.value, valCtrl),
                                    )
        eg.EqualizeWidths(modifyItemBox.GetColumnItems(0))
        panel.sizer.Add(modifyItemBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        key1Ctrl.GetValue(),
                        key2Ctrl.GetValue(),
                        key3Ctrl.GetValue(),
                        valCtrl.GetValue(), 
                        )

class AddItem(eg.ActionWithStringParameter):
    
    text = Text

    def __call__(self, key1, key2=None, key3=None, val=None):

        return self.plugin.Add(key1,key2,key3,val)

    def Configure(self, key1='', key2='', key3='', val=None):

        if val == None:
            val = ""
        text = self.text
        panel = eg.ConfigPanel()
        key1Ctrl = panel.TextCtrl(key1)
        key2Ctrl = panel.TextCtrl(key2)
        key3Ctrl = panel.TextCtrl(key3)
        valCtrl = panel.TextCtrl(val)
        
        addItemBox = panel.BoxedGroup(
                                    text.addbox,
                                    (text.keyword1, key1Ctrl),
                                    (text.keyword2, key2Ctrl),
                                    (text.keyword3, key3Ctrl),
                                    (text.value, valCtrl),
                                    )
        eg.EqualizeWidths(addItemBox.GetColumnItems(0))
        panel.sizer.Add(addItemBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        key1Ctrl.GetValue(),
                        key2Ctrl.GetValue(),
                        key3Ctrl.GetValue(),
                        valCtrl.GetValue(), 
                        )


class DeleteItem(eg.ActionWithStringParameter):

    text = Text

    def __call__(self, key1, key2=None, key3=None):

        return self.plugin.Delete(key1,key2,key3)

    def Configure(self, key1='', key2='', key3=''):
        
        text = self.text
        panel = eg.ConfigPanel()
        key1Ctrl = panel.TextCtrl(key1)
        key2Ctrl = panel.TextCtrl(key2)
        key3Ctrl = panel.TextCtrl(key3)
        
        deleteItemBox = panel.BoxedGroup(
                                    text.deletebox,
                                    (text.keyword1, key1Ctrl),
                                    (text.keyword2, key2Ctrl),
                                    (text.keyword3, key3Ctrl),
                                    )
        eg.EqualizeWidths(deleteItemBox.GetColumnItems(0))
        panel.sizer.Add(deleteItemBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        key1Ctrl.GetValue(),
                        key2Ctrl.GetValue(),
                        key3Ctrl.GetValue(), 
                        )

class QueryItem(eg.ActionWithStringParameter):
    
    text = Text

    def __call__(self, key1, key2=None, key3=None):

        return self.plugin.Query(key1,key2,key3)

    def Configure(self, key1='', key2='', key3=''):
        
        text = self.text
        panel = eg.ConfigPanel()
        key1Ctrl = panel.TextCtrl(key1)
        key2Ctrl = panel.TextCtrl(key2)
        key3Ctrl = panel.TextCtrl(key3)
        
        queryItemBox = panel.BoxedGroup(
                                    text.querybox,
                                    (text.keyword1, key1Ctrl),
                                    (text.keyword2, key2Ctrl),
                                    (text.keyword3, key3Ctrl),
                                    )
        eg.EqualizeWidths(queryItemBox.GetColumnItems(0))
        panel.sizer.Add(queryItemBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        key1Ctrl.GetValue(),
                        key2Ctrl.GetValue(),
                        key3Ctrl.GetValue(), 
                        )

class LoadFromFile(eg.ActionWithStringParameter):
    
    text = Text

    def __call__(self, fpath, fname):

        return self.plugin.LoadFile(fpath,fname)

    def Configure(self, fpath='', fname=''):
        
        text = self.text
        panel = eg.ConfigPanel()
        fpathCtrl = panel.TextCtrl(fpath)
        fnameCtrl = panel.TextCtrl(fname)
                
        loadFileBox = panel.BoxedGroup(
                                    text.loadbox,
                                    (text.filepath, fpathCtrl),
                                    (text.filename, fnameCtrl),
                                    )
        eg.EqualizeWidths(loadFileBox.GetColumnItems(0))
        panel.sizer.Add(loadFileBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        fpathCtrl.GetValue(),
                        fnameCtrl.GetValue(),
                        )


class SaveToFile(eg.ActionWithStringParameter):

    text = Text

    def __call__(self, fpath, fname):

        self.plugin.SaveFile(fpath,fname)

    def Configure(self, fpath='', fname=''):
        
        text = self.text
        panel = eg.ConfigPanel()
        fpathCtrl = panel.TextCtrl(fpath)
        fnameCtrl = panel.TextCtrl(fname)
        
        saveFileBox = panel.BoxedGroup(
                                text.savebox,
                                (text.filepath, fpathCtrl),
                                (text.filename, fnameCtrl),
                                )
        eg.EqualizeWidths(saveFileBox.GetColumnItems(0))
        panel.sizer.Add(saveFileBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        fpathCtrl.GetValue(),
                        fnameCtrl.GetValue(), 
                        )


class SystemDatabase(eg.PluginBase):

    text = Text

    def __init__(self):

        self.AddAction(PrintDB)
        self.AddAction(ModifyItem)
        self.AddAction(AddItem)
        self.AddAction(DeleteItem)
        self.AddAction(QueryItem)
        self.AddAction(LoadFromFile)
        self.AddAction(SaveToFile)


    def __start__(
                self,
                fileloadpath,
                fileloadname,
                filesavepath,
                filesavename
                ):

        if fileloadpath[-1:] != '\\':
            fileloadpath += '\\'
        if filesavepath[-1:] != '\\':
            filesavepath += '\\'

        self.fileloadpath=fileloadpath
        self.fileloadname=fileloadname
        self.filesavepath=filesavepath
        self.filesavename=filesavename

        starterror=False

        if self.fileloadpath == '':
            eg.PrintError('Load path cannot be blank.')
            starterror = True

        if self.fileloadname == '':
            eg.PrintError('Load filename cannot be blank.')
            starterror = True

        if self.filesavepath == '':
            eg.PrintError('Save path cannot be blank.')
            starterror = True

        if self.filesavename == '':
            eg.PrintError('Save filename cannot be blank.')
            starterror = True

        if starterror: return

        self.LoadFile(self.fileloadpath,self.fileloadname)

    def __stop__(self):

        self.SaveFile(self.filesavepath,self.filesavename)

    def Modify(self, key1, key2, key3, val):

        try:
            val = ast.literal_eval(val)
        except:
            pass

        if key2 != None and key2 != '' and key3 != None and key3 != '':
            try:
                oldval = DBase[key1][key2][key3]
                DBase[key1][key2][key3] = val
                eg.TriggerEvent(
                                'Modified',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:val}}}
                                )
                return True
            except KeyError:
                try:
                    oldval = DBase[key1][key2]
                    eg.PrintError('Key 3 Invalid')
                    print key3
                    return False
                except KeyError:
                    try:
                        oldval = DBase[key1]
                        eg.PrintError('Key 2 Invalid')
                        print key2
                        return False
                    except KeyError:
                        eg.PrintError('Key 1 Invalid')
                        print key1
                        return False

        elif key2 != None and key2 != '':
            try:
                oldval=DBase[key1][key2]
                DBase[key1][key2] = val
                eg.TriggerEvent(
                                'Modified',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:val}}
                                )
                return True
            except KeyError:
                try:
                    oldval = DBase[key1]
                    eg.PrintError('Key 2 Invalid')
                    print key2
                    return False
                except KeyError:
                    eg.PrintError('Key 1 Invalid')
                    print key1
                    return False
        else:
            try:
                oldval = DBase[key1]
                DBase[key1] = val
                eg.TriggerEvent(
                            'Modified',
                            prefix = 'SystemDatabase',
                            payload = {key1:val}
                            )
                return True
            except KeyError:
                eg.PrintError('Key 1 Invalid')
                print key1
                return False

    def Add(self, key1, key2, key3, val):

        try:
            val = ast.literal_eval(val)
        except:
            pass

        if key2 != None and key2 != '' and key3 != None and key3 != '':
            try:
                oldval = DBase[key1][key2][key3]
                eg.PrintError('Item already exists use the modify action')
                return False
            except KeyError:
                try:
                    DBase[key1][key2][key3] = val
                    eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:val}}}
                                )
                    return True
                except KeyError:
                    try:
                        DBase[key1][key2] = {key3:val}
                        eg.TriggerEvent(
                                    'Added',
                                    prefix = 'SystemDatabase',
                                    payload = {key1:{key2:{key3:val}}}
                                    )
                        return True
                    except KeyError:
                        DBase[key1] = {key2:{key3:val}}
                        eg.TriggerEvent(
                                    'Added',
                                    prefix = 'SystemDatabase',
                                    payload = {key1:{key2:{key3:val}}}
                                    )
                        return True

        elif key2 != None and key2 != '':
            try:
                oldval = DBase[key1][key2]
                eg.PrintError('Item already exists use the modify action')
                return False
            except KeyError:
                try:
                    DBase[key1][key2] = val
                    eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:val}}
                                )
                    return True
                except KeyError:
                    DBase[key1] = {key2:val}
                    eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:val}}
                                )
                    return True
    
        else:
            try:
                oldval = DBase[key1]
                eg.PrintError('Item already exists use the modify action')
                return False
            except KeyError:
                DBase[key1] = val
                eg.TriggerEvent(
                               'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:val}
                                )
                return True

    def Delete(self, key1, key2, key3):
        pass


    def Query(self, key1, key2, key3):

        if key2 != None and key2 != '' and key3 != None and key3 != '':
            try:
                eg.TriggerEvent(
                               'QueryResults.'+str(DBase[key1][key2][key3]),
                                prefix = 'SystemDatabase',
                                payload = DBase[key1][key2][key3]
                                )

                return DBase[key1][key2][key3]
            except KeyError:
                eg.PrintError('Key Error')
                print key1,key2,key3
                return 'KeyError'

        elif key2 != None and key2 != '':
            try:
                eg.TriggerEvent(
                               'QueryResults.'+str(DBase[key1][key2]),
                                prefix = 'SystemDatabase',
                                payload = DBase[key1][key2]
                                )
                return DBase[key1][key2]
            except KeyError:
                eg.PrintError('Key Error')
                print key1,key2
                return 'KeyError'

        else:
            try:
                eg.TriggerEvent(
                               'QueryResults.'+str(DBase[key1]),
                                prefix = 'SystemDatabase',
                                payload = DBase[key1]
                                )
                return DBase[key1]
            except KeyError:
                eg.PrintError('Key Error')
                print key1
                return 'KeyError'


    def LoadFile(self, fpath='', fname=''):

        strDict=''
        try:
            with open(fpath+fname,"r") as f:
                strDict=f.readline()
                print strDict
        except IOError:
            with open(fpath+fname,"w") as f:
                f.write("{}")
            with open(fpath+fname,"r") as f:
                strDict=f.readline()
        try:
            DBase = ast.literal_eval(strDict)
            print DBase
            self.filesavepath = fpath
            self.filesavename = fname

            return True
        except:
            eg.PrintError("Database data is malformed")
            return False
        

    def SaveFile(self, fpath='', fname=''):

        with open(fpath+fname,"w") as f:
            f.write(str(DBase))


    def Configure(
                self,
                fileloadpath='',
                fileloadname='',
                filesavepath='',
                filesavename=''
                ):
        text = self.text
        panel = eg.ConfigPanel()
        fileloadpathCtrl = panel.TextCtrl(fileloadpath)
        fileloadnameCtrl = panel.TextCtrl(fileloadname)
        filesavepathCtrl = panel.TextCtrl(filesavepath)
        filesavenameCtrl = panel.TextCtrl(filesavename)
        
        confBox = panel.BoxedGroup(
                                    text.confbox,
                                    (text.loadpath, fileloadpathCtrl),
                                    (text.loadname, fileloadnameCtrl),
                                    (text.savepath, filesavepathCtrl),
                                    (text.savename, filesavenameCtrl),
                                    )
        eg.EqualizeWidths(confBox.GetColumnItems(0))
        panel.sizer.Add(confBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                        fileloadpathCtrl.GetValue(),
                        fileloadnameCtrl.GetValue(),
                        filesavepathCtrl.GetValue(),
                        filesavenameCtrl.GetValue(), 
                        )
