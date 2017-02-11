#!/usr/bin/env python2

# XInput Game Controller APIs
# http://msdn.microsoft.com/en-us/library/windows/desktop/hh405053%28v=vs.85%29.aspx

# How can I use a DLL from Python
# https://stackoverflow.com/questions/252417/how-can-i-use-a-dll-from-python



import os, shutil, math, ctypes

PLUGIN_NAME                         = 'Xbox 360 Controller (XInput)'
PLUGIN_AUTHOR                       = 'TheRetroPirate'
PLUGIN_VERSION                      = '0.0.1'
PLUGIN_DESCRIPTION                  = """<rst>
Supports the "Microsoft X360 Controller for Windows", any compatible controller should also work.

*Features:*

- **requires "Xinput9_1_0.dll" shipped with Windows Vista or newer**
- **multiple controllers (up to 4)**
- **supports buttons, triggers and analog sticks**
- **analog inputs can be treated as buttons**
- **deadzone handling**
- **detects plug/unplug of controllers**
- **adjustable polling rate**

"""
PLUGIN_ICON                         = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAeJJREFUOMul
k09I02EYxz/Pu/e33J80R6UUlEsolDCCYkSJ5S3oD1RCHaJDSEhQEHjpItShSxAU1M2SCCLo0EU6
RV2KQCwkaqXk2PyTy0bbbGtuv/ftEK0xo0Y+3+vz+fLl+fKIxbKcUSxzFIAoccWRYq2QaCmKltLv
BEZkWz/T0q5i0iLxv8H+Dkls6mWGVZID0AAWowJDkt91wc4m4mRkXF7aYRuphr298rQtTM5ZQNl5
Uw8glUcUJe7RmyQDnaSfDOJO+b1v7eVCj5x3HresL23ojhB8FWVy9IztKjPVLSiPuKcHSTUdI/Nh
DD31HDe7EfaG0fEQI4/C9kjlvq6OaVzrWXND0gdLBPd34fMdRi8s4j5oYvhZqC5aU42fR2zD6maM
D3TaUJAcKnOL7QXJD9Rk0HZN3rQ2EwiV0BNRTOorxc27WbnikIwuqbT6BuvOytjJPhqddwTv3cZ4
/Jh6B919kex0EvfhXWKLd+y+MmAr1HCA8asxZo5fIQXKIhiLBcH41vL93AsSPUMk2KNf/2LKcHAn
c5feMxmO8A2UtSyV8lI6MUC27z6zTiufygaBDuY7rzPha6T4J7BSIHbHKb5s7efjz3RB8moLSaVx
/wVXStdRknbmRDy4xrWe//3GH4uN7Ni6Xm5TAAAAAElFTkSuQmCC"""






###################################
###                             ###
###   Install plugin            ###
###                             ###
###################################

if __name__ == '__main__':
	# this code is not called by EventGhost, only if executed as a normal script
	MB_OK              = 0x00000000
	MB_YESNO           = 0x00000004
	MB_ICONQUESTION    = 0x00000020
	MB_ICONERROR       = 0x00000010
	MB_ICONINFORMATION = 0x00000040
	IDYES              = 6
	IDNO               = 7
	MessageBox = ctypes.windll.user32.MessageBoxA
	if MessageBox(None, 'Install this plugin for EventGhost?', PLUGIN_NAME, MB_YESNO | MB_ICONQUESTION) == IDYES:
		fn = __file__
		if not os.path.exists(fn):
			MessageBox(None, 'Could not find plugin file.', PLUGIN_NAME, MB_OK | MB_ICONERROR)
			exit()
		
		# get EventGhost folder
		targets = ['%programfiles%/EventGhost/plugins',  '%programfiles(x86)%/EventGhost/plugins']
		target  = ''
		for t in targets:
			target = os.path.expandvars(t)
			if os.path.exists(target):
				break
			else:
				target = ''
		
		if target == '':
			MessageBox(None, 'Could not find EventGhost plugin folder, is it installed?', PLUGIN_NAME, MB_OK | MB_ICONERROR)
			exit()
		
		# check plugin subfolder
		target = os.path.join(target, 'XInput')
		if os.path.exists(target):
			if MessageBox(None, 'It seems this plugin is already installed, override?', PLUGIN_NAME, MB_YESNO | MB_ICONQUESTION) == IDNO:
				exit()
		
		# install
		if not os.path.exists(target):
			os.mkdir(target)
		
		try:
			t = os.path.join(target, '__init__.py')
			if os.path.exists(t):
				os.remove(t)
			shutil.copyfile(fn, t)
		except:
			MessageBox(None, 'Could not copy plugin file.', PLUGIN_NAME, MB_OK | MB_ICONERROR)
			exit()
		
	MessageBox(None, 'Plugin installed.', PLUGIN_NAME, MB_OK | MB_ICONINFORMATION)
	exit()
	






###################################
###                             ###
###   XInput                    ###
###                             ###
###################################

ERROR_SUCCESS                       =    0
ERROR_DEVICE_NOT_CONNECTED          = 1167 # 0x48F
XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE  = 7849
XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE = 8689
XINPUT_GAMEPAD_TRIGGER_THRESHOLD    =   30
XINPUT_GAMEPAD_RANGE                = range(0,4) # XInput allows up to four pads 0, 1, 2, 3


XInputDLL = ctypes.windll.LoadLibrary("Xinput9_1_0") # Windows Vista
#XInputDLL = ctypes.windll.LoadLibrary("xinput1_3")   # DirectX SDK
#XInputDLL = ctypes.windll.LoadLibrary("xinput1_4")   # Windows 8

# XINPUT_GAMEPAD structure
# http://msdn.microsoft.com/en-us/library/windows/desktop/microsoft.directx_sdk.reference.xinput_gamepad%28v=vs.85%29.aspx
# typedef struct _XINPUT_GAMEPAD {
#   WORD  wButtons;
#   BYTE  bLeftTrigger;
#   BYTE  bRightTrigger;
#   SHORT sThumbLX;
#   SHORT sThumbLY;
#   SHORT sThumbRX;
#   SHORT sThumbRY;
# } XINPUT_GAMEPAD, *PXINPUT_GAMEPAD;
class STRUCT_XINPUT_GAMEPAD(ctypes.Structure):
	_fields_ = [
					('wButtons'     , ctypes.c_ushort),
					('bLeftTrigger' , ctypes.c_ubyte),
					('bRightTrigger', ctypes.c_ubyte),
					('sThumbLX'     , ctypes.c_short),
					('sThumbLY'     , ctypes.c_short),
					('sThumbRX'     , ctypes.c_short),
					('sThumbRY'     , ctypes.c_short),
					]



# XINPUT_STATE structure
# http://msdn.microsoft.com/en-us/library/windows/desktop/microsoft.directx_sdk.reference.xinput_state%28v=vs.85%29.aspx
# typedef struct _XINPUT_STATE {
#   DWORD          dwPacketNumber;
#   XINPUT_GAMEPAD Gamepad;
# } XINPUT_STATE, *PXINPUT_STATE;
class STRUCT_XINPUT_STATE(ctypes.Structure):
	_fields_ = [
					('dwPacketNumber', ctypes.c_uint),
					('Gamepad'       , STRUCT_XINPUT_GAMEPAD)
					]



# XInputGetState function
# http://msdn.microsoft.com/en-us/library/windows/desktop/microsoft.directx_sdk.reference.xinputgetstate%28v=vs.85%29.aspx
# DWORD XInputGetState(
#   _In_   DWORD dwUserIndex,
#   _Out_  XINPUT_STATE *pState
# 
# );
XInputGetStateAPI          = XInputDLL.XInputGetState
XInputGetStateAPI.argtypes = [ctypes.c_uint, ctypes.c_void_p]
XInputGetStateAPI.restype = ctypes.c_uint

def XInputGetState( PacketNumber, XINPUT_STATE):
	return XInputGetStateAPI(ctypes.c_uint(PacketNumber), ctypes.byref(XINPUT_STATE))




GamePadButton = {
					'DPAD_UP'           : 'DPad UP',
					'DPAD_DOWN'         : 'DPad DOWN',
					'DPAD_LEFT'         : 'DPad LEFT',
					'DPAD_RIGHT'        : 'DPad RIGHT',
					'START'             : 'Start',
					'BACK'              : 'Back',
					'LTHUMB'            : 'Left Thumb',
					'RTHUMB'            : 'Right Thumb',
					'LSHOULDER'         : 'Left Shoulder',
					'RSHOULDER'         : 'Right Shoulder',
					'A'                 : 'A',
					'B'                 : 'B',
					'X'                 : 'X',
					'Y'                 : 'Y',
					
					'LTHUMB_UP'         : 'Left Thumb UP',
					'LTHUMB_DOWN'       : 'Left Thumb DOWN',
					'LTHUMB_LEFT'       : 'Left Thumb LEFT',
					'LTHUMB_RIGHT'      : 'Left Thumb RIGHT',
					'LTHUMB_UP_RIGHT'   : 'Left Thumb UP RIGHT',
					'LTHUMB_RIGHT_DOWN' : 'Left Thumb RIGHT DOWN',
					'LTHUMB_DOWN_LEFT'  : 'Left Thumb DOWN LEFT',
					'LTHUMB_LEFT_UP'    : 'Left Thumb LEFT UP',
					
					'RTHUMB_UP'         : 'Right Thumb UP',
					'RTHUMB_DOWN'       : 'Right Thumb DOWN',
					'RTHUMB_LEFT'       : 'Right Thumb LEFT',
					'RTHUMB_RIGHT'      : 'Right Thumb RIGHT',
					'RTHUMB_UP_RIGHT'   : 'Right Thumb UP RIGHT',
					'RTHUMB_RIGHT_DOWN' : 'Right Thumb RIGHT DOWN',
					'RTHUMB_DOWN_LEFT'  : 'Right Thumb DOWN LEFT',
					'RTHUMB_LEFT_UP'    : 'Right Thumb LEFT UP',
					
					'LTRIGGER'          : 'Left Trigger',
					'RTRIGGER'          : 'Right Trigger',
}

GamePadAxis = {
					'LTHUMBX'           : 'Left Thumb X',
					'LTHUMBY'           : 'Left Thumb Y',
					'RTHUMBX'           : 'Right Thumb X',
					'RTHUMBY'           : 'Right Thumb Y',
					'LTRIGGER'          : 'Left Trigger',
					'RTRIGGER'          : 'Right Trigger',
}

class GamePad:
	
	
	def __init__(self, ID):
		self._ID                         = max(min(ID, 3), 0) # 0..3
		self._Connected                  = False
		self._XINPUT_STATE               = STRUCT_XINPUT_STATE()
		self._Axis                       = {}
		self._Button                     = {}
		self.update()
	
	
	def _deadzone(self, sourceX, sourceY, INPUT_DEADZONE):
		# http://msdn.microsoft.com/en-us/library/windows/desktop/ee417001%28v=vs.85%29.aspx#dead_zone
		x = float(sourceX)
		y = float(sourceY)
		
		# determine how far the controller is pushed
		magnitude = math.sqrt( x*x + y*y )
		
		# check if the controller is outside a circular dead zone
		if magnitude > INPUT_DEADZONE:
			# determine the direction the controller is pushed
			normalizedX = x / magnitude
			normalizedY = y / magnitude
			
			# clip the magnitude at its expected maximum value
			magnitude = min(magnitude, 32767)
			
			# adjust magnitude relative to the end of the dead zone
			magnitude = magnitude - INPUT_DEADZONE
			
			# optionally normalize the magnitude with respect to its expected range
			# giving a magnitude value of 0.0 to 1.0
			normalizedMagnitude = magnitude / (32767 - INPUT_DEADZONE)
			
			return (normalizedX * normalizedMagnitude, normalizedY * normalizedMagnitude)
		else:
			return (0.0, 0.0)
	
	
	def getID(self):
		return self._ID
	
	
	def isConnected(self):
		return self._Connected
	
	
	def update(self):
		good            = XInputGetState(self._ID, self._XINPUT_STATE) == ERROR_SUCCESS
		self._Connected = good
		
		if good:
			### axis ###
			xy = self._deadzone(self._XINPUT_STATE.Gamepad.sThumbLX, self._XINPUT_STATE.Gamepad.sThumbLY, XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE)
			self._Axis['LTHUMBX'] = xy[0]
			self._Axis['LTHUMBY'] = xy[1]
			
			xy = self._deadzone(self._XINPUT_STATE.Gamepad.sThumbRX, self._XINPUT_STATE.Gamepad.sThumbRY, XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE)
			self._Axis['RTHUMBX'] = xy[0]
			self._Axis['RTHUMBY'] = xy[1]
			
			if self._XINPUT_STATE.Gamepad.bLeftTrigger > XINPUT_GAMEPAD_TRIGGER_THRESHOLD:
				self._Axis['LTRIGGER'] = (self._XINPUT_STATE.Gamepad.bLeftTrigger - XINPUT_GAMEPAD_TRIGGER_THRESHOLD) / float(0xFF - XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
			else:
				self._Axis['LTRIGGER'] = 0.0
			
			if self._XINPUT_STATE.Gamepad.bRightTrigger > XINPUT_GAMEPAD_TRIGGER_THRESHOLD:
				self._Axis['RTRIGGER'] = float(self._XINPUT_STATE.Gamepad.bRightTrigger - XINPUT_GAMEPAD_TRIGGER_THRESHOLD) / float(0xFF - XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
			else:
				self._Axis['RTRIGGER'] = 0.0
			
			### buttons ###
			self._Button['DPAD_UP']      = (self._XINPUT_STATE.Gamepad.wButtons & 0x0001) == 0x0001
			self._Button['DPAD_DOWN']    = (self._XINPUT_STATE.Gamepad.wButtons & 0x0002) == 0x0002
			self._Button['DPAD_LEFT']    = (self._XINPUT_STATE.Gamepad.wButtons & 0x0004) == 0x0004
			self._Button['DPAD_RIGHT']   = (self._XINPUT_STATE.Gamepad.wButtons & 0x0008) == 0x0008
			self._Button['START']        = (self._XINPUT_STATE.Gamepad.wButtons & 0x0010) == 0x0010
			self._Button['BACK']         = (self._XINPUT_STATE.Gamepad.wButtons & 0x0020) == 0x0020
			self._Button['LTHUMB']       = (self._XINPUT_STATE.Gamepad.wButtons & 0x0040) == 0x0040
			self._Button['RTHUMB']       = (self._XINPUT_STATE.Gamepad.wButtons & 0x0080) == 0x0080
			self._Button['LSHOULDER']    = (self._XINPUT_STATE.Gamepad.wButtons & 0x0100) == 0x0100
			self._Button['RSHOULDER']    = (self._XINPUT_STATE.Gamepad.wButtons & 0x0200) == 0x0200
			self._Button['A']            = (self._XINPUT_STATE.Gamepad.wButtons & 0x1000) == 0x1000
			self._Button['B']            = (self._XINPUT_STATE.Gamepad.wButtons & 0x2000) == 0x2000
			self._Button['X']            = (self._XINPUT_STATE.Gamepad.wButtons & 0x4000) == 0x4000
			self._Button['Y']            = (self._XINPUT_STATE.Gamepad.wButtons & 0x8000) == 0x8000
			
			# DPAD: do not allow UP+DOWN LEFT+RIGHT combinations
			if self._Button['DPAD_UP'] and self._Button['DPAD_DOWN']:
				self._Button['DPAD_DOWN'] = False
				
			if self._Button['DPAD_LEFT'] and self._Button['DPAD_RIGHT']:
				self._Button['DPAD_RIGHT'] = False
			
			# DAXIS: treat analog inputs as buttons
			lx = self.analogState('LTHUMBX')
			ly = self.analogState('LTHUMBY')
			rx = self.analogState('RTHUMBX')
			ry = self.analogState('RTHUMBY')
			self._Button['LTHUMB_UP']      = ly  >  0.50
			self._Button['LTHUMB_DOWN']    = ly  < -0.50
			self._Button['LTHUMB_LEFT']    = lx  < -0.50
			self._Button['LTHUMB_RIGHT']   = lx  >  0.50
			
			self._Button['RTHUMB_UP']    = ry  >  0.50
			self._Button['RTHUMB_DOWN']  = ry  < -0.50
			self._Button['RTHUMB_LEFT']  = rx  < -0.50
			self._Button['RTHUMB_RIGHT'] = rx  >  0.50
			
			self._Button['LTRIGGER']     = self.analogState('LTRIGGER') >  0.10
			self._Button['RTRIGGER']     = self.analogState('RTRIGGER') >  0.10
			
			
			# DAXIS: allow 8-way directions for the sticks
			# left
			if self._Button['LTHUMB_UP'] and self._Button['LTHUMB_RIGHT']:
				self._Button['LTHUMB_UP_RIGHT']   = True
				self._Button['LTHUMB_UP']         = False
				self._Button['LTHUMB_RIGHT']      = False
			else:
				self._Button['LTHUMB_UP_RIGHT']   = False
			
			if self._Button['LTHUMB_RIGHT'] and self._Button['LTHUMB_DOWN']:
				self._Button['LTHUMB_RIGHT_DOWN'] = True
				self._Button['LTHUMB_RIGHT']      = False
				self._Button['LTHUMB_DOWN']       = False
			else:
				self._Button['LTHUMB_RIGHT_DOWN'] = False
			
			if self._Button['LTHUMB_DOWN'] and self._Button['LTHUMB_LEFT']:
				self._Button['LTHUMB_DOWN_LEFT']  = True
				self._Button['LTHUMB_DOWN']       = False
				self._Button['LTHUMB_LEFT']       = False
			else:
				self._Button['LTHUMB_DOWN_LEFT']  = False
				
			if self._Button['LTHUMB_LEFT'] and self._Button['LTHUMB_UP']:
				self._Button['LTHUMB_LEFT_UP']    = True
				self._Button['LTHUMB_LEFT']       = False
				self._Button['LTHUMB_UP']         = False
			else:
				self._Button['LTHUMB_LEFT_UP']    = False
				
			# right
			if self._Button['RTHUMB_UP'] and self._Button['RTHUMB_RIGHT']:
				self._Button['RTHUMB_UP_RIGHT']   = True
				self._Button['RTHUMB_UP']         = False
				self._Button['RTHUMB_RIGHT']      = False
			else:
				self._Button['RTHUMB_UP_RIGHT']   = False
			
			if self._Button['RTHUMB_RIGHT'] and self._Button['RTHUMB_DOWN']:
				self._Button['RTHUMB_RIGHT_DOWN'] = True
				self._Button['RTHUMB_RIGHT']      = False
				self._Button['RTHUMB_DOWN']       = False
			else:
				self._Button['RTHUMB_RIGHT_DOWN'] = False
			
			if self._Button['RTHUMB_DOWN'] and self._Button['RTHUMB_LEFT']:
				self._Button['RTHUMB_DOWN_LEFT']  = True
				self._Button['RTHUMB_DOWN']       = False
				self._Button['RTHUMB_LEFT']       = False
			else:
				self._Button['RTHUMB_DOWN_LEFT']  = False
				
			if self._Button['RTHUMB_LEFT'] and self._Button['RTHUMB_UP']:
				self._Button['RTHUMB_LEFT_UP']    = True
				self._Button['RTHUMB_LEFT']       = False
				self._Button['RTHUMB_UP']         = False
			else:
				self._Button['RTHUMB_LEFT_UP']    = False
			
		else:
			self._Axis   = {}
			self._Button = {}
	
	
	def buttonPressed(self, BUTTON):
		b = BUTTON.upper()
		if b in self._Button:
			return self._Button[b]
		else:
			return False
	
	
	def anyButtonPressed(self):
		buttons = ['DPAD_UP', 'DPAD_DOWN', 'DPAD_LEFT', 'DPAD_RIGHT', 'START', 'BACK', 'LTHUMB', 'RTHUMB', 'LSHOULDER', 'RSHOULDER', 'A', 'B', 'X', 'Y']
		for b in buttons:
			if buttonPressed(b):
				return True
		return False
	
	
	def analogState(self, AXIS):
		a = AXIS.upper()
		if a in self._Axis:
			return self._Axis[a]
		else:
			return 0.0
	






###################################
###                             ###
###   EventGhost plugin stuff   ###
###                             ###
###################################

import time, threading
import eg, wx

eg.RegisterPlugin(
	name         = PLUGIN_NAME,
	author       = PLUGIN_AUTHOR,
	version      = PLUGIN_VERSION,
	description  = PLUGIN_DESCRIPTION,
	icon         = PLUGIN_ICON,
	kind         = "remote",
	guid         = "{0AC98F01-7096-4E0E-9E42-4A54EA389C65}",
	canMultiLoad = False
)



class XInputPlugin(eg.PluginBase):
	
	
	def __init__(self):
		self._thread = None
		# these are the analog controls if treated digital
		self._analogButtons = [
								'LTHUMB_UP',
								'LTHUMB_DOWN',
								'LTHUMB_LEFT',
								'LTHUMB_RIGHT',
								'LTHUMB_UP_RIGHT',
								'LTHUMB_RIGHT_DOWN',
								'LTHUMB_DOWN_LEFT',
								'LTHUMB_LEFT_UP',
								
								'RTHUMB_UP',
								'RTHUMB_DOWN',
								'RTHUMB_LEFT',
								'RTHUMB_RIGHT',
								'RTHUMB_UP_RIGHT',
								'RTHUMB_RIGHT_DOWN',
								'RTHUMB_DOWN_LEFT',
								'RTHUMB_LEFT_UP',
								
								'LTRIGGER',
								'RTRIGGER'
								]
	
	
	def __start__(self, treatAxisAsButton = True, includedGamepadPortId = False, releaseEvents = False, pollRate = 30, newPadsRate = 4):
		# get configuration
		self._treatAxisAsButton     = treatAxisAsButton                            # if true we treat the analog inputs as digital
		self._includedGamepadPortId = includedGamepadPortId                        # adds the ID of the controller to the events name
		self._releaseEvents         = releaseEvents                                # triggers an event when a button was releases, only works for the last button pressed
		self._newPadsTimeout        = float(newPadsRate)                           # we only check every N seconds for new pads
		self._lastCheckedForNewPads = 0.0                                          # we only check every N seconds for new pads
		self._pollRate              = 1.0 / float(pollRate)                        # in seconds
		
		# prepare valid buttons
		validButtons = []
		for b in GamePadButton:
			if (not self._treatAxisAsButton) and (b in self._analogButtons):
				pass
			else:
				validButtons.append(b)
		self._validButtons = validButtons
		
		# prep gamepad states
		self._gamepads        = {}                                                 # gamepads
		self._gamepadsButtons = {}                                                 # gamepads pressed buttons
		self._gamepadsAxis    = {}                                                 # gamepads analog values
		for i in XINPUT_GAMEPAD_RANGE:
			self._gamepads[i]        = None                                        # not connected
			self._gamepadsButtons[i] = []                                          # no buttons pressed
			self._gamepadsAxis[i]    = {}                                          # no buttons pressed
		
		# start polling thread
		self._threadRun = True
		self._thread    = threading.Thread(target = self._threadFunc)              # timer thread for polling
		self._thread.start()
		self._makeEvent('STARTED', -1)
	
	
	def __stop__(self):
		self._threadRun = False
		while self._thread.isAlive():
			time.sleep(0.1)
		
		# cancel last enduring events if any
		pads = self._gamepads
		for i in XINPUT_GAMEPAD_RANGE:
			pad     = pads[i]
			buttons = self._gamepadsButtons[i]
			if len(buttons) > 0:
				self.EndLastEvent()
				break
		
		self._makeEvent('STOPPED', -1)
	
	
	def _getEventName(self, name, id, value):
		if (id < 0) or (not self._includedGamepadPortId):
			ids = ''
		else:
			ids = '.%d' % id
		
		return '%s%s' % (name, ids)
	
	
	def _makeEvent(self, name, id, value = None):
		n = self._getEventName(name, id, value)
		if value:
			self.TriggerEvent(n, payload = value)
		else:
			self.TriggerEvent(n)
	
	
	def _startEnduringEvent(self, name, id, value = None):
		n = self._getEventName(name, id, value)
		self.TriggerEnduringEvent(n)
	
	
	def _stopEnduringEvent(self, name, id, value = None):
		self.EndLastEvent()
	
	
	def _getValidButtonList(self):
		return self._validButtons
	
	
	def _checkForNewPads(self):
		pads = self._gamepads
		# don't check every poll
		t = time.clock()
		if (t - self._lastCheckedForNewPads) > self._newPadsTimeout:
			self._lastCheckedForNewPads = time.clock()
			# check for new gamepads
			for i in XINPUT_GAMEPAD_RANGE:
				if not pads[i]:
					g = GamePad(i)
					if g.isConnected():
						# add new pad to list
						pads[i] = g
						# raise event
						self._makeEvent('PAD.CONNECTED', i)
	
	
	def _updateConnectedPads(self):
		pads = self._gamepads
		# check connected pads
		for i in XINPUT_GAMEPAD_RANGE:
			pad     = pads[i]
			buttons = self._gamepadsButtons[i]
			if pad:
				pad.update() # poll state
				if not pad.isConnected():
					# remove pad from list
					pads[i] = None
					# release enduring event if any
					if len(buttons) > 1:
						self.EndLastEvent()
					# empty pressed buttons
					buttons[:] = []
					# raise event
					self._makeEvent('PAD.DISCONNECTED', i)
	
	
	def _checkPressedButtons(self):
		pads = self._gamepads
		for i in XINPUT_GAMEPAD_RANGE:
			pad     = pads[i]
			buttons = self._gamepadsButtons[i]
			if pad:
				# check pressed buttons
				for b in buttons:
					if not pad.buttonPressed(b):
						# remove pressed button
						buttons.remove(b)
						# cancel enduring event
						self._stopEnduringEvent('BUTTON.PRESSED.%s' % b, i)
						# button released
						if self._releaseEvents:
							self._makeEvent('BUTTON.RELEASED.%s' % b, i)
						
				# buttons
				pressed = []
				for b in self._getValidButtonList():
					if pad.buttonPressed(b) and (not (b in buttons)):
						pressed.append(b)
				
				if len(pressed) > 0:
					for b in pressed:
						buttons.append(b)
						self._startEnduringEvent('BUTTON.PRESSED.%s' % b, i)
	
	
	def _checkAnalogInputs(self):
		pads = self._gamepads
		for i in XINPUT_GAMEPAD_RANGE:
			pad  = pads[i]
			axis = self._gamepadsAxis[i]
			if pad:
				for a in GamePadAxis:
					v = pad.analogState(a)
					if v != 0.0:
						if a in axis:
							ov = axis[a]
						else:
							ov = 0.0
							
						axis[a] = v
						
						if v != ov:
							self._makeEvent('AXIS.%s' % a, i, int(v * 0x7FFF))
	
	
	def _threadFunc(self):
		while self._threadRun:
			if self._thread:
				self._checkForNewPads()
				self._updateConnectedPads()
				self._checkPressedButtons()
				
				if not self._treatAxisAsButton:
					self._checkAnalogInputs()
				
			time.sleep(self._pollRate)
	
	
	def Configure(self, treatAxisAsButton = True, includedGamepadPortId = False, releaseEvents = False, pollRate = 30, newPadsRate = 4):
		panel        = eg.ConfigPanel(self, resizable=True)
		optionsSizer = wx.GridBagSizer(0, 5)
		
		treatAxisAsButtonCheckBox = wx.CheckBox(panel, -1, 'Should we treat the analog inputs as normal buttons?')
		treatAxisAsButtonCheckBox.SetValue(treatAxisAsButton)
		optionsSizer.Add(treatAxisAsButtonCheckBox, (0, 0))
		
		includedGamepadPortIdCheckBox = wx.CheckBox(panel, -1, 'Should we add the controllers ID to the event names?')
		includedGamepadPortIdCheckBox.SetValue(includedGamepadPortId)
		optionsSizer.Add(includedGamepadPortIdCheckBox, (2, 0))
		
		releaseEventsCheckBox = wx.CheckBox(panel, -1, 'Trigger events when a button was released?')
		releaseEventsCheckBox.SetValue(releaseEvents)
		optionsSizer.Add(releaseEventsCheckBox, (4, 0))
		
		pollRateLabel = wx.StaticText(panel, -1, 'Poll rate (how often we check the controllers for new buttons per second)')
		optionsSizer.Add(pollRateLabel, (6, 0))
		pollRateSpin = eg.SpinIntCtrl(panel, -1, pollRate, 10, 120)
		optionsSizer.Add(pollRateSpin, (7, 0))
		
		newPadsRateLabel = wx.StaticText(panel, -1, 'How often we check if a new controller has been attached (in seconds)')
		optionsSizer.Add(newPadsRateLabel, (9, 0))
		newPadsRateSpin = eg.SpinIntCtrl(panel, -1, newPadsRate, 1, 30)
		optionsSizer.Add(newPadsRateSpin, (10, 0))
		
		panel.sizer.Add(optionsSizer, 0, wx.TOP, 10)
		
		while panel.Affirmed():
			panel.SetResult(
				treatAxisAsButtonCheckBox.GetValue(),
				includedGamepadPortIdCheckBox.GetValue(),
				releaseEventsCheckBox.GetValue(),
				pollRateSpin.GetValue(),
				newPadsRateSpin.GetValue()
			)
	
	