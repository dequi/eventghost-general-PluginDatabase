# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
# Copyright (C) 2010 Tom St
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
#
# $LastChangedDate: $
# $LastChangedRevision: $
# $LastChangedBy: Tom St $

import eg

eg.RegisterPlugin(
    name="FHZ 1300 PC",
    kind="external",
    author="Bitmonster",
    version = "0.1",
)

import wx
import time
import os
from functools import partial
import wx.lib.masked as masked
from eg.WinApi.Dynamic import (
    byref, 
    windll,
    DWORD,
    GENERIC_READ,
    GENERIC_WRITE,
    OPEN_EXISTING,
    FILE_ATTRIBUTE_NORMAL,
    FILE_FLAG_OVERLAPPED,
    INVALID_HANDLE_VALUE,
)

FT_OPEN_BY_DESCRIPTION = 2

FS20FUNCTION = ["FS20_OFF", \
                "FS20_DIM_06", \
                "FS20_DIM_12", \
                "FS20_DIM_18", \
                "FS20_DIM_25", \
                "FS20_DIM_31", \
                "FS20_DIM_37", \
                "FS20_DIM_43", \
                "FS20_DIM_50", \
                "FS20_DIM_56", \
                "FS20_DIM_62", \
                "FS20_DIM_68", \
                "FS20_DIM_75", \
                "FS20_DIM_81", \
                "FS20_DIM_87", \
                "FS20_DIM_93", \
                "FS20_DIM_100", \
                "FS20_ON", \
                "FS20_TOGGLE", \
                "FS20_DIM_UP", \
                "FS20_DIM_DOWN", \
                "FS20_DIM_UPDOWN", \
                "FS20_TIMER", \
                "FS20_SENDSTATE", \
                "FS20_OFF_FOR_TIMER", \
                "FS20_ON_FOR_TIMER", \
                "FS20_ON_OLD_FOR_TIMER", \
                "FS20_RESET", \
                "FS20_RAMP_ON_TIME", \
                "FS20_RAMP_OFF_TIME", \
                "FS20_ON_OLD_FOR_TIMER_PREVIOUS", \
                "FS20_ON_100_FOR_TIMER_PREVIOUS"]

HMS_DEVICES  = ["HMS100TF", # Humidity and Temperature \
                "HMS100T",  # Temperature \
                "HMS100WD", #Water \
                "RM100_2",  #Smoke \
                "HMS100TFK_JUMPER1", #switch? \
                "HMS100TFK_JUMPER2", #switch? \
                "HMS100MG", #Gas detector \
                "HMS_UNDEFINED_1", \
                "HMS100CO", #Gas detector \
                "HMS_UNDEFINED_2", \
                "HMS_UNDEFINED_3", \
                "HMS_UNDEFINED_4", \
                "HMS_UNDEFINED_5", \
                "HMS_UNDEFINED_6", \
                "HMS100FIT"] # Earth Leakage Trigger Switch


class FHZ1300PC(eg.PluginBase):
    
    def __init__(self):
        self.AddAction(Off)
        self.AddAction(On)
        self.AddAction(Dim)
        self.AddAction(ToggleDim)
        self.AddAction(DimDown)
        self.AddAction(DimUp)
        self.AddAction(Toggle)
        self.AddAction(StartProgramTimer)
        self.AddAction(ResetToFactoryDefaults)
        
        
    def __start__(self):
        self.timeTask = None
        self.readBuffer = ""
        
        global d2xx
        try:
            d2xx = windll.LoadLibrary("ftd2xx.dll")
        except:
            raise self.Exception(
                "FHZ PC DLL not found (ftd2xx.dll).\n"
                "Make sure you have installed the driver for the device!"
            )
        self.ftHandle = d2xx.FT_W32_CreateFile(
            'ELV FHZ 1300 PC',
            GENERIC_READ|GENERIC_WRITE,
            0, # exclusive access
            0, # no security
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL|FILE_FLAG_OVERLAPPED|FT_OPEN_BY_DESCRIPTION,
            0
        )
        if self.ftHandle == INVALID_HANDLE_VALUE:
            raise self.Exceptions.DriverNotFound
        self.receiveThread = eg.SerialThread(self.ftHandle)
        self.receiveThread._WriteFile = d2xx.FT_W32_WriteFile
        self.receiveThread._ReadFile = d2xx.FT_W32_ReadFile
        self.receiveThread._ClearCommError = d2xx.FT_W32_ClearCommError
        self.receiveThread._CloseHandle = d2xx.FT_W32_CloseHandle
        
        d2xx.FT_SetLatencyTimer(self.ftHandle, 2)
        d2xx.FT_SetBaudRate(self.ftHandle, 9600)
        d2xx.FT_SetDataCharacteristics(self.ftHandle, 8, 0, 0)
        d2xx.FT_SetFlowControl(self.ftHandle, 0, 17, 19)
        d2xx.FT_SetTimeouts(self.ftHandle, 1000, 1000)
        
        self.receiveThread.Start()
        # Say hello
        self.WriteFhz(0xC9, 0x02, 0x01, 0x1f, 0x60)
        self.ReadFhz()
        self.WriteFhz(0xC9, 0x02, 0x01, 0x1f, 0x0a)
        self.ReadFhz()

        # Request Status/Serial
        self.WriteFhz(0x04, 0xc9, 0x01, 0x84, 0x57, 0x02, 0x08)
        self.ReadFhz()

        # HMS Init (if required)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x86)
        
        # FS20 Init (if required)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x96)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x96, 0x02)
        
        # calculate the time of the current minute
        t = list(time.localtime())
        t[5] = 0
        self.nextTaskTime = time.mktime(t)
        self.WriteFhz(*self.GetTimeData())
        self.nextTaskTime += 60.0
        self.timeTask = eg.scheduler.AddTaskAbsolute(
            self.nextTaskTime, 
            self.TimeScheduleTask
        )
        self.receiveThread.SetReadEventCallback(self.HandleReceive)
        
        
    def __stop__(self):
        if self.timeTask is not None:
            eg.scheduler.CancelTask(self.timeTask)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x97)
        if self.receiveThread:
            self.receiveThread.Close()
        
        
    def OnComputerSuspend(self, _suspendType):
        self.__stop__()
        
        
    def OnComputerResume(self, _suspendType):
        self.__start__()
    
    def GetStringFromAddress(self, address):
        valueStr = ""
        for i in range(11, -1, -1):
            x = (address >> i*2) & 0x03
            valueStr += str(x + 1)
        return valueStr[:4] +"-"+ valueStr[4:8] +"-"+ valueStr[8:]

    def GetAddressFromString(self, addressString):
        addressString=''.join(i for i in addressString if i.isdigit())
        address = 0
        for i in range(12):
            address <<= 2
            address += int(addressString[i]) - 1
        return address

    def HandleReceive(self, serial):
        # wait for start byte "0x81"
        startByte = self.Read(1)
        if startByte != "\x81":
            self.PrintError("Wrong start byte.")
            return None

        # read the number of bytes as specified in the datagram
        length = ord(self.Read(1))
        data = [ord(c) for c in self.Read(length)]
        telegramType = data[0]

        # read and calculate the CRC
        crc = data[1]
        newCrc = 0xff & sum(data[2:])

        # stop further processing of this datagram if CRC is invalid
        if crc != newCrc:
            self.PrintError("CRC does not match")
            return None

        #print "RAW: 81 " + " ".join(["%02X" % c for c in data])

        # check if it is a FS20 message
        if ((telegramType == 0x0C) or (telegramType == 0x04)) and \
           (data[2] == 0x01) and \
           (data[3] == 0x01) and \
           (data[4] == 0xa0) and \
           (data[5] == 0x01):

            address = (data[6] << 16) + (data[7] << 8) + data[8]

            # certain messages specify a timeout
            if (data[10] & 0x20) != 0:
                duration = 2 ** (((data[11] & 0xF0) / 16)) * (data[11] & 0x0F) / 4
                data[10] = data[10] & ~0x20
                self.TriggerEvent(FS20FUNCTION[data[10]]+","+self.GetStringFromAddress(address), duration)
                return None

            self.TriggerEvent(FS20FUNCTION[data[10]]+","+self.GetStringFromAddress(address))
            return None

        # check if it is a HMS message
        if (length == 0x0E) and \
           (telegramType == 0x04) and \
           ((data[3] & 0xF0 == 0x10) or (data[3] & 0xF0 == 0x50) or (data[3] & 0xF0 == 0x90)) and \
           (data[4] == 0xA0) and \
           (data[5] == 0x01):

            address = (data[6] << 8) + data[7]

            # determine the name of the HMS device
            deviceName = HMS_DEVICES[data[3] & 0x0F]

            # handle water detector
            if deviceName == "HMS100WD":
                battery = "Batt: OK"
                water   = "Water: No"

                if (data[3] & 0x40) != 0:
                    battery = "Batt: Empty"
                elif (data[10] & 0x80) != 0:
                    battery = "Batt: Replaced"

                # check water sensor
                if (data[10] & 0x0F) != 0:
                    water = "Water: Yes"

                self.TriggerEvent(deviceName +","+ water +","+str(address), battery)
                return None

            # handle temperature sensor
            if deviceName == "HMS100T":
                battery = "Batt: OK"
                temp    = "Temp: "

                if (data[3] & 0x40) != 0:
                    battery = "Batt: Empty"
                elif (data[10] & 0x80) != 0:
                    battery = "Batt: Replaced"

                #check if it a negative temperature
                if (data[10] & 0x10) != 0:
                    temp = '-'

                temp = temp + str(data[12] & 0x0F) + \
                       str((data[11] & 0xF0) >> 4) + \
                       '.' + \
                       str((data[11] & 0x0F))

                self.TriggerEvent(deviceName +","+str(address), temp +","+ battery)
                return None

            self.TriggerEvent(deviceName)
            return None

        print "HMS/FS20 device not implemented"
        
        
    def WriteFhzNoWait(self, telegramType, *args):
        crc = 0xff & sum(args)
        dataStr = "".join([chr(x) for x in args])
        data = "\x81" + chr(len(dataStr) + 2) + chr(telegramType) + chr(crc) + dataStr
        if eg.debugLevel:
            print "W: " + " ".join(["%02X" % ord(c) for c in data])
        self.receiveThread.Write(data)
        time.sleep(0.01)

        
    def WriteFhz(self, telegramType, *args):
        maxTime = time.clock() + 1.0
        dwStatus = DWORD()
        while True:
            d2xx.FT_GetModemStatus(self.ftHandle, byref(dwStatus))
            if dwStatus.value & 0xFF == 48:
                break
            if time.clock() > maxTime:
                self.PrintError("FHZ timeout error!")
                return
            time.sleep(0.01)
        self.WriteFhzNoWait(telegramType, *args)
        
        
    def ReadFhz(self):
        startByte = self.Read(1)
        if startByte != "\x81":
            self.PrintError("Wrong start byte.")
            return None
            # raise FhzException("Wrong start byte.")
        length = ord(self.Read(1))
        data = [ord(c) for c in self.Read(length)]
        telegramType = data[0]
        crc = data[1]
        newCrc = 0xff & sum(data[2:])
        if eg.debugLevel:
            dataStr = " ".join(["%02X" % x for x in data])
            print ("-> %02X %02X " % (ord(startByte), length)) + dataStr
        return telegramType, data[2:]
    
    
    def Read(self, numBytes):
        data = self.receiveThread.Read(numBytes, 1.0)
        if len(data) < numBytes:
            self.PrintError("FHZ read timeout error!")
        return data
        
    
        
    def GetTimeData(self):
        t_struct = time.localtime(self.nextTaskTime)
        year = t_struct.tm_year % 100 
        return(
            0xc9, 0x02, 0x01, 0x61, 
            year, t_struct.tm_mon, t_struct.tm_mday, 
            t_struct.tm_hour, t_struct.tm_min
        )
        
        
    def TimeScheduleTask(self, repeats=1):
        """
        Send the current time 50 times and schedule the next execution at the
        next minute.
        """
        data = self.GetTimeData()
        for i in range(repeats):
            eg.actionThread.CallWait(partial(self.WriteFhzNoWait, *data))
        self.nextTaskTime += 60.0
        self.timeTask = eg.scheduler.AddTaskAbsolute(
            self.nextTaskTime, 
            self.TimeScheduleTask
        )

        
    
class ActionBase(eg.ActionBase):
    defaultAddress = 0x094001
    funccode = None # must be assigned by subclass
    
    def __call__(self, address):
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        self.plugin.WriteFhz(0x04, 0x02, 0x01, 0x01, a2, a1, a0, self.funccode)


    def GetLabel(self, _address):
        return self.name
    
    
    def GetStringFromAddress(self, address):
        valueStr = ""
        for i in range(11, -1, -1):
            x = (address >> i*2) & 0x03
            valueStr += str(x + 1)
        return valueStr
        
        
    def GetAddressFromString(self, addressString):
        address = 0
        for i in range(12):
            address <<= 2
            address += int(addressString[i]) - 1
        return address
        
    
    def Configure(self, address=None):       
        if address is None:
            address = self.defaultAddress
            
        panel = eg.ConfigPanel()
            
        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(self.GetStringFromAddress(address))

        panel.AddLine("Address:", maskedCtrl)
        
        while panel.Affirmed():
            address = self.GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address)
            


class Dim(ActionBase):
    name = "Set dim-level"
    
    def __call__(self, address, level):
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        self.plugin.WriteFhz(0x04, 0x02, 0x01, 0x01, a2, a1, a0, level)
    
    
    def GetLabel(self, address, level):
        return "Set dim-level to %.02f %%" % (level * 100.00 / 16)
    
    
    def Configure(self, address=None, level=1):       
        if address is None:
            address = self.defaultAddress
        panel = eg.ConfigPanel()
            
        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(self.GetStringFromAddress(address))
        
        def LevelCallback(value):
            return "%.02f %%" % (value * 100.00 / 16)
        
        levelCtrl = eg.Slider(
            panel, 
            value=level, 
            min=1, 
            max=16, 
            minLabel="6.25 %",
            maxLabel="100.00 %",
            style = wx.SL_AUTOTICKS|wx.SL_TOP,
            size=(300,-1),
            levelCallback=LevelCallback
        )
        levelCtrl.SetMinSize((300, -1))
        
        panel.AddLine("Address:", maskedCtrl)
        panel.AddLine("Level:", levelCtrl)
        
        while panel.Affirmed():
            address = self.GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(
                address, 
                levelCtrl.GetValue(),
            )
            
            
            
class Off(ActionBase):
    funccode = 0x00
    
    
    
class On(ActionBase):
    funccode = 0x11
        
        
        
class ToggleDim(ActionBase):
    name = "Toggle dimming"
    funccode = 0x12
    
    

class DimUp(ActionBase):
    name = "Dim up"
    funccode = 0x13
    


class DimDown(ActionBase):
    name = "Dim down"
    funccode = 0x14
    
    

class Toggle(ActionBase):
    funccode = 0x15
    
    

class StartProgramTimer(ActionBase):
    name = "Start/stop programming timer"
    funccode = 0x16
    
    

class ResetToFactoryDefaults(ActionBase):
    name = "Reset to factory defaults"
    funccode = 0x1b

