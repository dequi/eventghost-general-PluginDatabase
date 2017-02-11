# -*- coding: utf-8 -*-
#
# Copyright (c) 2014, Walter Kraembring
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Walter Kraembring nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##############################################################################
# Revision history:
#
# 2015-04-13  Improved performance when editing report settings
# 2015-04-11  Added support for Fineoffset (temperature) and Oregon (humidity
#             and temperature) from ONH
# 2015-02-04  Added support for dewpoint data via normal events 
# 2015-02-02  Added support for light sensor via 1-wire 
# 2014-12-18  Added report combining multiple temperatures, humidities and rain
#             data selections. Separate reports for temperature & humidity have
#             been superseded by the combo report.
# 2014-12-10  Improved reports of temperature and humidity data (requires reset
#             of existing databases)
# 2014-12-08  Added support for Webserver with included websocket support 
# 2014-12-06  Rain data capture algorithm revised
# 2014-12-03  Added setting in actions for html report filename
# 2014-12-01  Generating html page for rain, temp, hum reports. With user
#             selectable range settings in 0-365 days and 0-24 hours
# 2014-10-16  Revised functions for temperature & humidity rule evaluations
# 2014-10-14  Supporting temperature, humidity and rule evaluation
# 2014-10-09  The first stumbling version supporting rain data
##############################################################################
##############################################################################
#
# Acknowledgements:
#
# Websocket Suite and Tornado plugins are Copyright (C)  2011-2014
# Pako (lubos.ruckl@quick.cz)
##############################################################################

eg.RegisterPlugin(
    name = "ClimateDataCalculation",
    guid = '{4CB0A57C-15ED-4F5B-8AFF-75F288785655}',
    author = "Walter Kraembring",
    version = "0.1.4",
    canMultiLoad = False,
    kind = "other",
    url = "http://eventghost.net/forum/viewtopic.php?f=9&t=6363",
    description = (
        '<p>Plugin to collect climate data from</p>'
        '<p> wireless sensors via a RFXtrx receiver and others</p>'
        '<center><img src="image.png" /></center>'
    ),
)

import eg
import sqlite3
import time
import datetime
import sys
import os
import CreateHtml
import CreateComboHtml
from threading import Event, Thread



class Text:
    port = "Port:"
    use_websockets = "Use Websocket Suite plugin for websockets " 
    use_tornadoWebsockets = "Use Tornado plugin for websockets "
    use_WebserverWebsockets = "Use Webserver plugin with included websockets support  "
    cHtml = "Generate html page to specified path and name"
    titleHtml = "Set the page title"
    headingHtml = "Set the report title"
    dbTableId = 'Give the table a name:'
    dbReportTableId = 'Select the table and the time to cover from history:'
    dbTableIdReset = 'Select the table to reset:'
    dbDevice = 'Set the correct device ID:'
    dbSensor = 'Set the correct sensor ID:'
    noData = 'No data found for selected date and time period'
    dateTimeFrom = 'Select the date & timestamp to start from:'
    dateTimeTo = 'Select the date & timestamp to end with:'
    nbrOfLastHours = 'Number of additional hours:'
    nbrOfLastDays = 'Number of days:'
    sInterval = 'Select the logging interval (minutes):'
    setPoint = 'Set the desired or target value (setpoint):'
    movAverage = 'Number of readings for the average calculation:'
    fMovAverage = 'Number of readings for the fast average calculation:'
    sMovAverage = 'Number of readings for the slow average calculation:'
    useHysteresis = 'Check to use hysteresis:'
    hysteresis = 'Select the hysteresis value:'
    useRule = 'Check to use a rule:'
    rule = 'Select the rule from the list:'
    
    

class ClimateDataCalculation(eg.PluginClass):
    text = Text
    
    def __init__(self):
        self.AddAction(CombinedReport)
        self.AddAction(RainReport)
        self.AddAction(RainRequestSearch)
        self.AddAction(RainRequestQuery)
        self.AddAction(RainDataCapture)
        self.AddAction(ResetRainData)
        self.AddAction(TempDataCapture)
        self.AddAction(ResetTempData)
        self.AddAction(HumDataCapture)
        self.AddAction(ResetHumData)
        self.AddAction(LightDataCapture)
        self.AddAction(ResetLightData)
        self.AddAction(DewPointDataCapture)
        self.AddAction(ResetDewPointData)

        self.rainData_db = 'rainData.db'
        self.tempData_db = 'tempData.db'
        self.humData_db = 'humData.db'
        self.lightData_db = 'lightData.db'
        self.dewPointData_db ='dewPointData_db'
        self.tablesRainData = []
        self.tablesTempData = []
        self.tablesHumData = []
        self.tablesLightData = []
        self.tablesDewPointData = []


    def __start__(self):
        # start the main thread (not doing anything for the moment)
        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()


    def __stop__(self):
        self.mainThreadEvent.set()


    def __close__(self):
        print "Plugin is closed."


    def main(self,mainThreadEvent): 
        self.tablesRainData = self.GetAllTableNames(self.rainData_db)
        self.tablesTempData = self.GetAllTableNames(self.tempData_db)
        self.tablesHumData = self.GetAllTableNames(self.humData_db)
        self.tablesLightData = self.GetAllTableNames(self.lightData_db)
        self.tablesDewPointData = self.GetAllTableNames(self.dewPointData_db)

        while not mainThreadEvent.isSet(): # Main Loop
            #remain = 61.0 - int(time.strftime("%S", time.localtime()))
            mainThreadEvent.wait(5.0)
        print "Main loop ended."


    def TornadoBroadcastMessage(self, msg):
        eg.plugins.Tornado.BroadcastMessage(
            msg.encode('utf-8'),
            True
        )

       
    def WebsocketSuiteBroadcastMessage(self, port, msg):
        eg.plugins.WebsocketSuite.BroadcastMessage(
            'All available interfaces',
            port,
            msg.encode('utf-8'),
            2
        )


    def WebserverBroadcastMessage(self, msg):
        eg.plugins.Webserver.BroadcastMessage(
            msg.encode('utf-8'),
            False
        )


    def GetAllTableNames(self, db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q = 'SELECT * FROM '+db.split('.')[0]
        try:
            c.execute(q)
            coll = c.fetchall()
            list = []
            for item in coll:
                name = item[2]
                if name not in list:
                    list.append(name)
            conn.close()
            return list
        except:
            conn.close()
            return None


    def CalculateMovAverage(self, dataSet, prm, endValue, r):
        res = 0
        cnt = 0
        for i in range(1, r):
            try:
                res += dataSet[-i][prm]
                cnt +=1
            except:
                pass
        res += endValue
        res = float(res/(cnt+1))
        return res


    def RuleEvaluator(
        self, 
        rule, 
        sMov, 
        setPoint, 
        lastCommand, 
        tableId, 
        hysteresis
    ):
        if rule == 'equal-less-greater':
            res = lastCommand
            if setPoint+hysteresis/2 < sMov:
                res = 'setPoint < MovAverage'
            if setPoint-hysteresis/2 > sMov:
                res = 'setPoint > MovAverage'
            if setPoint == sMov:
                res = 'setPoint == MovAverage'
            if res <> lastCommand:
                es = res
                pl = [res, setPoint, sMov]
                self.CreateEvent(es, pl, tableId)
            return res
            

    def CreateEvent(self, es, pl, tableId):             
        eg.TriggerEvent(
            tableId+'.'+es,
            payload = pl,
            prefix = 'ClimateDataCalculation'
        )


    def DelData(self, dbName, tableId):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        t = ((tableId),)
        c.execute('DELETE FROM '+dbName.split('.')[0]+' WHERE tableId=?', t)
        conn.commit()
        conn.close()


    def GetData(self, dbName, dbTableId, dateTimeFrom, dateTimeTo ):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        t = ((dbTableId),(dateTimeFrom),)
        u = ((dbTableId),(dateTimeTo),)
        v = ((dbTableId),(dateTimeFrom),(dateTimeTo),)
        try:
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=? AND date=?', t)
            start = c.fetchone()
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=? AND date=?', u)
            end = c.fetchone()
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=? AND date>=? AND date<=?', v)
            rows = c.fetchall()
            conn.close()
            return start, end, rows
        except:
            conn.close()
            return None, None, None

                
    def SearchData(
        self, 
        dbName, 
        dbTableId, 
        dateTimeFrom, 
        dateTimeTo 
    ):
        dbName = str(dbName)
        coll = self.GetAllData(dbName, dbTableId)
        s = coll[0]
        e = coll[-1]
        if len(coll) > 1:
            for item in coll:
                s_found = False
                if item[0].find(dateTimeFrom) != -1:
                    s = item
                    s_found = True
                if s_found:
                    break 
            for item in coll:
                e_found = False
                if item[0].find(dateTimeTo) != -1:
                    e = item
                    e_found = True
                if e_found:
                    break 
            return s, e

                
    def LastData(
        self, 
        dbName, 
        dbTableId, 
        dateTimeFrom
    ):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        v = ((dbTableId),(dateTimeFrom),)
        try:
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=? AND date>=?', v)
            rows = c.fetchall()
            conn.close()
            return rows
        except:
            conn.close()
            return None


    def GetAllData(
        self, 
        dbName, 
        dbTableId
    ):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        t = ((dbTableId),)
        try:
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=?', t)
            coll = c.fetchall()
            conn.close()
            return coll
        except:
            conn.close()
            return None


## Light level related ##############################################################
    def SaveLightData(
        self,
        tableId,
        lightlevel,
        sInterval,
        movAverage
    ):
        conn = sqlite3.connect(self.lightData_db)
        c = conn.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        s_epoch = int(round(time.time(),0))
        qs = 'CREATE TABLE IF NOT EXISTS '+self.lightData_db.split('.')[0]
        prm = ' (date text, s_epoch integer, tableId text, lightlevel real, sMov real)'
        c.execute(qs+prm) 
        t = ((tableId),)
        st =  "SELECT * FROM "+self.lightData_db.split('.')[0]+" WHERE tableId=?"        
        c.execute(st, t)
        coll = c.fetchall()
        res = ''
        dt = 0
        try:
            dt = coll[-1][1]
        except:
            pass
        if s_epoch > dt + sInterval*60-30:
            sMov = self.CalculateMovAverage(
                coll, 
                3, 
                lightlevel, 
                movAverage
            )
            sMov = float("%.2f" % sMov)
            lst = (date, s_epoch, tableId, lightlevel, sMov)
            ss = "INSERT INTO "+self.lightData_db.split('.')[0]+" VALUES (?,?,?,?,?)"
            c.execute(ss,lst)
            conn.commit()
        conn.close()
            
            
## Dewpoint related ##############################################################
    def SaveDewPointData(
        self,
        tableId,
        dewpoint
    ):
        conn = sqlite3.connect(self.dewPointData_db)
        c = conn.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        s_epoch = int(round(time.time(),0))
        qs = 'CREATE TABLE IF NOT EXISTS '+self.dewPointData_db.split('.')[0]
        prm = ' (date text, s_epoch integer, tableId text, dewpoint real)'
        c.execute(qs+prm) 
        t = ((tableId),)
        st =  "SELECT * FROM "+self.dewPointData_db.split('.')[0]+" WHERE tableId=?"        
        c.execute(st, t)
        coll = c.fetchall()
        res = ''
        dt = 0
        try:
            dt = coll[-1][1]
        except:
            pass
        if s_epoch > dt:
            lst = (date, s_epoch, tableId, dewpoint)
            ss = "INSERT INTO "+self.dewPointData_db.split('.')[0]+" VALUES (?,?,?,?)"
            c.execute(ss,lst)
            conn.commit()
        conn.close()


## Temperature related ##############################################################
    def SaveTempData(
        self,
        tableId,
        temperature,
        sInterval,
        setPoint,
        movAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        conn = sqlite3.connect(self.tempData_db)
        c = conn.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        s_epoch = int(round(time.time(),0))
        qs = 'CREATE TABLE IF NOT EXISTS '+self.tempData_db.split('.')[0]
        prm = ' (date text, s_epoch integer, tableId text, temperature real, lastcmd text, upperLimit real, lowerLimit real, sMov real)'
        c.execute(qs+prm) 
        t = ((tableId),)
        st =  "SELECT * FROM "+self.tempData_db.split('.')[0]+" WHERE tableId=?"        
        c.execute(st, t)
        coll = c.fetchall()
        res = ''
        dt = 0
        lastCmd = ''
        try:
            dt = coll[-1][1]
        except:
            pass
        try:
            lastCmd = coll[-1][4]
        except:
            pass
        if s_epoch > dt + sInterval*60-30:
            sMov = self.CalculateMovAverage(
                coll, 
                3, 
                temperature, 
                movAverage
            )
            sMov = float("%.2f" % sMov)
            if not useHysteresis:
                hysteresis = 0.0
            if useRule:
                res = self.RuleEvaluator(
                    rule, 
                    sMov, 
                    setPoint, 
                    lastCmd, 
                    tableId, 
                    hysteresis
                )
            uLimit = setPoint + hysteresis/2
            lLimit = setPoint - hysteresis/2
            lst = (date, s_epoch, tableId, temperature, res, uLimit, lLimit, sMov)
            ss = "INSERT INTO "+self.tempData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?,?)"
            c.execute(ss,lst)
            conn.commit()
        conn.close()
            
            
## Humidity related ##############################################################
    def SaveHumData(
        self,
        tableId,
        humidity,
        sInterval,
        setPoint,
        movAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        conn = sqlite3.connect(self.humData_db)
        c = conn.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        s_epoch = int(round(time.time(),0))
        qs = 'CREATE TABLE IF NOT EXISTS '+self.humData_db.split('.')[0]
        prm = ' (date text, s_epoch integer, tableId text, humidity integer, lastcmd text, upperLimit integer, lowerLimit integer, sMov integer)'
        c.execute(qs+prm) 
        t = ((tableId),)
        st =  "SELECT * FROM "+self.humData_db.split('.')[0]+" WHERE tableId=?"        
        c.execute(st, t)
        coll = c.fetchall()
        res = ''
        dt = 0
        lastCmd = ''
        try:
            dt = coll[-1][1]
        except:
            pass
        try:
            lastCmd = coll[-1][4]
        except:
            pass
        if s_epoch > dt + sInterval*60-30:
            sMov = self.CalculateMovAverage(
                coll, 
                3, 
                humidity, 
                movAverage
            )
            sMov = int(sMov)
            if not useHysteresis:
                hysteresis = 0
            if useRule:
                res = self.RuleEvaluator(
                    rule, 
                    sMov, 
                    setPoint, 
                    lastCmd, 
                    tableId, 
                    hysteresis
                )
            uLimit = setPoint + int(hysteresis/2)
            lLimit = setPoint - int(hysteresis/2)
            lst = (date, s_epoch, tableId, humidity, res, uLimit, lLimit, sMov)
            ss = "INSERT INTO "+self.humData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?,?)"
            c.execute(ss,lst)
            conn.commit()
        conn.close()


## Rain related ##############################################################
    def CalculateRainMovAverage(
        self, 
        dataSet, 
        prm, 
        endValue, 
        r
    ):
        res = 0
        cnt = 0
        for i in range(1, r):
            try:
                res += (dataSet[-i][prm]-dataSet[-(i+1)][prm])
                cnt +=1
                if cnt == 1:
                    endValue = endValue - dataSet[-i][prm]
            except:
                pass
        res += endValue
        res = float(res/(cnt+1))
        return res


    def RuleEvaluatorRain(
        self, 
        rule, 
        fMov,
        sMov, 
        lastCommand, 
        tableId, 
        hysteresis
    ):
        if rule == 'equal-less-greater':
            res = lastCommand
            if fMov+hysteresis/2 < sMov:
                res = 'fMovAverage < sMovAverage'
            if fMov-hysteresis/2 > sMov:
                res = 'fMovAverage > sMovAverage'
            if fMov == sMov:
                res = 'fMovAverage == sMovAverage'
            if res <> lastCommand:
                es = res
                pl = [res, fMov, sMov]
                self.CreateEvent(es, pl, tableId)
            return res


    def SaveRainData(
        self,
        tableId,
        rainRate,
        rainTotal,
        delta,
        sInterval,
        fMovAverage,
        sMovAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        conn = sqlite3.connect(self.rainData_db)
        c = conn.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        s_epoch = int(round(time.time(),0))
        qs = 'CREATE TABLE IF NOT EXISTS '+self.rainData_db.split('.')[0]
        prm = ' (date text, s_epoch integer, tableId text, rate_value integer, total_value integer, delta integer, lastcmd text)'
        c.execute(qs+prm)
        t = ((tableId),)
        st =  "SELECT * FROM "+self.rainData_db.split('.')[0]+" WHERE tableId=?"        
        c.execute(st, t)
        coll = c.fetchall()
        res = ''
        dt = 0
        lastCmd = ''
        rw = 0
        delta = 0
        prev_delta = 0
        try:
            dt = coll[-1][1]
        except:
            pass
        try:
            lastCmd = coll[-1][6]
        except:
            pass
        try:
            rw = coll[-1][4]
        except:
            pass
        try:
            prev_delta = coll[-1][5]
        except:
            pass

        if (
            s_epoch > dt + sInterval*60-30
            and
            (rainTotal < prev_delta + 100 or len(coll) == 0)
        ):
            delta = rainTotal #Save reading for next round comparison
            if rainTotal < rw: #Gauge has been resetted since start
                if rainTotal >= prev_delta:
                    rainTotal = rw + rainTotal - prev_delta   
                if rainTotal < prev_delta: #Gauge reset detected (battery change?)
                    rainTotal = rw + rainTotal   
            if useRule:
                fMov = self.CalculateRainMovAverage(
                    coll,
                    4,
                    rainTotal,
                    fMovAverage
                )
                fMov = int(fMov)
                sMov = self.CalculateRainMovAverage(
                    coll, 
                    4, 
                    rainTotal, 
                    sMovAverage
                )
                sMov = int(sMov)
                if not useHysteresis:
                    hysteresis = 0
                res = self.RuleEvaluatorRain(
                    rule, 
                    fMov, 
                    sMov, 
                    lastCmd, 
                    tableId, 
                    hysteresis
                )
            lst = (date, s_epoch, tableId, rainRate, rainTotal, delta, res)
            ss = "INSERT INTO "+self.rainData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?)"
            c.execute(ss,lst)
            conn.commit()
        conn.close()

             
            
## Actions ###################################################################
## Rain related actions ######################################################
class RainDataCapture(eg.ActionClass):
                
    def __call__(
        self,
        dbTableId = 'RainSensor on roof',
        deviceCode = '1796',
        sInterval = 10,
        fMovAverage = 5,
        sMovAverage = 15,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):
        tst = ''
        addr = ''
        delta = 0
        rainRate = 0
        rainTotal = 0
        newEvent = eg.event.suffix
        newPayload = eg.event.payload
        base = newEvent.split(':')
        addr = base[2].strip(' ')
        if( addr == deviceCode):
            e_lst = []
            tst = str(newPayload)
            e_lst = tst.split(':')
            print e_lst
            rainRate = int(e_lst[1].split(' ')[1])
            rainTotal = int(e_lst[2].split(' ')[1])
            self.plugin.SaveRainData(
                dbTableId,
                rainRate,
                rainTotal,
                delta,
                sInterval,
                fMovAverage,
                sMovAverage,
                useHysteresis,
                hysteresis,
                useRule,
                rule
            )

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'RainSensor on roof',
        deviceCode = '46592',
        sInterval = 10,
        fMovAverage = 5,
        sMovAverage = 15,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        fMovAverageCtrl = panel.SpinIntCtrl(fMovAverage, 1, 120)
        fMovAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.fMovAverage),
            (7,0)
        )

        sMovAverageCtrl = panel.SpinIntCtrl(sMovAverage, 1, 120)
        sMovAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sMovAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinIntCtrl(hysteresis, 0, 120)
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )

        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(strings=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )
 
        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(fMovAverageCtrl, (8,0))
        mySizer_2.Add(sMovAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                fMovAverageCtrl.GetValue(),
                sMovAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetRainData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        self.plugin.DelData(
            self.plugin.rainData_db, 
            dbTableId
        )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'RainSensor on roof'
    ):
        list = self.plugin.tablesRainData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )

                

class RainRequestQuery(eg.ActionClass):

    def __call__(
        self, 
        dbTableId = 'RainSensor on roof',
        dateTimeFrom = '2001-01-01 00:00:01',
        dateTimeTo = '2001-12-31 23:59:59',
    ):
        start, end = self.plugin.SearchData(
            self.plugin.rainData_db,
            dbTableId, 
            dateTimeFrom, 
            dateTimeTo
        )
        if start <> None and end <> None:
            return (end[4] - start[4])
        else:
            return 0



class RainRequestSearch(eg.ActionClass):

    def __call__(
        self, 
        dbTableId = 'RainSensor on roof',
        tornado = False,
        websocketsuite = False,
        port = 1235,
        bWebSServer = False
    ):
        pl = eg.event.payload
        dateTimeFrom = 'start'
        dateTimeTo = 'end'
        if len(pl)==1:       
            dateTimeFrom = pl[0]
            if dateTimeFrom == '':
                dateTimeFrom = 'start'
        if len(pl)==2:       
            dateTimeTo = pl[1]
            if dateTimeTo == '':
                dateTimeTo = 'end'
        start, end = self.plugin.SearchData(
            self.plugin.rainData_db,
            dbTableId, 
            dateTimeFrom, 
            dateTimeTo
        )
        if start <> None and end <> None:
            msg = 'Rain from '+start[0]+' until '+end[0]
            msg = msg + ' : ' + str((end[4] - start[4]))
            print msg
            if tornado:
                self.plugin.TornadoBroadcastMessage(msg)
            if websocketsuite:
                self.plugin.WebsocketSuiteBroadcastMessage(str(port), msg)
            if bWebSServer:
                self.plugin.WebserverBroadcastMessage(msg)
        else:
            print self.plugin.text.noData


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'RainSensor on roof',
        tornado = False,
        websocketsuite = False,
        port = 1235,
        bWebSServer = False
    ):
        list = self.plugin.tablesRainData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)
        
        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bWebSServerCtrl = wx.CheckBox(panel, -1, "")
        bWebSServerCtrl.SetValue(bWebSServer)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.use_WebserverWebsockets
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(bWebSServerCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bTornadoWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bTornadoWebSocketCtrl.SetValue(tornado)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.use_tornadoWebsockets
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(bTornadoWebSocketCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bWebSocketCtrl.SetValue(websocketsuite)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.use_websockets)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(bWebSocketCtrl, 1, wx.EXPAND)
        
        portCtrl = panel.SpinIntCtrl(port, 1234, 1500)
        portCtrl.SetInitialSize((30,-1))
        sizer5.Add(portCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection(),
                bTornadoWebSocketCtrl.GetValue(),
                bWebSocketCtrl.GetValue(),
                portCtrl.GetValue(),
                bWebSServerCtrl.GetValue()
            )


                
## Temperature related actions ###############################################
class TempDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Temperature ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 15.0,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 2.0,
        useRule = False,
        rule = ''
    ):
        tst = ''
        addr = ''
        temperature = 0.0
        newEvent = eg.event.suffix
        newPayload = eg.event.payload

        if eg.event.prefix == 'TellStickDuo':
            base = newEvent.split('.')
            addr = base[2]
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split('|')
                temperature = float("%.2f" % float(e_lst[0]))

        if eg.event.prefix == 'RFXtrx':
            base = newEvent.split(':')
            addr = base[2].strip(' ')
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split(':')
                temperature = float("%.2f" % float(e_lst[1].split(' ')[1]))

        if eg.event.suffix.find('FineOffset|')!= -1: #For NHS
            addr = str(eg.event.suffix.split('|')[1])
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split('|')
                temperature = float("%.2f" % float(e_lst[1]))

        if eg.event.suffix.find('Oregon|')!= -1: #For NHS
            addr = str(eg.event.suffix.split('|')[1])
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split('|')
                temperature = float("%.2f" % float(e_lst[1]))

        if addr <> '':
            self.plugin.SaveTempData(
                dbTableId,
                temperature,
                sInterval,
                setPoint,
                movAverage,
                useHysteresis,
                hysteresis,
                useRule,
                rule
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'Temperature ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 15.0,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 2.0,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        setPointCtrl = panel.SpinNumCtrl(
            setPoint,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = -99.9,
            max = 99.9,
            increment = 0.1
        )
        setPointCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.setPoint),
            (7,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinNumCtrl(
            hysteresis,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = 0.0,
            max = 40.0,
            increment = 0.1
        )
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )
        
        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(strings=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )
 
        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(setPointCtrl, (8,0))
        mySizer_2.Add(movAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                setPointCtrl.GetValue(),
                movAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetTempData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        self.plugin.DelData(
            self.plugin.tempData_db, 
            dbTableId
        )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Temperature ground'
    ):
        list = self.plugin.tablesTempData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Humidity related actions ###############################################
class HumDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Humidity ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 70,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):
        tst = ''
        addr = ''
        humidity = 0
        newEvent = eg.event.suffix
        newPayload = eg.event.payload

        if eg.event.prefix == 'TellStickDuo':
            base = newEvent.split('.')
            addr = base[2]
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split('|')
                humidity = int(e_lst[1])

        if eg.event.prefix == 'RFXtrx':
            base = newEvent.split(':')
            addr = base[2].strip(' ')
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split(':')
                humidity = int(e_lst[2].split(' ')[1])

        if eg.event.suffix.find('Oregon|')!= -1: #For NHS
            addr = str(eg.event.suffix.split('|')[1])
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split('|')
                humidity = int(e_lst[3])

        if addr <> '':
            self.plugin.SaveHumData(
                dbTableId,
                humidity,
                sInterval,
                setPoint,
                movAverage,
                useHysteresis,
                hysteresis,
                useRule,
                rule
            )

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'Humidity ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 70,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        setPointCtrl = panel.SpinIntCtrl(setPoint, 1, 100)
        setPointCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.setPoint),
            (7,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinIntCtrl(hysteresis, 0, 40)
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )

        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(strings=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )
 
        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(setPointCtrl, (8,0))
        mySizer_2.Add(movAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                setPointCtrl.GetValue(),
                movAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetHumData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        self.plugin.DelData(
            self.plugin.humData_db, 
            dbTableId
        )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Humidity ground'
    ):
        list = self.plugin.tablesHumData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Light level related actions ###############################################
class LightDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Light level roof',
        sensorId = '20.09F40C000000/volt.B',
        sInterval = 10,
        movAverage = 5
    ):
        tst = ''
        addr = ''
        lightlevel = 0
        newEvent = eg.event.suffix
        newPayload = eg.event.payload
        
        if eg.event.suffix == '/1wire':
            dic = eval(eg.event.payload)
            addr = dic['sensorId']
            if( addr == sensorId):
                lightlevel = dic['lightlevel']
                lightlevel = float("%.2f" % float(lightlevel))

        if addr <> '':
            self.plugin.SaveLightData(
                dbTableId,
                lightlevel,
                sInterval,
                movAverage
            )

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'Light level roof',
        sensorId = '20.09F40C000000/volt.B',
        sInterval = 10,
        movAverage = 5
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        sensorIdCtrl = wx.TextCtrl(panel, -1, sensorId)
        sensorIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbSensor),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (7,0)
        )

        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(sensorIdCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(movAverageCtrl, (8,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                sensorIdCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                movAverageCtrl.GetValue()
            )



class ResetLightData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        self.plugin.DelData(
            self.plugin.lightData_db, 
            dbTableId
        )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Light level roof'
    ):
        list = self.plugin.tablesLightData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Dewpoint related actions ###############################################
class DewPointDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Dewpoint attic',
        sensorId = 'Difference to dew point in Attic'
    ):
        dewpoint = 0.0
        if eg.event.suffix.find(sensorId) > 0:
            lst = eg.event.payload.split(' ')
            dewpoint = float("%.1f" % float(lst[1]))
            self.plugin.SaveDewPointData(
                dbTableId,
                dewpoint
            )

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Dewpoint attic',
        sensorId = 'Difference to dew point in Attic'
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        sensorIdCtrl = wx.TextCtrl(panel, -1, sensorId)
        sensorIdCtrl.SetInitialSize((250,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbSensor),
            (3,0)
        )

        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(sensorIdCtrl, (4,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                sensorIdCtrl.GetValue()
            )



class ResetDewPointData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        self.plugin.DelData(
            self.plugin.dewPointData_db, 
            dbTableId
        )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Dewpoint attic'
    ):
        list = self.plugin.tablesDewPointData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Report section ############################################################
class CombinedReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        dbTableId_1 = ['Temperature ground'],
        dbTableId_2 = ['Humidity ground'],
        dbTableId_3 = ['RainSensor on roof'],
        dbTableId_4 = ['Light level roof'],
        dbTableId_5 = ['Dewpoint attic'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        rprtName = '',
        rprtHeading = ''
    ):
        reload(CreateComboHtml)

        hrs_back = nbrOfLastDays*24 + nbrOfLastHours
        now = datetime.datetime.now()
        dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
        delta = datetime.timedelta(hours = -hrs_back)
        dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")

        rows_1 = {}
        rows_2 = {}
        rows_3 = {}
        rows_4 = {}
        rows_5 = {}
        
        for item in dbTableId_1:
            rows = self.plugin.LastData(
                self.plugin.tempData_db, 
                item, 
                dateTimeFrom
            )
            rows_1[item]=rows

        for item in dbTableId_2:
            rows = self.plugin.LastData(
                self.plugin.humData_db, 
                item, 
                dateTimeFrom
            )
            rows_2[item]=rows

        for item in dbTableId_3:
            rows = self.plugin.LastData(
                self.plugin.rainData_db, 
                item, 
                dateTimeFrom
            )
            rows_3[item]=rows
        
        for item in dbTableId_4:
            rows = self.plugin.LastData(
                self.plugin.lightData_db, 
                item, 
                dateTimeFrom
            )
            rows_4[item]=rows

        for item in dbTableId_5:
            rows = self.plugin.LastData(
                self.plugin.dewPointData_db, 
                item, 
                dateTimeFrom
            )
            rows_5[item]=rows

        CreateComboHtml.CreateComboHtml(
            rprtName, 
            "Comboreport", 
            fPath, 
            rows_1, 
            "['Column1', 'Temperature', { role: 'style' }]", 
            3,
            rows_2, 
            "['Column1', 'Humidity', { role: 'style' }]", 
            3,
            rows_3, 
            "['Time', 'Rain level', { role: 'style' } ]", 
            4,
            rows_4, 
            "['Time', 'Light level', { role: 'style' } ]", 
            4,
            rows_5, 
            "['Time', 'Dewpoint delta', { role: 'style' } ]", 
            3,
            rprtTitle,
            rprtHeading
         )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Combo Report',
        dbTableId_1 = [''],
        dbTableId_2 = [''],
        dbTableId_3 = [''],
        dbTableId_4 = [''],
        dbTableId_5 = [''],
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        rprtName = 'Filename',
        rprtHeading = 'EventGhost Climate Data Report Graph'
        ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_1 = self.plugin.tablesTempData
        if list_1 <> None:
            pass
        else:
            list_1 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        lbox11 = wx.ListBox(panel, 100, wx.DefaultPosition, wx.DefaultSize,
                        list_1, wx.LB_MULTIPLE)
        for item in dbTableId_1:
            if item in list_1:
                idx = list_1.index(item)
                lbox11.SetSelection(idx)    
        sizer11.Add(lbox11, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer11, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        list_2 = self.plugin.tablesHumData
        if list_2 <> None:
            pass
        else:
            list_2 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer12 = wx.BoxSizer(wx.HORIZONTAL)
        lbox12 = wx.ListBox(panel, 100, wx.DefaultPosition, wx.DefaultSize,
                        list_2, wx.LB_MULTIPLE)
        for item in dbTableId_2:
            if item in list_2:
                idx = list_2.index(item)
                lbox12.SetSelection(idx)    
        sizer12.Add(lbox12, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer12, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        list_3 = self.plugin.tablesRainData
        if list_3 <> None:
            pass
        else:
            list_3 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer13 = wx.BoxSizer(wx.HORIZONTAL)
        lbox13 = wx.ListBox(panel, 100, wx.DefaultPosition, wx.DefaultSize,
                        list_3, wx.LB_MULTIPLE)
        for item in dbTableId_3:
            if item in list_3:
                idx = list_3.index(item)
                lbox13.SetSelection(idx)    
        sizer13.Add(lbox13, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer13, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        list_4 = self.plugin.tablesLightData
        if list_4 <> None:
            pass
        else:
            list_4 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer14 = wx.BoxSizer(wx.HORIZONTAL)
        lbox14 = wx.ListBox(panel, 100, wx.DefaultPosition, wx.DefaultSize,
                        list_4, wx.LB_MULTIPLE)
        for item in dbTableId_4:
            if item in list_4:
                idx = list_4.index(item)
                lbox14.SetSelection(idx)    
        sizer14.Add(lbox14, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer14, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        list_5 = self.plugin.tablesDewPointData
        if list_5 <> None:
            pass
        else:
            list_5 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer15 = wx.BoxSizer(wx.HORIZONTAL)
        lbox15 = wx.ListBox(panel, 100, wx.DefaultPosition, wx.DefaultSize,
                        list_5, wx.LB_MULTIPLE)
        for item in dbTableId_5:
            if item in list_5:
                idx = list_5.index(item)
                lbox15.SetSelection(idx)    
        sizer15.Add(lbox15, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer15, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)

        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId_1 = GetSel(lbox11.GetSelections(),list_1)
            dbTableId_2 = GetSel(lbox12.GetSelections(),list_2)
            dbTableId_3 = GetSel(lbox13.GetSelections(),list_3)
            dbTableId_4 = GetSel(lbox14.GetSelections(),list_4)
            dbTableId_5 = GetSel(lbox15.GetSelections(),list_5)

            panel.SetResult(
                titleCtrl.GetValue(),
                dbTableId_1,
                dbTableId_2,
                dbTableId_3,
                dbTableId_4,
                dbTableId_5,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue()
            )



class RainReport(eg.ActionClass):

    def __call__(
        self, 
        dbTableId = 'RainSensor on roof',
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        rprtName = ''
    ):
        hrs_back = nbrOfLastDays*24 + nbrOfLastHours
        now = datetime.datetime.now()
        dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
        delta = datetime.timedelta(hours = -hrs_back)
        dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")
        rows = self.plugin.LastData(
            self.plugin.rainData_db,
            dbTableId, 
            dateTimeFrom
        )
        if len(rows) > 0:
            msg = (
                'Creating html page covering the range from '+
                rows[0][0]+
                ' until '+
                rows[-1][0]
            )
            print msg
            CreateHtml.CreateHtml(
                rprtName, 
                "Rain", 
                fPath, 
                rows, 
                "['Time', 'Rain level', { role: 'style' } ]", 
                4
            )
        else:
            print self.plugin.text.noData


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'RainSensor on roof',
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = eg.mainDir+'\Log',
        rprtName = 'Filename'
    ):
        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        list = self.plugin.tablesRainData
        if list <> None:
            pass
        else:
            list = ['Empty']
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(strings=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((250,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():

            panel.SetResult(
                dbTableIdCtrl.GetStringSelection(),
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                nameCtrl.GetValue()
            )







