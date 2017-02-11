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

# $LastChangedDate: 2015-09-16 3:30:00 +0100$
# $LastChangedRevision: 4 $
# $LastChangedBy: K $


import eg

eg.RegisterPlugin(
    name = "System Database",
    description = "Dictionary Based Database System",
    version = "0." + "$LastChangedRevision: 0 $".split()[1],
    author = "K",
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

import ast

class TransferDB(eg.ActionBase):

    name = 'Transfer Database'
    description = 'Returns the whole database to be stored in a variable of your choosing this is what is called a shallow copy. Any changes made will make the changes in the primary database as well.'

    def __call__(self):

        return dict(self.plugin.DBase)


class PrintDB(eg.ActionBase):

    name = 'Print Database'
    description = 'Prints the whole database into the EventGhost log.'

    def __call__(self):

        print self.plugin.DBase


class ModifyItem(eg.ActionWithStringParameter):

    baseText = Text

    def __call__(self, key1, key2=None, key3=None, value=None):

        return self.plugin.Modify(key1,key2,key3,value)

    def Configure(self, key1='', key2='', key3='', value=None):

        if value == None:
            value = ""
        text = self.baseText
        panel = eg.ConfigPanel()
        key1Ctrl = panel.TextCtrl(key1)
        key2Ctrl = panel.TextCtrl(key2)
        key3Ctrl = panel.TextCtrl(key3)
        valCtrl = panel.TextCtrl(value)
        
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
    
    baseText = Text

    def __call__(self, key1, key2=None, key3=None, value=None):

        return self.plugin.Add(key1,key2,key3,value)

    def Configure(self, key1='', key2='', key3='', value=None):

        if value == None:
            value = ""
        text = self.baseText
        panel = eg.ConfigPanel()
        key1Ctrl = panel.TextCtrl(key1)
        key2Ctrl = panel.TextCtrl(key2)
        key3Ctrl = panel.TextCtrl(key3)
        valCtrl = panel.TextCtrl(value)
        
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

    baseText = Text

    def __call__(self, key1, key2=None, key3=None):

        return self.plugin.Delete(key1,key2,key3)

    def Configure(self, key1='', key2='', key3=''):
        
        text = self.baseText
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
    
    baseText = Text

    def __call__(self, key1, key2=None, key3=None):

        return self.plugin.Query(key1,key2,key3)

    def Configure(self, key1='', key2='', key3=''):
        
        text = self.baseText
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
    
    baseText = Text

    def __call__(self, fpath, fname):

        return self.plugin.LoadFile(fpath,fname)

    def Configure(self, fpath='', fname=''):
        
        text = self.baseText
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

    baseText = Text

    def __call__(self, fpath, fname):

        return self.plugin.SaveFile(fpath,fname)

    def Configure(self, fpath='', fname=''):
        
        text = self.baseText
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

        eg.TriggerEvent(
            'System-Startup',
            prefix = 'MountainHome.Control-Systems',
            payload = ['System-Startup',['LoadingPlugins','.............']]
            )

        self.AddAction(TransferDB)
        self.AddAction(PrintDB)
        self.AddAction(ModifyItem)
        self.AddAction(AddItem)
        self.AddAction(DeleteItem)
        self.AddAction(QueryItem)
        self.AddAction(LoadFromFile)
        self.AddAction(SaveToFile)

        self.DBase = {}

    def __start__(
                self,
                fileloadpath,
                fileloadname,
                filesavepath,
                filesavename
                ):

        fileloadpath = self.PathCheck(fileloadpath)
        filesavepath = self.PathCheck(filesavepath)
        
        self.fileloadpath=fileloadpath
        self.fileloadname=fileloadname
        self.filesavepath=filesavepath
        self.filesavename=filesavename
        self.loadedMalformedData=None

        starterror = self.FileError(self.fileloadpath,self.fileloadname,'Load')
        starterror = self.FileError(self.filesavepath,self.filesavename,'Save')

        if starterror: return

        self.LoadFile(self.fileloadpath,self.fileloadname)

    def __stop__(self):

        self.SaveFile(self.filesavepath,self.filesavename)

    def Notice(self, message, item=None, messageOnly=False):

        if messageOnly:
            eg.PrintNotice(message)

        if not messageOnly:
            eg.PrintNotice(message+str(item))

    def Modify(self, key1, key2, key3, val):

        try:
            val = ast.literal_eval(val)
        except:
            pass

        if key2 != None and key2 != '' and key3 != None and key3 != '':

            try:

                oldval = self.DBase[key1][key2][key3]
                self.DBase[key1][key2][key3] = val

                eg.TriggerEvent(
                                'Modified',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:val}}}
                                )
                return True
            except:
                try:
                    oldval = self.DBase[key1][key2]
                    self.Notice('Modify: Invalid Key: Key3 = ',key3)
                    return False
                except:
                    try:
                        oldval = self.DBase[key1]
                        self.Notice('Modify: Invalid Key: Key2 = ',key2)
                        return False
                    except:
                        self.Notice('Modify: Invalid Key: Key1 = ',key1)
                        return False

        elif key2 != None and key2 != '':
            try:
                oldval=self.DBase[key1][key2]
                self.DBase[key1][key2] = val
                eg.TriggerEvent(
                                'Modified',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:val}}
                                )
                return True
            except:
                try:
                    oldval = self.DBase[key1]
                    self.Notice('Modify: Invalid Key: Key2 = ',key2)
                    return False
                except:
                    self.Notice('Modify: Invalid Key: Key1 = ',key1)
                    return False
        else:
            try:
                oldval = self.DBase[key1]
                self.DBase[key1] = val
                eg.TriggerEvent(
                            'Modified',
                            prefix = 'SystemDatabase',
                            payload = {key1:val}
                            )
                return True
            except:
                self.Notice('Modify: Invalid Key: Key1 = ',key1)
                return False

    def Add(self, key1, key2, key3, val):

        try:
            val = ast.literal_eval(val)
        except:
            pass

        if key2 != None and key2 != '' and key3 != None and key3 != '':
            try:
                oldval = self.DBase[key1][key2][key3]
                self.Notice('Add: Already exists use Modify',messageOnly=True)
                return False
            except:
                try:
                    self.DBase[key1][key2][key3] = val
                    eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:val}}}
                                )
                    return True
                except:
                    try:
                        self.DBase[key1][key2] = {key3: val}
                        eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:val}}}
                                )
                        return True
                    except:
                        try:
                            self.DBase[key1] = {key2: {key3: val}}
                            eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:val}}}
                                )
                            return True
                        except:
                            self.Notice('Add: Invalid Key: Key1 = ',str(key1)+', Key2 = '+str(key2)+', Key3 = '+str(key3))
                            return False

        elif key2 != None and key2 != '':
            try:
                oldval = self.DBase[key1][key2]
                self.Notice('Add: Already exists use Modify',messageOnly=True)
                return False
            except:
                try:
                    self.DBase[key1][key2] = val
                    eg.TriggerEvent(
                                'Added',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:val}}
                                )
                    return True
                except:
                    self.Notice('Add: Invalid Key: Key1 = ',str(key1)+', Key2 = '+str(key2))
                    return False
        else:
            try:
                oldval = self.DBase[key1]
                self.Notice('Add: Already exists use Modify',messageOnly=True)
                return False
            except:
                try:
                    self.DBase[key1] = val
                    eg.TriggerEvent(
                                   'Added',
                                    prefix = 'SystemDatabase',
                                    payload = {key1:val}
                                    )
                    return True
                except:
                    self.Notice('Add: Invalid Key: Key1 = ',key1)
                    return False


    def Delete(self, key1, key2, key3):
        
        if key2 != None and key2 != '' and key3 != None and key3 != '':
            try:
                oldval = self.DBase[key1][key2][key3]
                del self.DBase[key1][key2][key3]
                eg.TriggerEvent(
                                'Deleted',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:{key3:oldval}}}
                                )
                return True
            except:
                try:
                    oldval = self.DBase[key1][key2]
                    self.Notice("Delete: Invalid Key: Key3 = ",key3)
                    return False
                except:
                    try:
                        oldval = self.DBase[key1]
                        self.Notice("Delete: Invalid Key: Key2 = ",key2)
                        return False
                    except:
                        self.Notice("Delete: Invalid Key: Key1 = ",key1)
                        return False

        elif key2 != None and key2 != '':
            try:
                oldval = self.DBase[key1][key2]
                del self.DBase[key1][key2]
                eg.TriggerEvent(
                                'Deleted',
                                prefix = 'SystemDatabase',
                                payload = {key1:{key2:oldval}}
                                )
                return True
            except:
                try:
                    oldval = self.DBase[key1]
                    self.Notice("Delete: Invalid Key: Key2 = ",key2)
                    return False
                except:
                    self.Notice("Delete: Invalid Key: Key1 = ",key1)
                    return False
    
        else:
            try:
                oldval = self.DBase[key1]
                del self.DBase[key1]
                eg.TriggerEvent(
                                'Deleted',
                                prefix = 'SystemDatabase',
                                payload = {key1:oldval}
                                )
                return True
            except:
                self.Notice("Delete: Invalid Key: Key1 = ",key1)
                return False

    def Query(self, key1, key2, key3):

        if key2 != None and key2 != '' and key3 != None and key3 != '':
            try:
                eg.TriggerEvent(
                               'QueryResults.'+key1+'--'+key2+'--'+key3,
                                prefix = 'SystemDatabase',
                                payload = self.DBase[key1][key2][key3]
                                )

                return self.DBase[key1][key2][key3]
            except:
                self.Notice('Query: Invalid Key: Key1 = ',str(key1)+', Key2 = '+str(key2)+', Key3 = '+str(key3))
                return 'KeyError'

        elif key2 != None and key2 != '':
            try:
                eg.TriggerEvent(
                               'QueryResults.'+key1+'--'+key2,
                                prefix = 'SystemDatabase',
                                payload = self.DBase[key1][key2]
                                )
                return self.DBase[key1][key2]
            except:
                self.Notice('Query: Invalid Key: Key1 = ',str(key1)+', Key2 = '+str(key2))
                return 'KeyError'

        else:
            try:
                eg.TriggerEvent(
                               'QueryResults.'+key1,
                                prefix = 'SystemDatabase',
                                payload = self.DBase[key1]
                                )
                return self.DBase[key1]
            except:
                self.Notice('Query: Invalid Key: Key1 = ',key1)
                return 'KeyError'

    def PathCheck(self, fpath):

        if fpath[-1:] != '\\':
            fpath += '\\'
        return fpath

    def FileError(self, fpath, fname, state):

        stateerror=False

        if fpath == '':
            eg.PrintError(state+ ' path cannot be blank.')
            stateerror = True

        if fname == '':
            eg.PrintError(state+' filename cannot be blank.')
            stateerror = True

        return stateerror


    def EvalFile(self,evalString):

        try:
            self.DBase = ast.literal_eval(evalString)
            eg.TriggerEvent(
                        'DatabaseLoaded.'+self.filesavename.replace('.','--'),
                        prefix = 'SystemDatabase',
                        payload = self.filesavepath+self.filesavename
                        )
            return True

        except:
            eg.PrintError("Database data is malformed")
            return False

    def LoadFile(self, fpath='', fname=''):

        fpath = self.PathCheck(fpath)

        try:
            strDict=''
            try:
                with open(fpath+fname,"r") as f:
                    strDict=f.readline()

            except IOError:
                with open(fpath+fname,"w") as f:
                    f.write("{}")
                with open(fpath+fname,"r") as f:
                    strDict=f.readline()

            self.filesavepath = fpath
            self.filesavename = fname
            return self.EvalFile(strDict)

        except IOError:
            self.FileError(fpath,fname,'Load')
            return False

    def SaveFile(self, fpath='', fname=''):

        fpath = self.PathCheck(fpath)

        try:
            with open(fpath+fname,"w") as f:
                f.write(str(self.DBase))
            eg.TriggerEvent(
                        'DatabaseSaved.'+fname.replace('.','--'),
                        prefix = 'SystemDatabase',
                        payload = fpath+fname
                        )
            return True

        except IOError:
            self.FileError(fpath,fname,'Save')
            return False


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