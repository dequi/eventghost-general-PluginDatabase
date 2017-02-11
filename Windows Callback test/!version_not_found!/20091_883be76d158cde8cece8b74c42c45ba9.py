import eg

eg.RegisterPlugin(name = 'Windows Callback test',
                  kind = 'other',
                  canMultiLoad = True,
                  createMacrosOnAdd = True,
                  guid = '{08FDD8F9-60D4-4CD7-B3DE-6799C865B5F8}'
                  )

from ctypes import WinDLL, Structure, pointer, WINFUNCTYPE
from ctypes.wintypes import *

# header  file: Mmsystem.h
# library file: Winmm.dll
winmm_dll = WinDLL('Winmm')

# constants
NO_DEVICE_INDEX = -2
MIDI_MAPPER = -1
MAXPNAMELEN = 32
MIDIOUTCAPS_SIZE = 20 + (MAXPNAMELEN * 2)
CALLBACK_FUNCTION = 196608
MMSYSERR_NOERROR = 0

# types
MMVERSION = UINT
TCHAR_MAXPNAMELEN = WCHAR * MAXPNAMELEN
class MIDIOUTCAPS(Structure):
    _fields_ = [("wMid", WORD),
                ("wPid", WORD),
                ("vDriverVersion", MMVERSION),
                ("szPname", TCHAR_MAXPNAMELEN),
                ("wTechnology", WORD),
                ("wVoices", WORD),
                ("wNotes", WORD),
                ("wChannelMask", WORD),
                ("dwSupport", DWORD)]
MMRESULT = UINT
HMIDIOUT = HANDLE
UINT_PTR = UINT
DWORD_PTR = LPVOID
LPMIDIOUTCAPS = LPVOID
LPHMIDIOUT = LPVOID

# friendly names for the imported functions
midiOutGetNumDevs = winmm_dll.midiOutGetNumDevs
midiOutGetDevCaps = winmm_dll.midiOutGetDevCapsW
midiOutOpen = winmm_dll.midiOutOpen
midiOutClose = winmm_dll.midiOutClose

# parameter types for the imported functions
midiOutGetDevCaps.argtypes = [UINT_PTR, LPMIDIOUTCAPS, UINT]
midiOutOpen.argtypes = [LPHMIDIOUT, UINT, DWORD_PTR, DWORD_PTR, DWORD]
midiOutClose.argtypes = [HMIDIOUT]

# return types for the imported functions
midiOutGetNumDevs.restype = UINT
midiOutGetDevCaps.restype = MMRESULT
midiOutOpen.restype = MMRESULT
midiOutClose.restype = MMRESULT

# define the prototype for the MIDI Output callback function
MIDIOUTPUTCALLBACK = WINFUNCTYPE(None, HMIDIOUT, UINT, DWORD_PTR, DWORD_PTR, DWORD_PTR)

def MidiOutputCallback (hmo, wMsg, dwInstance, dwParam1, dwParam2):
    # Do not call any multimedia functions from inside the callback function, it can cause a deadlock.
    # Other system functions can safely be called from the callback.
    print '   MidiOutputCallback()'
    print '      wMsg : ' + str(wMsg)
    print '      dwInstance : ' + str(dwInstance)
    print '      dwParam1 : ' + str(dwParam1)
    print '      dwParam2 : ' + str(dwParam2)

class WinCallbackTest (eg.PluginBase):
    def __init__ (self):
        print('WinCallbackTest initialized.')
        self.is_open = False
        self.uDeviceID = NO_DEVICE_INDEX
        self.hmo = HMIDIOUT()
        self.Callback = MIDIOUTPUTCALLBACK(MidiOutputCallback)
        self.AddAction(OpenMidiOutputDevice)
        self.AddAction(CloseMidiOutputDevice)
    def __start__ (self, device_name):
        print('WinCallbackTest started with parameter: '+device_name)
        self.device_name = device_name
        self.is_connected = False
        i = 0
        n = midiOutGetNumDevs()
        midi_out_caps = MIDIOUTCAPS()
        lpMidiOutCaps = pointer(midi_out_caps)
        cbMidiOutCaps = MIDIOUTCAPS_SIZE
        device_index = NO_DEVICE_INDEX
        while i < n:
            result = midiOutGetDevCaps(i,lpMidiOutCaps,cbMidiOutCaps)
            if result == MMSYSERR_NOERROR:
                if device_name == midi_out_caps.szPname:
                    device_index = i
                    self.is_connected = True
            else:
                eg.PrintError('MMSYSERROR')
            i = i + 1
        self.uDeviceID = device_index
    def __stop__ (self):
        print('WinCallbackTest stopped.')
        if self.is_open == True:
            result = midiOutClose(self.hmo)
            if result == MMSYSERR_NOERROR:
                self.is_open = False
            else:
                eg.PrintError('MMSYSERROR')
    def __close__ (self):
        print('WinCallbackTest closed.')
    def Configure (self, device_name=''):
        uDeviceID = 0
        n = midiOutGetNumDevs()
        midi_out_caps = MIDIOUTCAPS()
        lpMidiOutCaps = pointer(midi_out_caps)
        cbMidiOutCaps = MIDIOUTCAPS_SIZE
        device_names = []
        # create a list of the MIDI output device names
        while uDeviceID < n:
            result = midiOutGetDevCaps(uDeviceID,lpMidiOutCaps,cbMidiOutCaps)
            if result == MMSYSERR_NOERROR:
                device_names.append(midi_out_caps.szPname)
            else:
                eg.PrintError('MMSYSERROR')
            uDeviceID = uDeviceID + 1
        # determine the current device, if any
        if device_name in device_names:
            current_device_index = device_names.index(device_name)
        else:
            current_device_index = -1
        # create the configuration dialog
        panel = eg.ConfigPanel()
        dropdown_listbox = panel.Choice(current_device_index,device_names)
        panel.AddLine('choose output device: ',dropdown_listbox)
        while panel.Affirmed():
            panel.SetResult(device_names[dropdown_listbox.GetValue()])

class OpenMidiOutputDevice (eg.ActionBase):
    class text:
        name = 'Open device'
        description = 'Opens this MIDI output device.'
    def __call__ (self):
        if self.plugin.is_connected == True:
            if self.plugin.is_open == False:
                lphmo = pointer(self.plugin.hmo)
                uDeviceID = self.plugin.uDeviceID
                dwCallback = self.plugin.Callback
                dwCallbackInstance = None
                dwFlags = CALLBACK_FUNCTION
                result = midiOutOpen(lphmo,uDeviceID,dwCallback,dwCallbackInstance,dwFlags)
                if result == MMSYSERR_NOERROR:
                    self.plugin.is_open = True
                else:
                    eg.PrintError('MMSYSERROR')
        else:
            eg.PrintError(self.plugin.device_name+' is not connected')

class CloseMidiOutputDevice (eg.ActionBase):
    class text:
        name = 'Close device'
        description = 'Closes this MIDI output device.'
    def __call__ (self):
        if self.plugin.is_open == True:
            result = midiOutClose(self.plugin.hmo)
            if result == MMSYSERR_NOERROR:
                self.plugin.is_open = False
            else:
                eg.PrintError('MMSYSERROR')