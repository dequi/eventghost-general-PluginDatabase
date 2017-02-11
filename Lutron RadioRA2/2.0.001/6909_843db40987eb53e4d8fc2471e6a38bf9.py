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
#
# $LastChangedDate: 2013-Nov-20 $
# $LastChangedRevision: 005 $
# $LastChangedBy: rdgerken $

"""<rst>
Adds actions to control `Lutron RadioRA2 <http://www.lutron.com/RadioRA2>`_.


**Lutron RadioRA2 Plugin**

Lutron RadioRA2 is a lighting home automation control that permits control
of individual zones of light in your home or scenes of grouped zones remotely via
network, rf or wall and table top keypads.


*Option/Setup*

Enter the TCP/IP address and the telnet port of your Lutron RadioRA2 Processor.  The 
default telnet port is 23. 

You must edit the _init_.py file in your eventghost\plugins\RadioRA2 directory and
enter your setup information where marked in the _init_.py file.  You will see a
section marked with Begin Customization and End Customization.  All information
can be found in the integration report from the RA2 software.

*Please Note*

When setting or querying LED's, the RA protocol starts numbering them at 101.   You do
not need to do that with the plugin.  If you want to check button one's LED, query for
one in your LED command.

*Known Issues*  - (I think these are firmware issues, not problems with the plugin)

1. Flashing an output does not appear to work with the latest firmware (6.2.0) at the time
of this writing.  It will flash all outputs in the system, not just the output commanded.

2. Getting the state of an LED does not seem to work until you first set the LED. Subsequent
queries to get the state of an LED then appears to work.

3. Flashing or RapidFlashing an LED on a keypad seems to only show up in the Home+ application.
It does not appear to do anything on the actual keypad itself.

*Hint*

Don't actually program anything to the actions created for you.  Create your own macros and
use either python commands or python scripts (right click on the actions created for you and
select Copy As Python) and then paste these in your own python actions.  This will allow you to
delete the entire Lutron RA2 plugin and then replace it with updated versions without impacting
your custom macros.  This makes for simple upgrading of the plugin.  (EG will not let you delete
a plugin that has references to it - this is a way to remove those direct references, but still
make use of the actions created for you)

"""

import eg

eg.RegisterPlugin(
    name = "Lutron RadioRA2",
    description = __doc__,
    author = "rdgerken via Fiasco via Bitmonster",
    version = "2.0." + "$LastChangedRevision: 001 $".split()[1],
    kind = "external",
    canMultiLoad = True,
    createMacrosOnAdd = True
)

# IntegrationID
# Types: Repeater, Timeclock, Maestro, Wallkeypad, Sivoiaqs, Motion, Hybrid, VCRX, Fan, Pico    !These are Case Sensitive

#========================= BEGIN CUSTOMIZATION SECTION ================================================

RADIORA2_CONFIG = {  #These are CASE sensitive
     '1' : 'Repeater',
     '2' : 'Motion',
     '3' : 'Maestro',
     '5' : 'Motion',
     '6' : 'Maestro',
     '7' : 'Maestro',
     '9' : 'Motion',
     '10' : 'Maestro',
     '11' : 'Maestro',
     '13' : 'Motion',
     '14' : 'Maestro',
     '15' : 'Maestro',
     '17' : 'Sivoiaqs',
     '18' : 'Maestro',
     '19' : 'Fan',
     '20' : 'Maestro',
     '22' : 'Sivoiaqs',
     '23' : 'Sivoiaqs',
     '25' : 'Maestro',
     '26' : 'Maestro',
     '29' : 'Maestro',
     '30' : 'Maestro',
     '31' : 'Motion',
     '33' : 'Timeclock',
     '35' : 'Motion',
     '36' : 'Maestro',
     '37' : 'Maestro',
     '39' : 'Motion',
     '40' : 'Maestro',
     '42' : 'Motion',
     '43' : 'Maestro',
     '44' : 'Maestro',
     '45' : 'Maestro',
     '46' : 'Maestro',
     '48' : 'Hybrid',
     '49' : 'Maestro',
     '50' : 'Maestro',
     '51' : 'Sivoiaqs',
     '53' : 'Motion',
     '54' : 'Maestro',
     '55' : 'Maestro',
     '57' : 'Motion',
     '58' : 'Hybrid',
     '59' : 'Maestro',
     '61' : 'Motion',
     '62' : 'Hybrid',
     '63' : 'Maestro',
     '64' : 'Maestro',
     '65' : 'Maestro',
     '66' : 'Sivoiaqs',
     '67' : 'Sivoiaqs',
     '69' : 'Hybrid',
     '70' : 'Motion',
     '71' : 'Maestro',
     '72' : 'Maestro',
     '74' : 'Motion',
     '75' : 'Maestro',
     '77' : 'Motion',
     '78' : 'Maestro',
     '79' : 'Maestro',
     '81' : 'Maestro',
     '82' : 'Hybrid',
     '83' : 'Maestro',
     '84' : 'Maestro',
     '85' : 'Sivoiaqs',
     '86' : 'Motion',
     '87' : 'Sivoiaqs',
     '88' : 'Sivoiaqs',
     '89' : 'Sivoiaqs',
     '90' : 'Sivoiaqs',
     '91' : 'Sivoiaqs',
     '93' : 'Motion',
     '94' : 'Maestro',
     '95' : 'Maestro',
     '96' : 'Maestro',
     '98' : 'Motion',
     '99' : 'Hybrid',
     '100' : 'Maestro',
     '101' : 'Sivoiaqs',
     '103' : 'Motion',
     '104' : 'Maestro',
     '105' : 'Maestro',
     '107' : 'Motion',
     '108' : 'Motion',
     '110' : 'Wallkeypad',
     '112' : 'Maestro',
     '113' : 'Motion',
     '114' : 'Maestro',
     '116' : 'Fan',
     '118' : 'Maestro',
     '119' : 'Motion',
     '120' : 'Motion',
     '121' : 'Motion'
}

# IntegrationID
# Description of device location

RADIORA2_LOCATION = {
     '1' : 'Main Repeater',
     '2' : 'Basement Motion',
     '3' : 'Basement Light',
     '5' : 'Hall Bath Motion',
     '6' : 'Hall Bath Fan',
     '7' : 'Hall Bath Light',
     '9' : 'Boy 1 Bedroom Motion',
     '10' : 'Family Room Fireplace',
     '11' : 'Boy 1 Bedroom Light',
     '13' : 'Girl 1 Bedroom Motion',
     '14' : 'Holiday Lights',
     '15' : 'Girl 1 Bedroom Light',
     '17' : 'Master Bedroom Window',
     '18' : 'Family Room Fan Light',
     '19' : 'Master Bedroom Ceiling Fan',
     '20' : 'Foyer Chandelier',
     '22' : 'Family Room North Side',
     '23' : 'Family Room South Side',
     '25' : 'Foyer Hall Cans',
     '26' : 'Foyer Coach Lights',
     '29' : 'Garage Coach Lights',
     '30' : 'Garage Overhead Lighting',
     '31' : 'Garage Motion',
     '33' : 'Project Timeclock',
     '35' : 'Jack N Jill Bath Motion',
     '36' : 'Jack N Jill Bath Overhead Fan',
     '37' : 'Jack N Jill Bath Overhead Light',
     '39' : 'Jack N Jill Vanity Motion',
     '40' : 'Jack N Jill Vanity Light',
     '42' : 'Kitchen Motion',
     '43' : 'Kitchen Cubby Light',
     '44' : 'Kitchen Island Pendant Lights',
     '45' : 'Kitchen Kitchen Cans',
     '46' : 'Kitchen Over Cabinet Lighting',
     '48' : 'Kitchen Scenes',
     '49' : 'Kitchen Sink Work',
     '50' : 'Upstairs Hall Upstairs Cans',
     '51' : 'Kitchen Window',
     '53' : 'Boy 2 Bedroom Motion',
     '54' : 'Family Room Fireplace Accents',
     '55' : 'Boy 2 Bedroom Light',
     '57' : 'Girl 2 Bedroom Motion',
     '58' : 'Family Room Scenes',
     '59' : 'Girl 2 Bedroom Light',
     '61' : 'Master Bathroom Motion',
     '62' : 'Master Bathroom Scenes',
     '63' : 'Master Bathroom Overhead Fan',
     '64' : 'Master Bathroom Overhead Light',
     '65' : 'Master Bathroom Sink',
     '66' : 'Master Bathroom S Window',
     '67' : 'Master Bathroom W Window',
     '69' : 'Master Bedroom Scenes',
     '70' : 'Master Bedroom Motion',
     '71' : 'Dining Room Overhead Light',
     '72' : 'Master Bedroom Light',
     '74' : 'Master Closet Motion',
     '75' : 'Master Closet Light',
     '77' : 'Master Commode Motion',
     '78' : 'Master Commode Fan',
     '79' : 'Master Commode Light',
     '81' : 'Boys Bath Vanity',
     '82' : 'Morning Room Scenes',
     '83' : 'Morning Room Outdoor Flood',
     '84' : 'Morning Room Overhead Light',
     '85' : 'Morning Room S Window W',
     '86' : 'Morning Room Motion',
     '87' : 'Morning Room W Window S',
     '88' : 'Morning Room W Window M',
     '89' : 'Morning Room W Window N',
     '90' : 'Morning Room S Window E',
     '91' : 'Morning Room S Window M',
     '93' : 'Mud Room Motion',
     '94' : 'Mud Room Entry Light',
     '95' : 'Mud Room Outside Light',
     '96' : 'Mud Room Washer Dryer Light',
     '98' : 'Office Motion',
     '99' : 'Office Scenes',
     '100' : 'Office Overhead Light',
     '101' : 'Office Window',
     '103' : 'Powder Room Motion',
     '104' : 'Powder Room Fan',
     '105' : 'Powder Room Light',
     '107' : 'Upstairs Hall Motion',
     '108' : 'Upstairs Laundry Motion',
     '110' : 'Virtual Scenes',
     '112' : 'Upstairs Laundry Overhead Light',
     '113' : 'Dining Room Motion',
     '114' : 'Kitchen Under Cabinet Lighting',
     '116' : 'Family Room Ceiling Fan',
     '118' : 'Living Room Lamp',
     '119' : 'Living Room Motion',
     '120' : 'Foyer Motion',
     '121' : 'Family Room Motion'
}

TIMECLOCK_ACTIONS = (
('SetTimeClockMode',   'Set Current Timeclock Mode','(Away OR Suspend OR Alternate OR Normal)',   '1', '#'),  #Timeclock modes are custom for the system - these are the default modes available
('GetTimeClockMode',   'Get Current Timeclock Mode','',   '1', '?'),
('GetSunriseTime',     'Get Sunrise Time','',             '2', '?'),
('GetSunsetTime',      'Get Sunset Time','',              '3', '?'),
('GetSchedule',        'Get Schedule for the day','',     '4', '?'),
('ExecuteEvent',       'Execute Event','(Index of Event)','5', '#')
)

#Timeclock Event Dictionaries - Custom for System - The commands are ONE BASED
TIMECLOCK_EVENTS = (
('Garage Vacancy','1'),
('Garage Occupancy','2')
)

timeclockEventDict = {  #These are the ZERO BASED EQUIVALENTS to the TIMECLOCK_EVENTS defined above... don't know why
    '0' : 'Garage Vacancy',
    '1' : 'Garage Occupancy'
}

#Timeclock Modes for this system - this is custom per system and can be discovered by sending '?HELP,#TIMECLOCK,1' to the main repeater
timeclockModeDict = {
    'Away'      : '0',
    'Suspend'   : '1',
    'Alternate' : '2',
    'Normal'    : '3',
    '0'         : 'Away',
    '1'         : 'Suspend',
    '2'         : 'Alternate',
    '3'         : 'Normal'
}
#========================= END CUSTOMIZATION SECTION ================================================


#Actions to register in EventGhost
REPEATER_DEVICE_ACTIONS = (
('Press',          'Phantom Button Press',         'Component',                   '3', '#'),
('Release',        'Phantom Button Release',       'component',                   '4', '#'),
('GetLED',         'Phantom Button Get LED State', 'Component',                   '9', '?')
)

REPEATER_MONITOR_ACTIONS = (
('MONITOR1ON',     'Diagnostic Monitoring On',  '1','1', '#'),
('MONITOR1OFF',    'Diagnostic Monitoring Off', '1','2', '#'),
('MONITOR3ON',     'Button Monitoring On',      '3','1', '#'),
('MONITOR3OFF',    'Button Monitoring Off',     '3','2', '#'),
('MONITOR4ON',     'LED Monitoring On',         '4','1', '#'),
('MONITOR4OFF',    'LED Monitoring Off',        '4','2', '#'),
('MONITOR5ON',     'Zone Monitoring On',        '5','1', '#'),
('MONITOR5OFF',    'Zone Monitoring Off',       '5','2', '#'),
('MONITOR11ON',    'Reply State On',            '11','1', '#'),
('MONITOR11OFF',   'Reply State Off',           '11','2', '#'),
('MONITOR12ON',    'Prompt State On',           '12','1', '#'),
('MONITOR12OFF',   'Prompt State Off',          '12','2', '#'),
('MONITOR255ON' ,  'All Monitoring On',         '255','1', '#'),
('MONITOR255OFF' , 'All Monitoring Off',        '255','2', '#')
)

WALLKEYPAD_DEVICE_ACTIONS = (
('Button1',        'Wall Keypad Button 1', '(Press OR Release OR Hold OR Multitap)', '1', '#'),
('Button2',        'Wall Keypad Button 2', '(Press OR Release OR Hold OR Multitap)', '2', '#'),
('Button3',        'Wall Keypad Button 3', '(Press OR Release OR Hold OR Multitap)', '3', '#'),
('Button4',        'Wall Keypad Button 4', '(Press OR Release OR Hold OR Multitap)', '4', '#'),
('Button5',        'Wall Keypad Button 5', '(Press OR Release OR Hold OR Multitap)', '5', '#'),
('Button6',        'Wall Keypad Button 6', '(Press OR Release OR Hold OR Multitap)', '6', '#'),
('Button7',        'Wall Keypad Button 7', '(Press OR Release OR Hold OR Multitap)', '7', '#'),
('TopLower',       'Wall Keypad Top Lower', '(Press OR Release)',                    '16', '#'),
('TopRaise',       'Wall Keypad Top Raise', '(Press OR Release)',                    '17', '#'),
('BotLower',       'Wall Keypad Bottom Lower', '(Press OR Release)',                 '18', '#'),
('BotRaise',       'Wall Keypad Bottom Raise', '(Press OR Release)',                 '19', '#'),
('SetLED1',        'Wall Keypad Button 1 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '81', '#'),
('SetLED2',        'Wall Keypad Button 2 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '82', '#'),
('SetLED3',        'Wall Keypad Button 3 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '83', '#'),
('SetLED4',        'Wall Keypad Button 4 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '84', '#'),
('SetLED5',        'Wall Keypad Button 5 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '85', '#'),
('SetLED6',        'Wall Keypad Button 6 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '86', '#'),
('SetLED7',        'Wall Keypad Button 7 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '87', '#'),
('GetLED1',        'Wall Keypad Button 1 LED State','',                              '81', '?'),
('GetLED2',        'Wall Keypad Button 2 LED State','',                              '82', '?'),
('GetLED3',        'Wall Keypad Button 3 LED State','',                              '83', '?'),
('GetLED4',        'Wall Keypad Button 4 LED State','',                              '84', '?'),
('GetLED5',        'Wall Keypad Button 5 LED State','',                              '85', '?'),
('GetLED6',        'Wall Keypad Button 6 LED State','',                              '86', '?'),
('GetLED7',        'Wall Keypad Button 7 LED State','',                              '87', '?')
)

HYBRID_DEVICE_ACTIONS = (
('Button1',        'Wall Keypad Button 1', '(Press OR Release)',                      '1', '#'),
('Button2',        'Wall Keypad Button 2', '(Press OR Release)',                      '2', '#'),
('Button3',        'Wall Keypad Button 3', '(Press OR Release)',                      '3', '#'),
('Button4',        'Wall Keypad Button 4', '(Press OR Release)',                      '4', '#'),
('Button5',        'Wall Keypad Button 5', '(Press OR Release)',                      '5', '#'),
('Button6',        'Wall Keypad Button 6', '(Press OR Release)',                      '6', '#'),
('Button7',        'Wall Keypad Button 7', '(Press OR Release)',                      '7', '#'),
('TopLower',       'Wall Keypad Top Lower', '(Press OR Release)',                    '16', '#'),
('TopRaise',       'Wall Keypad Top Raise', '(Press OR Release)',                    '17', '#'),
('BotLower',       'Wall Keypad Bottom Lower', '(Press OR Release)',                 '18', '#'),
('BotRaise',       'Wall Keypad Bottom Raise', '(Press OR Release)',                 '19', '#'),
('SetLED1',        'Wall Keypad Button 1 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '81', '#'),
('SetLED2',        'Wall Keypad Button 2 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '82', '#'),
('SetLED3',        'Wall Keypad Button 3 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '83', '#'),
('SetLED4',        'Wall Keypad Button 4 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '84', '#'),
('SetLED5',        'Wall Keypad Button 5 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '85', '#'),
('SetLED6',        'Wall Keypad Button 6 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '86', '#'),
('SetLED7',        'Wall Keypad Button 7 Set LED State','(Off OR On OR Flash OR Rapidflash)',                              '87', '#'),
('GetLED1',        'Wall Keypad Button 1 Get LED State','',                              '81', '?'),
('GetLED2',        'Wall Keypad Button 2 Get LED State','',                              '82', '?'),
('GetLED3',        'Wall Keypad Button 3 Get LED State','',                              '83', '?'),
('GetLED4',        'Wall Keypad Button 4 Get LED State','',                              '84', '?'),
('GetLED5',        'Wall Keypad Button 5 Get LED State','',                              '85', '?'),
('GetLED6',        'Wall Keypad Button 6 Get LED State','',                              '86', '?'),
('GetLED7',        'Wall Keypad Button 7 Get LED State','',                              '87', '?')
)

MAESTRO_OUTPUT_ACTIONS = (
('SetZoneLevel',      'Set Zone Level','(Level 0-100,Fade in MM:SS,Delay MM:SS) *optional', '1', '#'),
('GetZoneLevel',      'Get Zone Level','', '1', '?'),
('Raise',             'Start Raise Level','',      '2', '#'),
('Lower',             'Start Lower Level','',      '3', '#'),
('Stop',              'Stop Level Change','',      '4', '#'),
('Flash',             'Start Flashing','(Fade in MM:SS,Delay MM:SS) *optional',         '5', '#')
)

SIVOIAQS_OUTPUT_ACTIONS = (
('SetShadeLevel',   'Shade Set Zone Level','(Level 0-100,Fade in MM:SS,*Delay MM:SS) 100=Open | *N/A | **optional', '1', '#'),
('GetShadeLevel',   'Shade Get Zone Level','',   '1', '?'),
('RaiseShade',      'Start Raise Shade','',      '2', '#'),
('LowerShade',      'Start Lower Shade','',      '3', '#'),
('StopShade',       'Stop Shade','',             '4', '#')
)

FAN_OUTPUT_ACTIONS = (
('SetFanLevel',      'Set Fan Level','(0=Off, 1-25=Low, 26-50=Medium, 51-75=Medium High, 76-100=High)', '1', '#'),
('GetFanLevel',      'Get Fan Level','',                                                                '1', '?')
)

VCRX_DEVICE_ACTIONS = (
('Scene1',           'Scene 1', '(Press OR Release)',                          '1', '#'),
('Scene2',           'Scene 2', '(Press OR Release)',                          '2', '#'),
('Scene3',           'Scene 3', '(Press OR Release)',                          '3', '#'),
('Scene4',           'Scene 4', '(Press OR Release)',                          '4', '#'),
('Scene5',           'Scene 5', '(Press OR Release)',                          '5', '#'),
('Scene6',           'Scene 6', '(Press OR Release)',                          '6', '#'),
('FullSecurity',     'Full/Security', '(Open OR Close)',                       '30', '#'),
('SecurityFlash',    'Security Flash', '(Open OR Close)',                      '31', '#'),
('Input1',           'Input 1', '(Open OR Close)',                             '32', '#'),
('Input2',           'Input 2', '(Open OR Close)',                             '33', '#'),
('SetLEDSCENE1',     'Set LED Scene 1 State','(Off OR On OR Flash OR Rapidflash)',                               '81', '#'),
('SetLEDSCENE2',     'Set LED Scene 2 State','(Off OR On OR Flash OR Rapidflash)',                               '82', '#'),
('SetLEDSCENE3',     'Set LED Scene 3 State','(Off OR On OR Flash OR Rapidflash)',                               '83', '#'),
('SetLEDSCENE4',     'Set LED Scene 4 State','(Off OR On OR Flash OR Rapidflash)',                               '84', '#'),
('SetLEDSCENE5',     'Set LED Scene 5 State','(Off OR On OR Flash OR Rapidflash)',                               '85', '#'),
('SetLEDSCENE6',     'Set LED Scene 6 State','(Off OR On OR Flash OR Rapidflash)',                               '86', '#'),
('GetLEDSCENE1',     'Get LED Scene 1 State','',                               '81', '?'),
('GetLEDSCENE2',     'Get LED Scene 2 State','',                               '82', '?'),
('GetLEDSCENE3',     'Get LED Scene 3 State','',                               '83', '?'),
('GetLEDSCENE4',     'Get LED Scene 4 State','',                               '84', '?'),
('GetLEDSCENE5',     'Get LED Scene 5 State','',                               '85', '?'),
('GetLEDSCENE6',     'Get LED Scene 6 State','',                               '86', '?')
)

VCRX_OUTPUT_ACTIONS = (
('SetCCO',     'Set CCO','(0=Open, Nonzero=Closed)',                            '1', '#'),
('GetCCO',     'Get CCO','',                                                    '1', '?'),
('SetPulseCCO','Set Pulse CCO','(Pulse time in hh:mm:SS, or Delay in hh:mm:SS) *LCase Optional','6', '#')
)

PICO_DEVICE_ACTIONS = (
('Button1',        'Keypad Button 1', '(Press OR Release)',                      '2', '#'),
('Button2',        'Keypad Button 2', '(Press OR Release)',                      '3', '#'),
('Button3',        'Keypad Button 3', '(Press OR Release)',                      '4', '#'),
('ButtonRaise',    'Keypad Button Raise', '(Press OR Release)',                  '5', '#'),
('ButtonLower',    'Keypad Button Lower', '(Press OR Release)',                  '6', '#')
)

timeclockActionDict = {
    '1' : 'Timeclockmode',
    '2' : 'Sunrisetime',
    '3' : 'Sunsettime',
    '4' : 'Dayschedule',
    '5' : 'ExecuteEvent'
}

#Device Specific Dictionaries
onoffDict = {
    '0' : 'Off',
    '1' : 'On'
}
repeaterMonitorTypeDict = {
    '1'  : 'Diagnostic',
    '3'  : 'Button',
    '4'  : 'LED',
    '5'  : 'Zone',
    '11' : 'Reply',
    '12' : 'Prompt',
    '255': 'All'
} 
repeaterMonitorActionDict = {
    '1' : 'Enabled',
    '2' : 'Disabled'
}

repeaterDeviceDict = {
    '3'       : 'Press',
    '4'       : 'Release',
    '9'       : 'LED',
    'Press'   : '3',
    'Release' : '4',
    'LED'     : '9'
}

keypadDeviceActionDict = {
    'Press'    : '3',
    'Release'  : '4',
    'Hold'     : '5',
    'Multitap' : '6',
    'LED'      : '9',
    '3'        : 'Press',
    '4'        : 'Release',
    '5'        : 'Hold',
    '6'        : 'Multitap',
    '9'        : 'LED'
}

hybridDeviceActionDict = {
    '3'        : 'Press',
    '4'        : 'Release',
    '9'        : 'LED',
    'Press'    : '3',
    'Release'  : '4',
    'LED'      : '9'
}

vcrxDeviceActionDict = {
    '3'                     : 'Press',
    '4'                     : 'Release',
    '9'                     : 'LED',
    '3'                     : 'Close',
    '4'                     : 'Open',
    'Press'                 : '3',
    'Release'               : '4',
    'Close'                 : '3',
    'Open'                  : '4',
    'LED'                   : '9'
}

picoDeviceActionDict = {
    '3'        : 'Press',
    '4'        : 'Release',
    'Press'    : '3',
    'Release'  : '4'
}

maestroOutputDict = {
    '1' : 'Level',
    '2' : 'Raise',
    '3' : 'Lower',
    '4' : 'Stop',
    '5' : 'Flash'
}

shadesOutputDict = {
    '1' : 'ShadeLevel',
    '2' : 'RaiseShade',
    '3' : 'LowerShade',
    '4' : 'StopShade'
}

fanOutputDict = {
    '1' : 'Speed'
}

vcrxOutputDict = {
    '1' : 'OutputState'
}

motionEventStateDict = {
    '3' : 'Occupied',
    '4' : 'Vacant'
}

LEDDict = {
    '0'          : 'Off',
    '1'          : 'On',
    '2'          : 'Flash',
    '3'          : 'Rapidflash',
    'Off'        : '0',
    'On'         : '1',
    'Flash'      : '2',
    'Rapidflash' : '3'
}

import wx
import asynchat
import socket
import asyncore
import threading
import re
from types import ClassType
                
class Text:
    tcpBox = "TCP/IP Settings"
    hostLabel = "Host:"
    portLabel = "Port:"
    userLabel = "Username:"
    passLabel = "Password:"
      
class LutronRadioRA2Session(asynchat.async_chat):
    """
    Handles a Lutron RadioRA2 TCP/IP session.
    """
     
    def __init__ (self, plugin, address):
        self.plugin = plugin

        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('')
        
        # create and connect a socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        self.settimeout(2.0)
        try:
            self.connect(address)
        except:
            pass

    def handle_connect(self):
        """
        Called when the active opener's socket actually makes a connection. 
        """
        self.plugin.TriggerEvent("Connected")

    def handle_expt(self):
        # connection failed
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("NoConnection")
        self.close()

    def handle_close(self):
        """
        Called when the channel is closed.
        """
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("ConnectionLost")
        self.close()

    def collect_incoming_data(self, data):
        """
        Called with data holding an arbitrary amount of received data.
        """

        data = re.sub("([^0-9a-zA-Z\,\.\~\#\>])", '', data)        
        arguments = data.rsplit(',')
        command = arguments[0]

        if self.plugin.debug:  
           print "RadioRA2> Received: " + data

        try:   
            if command.upper() == 'LOGIN':
               self.plugin.DoCommand( self.plugin.lutronuser )
            if command.upper() == 'PASSWORD':
               self.plugin.DoCommand( self.plugin.lutronpass ) 
           
            if ( command.upper() == '~MONITORING' ):
               type   = arguments[1]
               action = arguments[2]
               self.plugin.TriggerEvent('Monitoring.' + repeaterMonitorTypeDict[type], repeaterMonitorActionDict[action])
               return

            if ( command.upper() == '~TIMECLOCK' ):
               integrationid   = arguments[1]
               location = RADIORA2_LOCATION[integrationid]
               action = arguments[2]
               value = arguments[3]
               if (action == '1'):
                   self.plugin.TriggerEvent('Timeclock.' + location + '.' + timeclockActionDict[action] + '.' + timeclockModeDict[value])
               elif (action == '5'):
                   self.plugin.TriggerEvent('Timeclock.' + location + '.' + timeclockActionDict[action] + '.' + timeclockEventDict[value])
               else:
                   self.plugin.TriggerEvent('Timeclock.' + location + '.' + timeclockActionDict[action], value)
               return

            if ( command.upper() == '~DEVICE' ):
                integrationid = arguments[1]
                devicetype    = RADIORA2_CONFIG[integrationid]
                location      = RADIORA2_LOCATION[integrationid]
                component     = arguments[2]
                value = ''
                lutronevent = ''
           
                if self.plugin.debug:
                    print "RadioRA2 Device> " + location + " " + devicetype + " " + component
                if ( devicetype == 'Repeater' ):
                    action       = repeaterDeviceDict[arguments[3]]
                    value        = ''
                    if ( int(component) > 100 ):
                        component = str(int(component) - 100) 
                    lutronevent  = devicetype + '.' + location + '.Button' + component 
                    if ( action == 'LED' ):
                        lutronevent = lutronevent + '.' + action
                        value     = onoffDict[arguments[4]]
                    if ( action == 'Press' ):
                        value = 'Press'
                    if ( action == 'Release'):
                        value = 'Release'                        

                if ( devicetype == 'Wallkeypad' ):
                    action       = keypadDeviceActionDict[arguments[3]]
                    if ( int(component) > 80 ):
                        component = str(int(component) - 80)
                    for className, descr, param, comp, pre in WALLKEYPAD_DEVICE_ACTIONS:
                        if ( component == comp ):
                            compaction = className
                            break
                    lutronevent  = devicetype + '.' + location + '.' + compaction
                    if ( action != 'LED' ):
                        value = action
                    else:
                        lutronevent  = lutronevent + '.' + action 
                        value        = LEDDict[arguments[4]]

                if ( devicetype == 'Hybrid' ):
                    action       = hybridDeviceActionDict[arguments[3]]
                    if ( int(component) > 80 ):
                        component = str(int(component) - 80)
                    for className, descr, param, comp, pre in HYBRID_DEVICE_ACTIONS:
                        if ( component == comp ):
                            compaction = className
                            break
                    lutronevent  = devicetype + '.' + location + '.' + compaction
                    if ( action != 'LED' ):
                        value = action
                    else:
                        lutronevent  = lutronevent + '.' + action 
                        value        = LEDDict[arguments[4]]

                if ( devicetype == 'Pico' ):
                    action       = picoDeviceActionDict[arguments[3]]
                    component = str(int(component) - 1)
                    for className, descr, param, comp, pre in PICO_DEVICE_ACTIONS:
                        if ( component == comp ):
                            compaction = className
                            break
                    lutronevent  = devicetype + '.' + location + '.' + compaction
                    value = action

                if ( devicetype == 'VCRX' ):
                    action       = vcrxDeviceActionDict[arguments[3]]
                    if ( int(component) > 80 ):
                        component = str(int(component) - 80)
                    for className, descr, param, comp, pre in VCRX_DEVICE_ACTIONS:
                        if ( component == comp ):
                            compaction = className
                            break
                    lutronevent  = devicetype + '.' + location + '.' + compaction
                    if ( action != 'LED' ):
                        value = action
                    else:
                        lutronevent  = lutronevent + '.' + action
                        value        = LEDDict[arguments[4]]

                if ( devicetype == 'Motion' ):
                    lutronevent = 'Motion.' + location + '.' + motionEventStateDict[arguments[3]]
                    value = motionEventStateDict[arguments[3]]

                if ( devicetype == 'Tablekeypad' ):
                    print "Table Keypad Not Available"              
                if ( devicetype == 'Grafikeye' ):
                    print "Grafikeye Not Available"                        
                if ( devicetype == 'Sivoiaqs' ):
                    print "Sivoia Shade Not Available"

                self.plugin.TriggerEvent(lutronevent, value)
                return

            if ( command.upper() == '~OUTPUT' ):
                integrationid   = arguments[1]
                devicetype      = RADIORA2_CONFIG[integrationid]
                location        = RADIORA2_LOCATION[integrationid]

                if ( devicetype == 'Maestro' ):
                    action          = maestroOutputDict[arguments[2]]
                    if (action == 'Flash'):
                        self.plugin.TiggerEvent(devicetype + '.' + location + '.' + action)
                    else:
                        parameters      = arguments[3].rsplit('.')
                        value           = parameters[0]
                        self.plugin.TriggerEvent(devicetype + '.' + location + '.' + action, value)

                if ( devicetype == 'Hybrid' ):
                    action          = maestroOutputDict[arguments[2]]
                    parameters      = arguments[3].rsplit('.')
                    value           = parameters[0]
                    self.plugin.TriggerEvent(devicetype + '.' + location + '.' + action, value)

                if ( devicetype == 'Sivoiaqs' ):
                    action          = shadesOutputDict[arguments[2]]
                    parameters      = arguments[3].rsplit('.')
                    value           = parameters[0]
                    self.plugin.TriggerEvent(devicetype + '.' + location + '.' + action, value)

                if ( devicetype == 'Fan' ):
                    action          = fanOutputDict[arguments[2]]
                    parameters      = arguments[3].rsplit('.')
                    value           = parameters[0]
                    if ( int(value) == 0 ):
                        value = 'Off'
                    else:  #Speed Must be Low, Medium, MediumHigh, or High
                        if ( int(value) <= 25 ):
                            value = 'Low'
                        else:  #Speed Must be Medium, MediumHigh, or High
                            if ( int(value) <= 50 ):
                                value = 'Medium'
                            else:  #Speed Must be MediumHigh or High
                                if ( int(value) <= 75 ):
                                    value = 'MediumHigh'
                                else:  #Speed Must be High
                                    value = 'High'
                    self.plugin.TriggerEvent(devicetype + '.' + location + '.' + action + '.' + value)

                if ( devicetype == 'VCRX' ):
                    action          = vcrxOutputDict[arguments[2]]
                    parameters      = arguments[3].rsplit('.')
                    value           = parameters[0]
                    if ( int(value) > 0 ):
                        value = 'Closed'
                    else:
                        value = 'Opened'
                    self.plugin.TriggerEvent(devicetype + '.' + location + '.' + action + '.' + value)

                return
        except:
            print "RadioRA2> Unexpected Response or Parse Error: " + data

    def found_terminator(self):
        """
        Called when the incoming data stream matches the termination 
        condition set by set_terminator.
        """

class NvAction(eg.ActionBase):  
    def __call__(self):
        self.plugin.DoCommand(self.command)

class KeypadAction(eg.ActionWithStringParameter):
    def __call__(self, value):
        value = eg.ParseString(value)
        action = keypadDeviceActionDict[value.title()]         
        actcommand = self.prefix + 'DEVICE,' + self.deviceid + ',' + self.component + ',' + action
        self.plugin.DoCommand(actcommand)

class TimeclockModeAction(eg.ActionWithStringParameter):
    def __call__(self, value):
        value = eg.ParseString(value)
        action = timeclockActionDict[value.title()]         
        actcommand = self.prefix + 'TIMECLOCK,' + self.deviceid + ',' + self.action + ',' + action 
        self.plugin.DoCommand(actcommand)

class TimeclockEventAction(eg.ActionBase):
    def __call__(self):         
        actcommand = self.prefix + 'TIMECLOCK,' + self.deviceid + ',' + self.action + ',' + self.timeclockeventindex 
        self.plugin.DoCommand(actcommand)

class VCRXAction(eg.ActionWithStringParameter):
    def __call__(self, value):
        value = eg.ParseString(value)
        action = vcrxDeviceActionDict[value.title()]         
        actcommand = self.prefix + 'DEVICE,' + self.deviceid + ',' + self.component + ',' + action
        self.plugin.DoCommand(actcommand)

class MaestroAction(eg.ActionWithStringParameter):    
    def __call__(self, value):
        value = eg.ParseString(value)
        if (value == ''):
            actcommand = self.prefix + 'OUTPUT,' + self.deviceid + ',' + self.action
        else:
            actcommand = self.prefix + 'OUTPUT,' + self.deviceid + ',' + self.action + ',' + value
        self.plugin.DoCommand(actcommand)

class SivoiaQSAction(eg.ActionWithStringParameter):    
    def __call__(self, value):
        value = eg.ParseString(value)
        actcommand = self.prefix + 'OUTPUT,' + self.deviceid + ',' + self.action + ',' + value
        self.plugin.DoCommand(actcommand)

class RepeaterAction(eg.ActionWithStringParameter):    
    def __call__(self, value):
        value = eg.ParseString(value)      
        if self.action == '9':
            value = int(value) + 100
        actcommand = self.prefix + 'DEVICE,' + self.deviceid + ',' + str(value) + ',' + self.action
        self.plugin.DoCommand(actcommand)

class SetLEDAction(eg.ActionWithStringParameter):
    def __call__(self, value):
        value = eg.ParseString(value)
        action = LEDDict[value.title()]         
        actcommand = self.prefix + 'DEVICE,' + self.deviceid + ',' + self.component + ',9,' + action
        self.plugin.DoCommand(actcommand)

class GetLEDState(eg.ActionBase):  
    def __call__(self):
        actcommand = self.prefix + 'DEVICE,' + self.deviceid + ',' + self.component + ',9'
        self.plugin.DoCommand(actcommand)

class LutronRadioRA2(eg.PluginBase):        
    text = Text

    def __init__(self):
        self.host = "localhost"
        self.port = 23
        self.lutronuser = "lutron"
        self.lutronpass = "lutron"
        self.isSessionRunning = False
        self.timeline = ""
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.session = None
        self.debug = False
       
        for devid, devtype in sorted(RADIORA2_CONFIG.items()):
            self.devid=devid
            devloc = RADIORA2_LOCATION[devid]               

            if devtype == 'Repeater':
                group = self.AddGroup('RA2 Repeater - ' + devid + " " + devloc)            
                for className, descr, montype, act, pre in REPEATER_MONITOR_ACTIONS:
                    cmd = pre + 'MONITORING,' + montype + ',' + act
                    clsAttributes = dict(name=descr, command=cmd)
                    cls = ClassType(className+devid, (NvAction,), clsAttributes)
                    group.AddAction(cls)               
                for className, descr, param, act, pre in REPEATER_DEVICE_ACTIONS:
                    clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc)
                    cls = ClassType(className+devid, (RepeaterAction,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'Timeclock':
                group = self.AddGroup('RA2 Timeclock - ' + devid + ' ' + devloc)
                for className, descr, param, act, pre in TIMECLOCK_ACTIONS:
                    if (className == 'SetTimeClockMode'):
                        clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, devicetype=devtype, devicelocation=devloc)
                        cls = ClassType(className+devid, (TimeclockModeAction,), clsAttributes)
                        group.AddAction(cls)
                    elif (className == 'ExecuteEvent'):
                        for event, eventindex in TIMECLOCK_EVENTS:
                            clsAttributes = dict(name=descr + ' ' + event, parameterDescription=param, action=act, prefix=pre, devicetype=devtype, devicelocation=devloc, timeclockeventindex=eventindex, deviceid=devid)
                            cls = ClassType(className+devid+event.replace(' ',''), (TimeclockEventAction,), clsAttributes)
                            group.AddAction(cls)
                    else:
                        cmd = pre + 'TIMECLOCK,' + devid + ',' + act
                        clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, devicetype=devtype, devicelocation=devloc, command = cmd)
                        cls = ClassType(className+devid+act, (NvAction,), clsAttributes)
                        group.AddAction(cls)

            if devtype == 'Hybrid':              
                group = self.AddGroup('RA2 Hybrid Keypad - ' + devid + ' ' + devloc )
                for className, descr, param, comp, pre in HYBRID_DEVICE_ACTIONS:
                    clsAttributes = dict(name=descr,parameterDescription=param,component=comp, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)   
                    if ( int(comp) < 20 ):                  
                        cls = ClassType(devtype+className+devid, (KeypadAction,), clsAttributes)
                    else:
                        if ( pre == '#' ):
                            cls = ClassType(devtype+className+devid, (SetLEDAction,), clsAttributes)
                        else:
                            cls = ClassType(devtype+className+devid, (GetLEDState,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'Wallkeypad':              
                group = self.AddGroup('RA2 Wall Keypad - ' + devid + ' ' + devloc )
                for className, descr, param, comp, pre in WALLKEYPAD_DEVICE_ACTIONS:
                    clsAttributes = dict(name=descr, parameterDescription=param, component=comp, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)   
                    if ( int(comp) < 27 ):                  
                        cls = ClassType(devtype+className+devid, (KeypadAction,), clsAttributes)
                    else:
                        if ( pre == '#' ):
                            cls = ClassType(devtype+className+devid, (SetLEDAction,), clsAttributes)
                        else:
                            cls = ClassType(devtype+className+devid, (GetLEDState,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'Maestro':
                group = self.AddGroup('RA2 Maestro - ' + devid + ' ' + devloc )
                for className, descr, param, act, pre in MAESTRO_OUTPUT_ACTIONS:
                    cmd = pre + 'OUTPUT,' + devid + ',' + act
                    clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)
                    if ( className == 'SetZoneLevel' or className == 'Flash'):
                        cls = ClassType(devtype+className+devid, (MaestroAction,), clsAttributes)
                    else:
                        cls = ClassType(devtype+className+devid, (NvAction,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'Sivoiaqs':
                group = self.AddGroup('RA2 Shade - ' + devid + ' ' + devloc )
                for className, descr, param, act, pre in SIVOIAQS_OUTPUT_ACTIONS:
                    cmd = pre + 'OUTPUT,' + devid + ',' + act               
                    clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd) 
                    if ( className == 'SetShadeLevel' ):
                        cls = ClassType(devtype+className+devid, (SivoiaQSAction,), clsAttributes)
                    else:
                        cls = ClassType(devtype+className+devid, (NvAction,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'Fan':
                group = self.AddGroup('RA2 Fan - ' + devid + ' ' + devloc )
                for className, descr, param, act, pre in FAN_OUTPUT_ACTIONS:
                    cmd = pre + 'OUTPUT,' + devid + ',' + act
                    clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)
                    if ( className == 'SetFanLevel' ):
                        cls = ClassType(devtype+className+devid, (MaestroAction,), clsAttributes)
                    else:
                        cls = ClassType(devtype+className+devid, (NvAction,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'Pico':              
                group = self.AddGroup('RA2 Pico Keypad - ' + devid + ' ' + devloc )
                for className, descr, param, comp, pre in PICO_DEVICE_ACTIONS:
                    cmd = pre + 'DEVICE,' + devid + ',' + comp
                    clsAttributes = dict(name=descr,parameterDescription=param,component=comp, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)   
                    cls = ClassType(devtype+className+devid, (KeypadAction,), clsAttributes)
                    group.AddAction(cls)

            if devtype == 'VCRX':              
                group = self.AddGroup('RA2 Visor Receiver - ' + devid + ' ' + devloc )
                for className, descr, param, act, pre in VCRX_OUTPUT_ACTIONS:
                    cmd = pre + 'OUTPUT,' + devid + ',' + act
                    clsAttributes = dict(name=descr, parameterDescription=param, action=act, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)
                    if ( className == 'SetCCO' or className == 'SetPulseCCO' ):
                        cls = ClassType(devtype+className+devid, (MaestroAction,), clsAttributes)
                    else:
                        cls = ClassType(devtype+className+devid, (NvAction,), clsAttributes)
                    group.AddAction(cls)
                for className, descr, param, comp, pre in VCRX_DEVICE_ACTIONS:
                    clsAttributes = dict(name=descr,parameterDescription=param,component=comp, prefix=pre, deviceid=devid, devicetype=devtype, devicelocation=devloc, command = cmd)   
                    if ( int(comp) < 34 ):                  
                        cls = ClassType(devtype+className+devid, (VCRXAction,), clsAttributes)
                    else:
                        if ( pre == '#' ):
                            cls = ClassType(devtype+className+devid, (SetLEDAction,), clsAttributes)
                        else:
                            cls = ClassType(devtype+className+devid, (GetLEDState,), clsAttributes)
                    group.AddAction(cls)

        self.AddAction(self.MyCommand)
        self.AddEvents()


    def __start__(
        self,
        host="192.168.1.10", 
        port=23,
        lutronuser="lutron",
        lutronpass="lutron",
        dummy1=None,
        dummy2=None,
        debug=False
    ):
        self.host = host
        self.port = port
        self.lutronuser = lutronuser
        self.lutronpass = lutronpass
        self.debug = debug
            
        if not self.isSessionRunning:
            self.session = LutronRadioRA2Session(self, (self.host, self.port))
            self.isSessionRunning = True
            if self.debug:
               print "RadioRA2> Session is Running" 
        
    def __stop__(self):
        if self.isSessionRunning:
            self.session.close()

    @eg.LogIt

    def DoCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = LutronRadioRA2Session(self, (self.host, self.port))
           
            self.isSessionRunning = True
            if self.debug:
               print "RadioRA2> Do Command Session is Running"
        try:
            if self.debug:
               print "RadioRA2> Trying: " + cmdstr 
            self.session.sendall(cmdstr + "\r\n")
        except:
            self.isSessionRunning = False
            self.TriggerEvent('close')
            self.session.close()
        self.waitFlag.wait(2.0)
        self.waitStr = None
        self.waitFlag.set()

    def SetOSD(self, text):
        self.DoCommand("1200 " + text)

    def Configure(
        self,
        host="192.168.1.10",
        port=23,
        lutronuser="lutron",
        lutronpass="lutron",
        dummy1=None,
        dummy2=None,
        debug=False
    ):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)       
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(lutronuser)
        passCtrl = panel.TextCtrl(lutronpass)
        debugCtrl = panel.CheckBox(debug, "")
        
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl),
            (text.portLabel, portCtrl),
            (text.userLabel, userCtrl),
            (text.passLabel, passCtrl),
            ('Debug', debugCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                userCtrl.GetValue(),
                passCtrl.GetValue(),
                None,
                None,
                debugCtrl.GetValue(),
            )

    class MyCommand(eg.ActionWithStringParameter):
        name = "Raw Command"
        def __call__(self, value):
            value = eg.ParseString(value)  
            self.plugin.DoCommand(value)