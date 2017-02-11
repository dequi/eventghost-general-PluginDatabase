# -*- coding: utf-8 -*-
#
# plugins/NetHomeServer/__init__.py
#
# Copyright (C) 2009
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2015-03-03  Separating connection problems at start up from those happening
#             when connection is established
#             Time out for lost sensors now configurable (100-7200 seconds)
# 2015-02-13  Monitoring of disconnection/connection of controllers added
# 2015-02-08  Added support for sending commands to control lamps defined in 
#             OpenNetHome. Currently only 'lamps' category is supported. 
# 2015-02-06  Added support for Oregon Temp/Hum sensors and FineOffset Temp
#             sensors
# 2013-12-15  Improved decoding to capture only completed messages
# 2013-10-03  Filtering out false events with house code 0 (zero)
# 2012-09-02  Commented out a number of print statements (info can be found
#             in the log files)
# 2011-09-19  New location for logfiles: eg.configDir/plugins/NetHomeServer
# 2011-12-14  Fixed to work with -translate switch
# 2010-11-13  Improved the event filtering
# 2010-11-09  Added action to trig the alarm buzzer in a NEXA Smoke Detector
# 2010-11-09  Modified the format to support NEXA Smoke Detector events
# 2010-11-09  Added repeat functions to pronto commands
# 2010-05-02  Changed from telnet to socket connections
# 2010-04-20  Improved event control & reconnection of lost telnet session
#             Improved event data capturing & evaluation
# 2010-03-23  Uses eg.PersistentData to save persistent data instead of pickle
#             Automatic migration of old weather data during startup
# 2010-02-07  Changed to support NetHomeManager new UPM message format
#             Fixed a bug in message repeat control function
# 2010-01-19  Rain and wind calculation/recording added
# 2010-01-09  Added rain average calculation
# 2010-01-08  Early bug fixing  in the Rain gauges support
# 2010-01-07  Added support for UPM Wind and Rain gauges
# 2010-01-04  Added action to send pronto code to NetHomeServer
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-05  First published version
# 2009-11-19  Improved control of received data 
# 2009-10-27  Small modification of the logging function
# 2009-10-17  The first alpha version
##############################################################################

eg.RegisterPlugin(
    name = "NetHomeServer",
    guid = '{7B2DF95B-DC3E-4D56-9785-0E13365C568F}',
    author = "Walter Kraembring",
    version = "1.1.7b4",
    canMultiLoad = False,
    kind = "other",
    url = "http://wiki.nethome.nu/doku.php/start",
    description = (
        '<p>Plugin to receive messages from and send commands to OpenNetHomeServer</p>'
        '\n\n<p><a href="http://opennethome.org/">Product details...</a></p>'
        '<center><img src="nethomeserver.png" /></center>'
    ),
)

import socket
import httplib
import time
import os
import sys
import winsound
import calendar
import random
from datetime import datetime, timedelta
from threading import Event, Thread



class Text:
    started = "Plugin started"
    listhl = "Currently active threads:"
    hostName = "Host name or ip:"
    portNumber = "Port number:"
    socketTimeOut = "Time Out for socket connection (seconds):"
    windSpeed = "Check if windspeed shall be presented in m/s:"
    colLabels = (
        "Action Name",
        "    ",
        "    "
    )
    subscribe = "Request to Subscribe: "
    connection_etablished = "Connection with NetHomeServer TCP interface established"
    connection_error = "Connection error: "
    rest_connection_error = "Connection with NetHomeServer REST interface failed"
    tcp_connection_error = "Connection with NetHomeServer TCP interface failed"
    tcp_connection_at_start = 'Failed to connect to NetHomeServer at startup'
    tcp_EOFError_error = "EOFError in connection with NetHomeServer"
    unsubscribe = "Request to Unsubscribe: "
    cleanUpmonitoring = "Cleaning up monitoring tasks..."
    readyStopped = "Plugin successfully stopped"
    ka_threadStopped = "Keep Alive thread ended"    
    read_error = "Read error: "
    txt_signal_back = "Recovered contact with sensor"
    txt_taskObj = "Lost contact with sensor"

    
    #Buttons
    b_abort = "Abort"
    b_abortAll = "Abort all"
    b_restartAll = "Restart All"
    b_refresh = "Refresh"

    #Threads
    n_loggerThread = "loggerThread"
    thr_abort = "Thread is terminating: "
    txt_ReadingData = "Reading weather data from file..."
    txt_WritingData = "Writing weather data to file..."

    class loggerAction:
        name = "Start new or control a running logger"
        description = (
            "Allows starting, stopping or resetting loggers, which "+
            "monitors events from NetHomeServer"
        )
        loggerName = "Logger name:"
        soundOnEvent = "Beep on events:"
        repeats = "Allow repeated events:"
        delay = "Delay of repeats:"
        delay_u = " s (seconds)"
        labelStart = ' "%s"'
        logToFile = "Log events to file:"
        debug = "Turn debug ON:"
        txtBattLow = "Battery low"
        lostSensors = "Set time out for lost sensors (sec)"

    class prontoCmd:
        deviceName = (
            "This is a device that can be controlled via NetHomeServer "+
            "using pronto codes"
        )
        pronto = "Paste the pronto code to be transmitted for this action"
        txtNbrBursts = "Number of events per control(1-10 bursts)"
        txtCmdDelay = "Delay between the events(0.5-5.0 s)"

    class smokeDetCmd:
        deviceName = (
            "This command can be used to start the buzzer in a NEXA smoke "+
            "detector device that is controlled by NetHomeServer "
        )
        address = "Paste/type the address of the smoke detector "

    class SendCommand:
        textRestPort = "Select the REST port in OpenNetHome"
        textBoxName = "Enter a descriptive name for the action"
        textBoxObj = "Select the object to be controlled"
        textBoxAttribute = "Select the command to send"
        rest_connection_error = "Connection with NetHomeServer REST interface failed"
   


class loggerThread(Thread):
    text = Text

    def __init__(
        self,
        name,
        hostName,
        lostSensors,
        bSound,
        bRepeats,
        delayRepeat,
        bLogToFile,
        bDebug,
        bSpeed_ms,
        plugin
    ):
        Thread.__init__(self, name=self.text.n_loggerThread)
        self.name = name
        self.hostName = hostName
        self.lostSensors = lostSensors
        self.bSound = bSound
        self.bRepeats = bRepeats
        self.delayRepeat = delayRepeat
        self.bLogToFile = bLogToFile
        self.bDebug = bDebug
        self.bSpeed_ms = bSpeed_ms
        self.finished = Event()
        self.abort = False
        self.bTaskAdded = False
        self.plugin = plugin
        self.wDirection = [
            'N',
            'NNE',
            'NE',
            'ENE',
            'E',
            'ESE',
            'SE',
            'SSE',
            'S',
            'SSW',
            'SW',
            'WSW',
            'W',
            'WNW',
            'NW',
            'NNW'
        ]

   
    def run(self):
        self.rain_levels = [0.0, 0.0]
        self.rain_Hour = [0.0]*4
        self.rain_Hour_previous = 0.0
        self.rain_Today = [0.0, 0.0]
        self.rain_Yesterday = 0.0
        self.rain_Week_levels = [0.0]*7
        self.rain_Week_dates = ['']*7
        self.rain_Week_sum = 0.0
        self.bNewDay = False
        self.wj = 0
        self.wi = 0
        self.wdLevels_15 = []
        self.wdLevels_60 = []
        self.wdLabel = ""
        self.wdLabelPrevious = "Unknown"
        self.old_lst = []
        taskObj = None
        iRainSim = 0
        bSimulate = False
#        bSimulate = True

        try:
            self.rain_Week_levels = WeatherData.rain_Week_levels[self.name]
            self.rain_Week_dates = WeatherData.rain_Week_dates[self.name]
        except:
            pass

        while (self.abort == False):
            self.finished.wait(0.05)
            lst = []
            iPronto = 0
            
            if self.abort:
                self.finished.wait(1)
                break
            
            if self.plugin.event_NHS != "":
                lst = self.plugin.event_NHS.split(',')
                self.plugin.event_NHS = ""
                
                if (
                    lst.count('UPM.HouseCode') > 0
                    and lst.count('UPM.SequenceNumber') > 0
                ):
                    #print lst
                    lst = lst[:15]

                try:
                    iPronto = lst.index('Pronto.Message')
                except ValueError:
                    iPronto = -1 # no match

            if lst.count("NetHomeServer") > 0:
                if not self.bTaskAdded or lst != self.old_lst:
                    self.old_lst = lst
                    try:
                        eg.scheduler.CancelTask(taskObj)
                        self.bTaskAdded = False
                    except ValueError:
                        pass
    
                    # Code used for UPM/ESIC Rain and Wind gauge simulation ####                
                    if bSimulate:
                        iRainSim += 1
        
                        if iRainSim%2==0:
                            lst = [
                                'NetHomeServer',
                                'event',
                                'UPM_Message',
                                'Direction',
                                'In',
                                'UPM.DeviceCode',
                                '3',
                                'UPM.HouseCode',
                                '10',
                                'UPM.Humidity',
                                '0',
                                'UPM.LowBattery',
                                '0',
                                'UPM.Temp',
                                '0'
                            ]
                            lst[14] = iRainSim
                        else:
                            lst = [
                                'NetHomeServer',
                                'event',
                                'UPM_Message',
                                'Direction',
                                'In',
                                'UPM.DeviceCode',
                                '2',
                                'UPM.HouseCode',
                                '10',
                                'UPM.Humidity',
                                '0',
                                'UPM.LowBattery',
                                '0',
                                'UPM.Temp',
                                '0'
                            ]
                            twd = random.randrange(0,30,2)
                            tws = random.random()* 9.0
                            lst[14] = tws
                            lst[10] = twd
                    #####################################
    
                    if len(lst) > 5 or iPronto > 0:
                        s_lst = ""
                        
                        for X in range (4,len(lst)):
                            s_lst += str(lst[X])
                            if X < len(lst):
                                s_lst += "|"
                       
                        if (
                            s_lst.find('Pronto.Message') > 0
                            or(
                                s_lst.find('NexaFire.Address') > 0
                            )
                            or(
                                s_lst.find('NexaL.Address') > 0
                                and s_lst.find('NexaL.Button') > 0
                                and s_lst.find('NexaL.Command') > 0
                            )
                            or(
                                s_lst.find('Nexa.Button') > 0
                                and s_lst.find('Nexa.Command') > 0
                                and s_lst.find('Nexa.HouseCode') > 0
                            )
                        ):
                            eg.TriggerEvent(s_lst, prefix = self.name)

                        if(s_lst.count("UPM_Message") > 0):
                            upmMsg = s_lst.split('|')
                            self.UpmMessage(upmMsg)
                        
                        if(s_lst.count("Oregon.Channel") > 0):
                            oregonMsg = s_lst.split('|')
                            self.OregonMessage(oregonMsg)
                        
                        if(s_lst.count("FineOffset.Identity") > 0):
                            fineOffsetMsg = s_lst.split('|')
                            self.FineOffsetMessage(fineOffsetMsg)
   
                        if self.bLogToFile:
                            self.LogToFile(
                                self.name
                                +"|"
                                +str(lst)
                            )
    
                        if self.bDebug:
                            self.debugLogToFile(
                                self.name
                                +"|"
                                +str(lst)
                            )
    
                        if self.bSound:                        
                            winsound.Beep(1000, 200)                
    
                        if self.bRepeats:
                            if not self.bTaskAdded:
                                taskObj = eg.scheduler.AddTask(
                                    self.delayRepeat,
                                    self.ClearBuffer
                                )
                                self.bTaskAdded = True
                        else:
                            self.bTaskAdded = True


    def FineOffsetMessage(self, fineOffsetMsg):
        try:
            fineOffsetTemperature = float(fineOffsetMsg[4])
            fineOffsetId = fineOffsetMsg[2]
    
            # Calculate values from the sensor readings
            fineOffsetTemperature = (
                fineOffsetTemperature/10.0
            )
            s_lst = (
                'FineOffset'+"|"+
                fineOffsetId
            )
            p_lod = (    
               'Temp'+"|"+
               str(fineOffsetTemperature)
            )
            eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.name)

            decode_param = None
            mon_param = None
            try:
                decode_param = self.plugin.decode_fineOffset_mem[s_lst]
            except:
                pass
            try:
                mon_param = self.plugin.monitor_fineOffset_mem[s_lst]
            except:
                pass
            self.plugin.monitor_fineOffset_mem[s_lst] = self.plugin.eventMonitor(
                mon_param,
                decode_param,
                s_lst,
                self.lostSensors
            )
            self.plugin.decode_fineOffset_mem[s_lst] = p_lod
        except:
            pass
            

    def OregonMessage(self, oregonMsg):
        try:
            oregonBattery = oregonMsg[6]
            oregonTemperature = float(oregonMsg[12])
            try:
                oregonHumidity = int(oregonMsg[8])
            except:
                oregonHumidity = 0
            oregonCh = oregonMsg[2]
            oregonId = oregonMsg[4]
    
            # Calculate values from the sensor readings
            oregonTemperature = (
                oregonTemperature/10.0
            )
            s_lst = (
                'Oregon'+"|"+
                oregonId+"|"+
                oregonCh+"|"
            )
            p_lod = (    
               'Temp'+"|"+
               str(oregonTemperature)+"|"+
               'Hum'+"|"+
               str(oregonHumidity)+"|"+
               'Batt'+"|"+
               str(oregonBattery)+"|"
            )
            eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.name)
    
            if int(oregonBattery) == 1:
                # Create the eg battery low event
                eg.TriggerEvent(
                    s_lst+
                    self.text.loggerAction.txtBattLow, prefix = self.name
                )
                if self.bLogToFile:
                    logStr = (
                        s_lst+
                        self.text.loggerAction.txtBattLow
                    )
                    self.LogToFile(logStr)

            decode_param = None
            mon_param = None
            try:
                decode_param = self.plugin.decode_oregon_mem[s_lst]
            except:
                pass
            try:
                mon_param = self.plugin.monitor_oregon_mem[s_lst]
            except:
                pass
            self.plugin.monitor_oregon_mem[s_lst] = self.plugin.eventMonitor(
                mon_param,
                decode_param,
                s_lst,
                self.lostSensors
            )
            self.plugin.decode_oregon_mem[s_lst] = p_lod
        except:
            pass


    def UpmMessage(self, upmMsg):
        if (
            len(upmMsg[1]) > 0
            and len(upmMsg[2]) > 0
            and len(upmMsg[3]) > 0
            and len(upmMsg[4]) > 0
            and len(upmMsg[5]) > 0
            and len(upmMsg[6]) > 0
            and upmMsg[6] != " "
            and upmMsg[6].isdigit()
            and len(upmMsg[7]) > 0
            and len(upmMsg[8]) > 0
            and len(upmMsg[9]) > 0
            and len(upmMsg[10]) > 0
            and upmMsg[10] != " "
            and upmMsg[10].isdigit()
        ):
            upmBattery = upmMsg[6]
            upmTemperature = float(upmMsg[8])
            upmHumidity = int(upmMsg[10])
            upmDevice = upmMsg[2]
            upmHouse = upmMsg[4]
    
            # Calculate values from the sensor readings
            if int(upmHouse) != 10:
                upmTemperature = (
                    (upmTemperature * 0.0625) - 50.0
                )
                upmHumidity = upmHumidity / 2
                s_lst = (
                    self.name+"|"+
                    str(upmMsg[3])+"|"+
                    str(upmHouse)+"|"+
                    str(upmMsg[1])+"|"+
                    str(upmDevice)+"|"
                )
                p_lod = (    
                   'Temp'+"|"+
                    str(upmTemperature)+"|"+
                   'Hum'+"|"+
                    str(upmHumidity)+"|"+
                    'Batt'+"|"+
                    str(upmBattery)+"|"
                 )
            else:
                # House/Device codes 10/2 are reserved
                # for wind gauges
                if int(upmDevice) == 2:
                    s_lst = (
                        self.name+"|"+
                        str(upmMsg[3])+"|"+
                        str(upmHouse)+"|"+
                        str(upmMsg[1])+"|"+
                        str(upmDevice)+"|"+
                        str(upmMsg[7])+"|"+
                        str(upmBattery)+"|"
                    )
                    p_lod = self.CalcWindData(
                        upmMsg[10],
                        upmMsg[6]
                    )
    
                # House/Device codes 10/3 are reserved
                # for rain gauges
                if int(upmDevice) == 3:
                    s_lst = (
                        self.name+"|"+
                        str(upmMsg[3])+"|"+
                        str(upmHouse)+"|"+
                        str(upmMsg[1])+"|"+
                        str(upmDevice)+"|"+
                        str(upmMsg[7])+"|"+
                        str(upmBattery)+"|"
                    )
                    p_lod = self.CalcRainData(
                        upmMsg[10]
                    )
    
            if int(upmHouse) > 0:
                eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.name)
    
            if int(upmHouse) > 0 and int(upmBattery) == 1:
                # Create the eg battery low event
                eg.TriggerEvent(
                    s_lst+
                    self.text.loggerAction.txtBattLow, prefix = self.name
                )
                    
                if self.bLogToFile:
                    logStr = (
                        s_lst+
                        self.text.loggerAction.txtBattLow
                    )
                    self.LogToFile(logStr)

            decode_param = None
            mon_param = None
            try:
                decode_param = self.plugin.decode_mandolyn_mem[s_lst]
            except:
                pass
            try:
                mon_param = self.plugin.monitor_mandolyn_mem[s_lst]
            except:
                pass
            self.plugin.monitor_mandolyn_mem[s_lst] = self.plugin.eventMonitor(
                mon_param,
                decode_param,
                s_lst,
                self.lostSensors
            )
            self.plugin.decode_mandolyn_mem[s_lst] = p_lod

    
    def CalcRainData(self, rLevel ):
        self.rain_Week_sum = 0.0
        rainLevel = float(rLevel) * 0.7
        self.rain_levels[0] = self.rain_levels[1]
        self.rain_levels[1] = rainLevel
        date = str(time.strftime("%m/%d/%Y", time.localtime()))
        ydate = datetime.today() - timedelta(1)
        toDate = str(time.strftime("%Y-%m-%d", time.localtime()))
        yesterDate = str(ydate).split(' ')[0]
        d = self.GetDayOfWeek(date) # Monday = 0
        dy = 0 

        if d == 0:
            dy = 6
        else:
            dy = d - 1

        if (self.rain_levels[0] > self.rain_levels[1]): # Rain gauge reset
            self.rain_levels = [0.0, 0.0]

        if ( # Plugin startup
            self.rain_Today[0] == 0.0
            and
            self.rain_Today[1] == 0.0
        ):
            start = time.clock()
            self.rain_Hour[1] = start
            
        if (self.rain_levels[1] >= self.rain_levels[0]):
            now = time.clock()
            self.rain_Hour[2] += self.rain_levels[1] - self.rain_levels[0]
            self.rain_Hour[3] = now
            self.rain_Today[1] += self.rain_levels[1] - self.rain_levels[0]

            #Last hour
            h_diff_time = now - self.rain_Hour[1]
            #print h_diff_time
            if (h_diff_time > 3600): # One hour has elapsed
                self.rain_Hour[0] = self.rain_Hour[2]
                self.rain_Hour[2] = 0.0
                self.rain_Hour[1] = now
                self.rain_Hour_previous = self.rain_Hour[0]
                
            #Last day & yesterday & week
            t_now = time.strftime("%H", time.localtime())
            if (int(t_now) == 0 and not self.bNewDay):
                self.bNewDay = True # A new day begins
                self.rain_Today[0] = self.rain_Today[1]
                self.rain_Today[1] = 0.0
                self.rain_Week_levels[dy] = self.rain_Today[0]
                self.rain_Week_dates[dy] = yesterDate
            if (int(t_now) > 0 and self.bNewDay):
                self.bNewDay = False
                                          
        for item in self.rain_Week_levels:
            self.rain_Week_sum += item

        self.rain_Yesterday = self.rain_Week_levels[dy]
        date_Yesterday = self.rain_Week_dates[dy]
        self.plugin.rain_level_values_last_week = self.rain_Week_levels
        self.plugin.rain_level_dates_last_week = self.rain_Week_dates
        p_lod = (    
            "UPM.RainLastHour|"+
            str(self.rain_Hour[2])+"|"+
            "mm"+"|"+
            "UPM.RainPreviousHour|"+
            str(self.rain_Hour_previous)+"|"+
            "mm"+"|"+
            "UPM.RainToday|"+
            str(self.rain_Today[1])+"|"+
            "mm"+"|"+
            "UPM.RainYesterday|"+
            str(date_Yesterday)+"|"+
            str(self.rain_Yesterday)+"|"+
            "mm"+"|"+
            "UPM.RainLastWeek|"+
            str(self.rain_Week_sum)+"|"+
            "mm"+"|"+
            "UPM.RainMeter|"+
            str(rainLevel)+"|"+
            "mm"+"|"
        )
        return p_lod
        
        
    def CalcWindData(self, wSpeed, wDir):    
        wdSpeed = float(wSpeed)
        windSpeedSum_15 = 0.0
        windSpeedSum_60 = 0.0

        if (int(wDir) <= 30):
            if (self.wdLabel != ""):
                if (self.wdLabelPrevious != self.wDirection[int(wDir)/2]):
                    self.wdLabelPrevious = self.wdLabel
            self.wdLabel = self.wDirection[int(wDir)/2]
        else:
            print "Wind direction out of range:", self.wdLabel
            print "Raw message: ", self.plugin.event_NHS
            self.wdLabel = "Out of range"

        if self.plugin.bSpeed_ms:
            wdSpeed = (wdSpeed*1000)/3600

        if len(self.wdLevels_15) < 15:
            self.wdLevels_15.append(wdSpeed)
        else:
            self.wdLevels_15[self.wi] = wdSpeed

        if len(self.wdLevels_60) < 60:
            self.wdLevels_60.append(wdSpeed)
        else:
            self.wdLevels_60[self.wj] = wdSpeed
        
        self.wi += 1
        self.wj += 1
        
        for k in range(len(self.wdLevels_15)):
            windSpeedSum_15 += self.wdLevels_15[k] 

        wdSpeedAv_15 = windSpeedSum_15 / self.wi

        for m in range(len(self.wdLevels_60)):
            windSpeedSum_60 += self.wdLevels_60[m] 

        wdSpeedAv_60 = windSpeedSum_60 / self.wj

        if (self.wi > 14):
            self.wi = 0

        if (self.wj > 59):
            self.wj = 0

        self.plugin.wind_level_average_15 = self.wdLevels_15
        self.plugin.wind_level_average_60 = self.wdLevels_60
        p_lod = (    
            "UPM.WindDirection|"+
            self.wdLabel+"|"+
            "UPM.WindDirectionPrevious|"+
            self.wdLabelPrevious+"|"+
            "UPM.WindSpeed|"+
            str(wdSpeed)+"|"+
            "UPM.WindSpeedAverage_15|"+
            str(wdSpeedAv_15)+"|"+
            "UPM.WindSpeedAverage_60|"+
            str(wdSpeedAv_60)+"|"
         )
        return p_lod


    def GetDayOfWeek(self, dateString):
        # day of week (monday = 0) of a given month/day/year
        ds = dateString.split('/')
        dayOfWeek = int(calendar.weekday(int(ds[2]),int(ds[0]),int(ds[1])))
        return(dayOfWeek)


    def ClearBuffer(self):
        self.old_lst = []
        self.bTaskAdded = False


    def Abortlogger(self):
        WeatherData.rain_Week_levels[self.name] = self.rain_Week_levels
        WeatherData.rain_Week_dates[self.name] = self.rain_Week_dates
        print self.text.thr_abort, self.text.n_loggerThread
        self.finished.wait(1.0)
        self.abort = True
        self.finished.set()
        time.sleep(3.0)

       
    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileDate = str(
            time.strftime("%Y%m%d", time.localtime())
        )
        logStr = timeStamp+" "+s+"<br\n>"
        fileHandle = None
        progData = eg.configDir + '\plugins\NetHomeServer'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        fileHandle = open (
            progData+'/'+fileDate+'Logger_'+
            self.name+'.html', 'a'
        )
        fileHandle.write ( logStr )
        fileHandle.close ()


    def debugLogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileDate = str(
            time.strftime("%Y%m%d", time.localtime())
        )
        logStr = timeStamp+" "+s+"<br\n>"
        fileHandle = None
        progData = eg.configDir + '\plugins\NetHomeServer'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        fileHandle = open (
            progData+'/'+fileDate+'Logger_debug'+
            self.name+'.html', 'a'
        )
        fileHandle.write ( logStr )
        fileHandle.close ()
               


class CurrentStateData(eg.PersistentData):
    sensors_status = {}



class WeatherData(eg.PersistentData):
    rain_Week_levels = {}
    rain_Week_dates = {}



class NetHomeServer(eg.PluginClass):
    text = Text
        
    def __init__(self):
        self.AddAction(loggerAction)
        self.AddAction(SendCommand)
        self.AddAction(ClearSensorsStatus)
        self.AddAction(GetWeeklyRainLevels)
        self.AddAction(GetAverageWindLevels)
        self.AddAction(prontoCmd)
        self.AddAction(smokeDetCmd)
        self.AllloggerNames = []
        self.AllLostS = []
        self.AllSound = []
        self.AllRepeats = []
        self.AllRepeatDelay = []
        self.AllLogToFile = []
        self.AllDebug = []
        self.lastloggerName = ""
        self.loggerThreads = {}
        self.counters = {}
        self.rain_level_values_last_week = []
        self.rain_level_dates_last_week = []
        self.wind_level_average_15 = []
        self.wind_level_average_60 = []
        self.sensors_status = CurrentStateData.sensors_status
        self.OkButtonClicked = False
        self.started = False


    def __start__(
        self,
        hostName,
        portNbr,
        bSpeed_ms,
        socketTout
    ):
        print self.text.started
        self.hostName = hostName
        self.portNbr = portNbr
        self.socketTout = socketTout
        self.bSpeed_ms = bSpeed_ms
        self.started = True
        self.event_NHS = ""
        self.semaPhore = True
        self.rest_port = 8020
        self.prefix = 'OpenNetHome'
        self.monitor_oregon_mem = {}        
        self.decode_oregon_mem = {}
        self.monitor_fineoffset_mem = {}        
        self.decode_fineoffset_mem = {}
        self.monitor_mandolyn_mem = {}        
        self.decode_mandolyn_mem = {}
        self.RestartAllLoggers()
#        if self.OkButtonClicked:
#            self.OkButtonClicked = False
#            self.RestartAllLoggers()

        progData = eg.configDir + '\plugins\NetHomeServer'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()

        self.keepAliveThreadEvent = Event()
        self.remain = 0.0
        keepAliveThread = Thread(
            target=self.keep_Alive,
            args=(self.keepAliveThreadEvent,)
        )
        keepAliveThread.start()


    def __stop__(self):
        self.mainThreadEvent.set()
        self.keepAliveThreadEvent.set()
        self.AbortAllLoggers()
        self.started = False

        print self.text.cleanUpmonitoring
        for i in self.monitor_oregon_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_oregon_mem[i])
            except:
                pass
        for i in self.monitor_fineoffset_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_fineoffset_mem[i])
            except:
                pass
        for i in self.monitor_mandolyn_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_mandolyn_mem[i])
            except:
                pass
        eg.Wait(self.remain + 0.5)
        print self.text.readyStopped


    def __close__(self):
        self.AbortAllLoggers()
        self.started = False


    def sensorLost(self, myArgument):
        eg.TriggerEvent(repr(myArgument), prefix = self.prefix)
        lc = myArgument.split(':')[1].split(' ')[1]
        try:
            del self.sensors_status[lc]
        except:
            pass
        try:
            self.sensors_status[lc] = myArgument
        except:
            pass

 
    def sensorBack(self, myArgument):
        eg.TriggerEvent(repr(myArgument), prefix = self.prefix)
        bc = myArgument.split(':')[3].split(' ')[1]
        try:
            del self.sensors_status[bc]
        except:
            pass
        try:
            self.sensors_status[bc] = myArgument
        except:
            pass
 
 
    def eventMonitor(self, monitored, pload, base, timeout):
        try:
            eg.scheduler.CancelTask(monitored)
        except:
            if pload <> None:
                self.sensorBack(
                    self.text.txt_signal_back+': '+base 
                )
        monitored = eg.scheduler.AddTask(
                timeout,
                self.sensorLost,
                self.text.txt_taskObj+': '+base
        )
        return monitored
       

    def GetConnection(self, host, port, URL):
        try:
            conn = httplib.HTTPConnection(host+':'+str(port))
            conn.request('GET', "http://"+host+':'+str(port)+URL)
            resp = conn.getresponse()
            if resp.status == 200:
                return resp
            else:
                eg.PrintError(self.text.rest_connection_error)
                return None
        except:
            return None
            

    def GetAttributes(self, host, port, URL):
        resp = self.GetConnection(host, port, URL)
        content = resp.read().replace('true', 'True')
        content.replace('false', 'False')
        return eval(content)['attributes']


    def GetClassName(self, host, port, URL):
        resp = self.GetConnection(host, port, URL)
        content = resp.read().replace('true', 'True')
        content.replace('false', 'False')
        return eval(content)['className']


    def keep_Alive(self,keepAliveThreadEvent): # Keep Alive Loop
        counter = 0
        while not keepAliveThreadEvent.isSet():
            if counter == 60:
                self.KeepAlive()
                counter = 0
            else:
                counter += 1
            keepAliveThreadEvent.wait(1.0)
        print self.text.ka_threadStopped


    def KeepAlive(self):
        objects = {}
        resp = self.GetConnection(
            self.hostName, 
            self.rest_port, 
            '/rest/items'
        )
        if resp <> None:
            content = eval(resp.read())
            for item in content:
                if item['category']=='Hardware':
                    className = self.GetClassName(
                        self.hostName,
                        self.rest_port, 
                        '/rest/items/'+item['id']
                    )
                    attribs = self.GetAttributes(
                        self.hostName,
                        self.rest_port, 
                        '/rest/items/'+item['id']
                    )
                    objects[className] = attribs[0]['value']
            for item in objects:
                if objects[item] <> 'Connected':
                    eg.TriggerEvent(
                        item+' is '+objects[item],
                        prefix = self.prefix
                    )
            

    def main(self,mainThreadEvent):

        def connectToHost():
            #print self.atStart
            try:
                self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.skt.settimeout(5.0)
                self.skt.connect((self.hostName, self.portNbr))
                self.skt.sendall("subscribe\r\n")
                rsp = self.skt.recv(8)
                if rsp.find("ok") != -1:
                    self.connectionError = False
                    self.skt.settimeout(self.socketTout)
                    if self.atStart != 1:
                        print self.text.connection_etablished
                        self.atStart = 1
            except socket.error, e:
                self.connectionError = True
                self.skt.settimeout(20.0)
                mainThreadEvent.wait(1.0)
        

        self.skt = None
        self.connectionError = True
        self.atStart = 0
        cCount = 0
        reConnects = 0
        eofErrors = 0
        event_Old = []
        connectToHost()

        while not mainThreadEvent.isSet():
            if self.semaPhore:
                tst = ''
                try:
                    if cCount > 10:
                        self.skt.sendall("dir\r\n")
                        mainThreadEvent.wait(0.2)
                        p = ''
                        #print 'start reading'
                        p = self.skt.recv(1028)
                        #print 'end reading'
                        #print'self.skt.gettimeout', self.skt.gettimeout()
                        cCount = 0
                        if p.find("ok") == -1:
                            self.connectionError = True
                    else:
                        mainThreadEvent.wait(0.2)
                        #print 'start reading'
                        tst = self.skt.recv(256)
                        #print 'end reading'
                        reConnects = 0
                        eofErrors = 0
                        cCount += 1
                        self.connectionError = False
                except EOFError:
                    #print 'EOFError', self.atStart
                    self.connectionError = True
                    eofErrors += 1
                    if eofErrors > 4:
                        eg.PrintError(self.text.tcp_EOFError_error)
                        eg.TriggerEvent(
                            self.text.tcp_EOFError_error,
                            prefix = self.prefix
                        )
                        eofErrors = 0
                except socket.error, e:
                    #print 'socket.error', self.atStart
                    self.connectionError = True
                    reConnects += 1
                    #if reConnects > 4:
                    if reConnects > 1:
                        if self.atStart == 1:
                            eg.PrintError(self.text.tcp_connection_error)
                            eg.TriggerEvent(
                                self.text.tcp_connection_error,
                                prefix = self.prefix
                            )
                            self.atStart = 2
                        reConnects = 0
                    if self.atStart == 0:
                        eg.PrintError(self.text.tcp_connection_at_start)
                        eg.TriggerEvent(
                            self.text.tcp_connection_at_start,
                            prefix = self.prefix
                        )
                        self.atStart = 3

                if(
                    len(tst) > 9
                    and(
                        tst.find('Pronto.Message') > 0
                        or(
                            tst.find('NexaFire_Message') > 0
                            and tst.find('NexaFire.Address') > 0
                        )
                        or(
                            tst.find('NexaL.Address') > 0
                            and tst.find('NexaL.Button') > 0
                            and tst.find('NexaL.Command') > 0
                        )
                        or(
                            tst.find('Nexa.Button') > 0
                            and tst.find('Nexa.Command') > 0
                            and tst.find('Nexa.HouseCode') > 0
                        )
                        or(
                            tst.find('UPM.HouseCode') > 0
                            and tst.find('UPM.DeviceCode') > 0
                            and tst.find('UPM.LowBattery') > 0
                        )
                        or(
                            tst.find('Oregon.Channel') > 0
                            and tst.find('Oregon.SensorId') > 0
                            and tst.find('Oregon.Temp') > 0
                        )
                        or(
                            tst.find('FineOffset_Message') > 0
                            and tst.find('FineOffset.Identity') > 0
                            and tst.find('FineOffset.Temp') > 0
                        )
                    )
                    and event_Old != tst
                ):
                    self.skt.settimeout(self.socketTout)
                    event_Old = tst
                    e_lst = []
                    e_lst = tst.split("\n\r")
                    myEvent = ''
                
                    for myEvent in e_lst:
                        if myEvent != '':
                            #print myEvent, len(e_lst)
                            self.event_NHS = "NetHomeServer" + "," + myEvent
                            mainThreadEvent.wait(0.2)
    
                if self.connectionError:
                    self.skt.close()
                    mainThreadEvent.wait(1.0)
                    connectToHost()        
            else:
                mainThreadEvent.wait(0.1)
            
        self.skt.close()
        time.sleep(0.1)
        print self.text.unsubscribe+"Main-"+self.text.thr_abort, mainThreadEvent

    
    def Startlogger(    #methods to Control loggers
        self,
        loggerName,
        hostName,
        lostSensors,
        bSound,
        bRepeats,
        repeatDelay,
        bLogToFile,
        bDebug,
        bSpeed_ms
    ):
        if self.loggerThreads.has_key(loggerName):
            t = self.loggerThreads[loggerName]
            print self.loggerThreads, loggerName
            if t.isAlive():
                t.Abortlogger()
            del self.loggerThreads[loggerName]
        t = loggerThread(
            loggerName,
            self.hostName,
            lostSensors,
            bSound,
            bRepeats,
            repeatDelay,
            bLogToFile,
            bDebug,
            self.bSpeed_ms,
            self
        )
        self.loggerThreads[loggerName] = t
        t.start()


    def Abortlogger(self, logger):
        if self.loggerThreads.has_key(logger):
            t = self.loggerThreads[logger]
            t.Abortlogger()
            del self.loggerThreads[logger]


    def AbortAllLoggers(self):
        for i, item in enumerate(self.loggerThreads):
            t = self.loggerThreads[item]
            t.Abortlogger()
            del t
        self.loggerThreads = {}


    def RestartAllLoggers(self, startNewIfNotAlive = True):
        for i, item in enumerate(self.GetAllLoggerNames()):
            if startNewIfNotAlive:
                self.Startlogger(
                    self.GetAllLoggerNames()[i],
                    self.hostName,
                    self.GetAllLostS()[i],
                    self.GetAllSound()[i],
                    self.GetAllRepeats()[i],
                    self.GetAllRepeatDelay()[i],
                    self.GetAllLogToFile()[i],
                    self.GetAllDebug()[i],
                    self.bSpeed_ms
                )


    def Configure(
        self,
        hostName = "192.168.10.252",
        portNbr = 8005,
        bSpeed_ms = True,
        socketTout = 600,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
      
        netHomeServerListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL
        )
       
        for i, colLabel in enumerate(self.text.colLabels):
            netHomeServerListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        netHomeServerListCtrl.InsertStringItem(
            0,
            "Test NetHome Name                     "
        )
        netHomeServerListCtrl.SetStringItem(0, 1, "  ")
        netHomeServerListCtrl.SetStringItem(0, 2, "  ")

        size = 0
        for i in range(3):
            netHomeServerListCtrl.SetColumnWidth(
                i,
                wx.LIST_AUTOSIZE_USEHEADER
            )
            size += netHomeServerListCtrl.GetColumnWidth(i)
       
        netHomeServerListCtrl.SetMinSize((size, -1))
        
        mySizer.Add(netHomeServerListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        hostNameCtrl = wx.TextCtrl(panel, -1, hostName)
        hostNameCtrl.SetInitialSize((250,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.hostName), (1,0))
        mySizer.Add(hostNameCtrl, (1,1))
    
        portCtrl = panel.SpinIntCtrl(portNbr, 0, 9000)
        portCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.portNumber), (2,0))
        mySizer.Add(portCtrl, (2,1))

        socketToutCtrl = panel.SpinIntCtrl(socketTout, 20, 9999)
        socketToutCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.socketTimeOut), (3,0))
        mySizer.Add(socketToutCtrl, (3,1))

        speedCtrl = panel.CheckBox(bSpeed_ms, "")
        speedCtrl.SetValue(bSpeed_ms)
        mySizer.Add(wx.StaticText(panel, -1, self.text.windSpeed), (4,0))
        mySizer.Add(speedCtrl, (4,1))

        #buttons
        abortButton = wx.Button(panel, -1, self.text.b_abort)
        mySizer.Add(abortButton, (5,0))
       
        abortAllButton = wx.Button(panel, -1, self.text.b_abortAll)
        mySizer.Add(abortAllButton, (5,1), flag = wx.ALIGN_RIGHT)
       
        restartAllButton = wx.Button(panel, -1, self.text.b_restartAll)
        mySizer.Add(restartAllButton, (5,2), flag = wx.ALIGN_RIGHT)

        refreshButton = wx.Button(panel, -1, self.text.b_refresh)
        mySizer.Add(refreshButton, (5,4), flag = wx.ALIGN_RIGHT)
       
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

       
        def PopulateList (event):
            netHomeServerListCtrl.DeleteAllItems()
            row = 0
            for j, item in enumerate(self.loggerThreads):
                t = self.loggerThreads[item]
                if t.isAlive():
                    netHomeServerListCtrl.InsertStringItem(row, t.name)
                    row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = netHomeServerListCtrl.GetFirstSelected()
            while item != -1:
                name = netHomeServerListCtrl.GetItemText(item)
                self.Abortlogger(name)
                item = netHomeServerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.AbortAllLoggers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            event.Skip()
            self.RestartAllLoggers()
            PopulateList(wx.CommandEvent())


        def ListSelection(event):
            flag = netHomeServerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()

           
        def OnSize(event):
            netHomeServerListCtrl.SetColumnWidth(
                6,
                wx.LIST_AUTOSIZE_USEHEADER
            )
            event.Skip()


        def OnApplyButton(event): 
            event.Skip()
            self.RestartAllLoggers()
            PopulateList(wx.CommandEvent())


        def OnOkButton(event): 
            event.Skip()
            self.OkButtonClicked = True
#            if not self.started:    
#                self.RestartAllLoggers()
            PopulateList(wx.CommandEvent())
        
        PopulateList(wx.CommandEvent())
       
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        netHomeServerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        netHomeServerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            hostName = hostNameCtrl.GetValue()
            portNbr = portCtrl.GetValue()
            bSpeed_ms = speedCtrl.GetValue()
            socketTout = socketToutCtrl.GetValue()
            panel.SetResult(
                        hostName,
                        portNbr,
                        bSpeed_ms,
                        socketTout,
                        *args
            )


    def GetAllLoggerNames(self):
        return self.AllloggerNames


    def GetAllSound(self):
        return self.AllSound


    def GetAllLostS(self):
        return self.AllLostS


    def GetAllRepeats(self):
        return self.AllRepeats


    def GetAllRepeatDelay(self):
        return self.AllRepeatDelay


    def GetAllLogToFile(self):
        return self.AllLogToFile


    def GetAllDebug(self):
        return self.AllDebug


    def AddloggerName(self, loggerName):
        if not loggerName in self.AllloggerNames:
            self.AllloggerNames.append(loggerName)
        return self.AllloggerNames.index(loggerName)


    def AddLostS(self, lostSensor, indx):
        try:
            del self.AllLostS[indx]
        except IndexError:
            i = -1 # no match
        self.AllLostS.insert(indx, lostSensor)


    def AddSound(self, bSound, indx):
        try:
            del self.AllSound[indx]
        except IndexError:
            i = -1 # no match
        self.AllSound.insert(indx, bSound)


    def AddDebug(self, bDebug, indx):
        try:
            del self.AllDebug[indx]
        except IndexError:
            i = -1 # no match
        self.AllDebug.insert(indx, bDebug)


    def AddLogToFile(self, bLogToFile, indx):
        try:
            del self.AllLogToFile[indx]
        except IndexError:
            i = -1 # no match
        self.AllLogToFile.insert(indx, bLogToFile)


    def AddRepeats(self, bRepeats, indx):
        try:
            del self.AllRepeats[indx]
        except IndexError:
            i = -1 # no match
        self.AllRepeats.insert(indx, bRepeats)


    def AddRepeatDelay(self, repeatDelay, indx):
        try:
            del self.AllRepeatDelay[indx]
        except IndexError:
            i = -1 # no match
        self.AllRepeatDelay.insert(indx, repeatDelay)


             
class loggerAction(eg.ActionClass):
    text = Text.loggerAction
    
    def __call__(
        self,
        loggerName,
        hostName,
        lostSensors,
        bSound,
        bRepeats,
        repeatDelay,
        bLogToFile,
        bDebug,
        bSpeed_ms
    ):
        self.plugin.Startlogger(
            loggerName,
            hostName,
            lostSensors,
            bSound,
            bRepeats,
            repeatDelay,
            bLogToFile,
            bDebug,
            bSpeed_ms
        )


    def GetLabel(
        self,
        loggerName,
        hostName,
        lostSensors,
        bSound,
        bRepeats,
        repeatDelay,
        bLogToFile,
        bDebug,
        bSpeed_ms
    ):
        indx = self.plugin.AddloggerName(loggerName)
        self.plugin.AddLostS(lostSensors, indx)
        self.plugin.AddSound(bSound, indx)
        self.plugin.AddRepeatDelay(repeatDelay, indx)
        self.plugin.AddRepeats(bRepeats, indx)
        self.plugin.AddLogToFile(bLogToFile, indx)
        self.plugin.AddDebug(bDebug, indx)
        return self.text.labelStart % (loggerName)


    def Configure(
        self,
        loggerName = "Give this logger a name",
        hostName = "name",
        lostSensors = 600,
        bSound = False,
        bRepeats = True,
        repeatDelay = 5.0,
        bLogToFile = True,
        bDebug = False,
        bSpeed_ms = True
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(5, 5)
        mySizer_3 = wx.GridBagSizer(10, 10)

        loggerNameCtrl = wx.TextCtrl(panel, -1, loggerName)
        loggerNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.loggerName), (0,0))
        mySizer_1.Add(loggerNameCtrl, (0,1))

        bRepeatsCtrl = wx.CheckBox(panel, -1, "")
        bRepeatsCtrl.SetValue(bRepeats)
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.repeats), (1,0))
        mySizer_1.Add(bRepeatsCtrl, (1,1))

        repeatDelayCtrl = panel.SpinNumCtrl(
            repeatDelay,
            decimalChar = '.', # by default, use '.' for decimal point
            groupChar = ',',   # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = 0.0,
            max = 999.9,
            increment = 0.5
        )
        repeatDelayCtrl.SetInitialSize((60,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.delay), (2,1))
        mySizer_2.Add(repeatDelayCtrl, (2,2))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.delay_u), (2,3))

        lostSensorsCtrl = panel.SpinIntCtrl(lostSensors, 100, 7200)
        lostSensorsCtrl.SetInitialSize((60,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.lostSensors
            ),
           (3,1)
        )
        mySizer_2.Add(lostSensorsCtrl,(3,2))

        bLogToFileCtrl = wx.CheckBox(panel, -1, "")
        bLogToFileCtrl.SetValue(bLogToFile)
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.logToFile), (3,0))
        mySizer_3.Add(bLogToFileCtrl, (3,1))

        bSoundCtrl = wx.CheckBox(panel, -1, "")
        bSoundCtrl.SetValue(bSound)
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.soundOnEvent), (4,0))
        mySizer_3.Add(bSoundCtrl, (4,1))

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.debug), (5,0))
        mySizer_3.Add(bDebugCtrl, (5,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)


        def OnButton(event): 
            # re-assign the OK button
            event.Skip()
            loggerName = loggerNameCtrl.GetValue()
            plugin.lastloggerName = loggerName
            indx = plugin.AddloggerName(loggerName)
            hostName = self.plugin.hostName
            lostSensors = lostSensorsCtrl.GetValue()
            plugin.AddLostS(lostSensors, indx)
            bSound = bSoundCtrl.GetValue()
            plugin.AddSound(bSound, indx)
            bRepeats = bRepeatsCtrl.GetValue()
            plugin.AddRepeats(bRepeats, indx)
            repeatDelay = repeatDelayCtrl.GetValue()
            plugin.AddRepeatDelay(repeatDelay, indx)
            bLogToFile = bLogToFileCtrl.GetValue()
            plugin.AddLogToFile(bLogToFile, indx)
            bDebug = bDebugCtrl.GetValue()
            plugin.AddDebug(bDebug, indx)
            bSpeed_ms = self.plugin.bSpeed_ms
            self.plugin.RestartAllLoggers()


        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            loggerName = loggerNameCtrl.GetValue()
            plugin.lastloggerName = loggerName
            indx = plugin.AddloggerName(loggerName)
            hostName = self.plugin.hostName
            lostSensors = lostSensorsCtrl.GetValue()
            plugin.AddLostS(lostSensors, indx)
            bSound = bSoundCtrl.GetValue()
            plugin.AddSound(bSound, indx)
            bRepeats = bRepeatsCtrl.GetValue()
            plugin.AddRepeats(bRepeats, indx)
            repeatDelay = repeatDelayCtrl.GetValue()
            plugin.AddRepeatDelay(repeatDelay, indx)
            bLogToFile = bLogToFileCtrl.GetValue()
            plugin.AddLogToFile(bLogToFile, indx)
            bDebug = bDebugCtrl.GetValue()
            plugin.AddDebug(bDebug, indx)
            bSpeed_ms = self.plugin.bSpeed_ms
            panel.SetResult(
                loggerName,
                hostName,
                lostSensors,
                bSound,
                bRepeats,
                repeatDelay,
                bLogToFile,
                bDebug,
                bSpeed_ms
            )



class prontoCmd(eg.ActionClass):
    text = Text.prontoCmd
    
    def __call__(
        self,
        deviceName,
        pronto,
        iNbrOfBursts,
        cmdDelay
    ):
        header = "event,Pronto_Message,Direction,Out,Pronto.Message,"
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            #print self.plugin.text.connection_error, e
            connectionError = True
            
        s = header+str(pronto)+"\r\n"
        time.sleep(0.05)
        for i in range(iNbrOfBursts):
            self.skt.sendall(s)
            time.sleep(cmdDelay)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True


    def Configure(
        self,
        deviceName = "Give the device a name",
        pronto = (
            "0000 0073 0000 0019 000e 002a 000e 002a 000e 002a 000e "+
            "002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a "+
            "000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e "+
            "002a 000e 002a 000e 002a 000e 002a 000e 002a 002a 000e "+
            "000e 002a 002a 000e 000e 002a 002a 000e 000e 0199"
        ),
        iNbrOfBursts = 4,
        cmdDelay = 0.5
        
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)

        #name
        deviceNameCtrl = wx.TextCtrl(panel, -1, deviceName)
        deviceNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.deviceName), (0,0))
        mySizer_1.Add(deviceNameCtrl, (1,0))

        #pronto
        prontoCtrl = wx.TextCtrl(panel, -1, pronto, style=wx.TE_MULTILINE)
        prontoCtrl.SetInitialSize((400,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.pronto), (1,0))
        mySizer_2.Add(prontoCtrl, (2,0))

        iNbrOfBurstsCtrl = panel.SpinIntCtrl(iNbrOfBursts, 1, 10)
        iNbrOfBurstsCtrl.SetInitialSize((45,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtNbrBursts
            ),
           (0,0)
        )
        mySizer_3.Add(iNbrOfBurstsCtrl,(0,1))

        cmdDelayCtrl = panel.SpinNumCtrl(
            cmdDelay,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.1,
            max = 5.0,
            increment = 0.1
        )
        cmdDelayCtrl.SetInitialSize((45,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtCmdDelay
            ),
           (1,0)
        )
        mySizer_3.Add(cmdDelayCtrl,(1,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            deviceName = deviceNameCtrl.GetValue()
            pronto = prontoCtrl.GetValue()
            iNbrOfBursts = iNbrOfBurstsCtrl.GetValue()
            cmdDelay = cmdDelayCtrl.GetValue()
            panel.SetResult(
                deviceName,
                pronto,
                iNbrOfBursts,
                cmdDelay
            )



class smokeDetCmd(eg.ActionClass):
    text = Text.smokeDetCmd
    
    def __call__(
        self,
        deviceName,
        address
    ):
    	header = "event,NexaFire_Message,Direction,Out,NexaFire.Address,"
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            #print self.plugin.text.connection_error, e
            connectionError = True
            
        s = header+str(address)+"\r\n"
        time.sleep(0.05)
        for i in range(0,2):
            self.skt.sendall(s)
            time.sleep(0.5)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True


    def Configure(
        self,
        deviceName = "Smoke detector description",
        address = "123456"
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        #name
        deviceNameCtrl = wx.TextCtrl(panel, -1, deviceName)
        deviceNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.deviceName), (0,0))
        mySizer_1.Add(deviceNameCtrl, (1,0))

        #address
        adrCtrl = wx.TextCtrl(panel, -1, address)
        adrCtrl.SetInitialSize((250,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.address), (1,0))
        mySizer_2.Add(adrCtrl, (2,0))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            deviceName = deviceNameCtrl.GetValue()
            address = adrCtrl.GetValue()
            panel.SetResult(
                deviceName,
                address
            )



class GetWeeklyRainLevels(eg.ActionClass):

    def __call__(self):
        
        print str(self.plugin.rain_level_values_last_week)
        print str(self.plugin.rain_level_dates_last_week)
        return(
            str(self.plugin.rain_level_values_last_week) +
            str(self.plugin.rain_level_dates_last_week)
        )

        

class GetAverageWindLevels(eg.ActionClass):

    def __call__(self):

        print str(self.plugin.wind_level_average_15)
        print str(self.plugin.wind_level_average_60)
        return(
            str(self.plugin.wind_level_average_15) +
            str(self.plugin.wind_level_average_60)
        )
        


class SendCommand(eg.ActionClass):
    text = Text.SendCommand
    objects = {}

    def __call__(
        self,
        obj,
        name,
        attribute,
        rest_port
    ):
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            connectionError = True
        s = 'call,'+obj+','+attribute+'\r\n'
        self.skt.sendall(s)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True

    
    def OnObjChoice(self, event = None):
        attribCtrl = self.attribCtrl
        objCtrl = self.objCtrl
        choice = objCtrl.GetSelection()
        obj = objCtrl.GetStringSelection()
        a_list = self.objects[obj]
        attribCtrl.Clear()
        attribCtrl.AppendItems(strings=a_list)
        if a_list.count(obj)==0:
            sel = 0
        else:
            sel = int(a_list.index(obj)) 
        attribCtrl.SetSelection(sel)
        if event:
            event.Skip()
        return choice 


    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def GetConnection(self, host, port, URL):
        try:
            conn = httplib.HTTPConnection(host+':'+str(port))
            conn.request('GET', "http://"+host+':'+str(port)+URL)
            resp = conn.getresponse()
            if resp.status == 200:
                return resp
            else:
                eg.PrintError(self.text.rest_connection_error)
                return None
        except:
            return None


    def GetActions(self, host, port, URL):
        resp = self.GetConnection(host, port, URL)
        content = resp.read().replace('true', 'True')
        content.replace('false', 'False')
        return eval(content)['actions']


    def Configure(
        self,
        obj = 'TF',
        name = 'Give the action a name',
        attribute = 'on',
        rest_port = 8020
    ):
        panel = eg.ConfigPanel(self)
        lamps = []
        resp = self.GetConnection(
            self.plugin.hostName, 
            rest_port, 
            '/rest/items'
        )
        content = eval(resp.read())
        for item in content:
            if item['category']=='Lamps':
                actions = self.GetActions(
                    self.plugin.hostName,
                    rest_port, 
                    '/rest/items/'+item['id']
                )
                self.objects[item['name']] = actions
        for item in self.objects:
            lamps.append(item)
            
        # Create a dropdown for object selection
        objCtrl = self.objCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        objCtrl.AppendItems(strings=lamps) 
        if lamps.count(obj)==0:
            objCtrl.Select(n=0)
        else:
            objCtrl.SetSelection(int(lamps.index(obj)))
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxObj)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(objCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        objCtrl.Bind(wx.EVT_CHOICE, self.OnObjChoice)

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for function selection
        attribCtrl = self.attribCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        self.OnObjChoice()  # This is used when opening the dialog
        a_list = attribCtrl.GetStrings()
        if attribute in a_list:
            attribCtrl.SetStringSelection(attribute)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxAttribute)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(attribCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        attribCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a field for selection of the REST interface port 
        portCtrl = panel.SpinIntCtrl(rest_port)
        staticBox = wx.StaticBox(panel, -1, self.text.textRestPort)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(portCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            self.plugin.rest_port = portCtrl.GetValue()
            panel.SetResult(
                objCtrl.GetStringSelection(),
                nameCtrl.GetValue(), 
                attribCtrl.GetStringSelection(),
                portCtrl.GetValue()
            )      



class ClearSensorsStatus(eg.ActionClass):
        
    def __call__(self):
        #Clear the repository for missing sensors
        time.sleep(0.5)
        CurrentStateData.sensors_status.clear()
        self.plugin.sensors_status = (
            CurrentStateData.sensors_status
        )



