# -*- coding: utf-8 -*-
#
# plugins/nest/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg

eg.RegisterPlugin(
    name = "Nest Thermostat",
    author = "Jason Kloepping",
    version = "2014.0509.0829",
    kind = "external",
    description = "Adds Actions to Control Nest Thermostat(s).  Information logging is available.",
)
    
# Change log:
# ----------
# 2013-04-13 Jason Kloepping
#   * initial version
#       Connecting to and getting information from devices
#       Very basic configure screen
#       Set commands for temp, fan 
#   version 2013.0415.1852
#       changed the current temp on event to reflect temperature scale.
#   * 2013-05-31 and 2013-06-01
#       changed so that set temp can be a variable
#   * 2013-06-13
#       minor bug fix 
#   * 2013-06-23
#       added error handling for initial login and retrieval
#   * 2013-06-24
#       added away setting
#   * 2013-08-06
#       added logging to text file
#   * 2013-09-05
#       added set temp range
#   * 2013-09-06
#       added set away temp range
#       added set away temp  (not sure this is the right way to do it)
#       added set mode (off, heat, cool, range)
#       added descriptions and names to all actions
#   * 2013-09-08
#       changed the configuration screens for all set commands.
#   * 2013-09-11
#       Added in all structure objects as well.
#   * 2013-09-12
#       Added a better output to time_to_target
#   * 2013-09-13
#       Actions, descriptions, and log messages reworked.  (from Abuttino)
#       Working on better get time_to_target
#   * 2013-10-12
#       Removed extra testing TTT
#       Fixed fan mode and temperature mode problem
#   * 2013-12-23
#       Changed the output of current temp and all other temp to reflect the temperature scale used in the thermostat.
#   * 2014-01-17
#       Changed the logging to reflect the temperature scale of the device.
#   * 2014-01-18
#       Re-added the correct calculations for Time To Target output
#   * 2014-02-27
#       Changed the way get object makes its list (now when Nest adds or changes values they are automatically changed).
#           This means anything added from firmware versions 3.5.1 and 4.0 are added.
#           Now when calling get_object() it is a string not an integer.
#       Changed set_heat_cool_mode, set_fan, set_away for better presentation
#   * 2014-03-01
#       fixed bug from changes in set away and set fan
#       Added turn on/off/set % humidity for humidifier/dehumidifier setups
#       Added set break even dual fuel outside temp (temp scale according to your settings)
#       Added enable/disable auto away feature
#   * 2014-03-14    Beta
#       Major change to add selectable devices in all actions that are needed.
#       Added Checker inside all actions and action configure to prevent errors in the log screen.
#   * 2014-03-16
#       Changed the nest events so ALL carry payload of event data, thermostat name.
#   * 2014-03-22
#       Switch from sslv3 to tlsv1 for nest security.
#   * 2014-03-23
#       Fixed bug in get object from Timestamp and Time To Target
#       Removed urllib, urllib2, httplib as no longer needed
#   * 2014-03-29
#       Added an internal set time to relogin.  To help minimize retrieval errors if left on for more than 48 hours with no user interaction.
#       Fixed an issue if the plugin was restarted, multiple threads could be generated for status retrieval.
#       Added Get Schedule Information action.
#       Added Current weather information to logging and get object.  Added check box in plugin config to enable/disable weather update events
#   *2014-04-10
#       Changed the automatic login to check every 15 minutes.  (Testing)
#   *2014-04-18
#       Reverted back to older style initial login for better reliability.
#   *2014-04-20
#       Alpha build to be tested by 
#   *2014-04-25
#       New Ciphers and private alpha release by abuttino
#   *2014-04-27
#       Release of new m2Crypto ssl connections
#       minor fix in get_object for weather
#       logs now show what device they come from again, thermostats, structure, or weather
#       Added fan duty-cycle(per our fan time) with bounding hours
#       Added fan timer function
#   *2014-05-03
#       Added full log output after a specified time (setting in plugin config) (Abuttino)
#       Password is now hidden in plugin config (Abuttino)
#   *2014-05-06
#       Minor code cleanup in several locations
#       Preliminary 10 day energy information output
#   *2014-05-09
#       Added Heat Index f and Wind Chill f in to the weather (via calculations)


# init.py was heavily modelled and some copied from: originated from https://github.com/smbaker/pynest
# (nest.py) -- a python interface to the Nest Thermostat
# by Scott M Baker, smbaker@gmail.com, http://www.smbaker.com/
#
# Usage:
#    'nest.py help' will tell you what to do and how to do it
#
# Licensing:
#    This is distributed under the Creative Commons 3.0 Non-commercial,
#    Attribution, Share-Alike license. You can use the code for non-commercial
#    purposes. You may NOT sell it. If you do use it, then you must make an
#    attribution to me (i.e. Include my name and thank me for the hours I spent
#    on this)
#
# Acknowledgements:
#    Chris Burris's Siri Nest Proxy was very helpful to learn the nest's
#       authentication and some bits of the protocol.

#Acknowledgment:
#   This plugin uses M2Crypto from
#   https://github.com/martinpaljak/M2Crypto        -   Current maintainer.


import time
import string
import sys
import ssl
import urllib
import urllib2
import threading
import re 
import math
try:
    import M2Crypto
except ImportError:
    print "Please put M2Crypto module in the main eventghost folder"
    print "A copy can be found in the Nest Thermostat plugin forum thread @"
    print "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5439"
from cStringIO import StringIO
from optparse import OptionParser
from datetime import datetime, timedelta
from M2Crypto import SSL, httpslib, m2urllib, m2urllib2


try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "No json library available. I recommend installing either python-json"
        print "or simplejson."
        sys.exit(-1)
        
def loads(res):
    if hasattr(json, "loads"):
        res = json.loads(res)
    else:
        res = json.read(res)
    return res
    
def Setter(self, data, DevSerial, area):
    transport = str(self.plugin.transport_url)
    transport = transport.replace('https://', '')
    transport = str(transport.replace(':443', ''))

    #ctx = str('tlsv1')
    ctx = SSL.Context('tlsv1')
    h = httpslib.HTTPSConnection(transport, 443, ssl_context=ctx)
    h.set_debuglevel(0)
    h.putrequest('POST', str("/v2/put/" + area + DevSerial))
    h.putheader('user-agent', 'Nest/2.1.3 CFNetwork/548.0.4')
    h.putheader('Authorization', str('Basic ' + str(self.plugin.access_token)))
    h.putheader('X-nl-user-id', str(self.plugin.userid))
    h.putheader('X-nl-protocol-version', '1')
    h.putheader('Accept-Language', 'en-us')
    h.putheader('Connection', 'keep-alive')
    h.putheader('Content-Length', str(len(data)))
    h.putheader('Accept', '*/*')
    h.endheaders()
    h.send(data)
    resp = h.getresponse()
    
    
class Nest(eg.PluginClass):
    TempScale = "C"
    SignedIN="False"
    class text:
        generalBox = "General Settings"
        index = "Device:"
        logging = "Logging:"
        loglocation = "Log Location:"
        tbu = "Seconds Between Forced (Full) Log Updates :"
        authBox = "Basic Authentication"
        username = "Username:"
        password = "Password:"
        weather = "Weather Events:"
    class Device:
        def __init__(self, serial=None,structure=None,name=None,objects=[],energy=[]):
            self.serial = serial
            self.structure = structure
            self.name = name
            self.objects = objects
            self.energy = energy
    CurrentWeather = []

    def Configure(self, index=0, logging=False, loglocation="", username="", password="", weather_events=False, tbu="", serial=None):

        self.abort = True
        text = self.text
        panel = eg.ConfigPanel(self)

        loggingCtrl = panel.CheckBox(logging)
        loglocationCtrl = panel.TextCtrl(loglocation)
        tbuCtrl = panel.TextCtrl(str(tbu))
        weatherCtrl = panel.CheckBox(weather_events)
        usernameCtrl = panel.TextCtrl(username)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)

        labels = (
            panel.StaticText(text.logging),
            panel.StaticText(text.loglocation),
            panel.StaticText(text.tbu),
            panel.StaticText(text.username),
            panel.StaticText(text.password),
            panel.StaticText(text.weather),
        )
        eg.EqualizeWidths(labels)

        ACV = wx.ALIGN_CENTER_VERTICAL
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[0], 0, ACV)
        sizer.Add(loggingCtrl)
        sizer.Add(labels[1], 0, ACV)
        sizer.Add(loglocationCtrl)
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(tbuCtrl)
        sizer.Add(labels[5], 0, ACV)
        sizer.Add(weatherCtrl)
        staticBox = wx.StaticBox(panel, label=text.generalBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(usernameCtrl)
        sizer.Add(labels[4], 0, ACV)
        sizer.Add(passwordCtrl)
        staticBox = wx.StaticBox(panel, label=text.authBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP, 10)

        while panel.Affirmed():
            panel.SetResult(
                index,
                loggingCtrl.GetValue(),
                loglocationCtrl.GetValue(),
                usernameCtrl.GetValue(),
                passwordCtrl.GetValue(),
                weatherCtrl.GetValue(),
                tbuCtrl.GetValue()
            )

    def __init__(self):
        self.AddAction(get_object)
        self.AddAction(set_heat_cool_mode)
        self.AddAction(set_temp)
        self.AddAction(set_range)
        self.AddAction(set_fan)
        self.AddAction(set_fan_with_timer)
        self.AddAction(set_auto_away)
        self.AddAction(set_away)
        self.AddAction(set_away_temp)
        self.AddAction(set_away_range)
        self.AddAction(set_humidity_mode)
        self.AddAction(set_humidity_level)
        self.AddAction(set_dual_fuel_breakpoint)
        self.AddAction(Schedule_Information)
        self.AddAction(get_energy_object)

    def __start__(self, index, logging, loglocation, username, password, weather_events, tbu):
        self.serials = ["False_Thermostat"]
        self.DeviceNames = ["False Thermostat"]
        self.logging = logging
        self.loglocation = loglocation
        self.username = username
        self.password = password
        self.WeatherEvents = weather_events
        self.logtype = "new"
        self.SecBeforeFullLogUpdate = tbu
        self.ConnectErrorCount = 0
        self.Logged = False
        self.LoginCount = 0
        self.PluginStart = datetime.now()
        self.Values_Retrival_Time = self.PluginStart
        self.abort = False
        self.Values_timestamp = 0
        self.poll = threading.Thread(target = self.Polling, args = ())
        self.poll.start()

    def __stop__(self):
        self.abort = True
        self.first_run = True
        
    def Polling(self):
        y = self.login()
        if y == False:
            print "Failed to Login to Nest"
            eg.TriggerEvent("LoginError", prefix="Nest")
            return
        print "Nest: Login to Nest sucessful"
        x = self.get_status()
        if x == False:
            print "************Nest*****************"
            print "*"
            print "*"
            print "*"
            print "Initial Retrieval or Login failed"
            print "Terminating plugin"
            print "Restart plugin to regain functionality"
            eg.TriggerEvent("InitialError", prefix="Nest")
            return
        self.get_weather()
        self.save_status(True)
        for Dev in self.Devices:
            self.get_energy(Dev)
        eg.TriggerEvent("LoginSuccess", prefix="Nest")
        counter = 0
        counter2 = 0
        while (self.abort == False):
            counter = counter + 1
            if counter  == 30:
                counter2 = counter2 + 1
                counter = 0
                if counter2 == 5760:
                    counter2 = 0
                    for Dev in self.Devices:
                        self.get_energy(Dev)
                self.get_weather()
                sucess = self.get_status()
                if sucess:
                    if datetime.now() > self.LastFullLog + timedelta(seconds=int(self.SecBeforeFullLogUpdate)):
                        self.save_status(True)
                    else:
                        self.save_status()
            time.sleep(0.5)   #in seconds

    def login(self):
        try:
            #in try in case of connectivity errors
            data = urllib.urlencode({"username": self.username, "password": self.password})

            req = urllib2.Request("https://home.nest.com/user/login",
                        data,
                        {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4"})
                        
            response = urllib2.urlopen(req).read()

            res = loads(response)
            self.transport_url = res["urls"]["transport_url"]
            self.weather_url = res["urls"]["weather_url"]
            self.access_token = res["access_token"]
            self.userid = res["userid"]
            self.PassExpire = res["expires_in"]
            self.LoginExpires = datetime.now() + timedelta(hours=47)
            self.SignedIN="True"
            self.LoginCount = self.LoginCount + 1
            return True
        except:
            return False

    def get_weather(self):
        try:
            #in try in case of connectivity errors
            response = urllib2.urlopen(eg.plugins.Nest.plugin.weather_url + eg.plugins.Nest.plugin.ZIP).read()
            res = loads(response)
            self.weather_status = res
            return True
        except:
            return False
            
    def get_status(self):
        if self.LoginExpires < datetime.now():  #A check if login will expire soon.  If true then re login.
            self.login()
        if self.Values_Retrival_Time < (datetime.now() - timedelta(minutes=15)):
            self.login()
        try:
            #in try in case of connectivity errors

        
            userid = str(self.userid)
            transport_url = str(self.transport_url)
            access_token = str(self.access_token)
            getreq = str('/v2/mobile/user.' + userid)
            auth = str('Basic ' + access_token)
            uid = str(userid)
            transport = transport_url
            transport = transport.replace('https://', '')
            transport = str(transport.replace(':443', ''))
 

            ctx = SSL.Context('tlsv1')
            h = httpslib.HTTPSConnection(transport, 443, ssl_context=ctx)
            h.set_debuglevel(0)
            h.putrequest('GET', getreq)
            h.putheader('user-agent', 'Nest/2.1.3 CFNetwork/548.0.4')
            h.putheader('Authorization', auth)
            h.putheader('X-nl-user-id', uid)
            h.putheader('X-nl-protocol-version', '1')
            h.putheader('Accept-Language', 'en-us')
            h.putheader('Connection', 'keep-alive')
            h.putheader('Accept', '*/*')
            h.endheaders()
            resp = h.getresponse()
            response = resp.read()
            res = loads(response)


            #get devices/serials/structure id of each
            try:
                self.Devices
            except:
                self.Devices = []
                for ser in res["link"].keys():
                    struc = res["link"][ser]["structure"]
                    struc = struc.split(".")[1]
                    name = res["shared"][ser]["name"]
                    self.Devices.append(self.Device(ser, struc, name))
            

            #get first structure zip for weather info
            self.ZIP = res["structure"][self.Devices[0].structure]["postal_code"]
            
            #get and set tempscale
            self.TempScale = res["device"][self.Devices[0].serial]["temperature_scale"]
            
            self.status = res

            self.Values_Retrival_Time = datetime.now()
            self.ConnectErrorCount = 0
            return True
        except:
            print "Nest: Unable to retrieve data"
            self.ConnectErrorCount = self.ConnectErrorCount + 1
            if self.ConnectErrorCount > 240:
                eg.TriggerEvent("RetrievalError", prefix="Nest")
            return False

    def get_energy(self, Dev):
        try:
            #get 10 day energy from Nest
            transport = self.transport_url
            transport = transport.replace('https://', '')
            transport = str(transport.replace(':443', ''))
            getreq = str('/v5/subscribe')
            dat = str('{"objects":[{"object_key":"energy_latest.' +Dev.serial +'"}]}')
            content = str(len(dat))
            ctx = SSL.Context('tlsv1')
            h = httpslib.HTTPSConnection(transport, 443, ssl_context=ctx)
            h.set_debuglevel(0)
            h.putrequest('POST', getreq)
            h.putheader('user-agent', 'Nest/2.1.3 CFNetwork/548.0.4')
            h.putheader('Authorization', str('Basic ' + str(self.access_token)))
            h.putheader('X-nl-user-id', str(self.userid))
            h.putheader('X-nl-protocol-version', '1')
            h.putheader('Content-Length', content)
            h.putheader('Accept-Language', 'en-us')
            h.putheader('Connection', 'keep-alive')
            h.putheader('Accept', '*/*')
            h.endheaders()
            h.send(dat)
            resp = h.getresponse()
            response = resp.read()
            res = loads(response)
            eg.TriggerEvent('Energy.Retrieved', prefix='Nest')
        except:
            print "Failed to get energy report from Nest"
            return
            
        
        OldEnergy = []
        #read from file if it exists
        try:
            r = open(eg.localPluginDir + "\\Nest." + Dev.serial + ".txt","r")
            for line in r.readlines():
                OldEnergy.append(loads(line))
            r.close()
        except:
            print "Old energy log not found"
            
            
        #try to read data, save list of days recorded
        OldEnergyDays = []
        try:
            for day in OldEnergy:
                OldEnergyDays.append(day['day'])
        except:
            print "Failed to read log data"
        
        #write to file (writes only new entries) (new entries are also stored Back into OldEnergy)
        with open(eg.localPluginDir + "\\Nest." + Dev.serial + ".txt","a") as outfile:
            for x in res["objects"]:
                for y in x["value"]["days"]:
                    #check if y["day"] already exists
                    if y["day"] in OldEnergyDays:
                        pass
                    else:
                        json.dump(y,outfile)
                        OldEnergy.append(y)
                        outfile.write("\n")
        
        #Copies OldEnergy into Device.energy for the appropriate Serial number
        Dev.energy = list(OldEnergy)
        
            
    def temp_in(self, temp):
        if (self.TempScale == "F"):
            return (temp - 32.0) / 1.8
        else:
            return temp

    def temp_out(self, temp):
        if (self.TempScale == "F"):
            return temp*1.8 + 32.0
        else:
            return temp

    def Nest_Events(self, category, data, device):
        pay = [device, data]
        if category == "auto_away" or category == "dehumidifier_state" or category == "fan_cooling_state" or category == "hvac_ac_state" or category == "hvac_alt_heat_state" or category == "hvac_alt_heat_x2_state" or category == "hvac_aux_heater_state" or category == "hvac_cool_x2_state" or category == "hvac_emer_heat_state" or category == "hvac_fan_state" or category == "hvac_heat_x2_state" or category == "hvac_heat_x3_state" or category == "hvac_heater_state":
            eg.TriggerEvent(category + "." + data, prefix="Nest", payload=pay)
        else:
            eg.TriggerEvent(category, prefix="Nest", payload=pay)

    def save_status(self, first=False):
        if first:
            self.LastFullLog = datetime.now()
            
        self.text.objects = []
        
        self.schedule = self.status["schedule"]
        
        if self.logging:
            fo = open(self.loglocation, "a")
            if self.logtype == "new":
                fo.write( '\n' )
                if first != True:
                    self.logtype = "old"
                    
        self.CurrentWeather= []            
        for wet in sorted(self.weather_status[self.ZIP]["current"].keys()): #weather data current
            strwet = str(wet)
            for char in strwet:
                if char in " ?.!/;:$":
                    strwet = strwet.replace(char,'')
            self.CurrentWeather.append(strwet)
            if self.logging and first == True:
                stringz =  "weather_current_" + str(strwet)
                fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + stringz.ljust(65) + str(self.weather_status[self.ZIP]["current"][wet])))
                fo.write('\n')
            if first != True:
                if getattr(self, "Values_weather_current_" + str(strwet)) != self.weather_status[self.ZIP]["current"][wet]:
                    #writing to file if logging enabled
                    if self.logging:
                        stringz =  "weather_current_" + str(strwet)
                        fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.weather_status[self.ZIP]["current"][wet])))
                        fo.write('\n')
                        self.logtype = "new"
                   #if value has changed then issue an event
                    if self.WeatherEvents:
                        self.Nest_Events(str(strwet),str(self.weather_status[self.ZIP]["current"][wet]), "weather_current")
            setattr(self, "Values_weather_current_" + str(strwet), self.weather_status[self.ZIP]["current"][wet])
            self.CurrentWeather.append(str(strwet))
        #now calc Heat Index and Wind Chill
        T = self.Values_weather_current_temp_f
        RH = self.Values_weather_current_humidity
        W = self.Values_weather_current_wind_mph
        HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH        
        if T > 79 and T < 88 and RH > 85:       #adjustment if RH is above 85
            HI = HI + (RH-85)/10 * (87-T)/5
            #HI = int(round(float(HI)))
        elif T > 80 and T < 112 and RH < 13:       #adjustment if RH is below 13
            x = math.fabs(T-95)
            x = math.sqrt((17-x)/17)
            HI = HI - ((13-RH)/4)*x
            #HI = int(round(float(HI)))
        elif T < 81:                        #If T is outside normal range
            HI = 0.5 * (T + 61.0 + ((T-68.0)*1.2) + (RH*0.094))
            #HI = int(round(float(HI)))
        y = math.pow(W,0.16)
        WC = 35.74 + 0.6215*T - 35.75*y + 0.4275*T*y
        strwet = "heat_index_f"
        if self.logging and first == True:
            stringz =  "weather_current_" + str(strwet)
            fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + stringz.ljust(65) + str(HI)))
            fo.write('\n')
        if first != True:
            HI = int(round(float(HI)))
            if getattr(self, "Values_weather_current_" + str(strwet)) != HI:
                #writing to file if logging enabled
                if self.logging:
                    stringz =  "weather_current_" + str(strwet)
                    fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(HI)))
                    fo.write('\n')
                    self.logtype = "new"
               #if value has changed then issue an event
                if self.WeatherEvents:
                    self.Nest_Events(str(strwet),str(int(round(float(HI)))), "weather_current")
        setattr(self, "Values_weather_current_" + str(strwet), int(round(float(HI))))
        self.CurrentWeather.append(str(strwet))
        strwet = "wind_chill_f"
        #WC = int(round(float(WC)))
        if self.logging and first == True:
            stringz =  "weather_current_" + str(strwet)
            fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + stringz.ljust(65) + str(WC)))
            fo.write('\n')
        if first != True:
            WC = int(round(float(WC)))
            if getattr(self, "Values_weather_current_" + str(strwet)) != WC:
                #writing to file if logging enabled
                if self.logging:
                    stringz =  "weather_current_" + str(strwet)
                    fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(WC)))
                    fo.write('\n')
                    self.logtype = "new"
               #if value has changed then issue an event
                if self.WeatherEvents:
                    self.Nest_Events(str(strwet),str(WC), "weather_current")
        setattr(self, "Values_weather_current_" + str(strwet), WC)
        self.CurrentWeather.append(str(strwet))
        DevCounter = -1
        for Dev in self.Devices:
            objects = []
            DevCounter = DevCounter + 1
            self.status["structure"][Dev.structure]["name"] = str(self.status["structure"][Dev.structure]["name"]).replace(" ", "_").lower()
            for x in sorted(self.status["structure"][Dev.structure].keys()):    #these values are NOT thermostat specific      and are labeled as StructureName.XXX
                strx = str(x)
                for char in strx:
                    if char in " ?.!/;:$":
                        strx = strx.replace(char,'')
                if self.logging and first == True:
                    stringz = str(self.status["structure"][Dev.structure]["name"]) + "_" + strx
                    fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.status["structure"][Dev.structure][x])))
                    fo.write('\n')
                if first != True:
                    if getattr(self, "Values_" + str(self.status["structure"][Dev.structure]["name"]) + "_structure_" +str(strx)) != self.status["structure"][Dev.structure][x]:
                        #writing to file if logging enabled
                        if self.logging:
                            stringz = str(self.status["structure"][Dev.structure]["name"]) + "_" + strx
                            fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.status["structure"][Dev.structure][x])))
                            fo.write('\n')
                            self.logtype = "new"
                        #if value has changed then issue an event
                        self.Nest_Events(str(strx),str(self.status["structure"][Dev.structure][x]), str(self.status["structure"][Dev.structure]["name"]))
                setattr(self, "Values_" + str(self.status["structure"][Dev.structure]["name"]) + "_structure_"+ str(strx), self.status["structure"][Dev.structure][x])
                strx = strx.replace("_", " ")
                strx = string.capwords(strx)
                objects.append(str("structure_" +str(strx)))   
            VarHelper = str(self.status["shared"][Dev.serial]["name"])
            VarHelper = VarHelper.replace(" ","_")
            VarHelper = VarHelper.lower()
            for x in sorted(self.status["shared"][Dev.serial]):     #these values are thermostat specific  and are labeled  as DeviceName.xxx
                strx = str(x)
                for char in strx:
                    if char in " ?.!/;:$":
                        strx = strx.replace(char,'')
                if str(strx) == "away_temperature_high" or str(strx) == "away_temperature_low" or str(strx) == "compressor_lockout_leaf" or str(strx) == "current_temperature" or str(strx) == "dual_fuel_breakpoint" or str(strx) == "heat_pump_aux_threshold" or str(strx) == "heat_pump_comp_threshold" or str(strx) == "leaf_away_high" or str(strx) == "leaf_away_low" or str(strx) == "leaf_threshold_cool" or str(strx) == "leaf_threshold_heat" or str(strx) == "lower_safety_temp" or str(strx) == "target_temperature" or str(strx) == "target_temperature_high" or str(strx) == "target_temperature_low" or str(strx) == "temperature_lock_high_temp" or str(strx) == "temperature_lock_low_temp" or str(strx) == "upper_safety_temp":
                    self.status["shared"][Dev.serial][x] = self.temp_out(float(self.status["shared"][Dev.serial][x]))
                if self.logging and first == True:
                    stringz = Dev.name + "_" + strx
                    fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.status["shared"][Dev.serial][x])))
                    fo.write('\n') 
                if first != True:
                    if getattr(self, "Values_" + VarHelper + "_shared_" +str(strx)) != self.status["shared"][Dev.serial][x]:
                        #writing to file if logging enabled
                        if self.logging:
                            stringz = Dev.name + "_" + strx
                            fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.status["shared"][Dev.serial][x])))
                            fo.write('\n')
                            self.logtype = "new"
                            #self.LastLogTime = time.time()
                        self.Nest_Events(str(strx),str(self.status["shared"][Dev.serial][x]), VarHelper)
                setattr(self, "Values_" + VarHelper + "_shared_"+ str(strx), self.status["shared"][Dev.serial][x])
                strx = strx.replace("_", " ")
                strx = string.capwords(strx)
                objects.append(str("shared_" +str(strx)))
            for x in sorted(self.status["device"][Dev.serial]):     #these values are thermostat specific  and are labeled  as DeviceName.xxx
                strx = str(x)
                for char in strx:
                    if char in " ?.!/;:$":
                        strx = strx.replace(char,'')
                if str(strx) == "away_temperature_high" or str(strx) == "away_temperature_low" or str(strx) == "compressor_lockout_leaf" or str(strx) == "current_temperature" or str(strx) == "dual_fuel_breakpoint" or str(strx) == "heat_pump_aux_threshold" or str(strx) == "heat_pump_comp_threshold" or str(strx) == "leaf_away_high" or str(strx) == "leaf_away_low" or str(strx) == "leaf_threshold_cool" or str(strx) == "leaf_threshold_heat" or str(strx) == "lower_safety_temp" or str(strx) == "target_temperature" or str(strx) == "target_temperature_high" or str(strx) == "target_temperature_low" or str(strx) == "temperature_lock_high_temp" or str(strx) == "temperature_lock_low_temp" or str(strx) == "upper_safety_temp":
                    self.status["device"][Dev.serial][x] = self.temp_out(float(self.status["device"][Dev.serial][x]))
                if self.logging and first == True:
                    stringz = Dev.name + "_" + strx
                    fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.status["device"][Dev.serial][x])))
                    fo.write('\n')
                if first != True:
                    if getattr(self, "Values_" + VarHelper + "_device_" +str(strx)) != self.status["device"][Dev.serial][x]:
                        #writing to file if logging enabled
                        if self.logging:
                            stringz = Dev.name + "_" + strx
                            fo.write(str(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')) + str(stringz.ljust(65)) + str(self.status["device"][Dev.serial][x])))
                            fo.write('\n')
                            self.logtype = "new"
                        #if value has changed then issue an event
                        self.Nest_Events(str(strx),str(self.status["device"][Dev.serial][x]), VarHelper)
                setattr(self, "Values_" + VarHelper + "_device_"+ str(strx), self.status["device"][Dev.serial][x])
                strx = strx.replace("_", " ")
                strx = string.capwords(strx)
                objects.append(str("device_" +str(strx)))
            self.Devices[DevCounter].objects = objects
        if self.logging:
                fo.close()

class get_object(eg.ActionBase):

    class text:
        name = "Get Nest Object"
        description = "Get an Attribute from the Nest Thermostat(s)"
        
    def __call__(self, object, Dev):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if Dev != "Weather":
            for x in self.plugin.Devices:
                if x.name == Dev:
                    struc = x.structure     #this is the internal name
                    StrucName = self.plugin.status["structure"][struc]["name"]  #this is the common name  (what we need)
            if object[:9] == "structure":
                object = StrucName + "_" + object
            else:
                object = Dev + "_" + object
        else:
            object = "weather_current_" + object
        object = object.lower()
        object = object.replace(" ","_")
        object = "Values_" + object
        #After this line individual outputs can be isolated and extra processing can occur
        search = re.search(r"timestamp\b",object)
        if search:
            return (datetime.fromtimestamp((float(getattr(self.plugin, object)))/1000))
        search = re.search(r"time_to_target\b",object)
        if search:
            if getattr(self.plugin, object) == 0:
                return(getattr(self.plugin, object))
            else:
                stamp = datetime.now()
                target = datetime.fromtimestamp(float(getattr(self.plugin, object)))
                ttt = target - stamp
            return(ttt)
        #if normal data (all other data sets)
        return(getattr(self.plugin, object))
        
    def Configure(self, object="", Dev = "Weather"):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevWeaChoices = []
        self.DevWeaChoices.append("Weather")
        for x in self.plugin.Devices:
            self.DevWeaChoices.append(x.name)
        wx.StaticText(panel, label="Device or Weather: ", pos=(10, 10))
        self.statChoice = wx.Choice(panel, pos=(10, 30), choices=self.DevWeaChoices)
        self.statChoice.Bind(wx.EVT_CHOICE, self.CategoryChanged)
        self.statChoice.Select(self.DevWeaChoices.index(Dev))
        self.objects = ["fake with a realllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllly long string"]
        wx.StaticText(panel, label="Object: ", pos=(10, 60))
        self.statObject = wx.Choice(panel, pos=(10, 80), choices=self.objects)
        self.CategoryChanged()
        if object in self.objects:
            self.statObject.SetStringSelection(object)
        
                
        while panel.Affirmed():
            panel.SetResult(
                self.objects[self.statObject.GetSelection()],
                self.DevWeaChoices[self.statChoice.GetSelection()]
                
            )
            
    def CategoryChanged(self, event=None):
        cat = self.DevWeaChoices[self.statChoice.GetSelection()]
        if cat == "Weather":
            self.objects = list(set(self.plugin.CurrentWeather))
        else:
            index = self.DevWeaChoices.index(cat) -1
            self.objects = self.plugin.Devices[index].objects
        self.statObject.Clear()
        self.statObject.AppendItems(self.objects)
        self.statObject.SetSelection(0)

class set_heat_cool_mode(eg.ActionBase):

    class text:
        name = "Set Heat/Cool Mode"
        description = "Set the Mode for a Nest Thermostat.  Modes are: Off, Heat, Cool, Range."
        states = ["Off", "Heat", "Cool", "Range"]
        
    def __call__(self, mode, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not str(mode).isdigit():
            mode = mode.lower()
            if mode != "cool":
                if mode != "heat":
                    if mode != "range":
                        if mode != "off":
                            print "Invalid Variable Data"
                            return
        else:
            try:
                mode = self.text.states[mode].lower()
            except:
                print "Invalid Variable Data"
                return
        data = json.dumps({"target_temperature_type":str(mode)})
        Setter(self, data, DevSerial, "shared.")

    def Configure(self, state="Off", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="HVAC Mode: ", pos=(10, 10))
        statChoice = wx.Choice(panel, pos=(10, 30), choices=self.text.states)
        statChoice.Select(self.text.states.index(state))
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(
                self.text.states[statChoice.GetSelection()],
                SerialSave      #want to output serial
            )

class set_temp(eg.ActionBase):

    class text:
        name = "Set Temperature"
        description = "Set the Temperature. (Same as Physically Turning The Dial.)"

    def __call__(self, temp, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not temp.isdigit():
            try:
                if str(eval(temp)).strip().isdigit():
                    temp = str(eval(temp)).strip()
                else:
                    print "Invalid Variable Data"
                    return
            except:
                print "Invalid Input"
                return
        temp = self.plugin.temp_in(float(temp))
        data = '{"target_change_pending":true,"target_temperature":' + '%0.1f' % temp + '}'
        Setter(self, data, DevSerial, "shared.")

    def Configure(self, temp="", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Temperature: ", pos=(10, 10))
        textControl = wx.TextCtrl(panel, pos=(10, 30), value=temp)
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(textControl.GetValue(),SerialSave)      #want to output serial)

class set_away_temp(eg.ActionBase):

    class text:
        name = "Set Away Temperature"
        description = "Set Away Temperature. (Works sometimes, have had issues.)"

    def __call__(self, temp, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not temp.isdigit():
            try:
                if str(eval(temp)).strip().isdigit():
                    temp = str(eval(temp)).strip()
                else:
                    print "Invalid Variable Data"
                    return
            except:
                print "Invalid Input"
                return
        temp = self.plugin.temp_in(float(temp))
        for x in self.plugin.Devices:
            if x.serial == serial:
                DevName = x.name
        if "Value_" + x.name + "_device_" + "away_temperature_low_enabled" == True and "Value_" + x.name + "_device_" + "away_temperature_high_enabled" == True:
            data = '{"away_temperature_high":' + '%0.1f' % temp + ',"away_temperature_low":' + '%0.1f' % temp + '}'
        elif "Value_" + x.name + "_device_" + "away_temperature_low_enabled" == True:
            data = '{"away_temperature_low":' + '%0.1f' % temp + '}'
        else:
            data = '{"away_temperature_high":' + '%0.1f' % temp + '}'
        Setter(self, data, DevSerial, "device.")

    def Configure(self, temp="", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Away Temperature: ", pos=(10, 10))
        textControl = wx.TextCtrl(panel, pos=(10, 30), value=temp)
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(textControl.GetValue(),SerialSave)

class set_range(eg.ActionBase):     

    class text:
        name = "Set Temperature Range"
        description = "Set Temperature Range. (Both High and Low Temperatures)"

    def __call__(self, high_temp, low_temp, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not high_temp.isdigit():
            try:
                if str(eval(high_temp)).strip().isdigit():
                    high_temp = str(eval(high_temp)).strip()
                else:
                    print "Invaid Variable Data in High Temp"
                    return
            except:
                print "Invalid Input in High Temp"
                return
        if not low_temp.isdigit():
            try:
                if str(eval(low_temp)).strip().isdigit():
                    low_temp = str(eval(low_temp)).strip()
                else:
                    print "Invalid Variable Data in Low Temp"
                    return
            except:
                print "Invalid Input in Low Temp"
                return
        high_temp = self.plugin.temp_in(float(high_temp))
        low_temp = self.plugin.temp_in(float(low_temp))
        data = '{"target_temperature_high":' + '%0.1f' % high_temp + ',"target_temperature_low":' + '%0.1f' % low_temp + '}'
        Setter(self, data, DevSerial, "shared.")

    def Configure(self, high_temp="", low_temp="", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="High Temperature: ", pos=(10, 10))
        textControlHigh = wx.TextCtrl(panel, pos=(10, 30), value=high_temp)
        wx.StaticText(panel, label="Low Temperature: ", pos=(10, 60))
        textControlLow = wx.TextCtrl(panel, pos=(10, 80), value=low_temp)
        wx.StaticText(panel, label="Device: ", pos=(10, 110))
        statDevice = wx.Choice(panel, pos=(10, 130), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(
                textControlHigh.GetValue(),
                textControlLow.GetValue(),
                SerialSave
            )

class set_away_range(eg.ActionBase):        

    class text:
        name = "Set Away Temperature Range"
        description = "Set Away Temperature Range (High and Low)"

    def __call__(self, high_temp, low_temp, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not high_temp.isdigit():
            try:
                if str(eval(high_temp)).strip().isdigit():
                    high_temp = str(eval(high_temp)).strip()
                else:
                    print "Invalid Variable Data in High Temp"
                    return
            except:
                print "Invalid Input in High Temp"
                return
        if not low_temp.isdigit():
            try:
                if str(eval(low_temp)).strip().isdigit():
                    low_temp = str(eval(low_temp)).strip()
                else:
                    print "Invalid Variable Data In Low Temp"
                    return
            except:
                print "Invalid Input In Low Temp"
                return
        high_temp = self.plugin.temp_in(float(high_temp))
        low_temp = self.plugin.temp_in(float(low_temp))
        data = '{"away_temperature_high":' + '%0.1f' % high_temp + ',"away_temperature_low":' + '%0.1f' % low_temp + '}'
        Setter(self, data, DevSerial, "device.")

    def Configure(self, high_temp="", low_temp="", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="High Temperature: ", pos=(10, 10))
        textControlHigh = wx.TextCtrl(panel, pos=(10, 30), value=high_temp)
        wx.StaticText(panel, label="Low Temperature: ", pos=(10, 60))
        textControlLow = wx.TextCtrl(panel, pos=(10, 80), value=low_temp)
        wx.StaticText(panel, label="Device: ", pos=(10, 110))
        statDevice = wx.Choice(panel, pos=(10, 130), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(
                textControlHigh.GetValue(),
                textControlLow.GetValue(),
                SerialSave
            )

class set_fan(eg.ActionBase):      

    class text:
        name = "Set Fan Mode"
        description = "Set Fan Mode. (Modes: Auto, On, Duty-Cycle).  Duty Cycyle is start hour and end hour, and how many minuets each hour."
        states = ["Auto", "On", "Duty-Cycle"]
        hours = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"]
        mins = ["15 Min", "30 Min", "45 Min", "60 Min"]

    def __call__(self, state, DevSerial, start, end, min):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        state = state.lower()
        start = self.text.hours.index(start)
        start = int(start)*3600
        end = self.text.hours.index(end)
        end = int(end)*3600
        min = int(self.text.mins.index(min)) + 1
        min = min*15*60
        if state == "auto":
            data = json.dumps({"fan_mode":"auto"})
        elif state == "on":
            data = json.dumps({"fan_mode":"on"})
        elif state == "duty-cycle":
            data = '{"fan_mode":"duty-cycle","fan_duty_start_time":' + str(start) + ',"fan_duty_end_time":' + str(end) + ',"fan_duty_cycle":' + str(min) + '}'
        else:
            print "Invalid Variable Data Fan Mode"
            return
        Setter(self, data, DevSerial, "device.")

    def Configure(self, state="Auto", serial="", start="12am", end="12am", min="15 Min"):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Fan Mode: ", pos=(10, 10))
        statChoice = wx.Choice(panel, pos=(10, 30), choices=self.text.states)
        statChoice.Select(self.text.states.index(state))
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        wx.StaticText(panel, label="Start Hour (For Duty-Cycle): ", pos=(150, 10))
        statStart = wx.Choice(panel, pos=(150, 30), choices=self.text.hours)
        statStart.Select(self.text.hours.index(start))
        wx.StaticText(panel, label="End Hour (For Duty-Cycle): ", pos=(150, 60))
        statEnd = wx.Choice(panel, pos=(150, 80), choices=self.text.hours)
        statEnd.Select(self.text.hours.index(end))
        wx.StaticText(panel, label="Min Each Hour (For Duty-Cycle): ", pos=(150, 110))
        statMin = wx.Choice(panel, pos=(150, 130), choices=self.text.mins)
        statMin.Select(self.text.mins.index(min))
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(self.text.states[statChoice.GetSelection()],
            SerialSave,
            self.text.hours[statStart.GetSelection()],
            self.text.hours[statEnd.GetSelection()],
            self.text.mins[statMin.GetSelection()])

class set_fan_with_timer(eg.ActionBase):      

    class text:
        name = "Set Fan With Timer"
        description = "Turn ON/OFF Fan with a timer.  0 will turn OFF fan if it was on timer only."

    def __call__(self, interval, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if str(interval) == str(0):
            data = '{"fan_timer_timeout":' + str(interval) + '}'
        else:
            data = '{"fan_timer_timeout":' + str(int(time.time()) + int(interval)*60) + '}'
        Setter(self, data, DevSerial, "device.")

    def Configure(self, interval="", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Device: ", pos=(10, 10))
        statDevice = wx.Choice(panel, pos=(10, 30), choices=self.DevChoices)
        wx.StaticText(panel, label="Time Duration in Minutes: ", pos=(10, 60))
        textControl = wx.TextCtrl(panel, pos=(10, 80), value=interval)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(textControl.GetValue(),SerialSave)
            
class set_auto_away(eg.ActionBase):     

    class text:
        name = "Set Auto Away"
        description = "Set Auto Away Function. (Status Available: True (Enabled), False (Disabled))"
        states = ["True","False"]

    def __call__(self, state, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        time_since_epoch   = time.time()
        state = state.lower()
        if state == "true":
            data = '{"auto_away_enable":true}'
        elif state == "false":
            data = '{"auto_away_enable":false}'
        else:
            print "Invalid Variable Data in Auto Away State"
            return

        Setter(self, data, DevSerial, "device.")

    def Configure(self, state="True", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Auto Away Function: ", pos=(10, 10))
        statChoice = wx.Choice(panel, pos=(10, 30), choices=self.text.states)
        statChoice.Select(self.text.states.index(state))
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(self.text.states[statChoice.GetSelection()], SerialSave)
            
class set_away(eg.ActionBase):      

    class text:
        name = "Set Away Status"
        description = "Set Away Status. (Status Available: Home, Away)"
        states = ["Home","Away"]

    def __call__(self, state, struc):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        time_since_epoch   = time.time()
        state = state.lower()
        
        if (state == "away"):
            data = '{"away_timestamp":' + str(time_since_epoch) + ',"away":true,"away_setter":0}'
        elif (state == "home"):
            data = '{"away_timestamp":' + str(time_since_epoch) + ',"away":false,"away_setter":0}'
        else:
            print "Invalid Variable Data in Away State"
            return

        Setter(self, data, str(struc), "structure.")

    def Configure(self, state="Home", struc=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.StrucChoices = []
        for x in self.plugin.Devices:
            self.StrucChoices.append(self.plugin.status["structure"][x.structure]["name"])
        panel.sizer.Add(panel.StaticText("Away Status:"), 0, wx.EXPAND)
        statChoice = wx.Choice(panel, 0, choices = self.text.states)
        statChoice.Select(self.text.states.index(state))
        wx.StaticText(panel, label="Structure: ", pos=(10, 60))
        statStruc = wx.Choice(panel, pos=(10, 80), choices=self.StrucChoices)
        panel.sizer.Add(statChoice)
        if struc == "":
            statStruc.Select(0)
        else:
            for x in self.plugin.Devices:
                if self.plugin.status["structure"][x.structure]["name"] == struc:
                    statStruc.Select(self.StrucChoices.index(self.plugin.status["structure"][x.structure]["name"]))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if self.plugin.status["structure"][x.structure]["name"] == self.StrucChoices[statStruc.GetSelection()]:
                    StrucSave = x.structure
            panel.SetResult(self.text.states[statChoice.GetSelection()], StrucSave)

class set_humidity_mode(eg.ActionBase):     

    class text:
        name = "Set Humidity Status"
        description = "Set Humidity Status. (Status Available: True (Enabled), False (Disabled))"
        states = ["True","False"]

    def __call__(self, state, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        state = state.lower()
        
        if (state == "true"):
            data = '{"target_humidity_enabled":true}'
        elif (state == "false"):
            data = '{"target_humidity_enabled":false}'
        else:
            print "Invalid Variable Data in humidity mode"
            return

        Setter(self, data, DevSerial, "device.")

    def Configure(self, state="False", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Humidistat Mode: ", pos=(10, 10))
        statChoice = wx.Choice(panel, pos=(10, 30), choices=self.text.states)
        statChoice.Select(self.text.states.index(state))
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(self.text.states[statChoice.GetSelection()], SerialSave)
            
class set_humidity_level(eg.ActionBase):        

    class text:
        name = "Set Humidity Percent"
        description = "Set Humidity Percent."

    def __call__(self, level, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not level.isdigit():
            try:
                if str(eval(level)).strip().isdigit():
                    level = str(eval(level)).strip()
                else:
                    print "Invaid Variable Data"
                    return
            except:
                print "Invalid Input"
                return
        level = float(level)
        data = '{"target_humidity":' + '%0.1f' % level + '}'

        Setter(self, data, DevSerial, "device.")

    def Configure(self, level="35", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Humidty %: ", pos=(10, 10))
        textControl = wx.TextCtrl(panel, pos=(10, 30), value=level)
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(textControl.GetValue(), SerialSave)
            
class set_dual_fuel_breakpoint(eg.ActionBase):      

    class text:
        name = "Set Outside Temperature for Dual Fuel Breakpoint"
        description = "Set Outside Temperature for Dual Fuel Breakpoint."

    def __call__(self, temp, DevSerial):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        if not temp.isdigit():
            try:
                if str(eval(temp)).strip().isdigit():
                    temp = str(eval(temp)).strip()
                else:
                    print "Invaid Variable Data"
                    return
            except:
                print "Invalid Input"
                return
        temp = self.plugin.temp_in(float(temp))
        data = '{"dual_fuel_breakpoint_override":"none","dual_fuel_breakpoint":' + '%0.1f' % temp + '}'

        Setter(self, data, DevSerial, "device.")

    def Configure(self, temp="", serial=""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Temperature: ", pos=(10, 10))
        textControl = wx.TextCtrl(panel, pos=(10, 30), value=temp)
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(textControl.GetValue(), SerialSave)
            
class Schedule_Information(eg.ActionBase):      

    class text:
        name = "Get schedule information"
        description = "Get schedule information. (in form of a list))"
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def TimeSchedule(self, time):
        hour = int(time)/3600
        min = str((time-(hour*3600))/60).zfill(2)
        time = str(hour) + ":" + str(min)
        return time

    def __call__(self, day, DevSerial, pp = False):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
                
        sl = []
        if day == "Sunday" or 0:
            key = "0"
        elif day == "Monday" or 1:
            key = "1"
        elif day == "Tuesday" or 2:
            key = "2"
        elif day == "Wednesday" or 3:
            key = "3"
        elif day == "Thursday" or 4:
            key = "4"
        elif day == "Friday" or 5:
            key = "5"
        elif day == "Saturday" or 6:
            key = "6"
        else:
            print "Error: for day schedule"
            return
        
        for x in sorted(self.plugin.schedule[DevSerial]["days"][key].keys()):
            sl.append(str(self.plugin.schedule[DevSerial]["days"][key][x]["type"]) + " @ " + str(self.TimeSchedule(self.plugin.schedule[DevSerial]["days"][key][x]["time"])) + " , " + str(self.plugin.temp_out(self.plugin.schedule[DevSerial]["days"][key][x]["temp"])))
        if pp:
            for x in sl:
                print x
        return sl
        
    def Configure(self, day="Sunday", serial="", pp = False):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Day: ", pos=(10, 10))
        statChoice = wx.Choice(panel, pos=(10, 30), choices=self.text.days)
        statChoice.Select(self.text.days.index(day))
        wx.StaticText(panel, label="Device: ", pos=(10, 60))
        statDevice = wx.Choice(panel, pos=(10, 80), choices=self.DevChoices)
        wx.StaticText(panel, label="Print Output: ", pos=(10, 110))
        statPrint = wx.CheckBox(panel, pos=(10, 130))
        statPrint.SetValue(pp)
        if serial == "":
            statDevice.Select(0)
        else:
            for x in self.plugin.Devices:
                if x.serial == serial:
                    statDevice.Select(self.DevChoices.index(x.name))
        while panel.Affirmed():
            for x in self.plugin.Devices:
                if x.name == self.DevChoices[statDevice.GetSelection()]:
                    SerialSave = x.serial
            panel.SetResult(self.text.days[statChoice.GetSelection()], SerialSave, statPrint.GetValue())
            
class get_energy_object(eg.ActionBase):

    class text:
        name = "Get Energy Report Object"
        description = "Get an Attribute from the Nest Thermostat(s) Energy Report"
        
    def __call__(self, object, Dev, Day):
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            return
        for x in self.plugin.Devices:
            if x.name == Dev:
                for y in x.energy:
                    if y["day"] == Day:
                        return y[object]
        
    def Configure(self, object="", Dev = "", Day = ""):
        panel = eg.ConfigPanel()
        if self.plugin.SignedIN == "False":
            print "Not Signed in to Nest"
            panel.Destroy()
            return
        self.DevChoices = []
        for x in self.plugin.Devices:
            self.DevChoices.append(x.name)
        wx.StaticText(panel, label="Device: ", pos=(10, 10))
        self.statChoice = wx.Choice(panel, pos=(10, 30), choices=self.DevChoices)
        self.statChoice.Bind(wx.EVT_CHOICE, self.DevChanged)
        if Dev == "":
            self.statChoice.Select(0)
        else:
            self.statChoice.Select(self.DevChoices.index(Dev))
        wx.StaticText(panel, label="Day: ", pos=(10, 60))
        self.Days = []
        for x in self.plugin.Devices:
            if Dev == x.name:
                for y in x.energy:
                    self.Days.append(y["day"])
        self.statDay = wx.Choice(panel, pos=(10, 80), choices=self.Days)
        self.statDay.Bind(wx.EVT_CHOICE, self.DayChanged)
        if Day == "":
            self.statDay.Select(0)
        else:
            self.statDay.Select(self.Days.index(Day))
        self.objects = ["fake with a realllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllly long string"]
        wx.StaticText(panel, label="Object: ", pos=(10, 110))
        self.statObject = wx.Choice(panel, pos=(10, 130), choices=self.objects)
        if Day == "":
            self.DevChanged()
        else:
            self.DayChanged()
        if object in self.objects:
            self.statObject.SetStringSelection(object)
        
                
        while panel.Affirmed():
            panel.SetResult(
                self.objects[self.statObject.GetSelection()],
                self.DevChoices[self.statChoice.GetSelection()],
                self.Days[self.statDay.GetSelection()]
                
            )
            
    def DevChanged(self, event=None):
        Dev = self.DevChoices[self.statChoice.GetSelection()]
        self.Days = []
        for x in self.plugin.Devices:
            if Dev == x.name:
                for y in x.energy:
                    self.Days.append(y["day"])
        self.statDay.Clear()
        self.statDay.AppendItems(self.Days)
        self.statDay.SetSelection(0)
        self.DayChanged()
     
    def DayChanged(self, event=None):
        Dev = self.DevChoices[self.statChoice.GetSelection()]
        for x in self.plugin.Devices:
            if Dev == x.name:
                self.objects = x.energy[self.statDay.GetSelection()].keys()
        self.statObject.Clear()
        self.statObject.AppendItems(self.objects)
        self.statObject.SetSelection(0)
        
        