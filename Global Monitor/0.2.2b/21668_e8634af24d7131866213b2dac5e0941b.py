# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg

eg.RegisterPlugin(
    eg.RegisterPlugin(
        name='Global Monitor',
        description=(
            'Manages variables that are set into eg.globals.'
        ),
        help=(
            'This plugin allows for creating and deleting of variables.\n\n '
            'It also monitors if the variable changes at all and gives a nice '
            'UI to view any changes.\n\n'
            'An added feature is that it makes subclassing or nesting '
            'variables really easy.\n An example is take these 2 globals\n'
            '"eg.globals.bedroomOverheadLight"\n'
            '"eg.globals.bedroomWallLight"\n'
            'Nesting the variables would look like this.\n'
            '"eg.globals.Lights.Bedroom.Wall"\n'
            '"eg.globals.Lights.Bedroom.Overhead"\n'
            'The benefit to this would be the ability to iterate or pull up '
            'each variable in a group. But it also makes for a little more '
            'organization of the variables. That is if you have a lot of them.'
        ),
        version='0.2.2b',
        author='K',
        canMultiLoad=True,
        guid='{B2B1CE64-2FF5-4C11-B247-8A2F13F57EA3}'
    )
)

import wx # NOQA
import inspect # NOQA
import threading # NOQA
import wx.aui # NOQA


class Config(eg.PersistentData):
    treePosition = (-1, -1)
    listPosition = (-1, -1)
    col0Size = 100
    col1Size = 100
    col2Size = 200
    col3Size = 100
    treeSize = (200, 300)
    listSize = (500, 300)


class Text(eg.TranslatableStrings):
    treeTitle = 'Global Variable Monitor: Nested Attributes'
    listTitle = 'Global Variable Monitor: Variable List'
    treeShow = 'Show Nested Attributes'
    listShow = 'Show Variable List'
    menuLbl = 'Global Variable Monitor'
    addLbl = 'Add Variable'
    deleteLbl = 'Delete Variable'
    autoLbl = 'Create Variable\nAt Start'
    attributeError = '%s does not have attribute %s'

    addMessage = (
        'Add Variable\n\n'
        'All variables will be made in the eg.globals \n'
        'container. If you want to nest the variables \n'
        'then put a "." between each of the levels.\n\n'
        'Example: Lights.Bedroom.Overhead\n'
        'This will create eg.globals.Lights.Bedroom.Overhead\n'
        'and it will set the "Overhead" variable to None\n'
    )
    deleteMessage = (
        'Delete Variable\n\n'
        'Variables will be deleted from the eg.globals \n'
        'container. If you want to nest the variables \n'
        'then put a "." between each of the levels.\n\n'
        'Example: Lights.Bedroom.Overhead\n'
        'This will load the eg.globals.Lights.Bedroom \n'
        ' container and delete the "Overhead" variable\n\n'
    )
    setValueMessage = (
        'Set Variable Value\n\n'
        'New value will be evaluated.\n'
        'Examples:\n'
        '[1, 2, 3, 4] becomes a list\n'
        '{"Hi": "There"} becomes a dict\n'
        'eg.plugins.SomePlugin.SomeAction becomes an instance\n\n'
        'To bypass being evaluated you need to wrap the value\n'
        'in str()\n'
        'Examples:\n'
        'str([1, 2, 3, 4])\n'
        'str({"Hi": "There"})\n\n'
        'Please enter a new value for global\n%s\n\n'
    )
    lookupValueMessage = (
        'Lookup Variable\n'
        'The entered variable will be looked up in \n'
        'the eg.globals container. If found you will \n'
        'be prompted to enter a new value. Otherwise \n'
        'a message will be displayed in the log.\n\n'
        'For a nested variable follow the example below.\n'
        'Example: Lights.Bedroom.Overhead.lights\n'
        'This will load the eg.globals.Lights.Bedroom \n'
        'container and you will be prompted to input a \n'
        'value for the lights variable\n\n'
    )

    set = 'Set Value'
    retrieved = 'Retrieved Value'
    deleted = 'Deleted Attribute'
    created = 'Created Attribute'
    attributeLbl = 'Variable Name'
    valueLabel = 'Variable Value'
    functionLbl = 'Last Function Call'
    callTypeLbl = 'Last Call Type'
    changeLbl = 'Change Value'

MODULE_NAMES = [
    'eg.CorePluginModule.GlobalMonitor',
    'eg.UserPluginModule.GlobalMonitor']


class VariableBase(object):

    def __init__(self, parent, attrName):
        self.__dict__['_lock'] = threading.Lock()
        self.__dict__['callerLog'] = {}
        self.__dict__['_attrName'] = attrName
        self.__dict__['_parent'] = parent
        self.__dict__['vars'] = {}

    def _GetCaller(self, item, text):
        stack = inspect.stack()
        callingFrame = stack[2][0]

        name = []
        module = inspect.getmodule(callingFrame)
        if module:
            name.append(module.__name__)
        if 'self' in callingFrame.f_locals:
            name.append(callingFrame.f_locals['self'].__class__.__name__)
        codename = callingFrame.f_code.co_name
        if codename != '<module>':
            name.append(codename)
        name = ".".join(name)

        isMod = False
        for modName in MODULE_NAMES:
            if name.startswith(modName):
                isMod = True
        if not isMod:
            if not name:
                newFrame = stack[3][0]
                if 'PythonScript' in newFrame.f_globals:
                    name = repr(newFrame.f_globals['PythonScript'])
                    name = name.split("'")[1]
                del newFrame
            self.__dict__['callerLog'][item] = [name, text]
        del callingFrame

    def __repr__(self):
        return "%s.%s'>" % (
            repr(self.__dict__['_parent'])[:-2],
            self.__dict__['_attrName']
        )

    def __getattr__(self, item):
        dct = self.__dict__
        dct['_lock'].acquire()
        try:
            if item in dct['vars']:
                if not item.startswith('_'):
                    self._GetCaller(item, Text.retrieved)
                return dct['vars'][item]

            if item in dct:
                return dct[item]

        finally:
            dct['_lock'].release()

        raise AttributeError(Text.attributeError % (repr(self), item))

    def __setattr__(self, key, value):
        dct = self.__dict__
        dct['_lock'].acquire()

        if not key.startswith('_') and key not in ('callerLog', 'vars'):
            if key in ['vars']:
                self._GetCaller(key, Text.set)
            else:
                self._GetCaller(key, Text.created)
            dct['vars'][key] = value

        else:
            dct[key] = value

        dct['_lock'].release()

    def __iter__(self):
        dct = self.__dict__
        dct['_lock'].acquire()

        self._GetCaller('__iter__', '__iter__')

        for key in sorted(dct['vars'].keys()):
            if not key.startswith('_'):
                yield key, dct['vars'][key]

        dct['_lock'].release()

    def __delattr__(self, item):
        dct = self.__dict__
        dct['_lock'].acquire()

        try:
            if item in dct['vars']:
                self._GetCaller(item, Text.deleted)
                del(dct['vars'][item])
                return

            elif item in dct:
                del(dct[item])
                return
        finally:
            dct['_lock'].release()

        raise AttributeError(Text.attributeError % (repr(self), item))


class NOValue:
    blah = None


class GlobalMonitor(eg.PluginBase):

    def __init__(self):
        self.oldShowFrame = eg.document.ShowFrame
        eg.PluginBase.__init__(self)
        self.newGlobals = VariableBase(eg, 'globals')
        self.oldGlobals = None
        self.menuThread = None
        self.UI = None
        self.oldClose = eg.Document.Close

    @eg.LogIt
    def CreateMenu(self):
        menu = wx.Menu()

        addItem = wx.MenuItem(menu, Id.ADD, Text.addLbl)
        menu.AppendItem(addItem)
        deleteItem = wx.MenuItem(menu, Id.DELETE, Text.deleteLbl)
        menu.AppendItem(deleteItem)
        changeItem = wx.MenuItem(menu, Id.CHANGE, Text.changeLbl)
        menu.AppendItem(changeItem)

        menu.AppendSeparator()

        treeItem = wx.MenuItem(menu, Id.TREE_SHOW, Text.treeShow)
        menu.AppendItem(treeItem)
        listItem = wx.MenuItem(menu, Id.LIST_SHOW, Text.listShow)
        menu.AppendItem(listItem)

        def OnAdd(evt):
            self.Add()

        def OnDelete(evt):
            self.Delete()

        def OnChange(evt):
            self.Value()

        frame = eg.document.frame
        frame.Bind(wx.EVT_MENU, OnAdd, addItem)
        frame.Bind(wx.EVT_MENU, OnDelete, deleteItem)
        frame.Bind(wx.EVT_MENU, OnChange, changeItem)

        frame.Bind(wx.EVT_MENU, self.UI.treeCtrl.Show, treeItem)
        frame.Bind(wx.EVT_MENU, self.UI.listCtrl.Show, listItem)

        return menu

    def ShowFrame(self):
        if eg.document.reentrantLock.acquire(False):
            if eg.document.frame is None:
                eg.document.frame = eg.MainFrame(eg.document)
                eg.document.frame.Show()
                self.UI = UI(self)
                eg.document.frame.menuBar.Insert(
                    3,
                    self.CreateMenu(),
                    Text.menuLbl
                )
                eg.document.frame.menuBar.Refresh()
            eg.document.frame.Raise()
            eg.document.reentrantLock.release()

    def __start__(self):
        for key in eg.globals.__dict__.keys():
            if not key.startswith('__'):
                setattr(self.newGlobals, key, eg.globals.__dict__[key])

        eg.globals = self.newGlobals

        if eg.document.frame is not None:
            self.UI = UI(self)
            eg.document.frame.menuBar.Insert(3, self.CreateMenu(), Text.menuLbl)
            eg.document.frame.menuBar.Refresh()

        eg.document.ShowFrame = self.ShowFrame


    @eg.LogIt
    def __stop__(self):
        eg.document.ShowFrame = self.oldShowFrame

        if self.UI is not None:
            try:
                self.UI.CloseUI()
            except:
                import traceback
                traceback.print_exc()

        if eg.document.frame is not None:
            eg.document.frame.menuBar.Remove(3)

        if eg.globals == self.newGlobals:
            def IterVariable(old, new=eg.Bunch):
                cls = new(**old)
                for key in old.keys():
                    if isinstance(old[key], VariableBase):
                        setattr(cls, key, IterVariable(old[key].vars))
                return cls

            eg.globals = IterVariable(self.newGlobals.vars)
            self.oldGlobals = None

    @eg.LogIt
    def Value(self, attrLoc=None):
        if attrLoc is None:
            attrLoc = self.Dialog('lookupValueMessage')
            if attrLoc != NOValue:
                if not attrLoc.startswith('eg.globals'):
                    attrLoc = 'eg.globals.' + attrLoc
            else:
                return

        attrLoc = attrLoc.split('.')
        attr = self.GetAttribute(attrLoc[2:-1])
        if attr != NOValue:
                attrName = attrLoc[-1]
                try:
                    value = str(getattr(attr, attrName))
                except AttributeError:
                    eg.PrintError(Text.attributeError % (repr(attr), attrName))
                    return

                newValue = self.Dialog('setValueMessage', value)
                if newValue != NOValue:
                    try:
                        newValue = eval(newValue)
                    except:
                        pass
                    setattr(attr, attrName, newValue)

    @eg.LogItWithReturn
    def Dialog(self, message, value=''):
        defaultValue = value.replace('eg.globals.', '').replace('eg.globals', '')
        dlg = wx.TextEntryDialog(
            eg.document.frame,
            message=getattr(Text, message),
            defaultValue=defaultValue
        )
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            res = dlg.GetValue()
        else:
            res = NOValue
        dlg.Destroy()
        return res

    @eg.LogIt
    def Add(self, value=''):
        variable = self.Dialog('addMessage', value)
        if variable != NOValue:
            variable = variable.split('.')
            attr = eg.globals
            for attrName in variable[:-1]:
                try:
                    attr = getattr(attr, attrName)
                except AttributeError:
                    cls = VariableBase(attr, attrName)
                    setattr(attr, attrName, cls)
                    attr = cls
            setattr(attr, variable[-1], None)

    def GetAttribute(self, attrNames):
        attr = eg.globals
        for attrName in attrNames:
            try:
                attr = getattr(attr, attrName)
            except AttributeError:
                eg.PrintError(Text.attributeError % (repr(attr), attrName))
                return NOValue
        return attr

    @eg.LogIt
    def Delete(self, value=''):
        variable = self.Dialog('deleteMessage', value)
        if variable != NOValue:
            variable = variable.split('.')
            attr = self.GetAttribute(variable[:-1])
            if attr != NOValue:
                delattr(attr, variable[-1])


class _Id(object):
    def __getattr__(self, item):
        attr = wx.NewId()
        setattr(self, item, attr)
        return attr

Id = _Id()


class UIUpdateThread:

    def __init__(self, callback):
        self.event = threading.Event()
        self.thread = threading.Thread(
            name='Global_Monitor_UI_Updater',
            target=self.Run,
            args=(callback,)
        )
        self.thread.start()

    def Run(self, callback):
        while not self.event.isSet():
            try:
                callback()
            except:
                pass
            self.event.wait(0.05)

    def Stop(self):
        self.event.set()
        self.thread.join(2.0)


class ListMenu(wx.Menu):
    def __init__(self, plugin, data):
        wx.Menu.__init__(self)

        self.Append(Id.LIST_DELETE, Text.deleteLbl)
        self.Append(Id.LIST_VALUE, Text.changeLbl)

        def OnMenu(evt):
            if evt.GetId() == Id.LIST_VALUE:
                plugin.Value(data)

            elif evt.GetId() == Id.LIST_DELETE:
                plugin.Delete(data)

            evt.Skip()

        self.Bind(wx.EVT_MENU, OnMenu)


class TreeMenu(wx.Menu):
    def __init__(self, plugin, data):
        wx.Menu.__init__(self)

        self.Append(Id.TREE_ADD, Text.addLbl)
        self.Append(Id.TREE_DELETE, Text.deleteLbl)

        def OnMenu(evt):
            if evt.GetId() == Id.TREE_ADD:
                plugin.Add(data)
            elif evt.GetId() == Id.TREE_DELETE:
                plugin.Delete(data)
        self.Bind(wx.EVT_MENU, OnMenu)


class UIList(wx.ListCtrl):

    def __init__(self, parent, style, size):
        wx.ListCtrl.__init__(self, parent, -1, style=style, size=size)

        self.InsertColumn(0, Text.attributeLbl)
        self.InsertColumn(1, Text.valueLabel)
        self.InsertColumn(2, Text.functionLbl)
        self.InsertColumn(3, Text.callTypeLbl)

        self.SetColumnWidth(0, Config.col0Size)
        self.SetColumnWidth(1, Config.col1Size)
        self.SetColumnWidth(2, Config.col2Size)
        self.SetColumnWidth(3, Config.col3Size)

    def Destroy(self):
        Config.listSize = self.GetSizeTuple()
        Config.col0Size = self.GetColumnWidth(0)
        Config.col1Size = self.GetColumnWidth(1)
        Config.col2Size = self.GetColumnWidth(2)
        Config.col3Size = self.GetColumnWidth(3)
        Config.listPosition = self.GetPosition()
        self.Hide()
        pass

    def Show(self, flag=True):
        flag = bool(flag)
        if not self.IsShown() and flag:
            pane = wx.aui.AuiPaneInfo().Name('globalmanagerlist'). \
                Bottom().MinSize((100, 100)).Floatable(True).Dockable(True). \
                MaximizeButton(True).Caption(' ' + Text.listTitle). \
                CloseButton(True).DestroyOnClose(True)# .\
            #     FloatingSize(Config.listSize).FloatingPosition(
            # Config.listPosition)
            wx.ListCtrl.Show(self, flag)
            eg.document.frame.auiManager.AddPane(self, pane)
            eg.document.frame.auiManager.Update()
        else:
            wx.ListCtrl.Show(self, flag)

    def DestroyUI(self):
        wx.ListCtrl.Destroy(self)

    def SetNewList(self, newData):
        self.DeleteAllItems()
        index = 0
        for data in newData:
            self.InsertStringItem(index, data[1])
            self.SetStringItem(index, 1, data[2])
            if len(data) > 3:
                self.SetStringItem(index, 2, data[3])
                self.SetStringItem(index, 3, data[4])
            else:
                self.SetStringItem(index, 2, 'NO DATA')
                self.SetStringItem(index, 3, 'NO DATA')
            index += 1
        self.Refresh()


class UITree(wx.TreeCtrl):

    def __init__(self, parent, style, size):
        wx.TreeCtrl.__init__(self, parent, -1, style=style, size=size)

    def Destroy(self):
        Config.treeSize = self.GetSizeTuple()
        Config.treePosition = self.GetPosition()
        self.Hide()
        pass

    def DestroyUI(self):
        wx.TreeCtrl.Destroy(self)

    def Show(self, flag=True):
        flag = bool(flag)
        if not self.IsShown() and flag:
            pane = wx.aui.AuiPaneInfo().Name('globalmanagertree'). \
                Bottom().MinSize((100, 100)).Floatable(True).Dockable(True). \
                MaximizeButton(True).Caption(' ' + Text.treeTitle). \
                CloseButton(True).DestroyOnClose(True)# .\
            #     FloatingSize(Config.treeSize).FloatingPosition(
            # Config.treePosition)
            wx.TreeCtrl.Show(self, flag)
            eg.document.frame.auiManager.AddPane(self, pane)
            eg.document.frame.auiManager.Update()

        else:
            wx.TreeCtrl.Show(self, flag)


class PyData(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def GetAttributeName(self):
        return self.key

    def GetAttributeRepr(self):
        return repr(self.value).split(' ')[1][1:-2]

    def GetAttributeData(self):
        return self.value


class UI:
    def __init__(self, plugin):
        self.plugin = plugin
        frame = eg.document.frame

        self.listData = []

        self.listCtrl = listCtrl = UIList(
            frame,
            style=wx.LC_REPORT,
            size=Config.listSize
        )
        self.treeCtrl = treeCtrl = UITree(
            frame,
            style=wx.TR_HAS_BUTTONS,
            size=Config.treeSize
        )

        treeCtrl.Hide()
        listCtrl.Hide()

        def SetListData(data):
            data = sorted(data)
            if data != self.listData:
                listCtrl.SetNewList(data)
                self.listData = data

        def IterGlobals(treeItem):
            childId, cookie = treeCtrl.GetFirstChild(treeItem)
            childNames = []
            treeItemData = treeCtrl.GetPyData(treeItem)
            attributeData = treeItemData.GetAttributeData()
            while childId.IsOk():
                childData = treeCtrl.GetPyData(childId)
                attributeName = childData.GetAttributeName()
                if not hasattr(attributeData, attributeName):
                    self.treeCtrl.DeleteChildren(childId)
                    self.treeCtrl.Delete(childId)
                else:
                    childNames.append(attributeName)
                    IterGlobals(childId)
                childId, cookie = treeCtrl.GetNextChild(childId, cookie)

            def IterData(tItem, pyData, cNames=[]):
                aRepr = pyData.GetAttributeRepr()
                aData = pyData.GetAttributeData()
                listData = []

                for key, value in aData:
                    aName = aRepr + '.' + key
                    newEntry = [aName, key, repr(value)]

                    if key in aData.callerLog:
                        newEntry.extend(aData.callerLog[key])
                    listData.append(newEntry)

                    if isinstance(value, VariableBase):
                        treeCtrl.SetItemHasChildren(tItem, True)
                        if key not in cNames:
                            data = PyData(key, value)
                            child = treeCtrl.AppendItem(
                                tItem,
                                key,
                                data=wx.TreeItemData(data)
                            )
                            cNames.append(key)
                            IterData(child, data)

                if cNames:
                    treeCtrl.SetItemHasChildren(tItem, True)
                else:
                    treeCtrl.SetItemHasChildren(tItem, False)
                if treeCtrl.IsSelected(tItem):
                    SetListData(listData)

            IterData(treeItem, treeItemData, childNames)

        root = treeCtrl.AddRoot(
            'eg.globals',
            data=wx.TreeItemData(PyData('globals', eg.globals))
        )
        treeCtrl.SelectItem(root)

        def ThreadCallback():
            IterGlobals(root)
            treeCtrl.Refresh()

        def OnTreectivated(evt):
            treeItem = treeCtrl.GetSelection()
            if treeItem:
                pyData = treeCtrl.GetItemPyData(treeItem)
                plugin.Add(pyData.GetAttributeRepr())

        def OnTreeMenu(evt):
            treeItem = treeCtrl.GetSelection()
            if treeItem:
                pyData = treeCtrl.GetItemPyData(treeItem)
                menu = TreeMenu(plugin, pyData.GetAttributeRepr())
                treeCtrl.PopupMenu(menu)

        def OnListMenu(evt):
            idx = listCtrl.HitTest(evt.GetPosition())[0]
            if idx != wx.NOT_FOUND:
                listCtrl.Select(idx)
                menu = ListMenu(plugin, self.listData[idx][0])
                listCtrl.PopupMenu(menu)

        def OnListActivated(evt):
            idx = listCtrl.HitTest(evt.GetPosition())[0]
            if idx != wx.NOT_FOUND:
                plugin.Value(self.listData[idx][0])

        treeCtrl.Bind(wx.EVT_TREE_ITEM_MENU, OnTreeMenu)
        treeCtrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, OnTreectivated)

        listCtrl.Bind(wx.EVT_RIGHT_UP, OnListMenu)
        listCtrl.Bind(wx.EVT_LEFT_DCLICK, OnListActivated)

        eg.document.frame.Bind(wx.EVT_CLOSE, self.OnClose)

        self.auiManager = eg.document.frame.auiManager
        self.updateThread = UIUpdateThread(ThreadCallback)

    def OnClose(self, evt):
        self.CloseUI()
        evt.Skip()

    @eg.LogIt
    def CloseUI(self):
        if self.updateThread is not None:
            self.updateThread.Stop()
            self.updateThread = None
            eg.document.frame.Unbind(wx.EVT_CLOSE, handler=self.OnClose)

        if self.treeCtrl is not None:
            self.auiManager.DetachPane(self.treeCtrl)
            self.auiManager.Update()
            self.treeCtrl.Destroy()
            self.treeCtrl.DestroyUI()
            self.treeCtrl = None

        if self.listCtrl is not None:
            self.auiManager.DetachPane(self.listCtrl)
            self.auiManager.Update()
            self.listCtrl.Destroy()
            self.listCtrl.DestroyUI()
            self.listCtrl = None

    def __getattr__(self, item):
        return getattr(self.plugin, item)









