import eg

eg.RegisterPlugin(
    name = "ActionValue",
    author = "rdgerken",
    version = "0.0.1",
    kind = "other",
    description = "This plugin is for action value troubleshooting.",
    canMultiLoad = True,
    createMacrosOnAdd = True
)

CONFIG = {
     '100' : 'Room A',
     '200' : 'Room B',
     '300' : 'Room C',
     '400' : 'Room D'         
}

# IntegrationID
# Description of device location

LOCATION = {
     '100' : 'This is Room A',
     '200' : 'This is Room B',
     '300' : 'This is Room C',
     '400' : 'This is Room D'
}

DEVICE_ACTIONS = (
('SETZONELEVEL',   'Maestro Set Zone Level (Level 0-100, *Fade in MM:SS, *Delay MM:SS) *optional', '1', '#'),
('GETZONELEVEL',   'Maestro Get Zone Level', '1', '?'),
('RAISE',          'Start Raise Level',      '2', '#'),
('LOWER',          'Start Lower Level',      '3', '#'),
('STOP',           'Stop Level Change',      '4', '#'),
('FLASH',          'Start Flashing',         '5', '#'),
('STOPFLASH',      'Stop Flashing',          '6', '#')
)

from types import ClassType

class ActionValuePlugin(eg.PluginBase):

    def __init__(self):
        for deviceid, devicetype in sorted(CONFIG.items()):
            devicelocation = LOCATION[deviceid]
            group = self.AddGroup('TestRoom - ' + deviceid + ' ' + devicelocation )
            for className, descr, act, pre in DEVICE_ACTIONS:
                command = pre + 'OUTPUT,' + deviceid + ',' + act               
                clsAttributes = dict(
                name=descr,
                action=act,
                prefix=pre,
                deviceid=deviceid,
                devicetype=devicetype,
                devicelocation=devicelocation,
                command = command
                )
                cls = ClassType(className, (MyAction,), clsAttributes)
                group.AddAction(cls)


class MyAction(eg.ActionWithStringParameter):
    name = "Action Test"
    description = "This action tests values."

    def __call__(self, value):
        print "Action Test called: user value   = " + value
        print "Action Test called: command value   = " + self.command