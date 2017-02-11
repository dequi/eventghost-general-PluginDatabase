#
# EPSON EH-TW 9100 V0.1
# =====================
# Written by 0815, <th.wittstock@gmail.com>
# 
# Revision history:
# -----------------
# 0.1 - initial
#


eg.RegisterPlugin(
    name = "EPSON EH-TW 9100 Serial",
    author = "Thomas Wittstock",
    version = "0.1",
    kind = "external",
    description = "Control an EPSON EH-TW 9100 projector via RS232",
    guid = "",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARn"
        "QU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdw"
        "nLpRPAAAABZ0RVh0U29mdHdhcmUAUGFpbnQuTkVUIDIuNmyodLUAAAJCSURBVDhPpZNb"
        "bxJRFIWtIQVaBmFA7jCUAcr9futQSoFQKIg0sfqs6YMmPumbhsQHr9E02liDiZqmbQoo"
        "tMVL/CU+6K9ZPTMppHFoYuIk83L2Wd9ee2edqd9/fl34r48H/PVLvv8cYvPNJlqPWnj8"
        "/Cn2DnYx4Z6gOyuWfNxpo7l+De5ABJ5QDPOhKFhfEDZ2HuVaHa9ev0Snt8/DFCPgGNDt"
        "7aLWXEN0YQneaAI2lwdmhoXZ7oTDG4DTFwK3XMR2ewuHx/2xozGAp6fzJYSSGegtDJS0"
        "DiatA15DGHaLG3Mev+Bq485tDI6+iAF8gStViF03KLUWCpUGapUeJpqFy+CF3mhFIJZG"
        "oVJDb9AVAxrr14mDImidUehOa+xwmMJgaQYqAqK1BrKPEFK5ZXT7EwArjSYSpHhJo4NR"
        "ZycCC+RKGlL5LKZlM8TVZWEPqVwBnw8njFBavYLF8ioMNh8BeODUBkERgEyugJQANAYz"
        "vOE4cuUqBsOBeIRCeQXF+hpiXBW0MULGsGKGUkE6q4SSuLLMuUhtCaV6A19/DMWAmxu3"
        "EE5lka9eRWrxBsxsFmodAxPjINaDCMTTcPkjuHvvPi/OiHIw/NYX5o9zeXDFChYKdSET"
        "vkgC0UwOvlgKSS6Hvc7kIE3xxAeth2RpFKzErj+aRDidFTqb7C4hjVvvtkfdnSIHpwfK"
        "Jy+egSGXZQoV5JQaFK0HRwL2YefTSHyR3JWcB+CTyc/n3O8c4G37PQbHR7xw+l8e0yjW"
        "44dynujs+Qnye/WIemQx5AAAAABJRU5ErkJggg=="
    ),
)


import thread
import time
import re


cmdList = (
('Power', None, None, None),
('PowerOn', 'Power On', 'PWR ON', None ), 
('PowerOff', 'Power Off', 'PWR OFF', None ),
('PowerStatus', 'Power Status', 'PWR?', None ),
#*****************************
('ProjectionScreenAdjustment', None, None, None),
('VKeystoneUp', 'Vertical Keystone Up', 'VKEYSTONE INC', None ),
('VKeystoneDown', 'Vertical Keystone Down', 'VKEYSTONE DEC', None ),
('VKeystoneSet', 'Vertical Keystone Set', 'VKEYSTONE', '0-255' ),
('VKeystoneStatus', 'Vertical Keystone Status', 'VKEYSTONE?', None ),
#*****************************
('AspectNormal', 'Aspect Normal', 'ASPECT 00', None ),
('AspectAuto', 'Aspect Auto', 'ASPECT 30', None ),
('AspectFull', 'Aspect Full', 'ASPECT 40', None ),
('AspectZoom', 'Aspect Zoom', 'ASPECT 50', None ),
('AspectWide', 'Aspect Wide', 'ASPECT 70', None ),
('AspectAnamorphic', 'Aspect Anamorphic', 'ASPECT 80', None ),
('AspectHsqueeze', 'Aspect Hsqueeze', 'ASPECT 90', None ),
('AspectStatus', 'Aspect Status', 'ASPECT?', None ),
#*****************************
('LuminanceNormal', 'Luminance Normal', 'LUMINANCE 00', None ),
('LuminanceEco', 'Luminance Eco', 'LUMINANCE 01', None ),
('LuminanceStatus', 'Luminance Status', 'LUMINANCE?', None ),
#*****************************
('OverscanOff', 'Overscan Off', 'OVSCAN 00', None ),
('Overscan2Percent', 'Overscan 2 Percent', 'OVSCAN 01', None ),
('Overscan4Percent', 'Overscan 4 Percent', 'OVSCAN 02', None ),
('Overscan6percent', 'Overscan 6 Percent', 'OVSCAN 03', None ),
('Overscan8Percent', 'Overscan 8 Percent', 'OVSCAN 04', None ),
('OverscanAuto', 'Overscan Auto', 'OVSCAN A0', None ),
('OverscanStatus', 'Overscan Status', 'OVSCAN?', None ),
#*****************************
('Inputs/Routing', None, None, None),
#Input1
('Input1Component2RCA', 'Input 1 Component 2RCA', 'SOURCE 10', None ),
('Input1ComponentYCbCr', 'Input 1 Component YCbCr', 'SOURCE 14', None ),
('Input1ComponentYPbPr', 'Input 1 Component YPbPr', 'SOURCE 15', None ),
('Input1Auto', 'Input 1 Auto', 'SOURCE 1F', None ),
#Input2
('Input2Dsub13', 'Input 2 Dsub13', 'SOURCE 20', None ),
('Input2RGB', 'Input 2 RGB', 'SOURCE 21', None ),
#Input3
('Input3HDMI1', 'Input 3 HDMI 1', 'SOURCE 30', None ),
('Input3DigitalRGB', 'Input 3 Digital RGB', 'SOURCE 31', None ),
('Input3RGBVideo', 'Input 3 RGB-Video', 'SOURCE 33', None ),
('Input3YCbCr', 'Input 3 YCbCr', 'SOURCE 34', None ),
('Input3YPbPr', 'Input 3 YPbPr', 'SOURCE 35', None ),
#*****************************
('InputVideo', 'Input Video', 'SOURCE 40', None ),
('InputVideoRCA', 'Input Video RCA', 'SOURCE 41', None ),
('InputHDMI2', 'Input HDMI 2', 'SOURCE A0', None ),
('InputDigitalRGB', 'Input Digital RGB', 'SOURCE A1', None ),
('InputRGBVideo', 'Input RGB-Video', 'SOURCE A3', None ),
('InputYCbCr', 'Input YCbCr', 'SOURCE A4', None ),
('InputYPbPr', 'Input YPbPr', 'SOURCE A5', None ),
#cyclic
('InputAllCyclic', 'Input All Cyclic', 'SOURCE F0', None ),
('InputPCcyclic', 'Input PC Cyclic', 'SOURCE F1', None ),
('InputVideoCyclic', 'Input Video Cyclic', 'SOURCE F2', None ),
#*****************************
('InputStatus', 'Input Status', 'SOURCE?', None ),
#*****************************
('ImageSetting', None, None, None),
('BrightUp', 'Bright Up', 'BRIGHT INC', None ),
('BrightDown', 'Bright Down', 'BRIGHT DEC', None ),
('BrightSet', 'Bright Set', 'BRIGHT', '0-255' ),
('BrightStatus', 'Bright Status', 'BRIGHT?', None ),
#*****************************
('ContrastUp', 'Contrast Up', 'CONTRAST INC', None ),
('ContrastDown', 'Contrast Down', 'CONTRAST DEC', None ),
('ContrastSet', 'Contrast Set', 'CONTRAST', '0-255' ),
('ContrastStatus', 'Contrast Status', 'CONTRAST?', None ),
#*****************************
('DensityUp', 'Density Up', 'DENSITY INC', None ),
('DensityDown', 'Density Down', 'DENSITY DEC', None ),
('DensitySet', 'Density Set', 'DENSITY', '0-255' ),
('DensityStatus', 'Density Status', 'DENSITY?', None ),
#*****************************
('TintUp', 'Tint Up', 'TINT INC', None ),
('TintDown', 'Tint Down', 'TINT DEC', None ),
('TintSet', 'Tint Set', 'TINT', '0-255' ),
('TintStatus', 'Tint Status', 'TINT?', None ),
#*****************************
('SharpUp', 'Sharp Up', 'SHARP INC', None ),
('SharpDown', 'Sharp Down', 'SHARP DEC', None ),
('SharpSet', 'Sharp Set', 'SHARP', '0-255' ),
('SharpStatus', 'Sharp Status', 'SHARP?', None ),
#*****************************
('ColorTempUp', 'ColorTemp Up', 'CTEMP INC', None ),
('ColorTempDown', 'ColorTemp Down', 'CTEMP DEC', None ),
('ColorTempSet', 'ColorTemp Set', 'CTEMP', '0-255' ),
('ColorTempStatus', 'ColorTemp Status', 'CTEMP?', None ),
#*****************************
('FColorUp', 'FColor Up', 'FCOLOR INC', None ),
('FColorDown', 'FColor Down', 'FCOLOR DEC', None ),
('FColorSet', 'FColor Set', 'FCOLOR', '0-255' ),
('FColorStatus', 'FColor Status', 'FCOLOR?', None ),
#*****************************
('HorizontalPosUp', 'HorizontalPos Up', 'HPOS INC', None ),
('HorizontalPosDown', 'HorizontalPos Down', 'HPOS DEC', None ),
('HorizontalPosSet', 'HorizontalPos Set', 'HPOS', '0-255' ),
('HorizontalPosStatus', 'HorizontalPos Status', 'HPOS?', None ),
#*****************************
('VerticalPosUp', 'VerticalPos Up', 'VPOS INC', None ),
('VerticalPosDown', 'VerticalPos Down', 'VPOS DEC', None ),
('VerticalPosSet', 'VerticalPos Set', 'VPOS', '0-255' ),
('VerticalPosStatus', 'VerticalPos Status', 'VPOS?', None ),
#*****************************
('TrackingUp', 'Tracking Up', 'TRACKING INC', None ),
('TrackingDown', 'Tracking Down', 'TRACKING DEC', None ),
('TrackingSet', 'Tracking Set', 'TRACKING', '0-255' ),
('TrackingStatus', 'Tracking Status', 'TRACKING?', None ),
#*****************************
('SyncUp', 'Sync Up', 'SYNC INC', None ),
('SyncDown', 'Sync Down', 'SYNC DEC', None ),
('SyncSet', 'Sync Set', 'SYNC', '0-255' ),
('SyncStatus', 'Sync Status', 'SYNC?', None ),
#*****************************
('NrsOff', 'Nrs Off', 'NRS 01', None ),
('NrsSetting1', 'Nrs Setting 1', 'NRS 02', None ),
('NrsSetting2', 'Nrs Setting 2', 'NRS 03', None ),
('NrsSetting3', 'Nrs Setting 3', 'NRS 04', None ),
('NrsStatus', 'Nrs Status', 'NRS?', None ),
#*****************************
('OffSetRUp', 'OffSetR Up', 'OFFSETR INC', None ),
('OffSetRDown', 'OffSetR Down', 'OFFSETR DEC', None ),
('OffSetRSet', 'OffSetR Set', 'OFFSETR', '0-255' ),
('OffSetRStatus', 'OffSetR Status', 'OFFSETR?', None ),
#*****************************
('OffSetGUp', 'OffSetG Up', 'OFFSETG INC', None ),
('OffSetGDown', 'OffSetG Down', 'OFFSETG DEC', None ),
('OffSetGSet', 'OffSetG Set', 'OFFSETG', '0-255' ),
('OffSetGStatus', 'OffSetG Status', 'OFFSETG?', None ),
#*****************************
('OffSetBUp', 'OffSetB Up', 'OFFSETB INC', None ),
('OffSetBDown', 'OffSetB Down', 'OFFSETB DEC', None ),
('OffSetBSet', 'OffSetB Set', 'OFFSETB', '0-255' ),
('OffSetBStatus', 'OffSetB Status', 'OFFSETB?', None ),
#*****************************
('GainRUp', 'GainR Up', 'GAINR INC', None ),
('GainRDown', 'GainR Down', 'GAINR DEC', None ),
('GainRSet', 'GainR Set', 'GAINR', '0-255' ),
('GainRStatus', 'GainR Status', 'GAINR?', None ),
#*****************************
('GainGUp', 'GainG Up', 'GAING INC', None ),
('GainGDown', 'GainG Down', 'GAING DEC', None ),
('GainGSet', 'GainG Set', 'GAING', '0-255' ),
('GainGStatus', 'GainG Status', 'GAING?', None ),
#*****************************
('GainBUp', 'GainB Up', 'GAINB INC', None ),
('GainBDown', 'GainB Down', 'GAINB DEC', None ),
('GainBSet', 'GainB Set', 'GAINB', '0-255' ),
('GainBStatus', 'GainB Status', 'GAINB?', None ),
#********ToDoList*************
#GAMMA xx
#GAMMALV x1 x2
#GAMMALV? xx
#POPMEM x1 x2
#PUSHMEM x1 x2
#ERASEMEM x1 x2
#CSEL?
#CGAMUT xx
#SUPERRES x1
#PULLDOWN x1
#MCFI xx


#*****************************
('UniqueFunction', None, None, None),
('ExecuteBlank', 'Execute Blank', 'MUTE ON', None ),
('CancelBlank', 'Cancel Blank', 'MUTE OFF', None ),
('StatusMute', 'Status Mute', 'MUTE?', None ),
#*****************************
('3dSetting', None, None, None),
('3DdisplayOff', '3D Display Off', '3DIMENSION 01 00', None ),
('3DdisplayOn', '3D Display On', '3DIMENSION 01 01', None ),
('3DdisplayStatus', '3D Display Status', '3DIMENSION? 01', None ),
#*****************************
('2Dto3DconversionOff', '2D-to-3D Conversion Off', '3DIMENSION 02', None ),
#*****************************
('MainKey', None, None, None),
('Power', 'Power', 'KEY 01', None ),
('Menu', 'Menu', 'KEY 03', None ),
('ESC', 'ESC', 'KEY 05', None ),
('Enter', 'Enter', 'KEY 16', None ),
('Up', 'Up', 'KEY 35', None ),
('Down', 'Down', 'KEY 36', None ),
('Left', 'Left', 'KEY 37', None ),
('Right', 'Right', 'KEY 38', None ),
('Source', 'Source', 'KEY 48', None ),
#*****************************
('Raw', 'Send Raw command', '', '*'),
)


class EpsonEHTW9100Serial(eg.PluginClass):

    def __init__(self):
        self.serial = None
        group = self
        self.EventList = {
			'ERR':{
				'content':'Error'
				},
			'PWR':{
				'content':'PowerStatus',
				'00':'Standby',
				'01':'LampON',
				'02':'Warmup',                             
				'03':'CoolDown',
				'05':'AbnormalityStandby'
				},
			'VKEYSTONE':{
				'content':'VertikalKeyStone'
				},
			'ASPECT':{
				'content':'AspectRatio',
				'00':'Normal',
				'30':'Auto',
				'40':'Full',
				'50':'Zoom',
				'70':'Wide',
				'80':'Anamorphic',
				'90':'Hsqueeze'
				},
			'LUMINANCE':{
				'content':'Luminance',
				'00':'Normal',
				'01':'Eco'
				},
			'OVSCAN':{
				'content':'Overscan',
				'00':'Off',
				'01':'2%',
				'02':'4%',
				'03':'6%',
				'04':'8%',
				'A0':'Auto'
				},
			'SOURCE':{
				'content':'Source',			
				'10':'Input1Component2RCA',
				'14':'Input1ComponentYCbCr',
				'15':'Input1ComponentYPbPr',
				'1F':'Input1Auto',
				'20':'Input2Dsub13',
				'21':'Input2RGB',
				'30':'Input3HDMI1',
				'31':'Input3DigitalRGB',
				'33':'Input3RGBVideo',
				'34':'Input3YCbCr',
				'35':'Input3YPbPr',
				'40':'InputVideo',
				'41':'InputVideoRCA',
				'A0':'InputHDMI2',
				'A1':'InputDigitalRGB',
				'A3':'InputRGBVideo',
				'A4':'InputYCbCr',
				'A5':'InputYPbPr',
				'F0':'InputAllCyclic',
				'F1':'InputPCcyclic',
				'F2':'InputYPbPr'
				},				
			'MUTE':{
				'content':'ScreenStatus',
				'OFF':'NotBlank',
				'ON':'Blank'
				},
			'3DIMENSION':{
				'content':'3dSetting',
				'00':'Off',
				'01':'On'
				},					
		}

		
        def createWriter(cmd):
            def write(self):
                self.plugin.serial.write(cmd)
                self.plugin.serial.write(chr(13))
            return write
            
        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_name)
            else:
                # Argumentless command
                class Handler(eg.ActionClass):
                    name = cmd_name
                    description = cmd_text
                    __call__ = createWriter(cmd_cmd)
                Handler.__name__ = cmd_name
                group.AddAction(Handler)
               

    # Serial port reader
    def reader(self):
        line = ""
        while self.readerkiller is False:
            ch = self.serial.read()
            if ch == '\r':
				#print line
				if line.find('=') > 0 :
					m = line.replace(':', '').split('=')
					if (m[0] in self.EventList) and (m[1] in self.EventList[m[0]]) :
						self.TriggerEvent(self.EventList[m[0]]['content']+ '.' + self.EventList[m[0]][m[1]])
					elif (m[0] in self.EventList) and (m[1] not in self.EventList[m[0]]) :
						self.TriggerEvent(self.EventList[m[0]]['content']+ '.' + m[1])
					elif (m[0] not in self.EventList) :
						self.TriggerEvent(m[0] + '.' + m[1])
				else:
					m = line.replace(':', '')
					if (m in self.EventList) :
						self.TriggerEvent(self.EventList[m]['content'])
					else :
						self.TriggerEvent(m)
				line = ""		
            else:
                line += ch

				
    def __start__(self, port):
        try:
            self.serial = eg.SerialPort(port)
        except:
            raise eg.Exception("Can't open serial port.")
        self.serial.baudrate = 9600
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader, ());
        
        
    def __stop__(self):
        self.readerkiller = True
        if self.serial is not None:
            self.serial.close()
            self.serial = None
            
            
    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())
                    
