#
# HAI OmniStat Serial
# ================

# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
# 0.2 - revised by Fiasco for HAI Omnistat thermostat series

help = """\
Plugin to control HAI Omnistat."""


eg.RegisterPlugin(
    name = "HAI Omnistat",
    author = "Fiasco",
    version = "0.2." + "$LastChangedRevision: 1181 $".split()[1],
    kind = "external",
    description = "Control HAI Omnistat Thermostats via RS232\nYour HAI Thermostat Baud should be set to 2400",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAA"
        "AAd0SU1FB9YDBAsPCqtpoiUAAAAWdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCAyLjZsqHS1"
        "AAADe0lEQVQ4T02TXVCUZRSAPyZsxpnqoovum+miq+6qFUJYQP7cogS2VpGFAAlKpyAC"
        "EVh+4k80WGADQWlxZRfZACH5ECVY5TdHiEbAIQVkHRzUCZK/ZWGXp10SxjPzXrzvvM9z"
        "zpw5xwUQXg7ndX1jw3VkYmrzycK/gusrgrB3z17hvXfffv2tN99YcXHEi///g07Bznkw"
        "+9i1yvAbqvJKolRJhJ2KQp4ZQWTWd5wsV9Ni6sWybn3tZWYXvjt531V1tgJF8lcEZbij"
        "MLgRbTpAVHcgyk5/QnSefHrmc7QdV1hbX9+VbAvuTk67ZpfVIDsWgu/ZfURfD+TElVBy"
        "m4+TooshvDaAL697EPOHLzK1L9prbayuWbYlwsLzFZfCql+Qx8XhqfoAZUsIhsEGLGsW"
        "Nm12FlZtTM0/w2DSEmn0dEgclRSFcFG8wcamTRAqtO0kpRficdQLpV5Gr7mf3qFHzC1u"
        "YF61MvrIztD0OsP3F6m/ZUDZ7klosxfxJZn0j04hpJ+uIvZ4EpJvJKhvFWOzW1lc2qT/"
        "zznuzdnoGnlG+8BDWnvMDE7M8q1eQcygN6GFkWj0nQgp+WUcilTyUaIHzRPtWKx2rLYt"
        "5hfXHBnMNIjDtHbfY3RmmcdLdkrEfKIHDyDLPYS6vhnhh9wSgiPCcYvbT+3gNQbGluib"
        "WOTG8EOaTGOY/nrKwPgynXdm+H3gCZkNeQ6BP0GnZGgMRoTUnDMcSfgaiUJKWuPP6MRx"
        "LhjvUN3Qh671NnVNQ1y9Oe2YgUmaeqY4WnMEpSgl5ORhzhmaEFRFpSTnOpool+GXFoa6"
        "sQNNXReVupucv9zHeWM3Gl0HNY0mci7VEtF2EJ+8fSTkpSP23EaYmpl1ySgowk8ehiTc"
        "i6iiExRcNKC+0IlG20m5XqRCK5J9qYxoMZSgail+scEUn6vn+bJFImxtbQkl5dWoCkvx"
        "Cg3k/Uh3grKCSahJJln3E8n1BSQ2JhArHuSTUgneET6kFWno6h3GyW5P4sqqRUhMLSCn"
        "uJQA+cdIFYF8GC3F/Xs3vDM8kaZ4sP+YD/4RX5B+Wk1l3SXnkG2zu7uwZrHuqa1rILuw"
        "hNSsfOSxsQQoPkN2WI4iPp7EzBx+dPRLb7zK0orl1Z2FEmwvTM4HZ0kzZvM7hqZfMbaJ"
        "jEw8YHh8kvrGFmr1euaf/iPZAW12uzD2t1n4DwtSpLoLWTYZAAAAAElFTkSuQmCC"
    ),
)


import re
import binascii
import time

cmdList = (
    ('Poll Thermostat', None, None, None),
        ('PollTherm1',             'Poll Thermostat 1 for Group 1 Data',  '0102',                 None),
        ('PollTherm2',             'Poll Thermostat 1 for Group 2 Data',  '0103',                 None),
        ('PollTherm3',             'Poll Thermostat 1 for Group 3 Data',  '0104',                 None),
        ('GetTemp',                'Get Current Temperature',             '01204001',             None),
        ('GetOutTemp',             'Get Current Outside Temperature',     '01204401',             None),        
        ('GetScreenColor',         'Get Current Screen Color',            '01208c01',             None),
        ('GetFanMode',             'Get Current Fan Mode',                '01203e01',             None),
        ('GetHoldMode',            'Get Current Hold Mode',               '01203f01',             None),
        ('GetEPL',                 'Get Energy Price Level',              '01204601',             None),
        ('GetSetPointHeat',        'Get Heat Set Point',                  '01203c01',             None),
        ('GetSetPointCool',        'Get Cool Set Point',                  '01203b01',             None),
        ('GetCurrentMode',         'Get Current Mode',                    '01203d01',             None),
        ('GetFilterReminder',      'Get Days Till Replace Filter',        '01200f01',             None),
        ('GetCWeekUse',            'Get Current Week Runtime',            '01201001',             None),
        ('GetLWeekUse',            'Get Last Week Runtime',               '01201101',             None),
        ('GetHVAC1Use',            'Get HVAC use week 1',                 '01209801',             None),
        ('GetHVAC2Use',            'Get HVAC use week 2',                 '01209901',             None),
        ('GetHVAC3Use',            'Get HVAC use week 3',                 '01209a01',             None),
        ('GetHVAC4Use',            'Get HVAC use week 4',                 '01209b01',             None),
        
    ('General', None, None, None),
        ('ScreenColor',            'Set Screen Color (1-100)',            '01218c',               '1-100'),
        ('SetPointCoolUp',         'Increase Cool Set Point',             'coolup',               None),        
        ('SetPointCoolDn',         'Decrease Cool Set Point',             'cooldn',               None),        
        ('SetPointHeatUp',         'Increase Heat Set Point',             'heatup',               None),        
        ('SetPointHeatDn',         'Decrease Heat Set Point',             'heatdn',               None),        
    ('Fan Mode', None, None, None),
        ('FanModeAuto',            'Fan Mode Auto',                       '01213e00',             None),
        ('FanModeOn',              'Fan Mode On',                         '01213e01',             None),
        ('FanModeCycle',           'Fan Mode Cycle',                      '01213e02',             None),
    ('Hold Mode', None, None, None),
        ('HoldModeOff',            'Hold Mode Off',                       '01213f00',             None),
        ('HoldModeOn',             'Hold Mode On',                        '01213f01',             None),
        ('HoldModeVac',            'Hold Mode Vacation',                  '01213f02',             None),
    ('Energy Price Level', None, None, None),
        ('EPLLow',                 'Energy Price Level Low',              '0121a900',             None),
        ('EPLMid',                 'Energy Price Level Middle',           '0121a901',             None),
        ('EPLHigh',                'Energy Price Level High',             '0121a902',             None),
        ('EPLCritical',            'Energy Price Level Critical',         '0121a904',             None),         
    ('Set Points', None, None, None),
        ('LowCoolLimit',           'Low Cool Limit in F (51-91)',         '012105',               '51-91'),
        ('HighHeatLimit',          'High Heat Limit in F (51-91)',        '012106',               '51-91'),
        ('SetPointCool',           'Set Cool Set Point in F (51-91)',     '01213b',               '51-91'),
        ('SetPointHeat',           'Set Heat Set Point in F (51-91)',     '01213c',               '51-91'),
    ('Current Mode', None, None, None),
        ('CurrentModeOff',         'Current Mode Off',                    '01213d00',             None),
        ('CurrentModeHeat',        'Current Mode Heat',                   '01213d01',             None),
        ('CurrentModeCool',        'Current Mode Cool',                   '01213d02',             None),
        ('CurrentModeAuto',        'Current Mode Auto',                   '01213d03',             None),
    ('Energy Efficient Control', None, None, None),
        ('EECOn',                  'Energy Efficient Control On',         '012101',               None),
        ('EECOff',                 'Energy Efficient Control Off',        '012100',               None),         
    (None, None, None, None),       
)
                
def generatechecksum(value):
    data = value.decode("hex")
    sum = 0
    for byte in data:
        sum += ord(byte)
    sum = hex(sum)
    if ( len(str(sum)) > 3 ):
       data = str(sum)[-2:]   
    else:
       data = str(sum)[2:]
    if ( len(data) < 2 ):    
       data = '0' + data
    return data




    
    
def CoolUp(self):
    if self.plugin.coolsetpoint < 91:
       self.plugin.coolsetpoint += 1
    data = self.plugin.omniTempDict[str(self.plugin.coolsetpoint)]
    data = hex(data)[2:]    
    return "01213b" + data   
    
def CoolDown(self):
    if self.plugin.coolsetpoint > 51:
       self.plugin.coolsetpoint -= 1
    data = self.plugin.omniTempDict[str(self.plugin.coolsetpoint)]
    data = hex(data)[2:]    
    return "01213b" + data  

def HeatUp(self):
    if self.plugin.heatsetpoint < 88:
       self.plugin.heatsetpoint += 1
    data = self.plugin.omniTempDict[str(self.plugin.heatsetpoint)]
    data = hex(data)[2:]    
    return "01213c" + data   
    
def HeatDown(self):
    if self.plugin.heatsetpoint > 51:
       self.plugin.heatsetpoint -= 1
    data = self.plugin.omniTempDict[str(self.plugin.heatsetpoint)]
    print data
    data = hex(data)[2:]    
    return "01213c" + data  
    

class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        cmd = self.cmd
        if self.cmd == 'heatup':
           cmd = HeatUp(self)           
        if self.cmd == 'heatdn':
           cmd = HeatDown(self)
        if self.cmd == 'coolup':
           cmd = CoolUp(self)
        if self.cmd == 'cooldn':
           cmd = CoolDown(self)
           
        # Is this a Group Data request?
        if self.cmd == '0102':
           self.plugin.lastdatagroup = 'group1'          
        if self.cmd == '0103':
           self.plugin.lastdatagroup = 'group2'        
        if self.cmd == '0104':
           self.plugin.lastdatagroup = 'group3'        

        value = generatechecksum(cmd)
        value = binascii.a2b_hex(cmd + value)
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()
        
        #if (self.cmd == 'heatup') | (self.cmd == 'heatdn') | (self.cmd == 'coolup') | (self.cmd == 'cooldn'):
        time.sleep(.2)
        self.plugin.lastdatagroup = 'group1'                     
        self.plugin.writeinit(binascii.a2b_hex('010203'))           
  



class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        data = eg.ParseString(data)
                
        # Call To Set Heat/Cool SetPoint
        if (self.cmd == '01213c') | (self.cmd == '01213b'):           
           data = self.plugin.omniTempDict[data]
           data = hex(data)[2:]              

        if  (self.cmd == '01213b') | ( self.cmd == '012105') | ( self.cmd == '012106'):
           data = self.plugin.omniTempDict[data]
           data = hex(data)[2:]
        if ( self.cmd == '01218C' ):
           data = int(data)
           
           data = hex(data)[2:]
        if ( len(data) < 2 ):    
           data = '0' + data           
      
        
        value = generatechecksum(self.cmd + data)
        #print "Writing " + self.cmd + data + value
        value = binascii.a2b_hex(self.cmd + data + value)
        
        self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()
        
        time.sleep(.2)
        self.plugin.lastdatagroup = 'group1'                     
        self.plugin.writeinit(binascii.a2b_hex('010203'))           

class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        value = generatechecksum(data)
        print data + value
        value = binascii.a2b_hex(data + value)
        print "Writing in hex "+ value
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(value)       
        self.plugin.serialThread.ResumeReadEvents()
        time.sleep(.2)
        self.plugin.lastdatagroup = 'group1'                     
        self.plugin.writeinit(binascii.a2b_hex('010203'))           




class HAIOmnistat(eg.PluginClass):     
    def __init__(self):
        self.serial = None
        group = self
        self.lastdatagroup = "none"
        

        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_name)
            elif cmd_rangespec is not None:
                # Command with argument
                actionName, paramDescr = cmd_text.split("(")
                actionName = actionName.strip()
                paramDescr = paramDescr[:-1]
                minValue, maxValue = cmd_rangespec.split("-")

                class Action(ValueAction):
                    name = actionName
                    cmd = cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr
                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd =  cmd_cmd
                Action.__name__ = cmd_name
                group.AddAction(Action)

        group.AddAction(Raw)
          
        self.fanDict = {
            '00': 'Auto',
            '01': 'On',
            '02': 'Cycle'
        } 
        self.holdDict = {
            '00': 'Off',
            '01': 'On',
            '02': 'Vacation'
        }             
        self.currentModeDict = {
            '00': 'Off',
            '01': 'Heat',
            '02': 'Cool',
            '03': 'Auto',
        }
        self.energyDict = {
            '00': 'Low',
            '01': 'Mid',
            '02': 'High',
            '03': 'Critical',
            'ff': 'Undefined'
        }
        self.energyPriceDict = {
            '00': 'Low',
            '01': 'Mid',
            '02': 'High',
            '04': 'Critical'
        }
        
        self.omniTempDict = {
            '0': 0,
            '51': 101,
            '52': 102,
            '53': 103,
            '54': 104,
            '55': 106,
            '56': 107,
            '57': 108,
            '58': 109,
            '59': 110,
            '60': 111,
            '61': 112,
            '62': 113,
            '63': 114,
            '64': 116,
            '65': 117,
            '66': 118,
            '67': 119,
            '68': 120,
            '69': 121,
            '70': 122,
            '71': 123,
            '72': 124,
            '73': 126,
            '74': 127,
            '75': 128,
            '76': 129,
            '77': 130,
            '78': 131,
            '79': 132,
            '80': 133,
            '81': 135,
            '82': 136,
            '83': 137,
            '84': 138,
            '85': 139,
            '86': 140,
            '87': 141,
            '88': 142,
            '89': 143,
            '90': 144,
            '91': 146                  
        }
        self.omniTempDictReverse = {
            '0': 0,
            '101': 51,
            '102': 52,
            '103': 53,
            '104': 54,
            '106': 55,
            '107': 56,
            '108': 57,
            '109': 58,
            '110': 59,
            '111': 60,
            '112': 61,
            '113': 62,
            '114': 63,
            '116': 64,
            '117': 65,
            '118': 66,
            '119': 67,
            '120': 68,
            '121': 69,
            '122': 70,
            '123': 71,
            '124': 72,
            '126': 73,
            '127': 74,
            '128': 75,
            '129': 76,
            '130': 77,
            '131': 78,
            '132': 79,
            '133': 80,
            '135': 81,
            '136': 82,
            '137': 83,
            '138': 84,
            '139': 85,
            '140': 86,
            '141': 87,
            '142': 88,
            '143': 89,
            '144': 90,
            '146': 91,
            '147': 92,
            '148': 93,
            '149': 94,
            '150': 95,
            '151': 96,
            '152': 97,
            '153': 98,
            '154': 99,
            '155': 100,
            '156': 101,
            '157': 102,
            '158': 103,
            '159': 104,
            '160': 105,
            '161': 106,
            '162': 107,
            '163': 108,
            '164': 109,
            '165': 110,
            '166': 111,
            '167': 112,
            '168': 113,
            '169': 114,
            '170': 115            
        }        

    def initialize(self):
        self.lastdatagroup = 'group1'          
        self.writeinit(binascii.a2b_hex('010203'))
        time.sleep(.2)
        self.lastdatagroup = 'group2'                  
        self.writeinit(binascii.a2b_hex('010304'))
        time.sleep(.2)
        self.lastdatagroup = 'group3'          
        self.writeinit(binascii.a2b_hex('010405'))

    def writeinit(self, value):

        self.serialThread.SuspendReadEvents()
        self.serialThread.Write(value)
        self.serialThread.ResumeReadEvents()    
    
                    
    def __start__(self, port):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 2400, '8N1')
        self.serialThread.SetRts()
        self.serialThread.SetDtr(True)
        self.serialThread.Start() 
        self.initialize()

        
     
    def __stop__(self):
        self.serialThread.Close()
        
    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())

    def OnReceive(self, serial):	 
        buffer = []
        value = 0
        cmdhexlength = 0
        cmdstrlength = ""
        fsthexvalue = 0
        fststrvalue = ""
        commandlength = 0
        checksum = 0
        command = ""
        groupdata = False

        while True:
             hexid = serial.Read(1, 0.1)
             if hexid == "":
                return
             strng = binascii.b2a_hex(hexid)

             buffer.append(strng.upper())
             #print "END OF COMMAND " + "".join(buffer)
            
             # First Element
             if ( len(buffer) == 1 ):
                fsthexvalue = hexid
                fststrvalue = strng
                continue

             # DL/MT in case of Group Data request this value is "63"
             if ( len(buffer) == 2 ):
                cmdhexlength = hexid
                cmdstrlength = strng
                commandlength = int(strng[0:1],16)
                # Is this a response ack?
                if ( strng == "00" ):
                   continue

                # Is this a Group Data request?
                if ( (strng == "63") | (strng == 'c3') ):
                   groupdata = True
                continue
 
             # Command String if not Group Data
             if ( len(buffer) == 3 ) & (not groupdata):
                if (cmdstrlength == "00"):
                   if (strng ==  fststrvalue):
                      print "Command Success"
                      return
                   else:
                      print "Command Failed"
                      return
                command = strng
                continue
                
             # Group Data Processing
             if ( len(buffer) > 2 ) & ( groupdata ): # & (len(buffer) < 9):
                if ( self.lastdatagroup == 'group1' ):   # GROUP 1
                   if ( len(buffer) == 3 ):     # Current Cool Setpoint
                      temp = self.omniTempDictReverse[str(int(strng,16))]
                      self.TriggerEvent("coolsetpoint", str(temp))  
                      self.coolsetpoint = temp     
                      continue
                   if ( len(buffer) == 4 ):     # Current Heat Setpoint
                      temp = self.omniTempDictReverse[str(int(strng,16))]
                      self.TriggerEvent("heatsetpoint", str(temp))
                      self.heatsetpoint = temp
                      continue
                   if ( len(buffer) == 5 ):     # Current System Mode
                      temp = self.currentModeDict[strng]
                      self.TriggerEvent("currentmode" + temp) 
                      continue
                   if ( len(buffer) == 6 ):     # Current Fan Mode
                      temp = self.fanDict[strng]
                      self.TriggerEvent("fanmode" + temp)
                      continue
                   if ( len(buffer) == 7 ):     # Current Hold Mode
                      temp = self.holdDict[strng]
                      self.TriggerEvent("holdmode" + temp)
                      continue
                   if ( len(buffer) == 8 ):     # Current Temperature
                      temp = self.omniTempDictReverse[str(int(strng,16))]
                      self.TriggerEvent("insidetemp", str(temp))
                   return
                      
                if ( self.lastdatagroup == 'group2' ):    # GROUP 2
                   if ( len(buffer) == 3 ):     # Current Indoor Humidty
                      temp = int(strng,16)
                      self.TriggerEvent("indoorhumidity", str(temp))
                      continue
                   if ( len(buffer) == 4 ):     # Current Dehumidfy Setpoint
                      temp = int(strng,16)
                      self.TriggerEvent("dehumidifysetpoint", str(temp))
                      continue                    
                   if ( len(buffer) == 5 ):     # Current Humidify Setpoint
                      temp = int(strng,16)
                      self.TriggerEvent("humidifysetpoint", str(temp))
                      continue
                   if ( len(buffer) == 6 ):     # Current Outdoor Temperature
                      temp = self.omniTempDictReverse[str(int(strng,16))]
                      self.TriggerEvent("outsidetemp", str(temp))
                      continue
                   if ( len(buffer) == 7 ):     # Current Filter Days Remaining
                      temp = int(strng,16)
                      self.TriggerEvent("filterdays", str(temp))
                      continue
                   if ( len(buffer) == 8 ):     # Current Energy Level
                      temp = self.energyDict[strng]
                      self.TriggerEvent("energymode", str(temp))
                   return
                if ( self.lastdatagroup == 'group3' ):    # GROUP 3
                   if ( len(buffer) == 3 ):     # Current Energy Level
                      temp = self.energyDict[strng]
                      self.TriggerEvent("energymode", str(temp))
                      continue
                   if ( len(buffer) == 4 ):     # Mid Level Setback
                      temp = int(strng,16)
                      self.TriggerEvent("midlevelsetback", str(temp))
                      continue
                   if ( len(buffer) == 5 ):     # High Level Setback
                      temp = int(strng,16)
                      self.TriggerEvent("highlevelsetback", str(temp))
                      continue
                   if ( len(buffer) == 6 ):     # Critical Level Setback
                      temp = int(strng,16)
                      self.TriggerEvent("criticallevelsetback", str(temp))
                      continue                   
                   if ( len(buffer) == 7 ):     # Energy Price
                      temp = int(strng,16)
                      self.TriggerEvent("energyprice", str(temp))
                      continue                      
                   if ( len(buffer) == 8 ):     # Energy Total Cost Upper
                      temp = int(strng,16)
                      self.TriggerEvent("energycostupper", str(temp))
                      continue                   
                   if ( len(buffer) == 9 ):     # Energy Total Cost Lower
                      temp = int(strng,16)
                      self.TriggerEvent("energycostlower", str(temp))
                      continue                   
                   if ( len(buffer) == 10):     # Medium Price
                      temp = int(strng,16)
                      self.TriggerEvent("energymidprice", str(temp))
                      continue                   
                   if ( len(buffer) == 11):     # High Price
                      temp = int(strng,16)
                      self.TriggerEvent("energyhighprice", str(temp))
                      continue                  
                   if ( len(buffer) == 12):     # Critical Price
                      temp = int(strng,16)
                      self.TriggerEvent("energycriticalprice", str(temp))
                   return                  
                
               

             if ( len(buffer) == 4 ) & ( not groupdata ): 
                   # Current Temperature
                   if ( command == "40" ):      # Current Temperature
                      omnit = int(strng,16)
                      temp = self.omniTempDictReverse[str(omnit)]
                      self.TriggerEvent("insidetemp", str(temp))
                   if ( command == "44" ):      # Outside Temperature
                      omnit = int(strng,16)
                      temp = self.omniTempDictReverse[str(omnit)]
                      self.TriggerEvent("outsidetemp", str(temp))
                   if ( command == "8c" ):      # Screen Color
                      self.TriggerEvent("screencolor", strng)
                   if ( command == "3e" ):      # Fan Mode
                      temp = self.fanDict[strng]
                      self.TriggerEvent("fanmode", temp)
                   if ( command == "3f" ):      # Hold Mode
                      temp = self.holdDict[strng]
                      self.TriggerEvent("holdmode", temp)
                   if ( command == "a9"):       # Energy Mode
                      temp = self.energyDict[strng]
                      self.TriggerEvent("energymode", temp)
                   if ( command == "3c"):       # Heat Setpoint
                      omnit = int(strng,16)
                      temp = self.omniTempDictReverse[str(omnit)]
                      self.TriggerEvent("heatsetpoint", str(temp))
                   if ( command == "3b"):       # Cool Setpoint
                      omnit = int(strng,16)
                      temp = self.omniTempDictReverse[str(omnit)]
                      self.TriggerEvent("coolsetpoint", str(temp))
                   if ( command == "3d"):       # Current Mode
                      temp = self.currentModeDict[strng]
                      self.TriggerEvent("currentmode", temp) 
                   if ( command == "0f"):       # Filter Days Remaining
                      self.TriggerEvent("filterdays", int(strng,16))
                   if ( command == "10"):       # Current Week Use
                      self.TriggerEvent("cweekuse", int(strng,16))
                   if ( command == "11"):       # Last Week Use
                      self.TriggerEvent("lweekuse", int(strng,16))
                   if ( command == "4a"):       # Current cost
                      self.TriggerEvent("currentcost", int(strng,16))
                   if ( command == "98"):       # Week One Hours
                      self.TriggerEvent("hvacweek1", int(strng,16))
                   if ( command == "99"):       # Week Two Hours
                      self.TriggerEvent("hvacweek2", int(strng,16))
                   if ( command == "9a"):       # Week Three Hours
                      self.TriggerEvent("hvacweek3", int(strng,16))
                   if ( command == "9b"):       # Week Four Hours
                      self.TriggerEvent("hvacweek4", int(strng,16))  

                     
                      
             if len(buffer) == (commandlength + 2):
                checksum = generatechecksum( "".join(buffer))
                
                
             if len(buffer) > (commandlength + 2):
                if checksum == strng:
                   #print "Command Successfull"
                   return   
             
                
            
            	 
