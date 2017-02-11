# -*- coding: utf-8 -*-

ur"""<rst>
Plugin for the Holtek.

.. image:: picture.gif
   :align: center
"""

import eg

eg.RegisterPlugin(
    name = "Holtek",
    author = "bob",
    version = "1.0.0",
    kind = "remote",
    guid = "{4D1E55B2-F16F-11CF-88CB-001111005530}",
    description = __doc__,
   hardwareId = "USB\\VID_1241&PID_F767",
)

class Holtek(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "Holtek",
            "USB\\VID_1241&PID_F767", 
            "{4D1E55B2-F16F-11CF-88CB-001111006630}",
            self.ButtonsCallback,
            4,
        )
        self.usb.Open()


    def __stop__(self):
        self.usb.Close()


    def ButtonsCallback(self, data):
        print "Holtek:", data