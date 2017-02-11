# last modified by K on 5/29/2016 Added Color Temp (Kelvin) to RGB conversion for the color chooser


import eg
import re

eg.RegisterPlugin(
	name = "LIFX",
	author = "Marcus Hultman, Last Edited by K",
	version = "0.0.3",
	kind = "external",
	description = "This plugin connects to your LIFX lights.",
	createMacrosOnAdd = True,
)

# HTTP
import math
import requests
from wx.lib import masked

class KelvinToRGB(tuple):

  def __new__(cls, kelvin):
	kelvin = kelvin/100
	RGB = [0]*3
	if kelvin <= 66:
	  RGB[0] = 255
	  RGB[1] = 99.4708025861*math.log(kelvin)-161.1195681661
	  if kelvin <= 19:
		RGB[2] = 0
	  else:
		RGB[2] = 138.5177312231*math.log(kelvin-10)-305.0447927307
	else:
		RGB[0] = 329.698727446*math.pow(kelvin-60, -0.1332047592)
		RGB[1] = 288.1221695283*math.pow(kelvin-60, -0.0755148492)
		RGB[2] = 255
	for i, color in enumerate(RGB):
	  color = max([0, color])
	  RGB[i] = int(round(min([255, color])))

	RGB += (255,)
	return tuple.__new__(cls, RGB)

# LAN
#import struct
#import socket

class LIFXPlugin(eg.PluginBase):

  def __init__(self):
	self.AddAction(ListLights)
	self.AddAction(SetState)
	self.AddAction(TogglePower)
	self.AddAction(BreatheEffect)
	self.AddAction(PulseEffect)

  def __start__(self, token):
  	self.VALIDKELVIN = tuple((KelvinToRGB(i) for i in range(1700, 27001)))
	self.auth = { 'Authorization' : 'Bearer {0}'.format(token) }
	self.base_url = 'https://api.lifx.com/v1/'

  def Configure(self, token=""):
	panel = eg.ConfigPanel(self)
	tokenCtrl = panel.TextCtrl(token)
	panel.AddLine("Token: ", tokenCtrl)

	while panel.Affirmed():
	  panel.SetResult(tokenCtrl.GetValue())

# Abstract Actions
class LifxAction(eg.ActionBase):

  GET = 0
  PUT = 1
  POST = 2

  def action(self, url, *args, **kwargs):
    return {
        0: requests.get,
        1: requests.put,
        2: requests.post,
    }[self.method if hasattr(self, 'method') else
      LifxAction.GET](url, *args, **kwargs).json()

  def form_url(self):
    if not hasattr(self, 'url'):
      self.url = ''
    return self.plugin.base_url + self.url

  def __call__(self, *data):
    url = self.form_url()
    payload = dict(filter(lambda x: x[1] is not None, zip(
      self.payload if hasattr(self, 'payload') else (), data)))
    return self.action(url, headers=self.plugin.auth, data=payload)

class SelectorLifxAction(LifxAction):

  def form_url(self):
	return self.plugin.base_url + self.url.format(self.selector)

  def __call__(self, selector, *data):
	self.selector = selector
	return super(SelectorLifxAction, self).__call__(*data)

# Extra controls
class SelectorCtrl(wx.BoxSizer):

  choices = ["all", "label:", "id:", "group_id:", "group:", "location_id:", "location:", "scene_id:"]

  def __init__(self, panel, selector, *args, **kwargs):
	super(SelectorCtrl, self).__init__(*args, **kwargs)
	i, e = 0, ''

	if selector is not None:
	  t, e = re.match('(\w*:?)(\w*)', selector).groups()
	  i = SelectorCtrl.choices.index(t)

	self.typeCtrl = panel.Choice(i, SelectorCtrl.choices)
	self.argCtrl = panel.TextCtrl(e)
	self.Add(self.typeCtrl)
	self.Add(self.argCtrl, flag=wx.LEFT, border=10)

  def GetValue(self):
	type = SelectorCtrl.choices[self.typeCtrl.GetValue()]
	return type + self.argCtrl.GetValue() if type[-1] == ':' else type
  

# Implementations
class ListLights(SelectorLifxAction):
  name = "List Lights"
  description = "."

  def __init__(self):
	self.url = 'lights/{0}'

  def Configure(self, selector=None):
	panel = eg.ConfigPanel(self)
	selectorCtrl = SelectorCtrl(panel, selector)
	panel.AddLine('Selector: ', selectorCtrl)

	while panel.Affirmed():
	  panel.SetResult(selectorCtrl.GetValue())


class SetState(SelectorLifxAction):

  name = "Set State"
  description = "."
  pwrCh = ['on', 'off']

  def __init__(self):
	self.method = LifxAction.PUT
	self.url = 'lights/{0}/state'
	self.payload = ('power', 'color', 'brightness', 'duration')

  def Configure(self, selector=None, power=None, color=None, brightness=None, duration=None):

	panel = eg.ConfigPanel(self)
	selectorCtrl = SelectorCtrl(panel, selector)
	colourPickerCtrl = ColourCtrl(self, panel)
	
	powerECtrl = panel.CheckBox(power is not None)
	powerCtrl = panel.Choice(SetState.pwrCh.index(power) if power is not None else 0, SetState.pwrCh)
	kelvinECtrl, kelvinCtrl = colourPickerCtrl.KelvinCtrl()
	colorECtrl, colorCtrl = colourPickerCtrl.ColourCtrl(color)
	brightnessECtrl = panel.CheckBox(brightness is not None)
	brightnessCtrl = panel.SpinNumCtrl(brightness, min=0, max=1.0, increment=0.01)
	durationECtrl = panel.CheckBox(duration is not None)
	durationCtrl = panel.SpinNumCtrl(duration)

	eg.EqualizeWidths((powerCtrl, kelvinCtrl, brightnessCtrl, durationCtrl))

	panel.AddLine('Selector: ', selectorCtrl)
	panel.AddLine(' ')
	panel.AddLine('Use Item', 'Item Name', 'Item Value')
	panel.AddLine('_'*51)
	panel.AddLine(powerECtrl, 'Power: ', powerCtrl)
	panel.AddLine(colorECtrl, 'Color: ', colorCtrl)
	panel.AddLine(kelvinECtrl, 'Color temp (Kelvin): ', kelvinCtrl)
	panel.AddLine(brightnessECtrl, 'Brightness: ', brightnessCtrl)
	panel.AddLine(durationECtrl, 'Duration: ', durationCtrl)

	while panel.Affirmed():
	  panel.SetResult(
		selectorCtrl.GetValue(),
		SetState.pwrCh[powerCtrl.GetValue()] if powerECtrl.GetValue() else None,
		colourPickerCtrl.GetHTMLColour(),
		durationCtrl.GetValue() if durationECtrl.GetValue() else None
	  )


class TogglePower(SelectorLifxAction):

  name = "Toggle Power"
  description = "."

  def __init__(self):
	self.method = LifxAction.POST
	self.url = 'lights/{0}/toggle'
	self.payload = ('duration',)

  def Configure(self, selector=None, duration=None):

	panel = eg.ConfigPanel(self)
	selectorCtrl = SelectorCtrl(panel, selector)

	durationECtrl = panel.CheckBox(duration is not None)
	durationCtrl = panel.SpinNumCtrl(duration, size=(106, 22))

	panel.AddLine('Selector: ', selectorCtrl)
	panel.AddLine(' ')
	panel.AddLine('Use Item', 'Item Name', 'Item Value')
	panel.AddLine('_'*51)
	panel.AddLine(durationECtrl, 'Duration: ', durationCtrl)

	while panel.Affirmed():
	  panel.SetResult(
		selectorCtrl.GetValue(),
		durationCtrl.GetValue() if durationECtrl.GetValue() else None
	  )


class BreatheEffect(SelectorLifxAction):

  name = "Breathe Effect"
  description = "."

  def __init__(self):
	self.method = LifxAction.POST
	self.url = 'lights/{0}/effects/breathe'
	self.payload = ('color', 'from_color', 'period', 'cycles', 'persist', 'power_on', 'peak')

  def Configure(self, selector=None, color=None, from_color=None, period=None, cycles=None, persist=None, power_on=None, peak=None):

	panel = eg.ConfigPanel(self)
	selectorCtrl = SelectorCtrl(panel, selector)
	colourPickerCtrl = ColourCtrl(self, panel)
	from_colourPickerCtrl = ColourCtrl(self, panel)

	kelvinECtrl, kelvinCtrl = colourPickerCtrl.KelvinCtrl()
	colorECtrl, colorCtrl = colourPickerCtrl.ColourCtrl(color, checkbox=False)
	from_kelvinECtrl, from_kelvinCtrl = from_colourPickerCtrl.KelvinCtrl()
	from_colorECtrl, from_colorCtrl = from_colourPickerCtrl.ColourCtrl(from_color)
	periodECtrl = panel.CheckBox(period is not None)
	periodCtrl = panel.SpinNumCtrl(period)
	cyclesECtrl = panel.CheckBox(cycles is not None)
	cyclesCtrl = panel.SpinIntCtrl(cycles)
	persistECtrl = panel.CheckBox(persist is not None)
	persistCtrl = panel.CheckBox(persist)
	power_onECtrl = panel.CheckBox(power_on is not None)
	power_onCtrl = panel.CheckBox(power_on)
	peakECtrl = panel.CheckBox(peak is not None)
	peakCtrl = panel.TextCtrl(peak or '')

	eg.EqualizeWidths((kelvinCtrl, from_kelvinCtrl, periodCtrl, cyclesCtrl, peakCtrl))

	panel.AddLine('Selector: ', selectorCtrl)
	panel.AddLine(' ')
	panel.AddLine('Use Item', 'Item Name', 'Item Value')
	panel.AddLine('_'*51)
	panel.AddLine(colorECtrl, 'Color: ', colorCtrl)
	panel.AddLine(kelvinECtrl, 'Color temp (Kelvin): ', kelvinCtrl)
	panel.AddLine(from_colorECtrl, 'From color:', from_colorCtrl)
	panel.AddLine(from_kelvinECtrl, 'From color temp (Kelvin): ', from_kelvinCtrl)
	panel.AddLine(periodECtrl, 'Period: ', periodCtrl)
	panel.AddLine(cyclesECtrl, 'Cycles:', cyclesCtrl)
	panel.AddLine(persistECtrl, 'Persist:', persistCtrl)
	panel.AddLine(power_onECtrl, 'Power on:', power_onCtrl)
	panel.AddLine(peakECtrl, 'Peak:', peakCtrl)

	while panel.Affirmed():
	  panel.SetResult(
		selectorCtrl.GetValue(),
		colourPickerCtrl.GetHTMLColour(),
		from_colourPickerCtrl.GetHTMLColour(),
		periodCtrl.GetValue() if periodECtrl.GetValue() else None,
		cyclesCtrl.GetValue() if cyclesECtrl.GetValue() else None,
		persistCtrl.GetValue() if persistECtrl.GetValue() else None,
		power_onCtrl.GetValue() if power_onECtrl.GetValue() else None,
		peakCtrl.GetValue() if peakECtrl.GetValue() else None,
	  )


class PulseEffect(SelectorLifxAction):

  name = "Pulse Effect"
  description = "."

  def __init__(self):
	self.method = LifxAction.POST
	self.url = 'lights/{0}/effects/pulse'
	self.payload = ('color', 'from_color', 'period', 'cycles', 'persist', 'power_on', 'peak')

  def Configure(self, selector=None, color=None, from_color=None, period=None, cycles=None, persist=None, power_on=None, peak=None):

	panel = eg.ConfigPanel(self)
	selectorCtrl = SelectorCtrl(panel, selector)
	colourPickerCtrl = ColourCtrl(self, panel)
	from_colourPickerCtrl = ColourCtrl(self, panel)

	kelvinECtrl, kelvinCtrl = colourPickerCtrl.KelvinCtrl()
	colorECtrl, colorCtrl = colourPickerCtrl.ColourCtrl(color, checkbox=False)
	from_kelvinECtrl, from_kelvinCtrl = from_colourPickerCtrl.KelvinCtrl()
	from_colorECtrl, from_colorCtrl = from_colourPickerCtrl.ColourCtrl(from_color)
	periodECtrl = panel.CheckBox(period is not None)
	periodCtrl = panel.SpinNumCtrl(period)
	cyclesECtrl = panel.CheckBox(cycles is not None)
	cyclesCtrl = panel.SpinIntCtrl(cycles)
	persistECtrl = panel.CheckBox(persist is not None)
	persistCtrl = panel.CheckBox(persist)
	power_onECtrl = panel.CheckBox(power_on is not None)
	power_onCtrl = panel.CheckBox(power_on)
	peakECtrl = panel.CheckBox(peak is not None)
	peakCtrl = panel.TextCtrl(peak or '')

	eg.EqualizeWidths((kelvinCtrl, from_kelvinCtrl, periodCtrl, cyclesCtrl, peakCtrl))

	panel.AddLine('Selector: ', selectorCtrl)
	panel.AddLine(' ')
	panel.AddLine('Use Item', 'Item Name', 'Item Value')
	panel.AddLine('_'*51)
	panel.AddLine(colorECtrl, 'Color: ', colorCtrl)
	panel.AddLine(kelvinECtrl, 'Color temp (Kelvin): ', kelvinCtrl)
	panel.AddLine(from_colorECtrl, 'From color:', from_colorCtrl)
	panel.AddLine(from_kelvinECtrl, 'From color temp (Kelvin): ', from_kelvinCtrl)
	panel.AddLine(periodECtrl, 'Period: ', periodCtrl)
	panel.AddLine(cyclesECtrl, 'Cycles:', cyclesCtrl)
	panel.AddLine(persistECtrl, 'Persist:', persistCtrl)
	panel.AddLine(power_onECtrl, 'Power on:', power_onCtrl)
	panel.AddLine(peakECtrl, 'Peak:', peakCtrl)

	while panel.Affirmed():
	  panel.SetResult(
		selectorCtrl.GetValue(),
		colourPickerCtrl.GetHTMLColour(),
		from_colourPickerCtrl.GetHTMLColour(),
		periodCtrl.GetValue() if periodECtrl.GetValue() else None,
		cyclesCtrl.GetValue() if cyclesECtrl.GetValue() else None,
		persistCtrl.GetValue() if persistECtrl.GetValue() else None,
		power_onCtrl.GetValue() if power_onECtrl.GetValue() else None,
		peakCtrl.GetValue() if peakECtrl.GetValue() else None,
	  )


class ColourCtrl:

	def __init__(self, plugin, panel):
		self.plugin = plugin.plugin
		self.panel = panel
		self.updatingKelvin = False

	def KelvinCtrl(self):
		self.savedKelvin = wx.Colour(*KelvinToRGB(1700))
		self.kelvinECtrl = self.panel.CheckBox(False)
		self.savedkelvinECtrl = False

		self.kelvinCtrl = masked.NumCtrl(
										self.panel,
										-1,
										1700,
										min=1700,
										max=27000,
										fractionWidth=0,
										limited=False,
										invalidBackgroundColour=wx.RED,
										)

		self.kelvinCtrl.Enable(False)
		self.returnColour = None
		self.kelvinECtrl.Bind(wx.EVT_CHECKBOX, self.onEKelvin)
		self.kelvinCtrl.Bind(masked.EVT_NUM, self.onKelvin)

		return self.kelvinECtrl, self.kelvinCtrl

	def ColourCtrl(self, colour, checkbox=True):
		self.returnNone = checkbox
		self.savedColour = wx.Colour(0, 0, 0) if colour is None else colour
		self.colourECtrl = self.panel.CheckBox(bool(self.savedColour))	
		self.colourCtrl = ColourPickerCtrl(self.panel, self.plugin, self.savedColour, self.kelvinCtrl.GetSize())
		self.returnColour = colour
		if not checkbox:
			self.colourECtrl.SetValue(True)
			self.colourECtrl.Enable(False)
		else: self.colourECtrl.Bind(wx.EVT_CHECKBOX, self.onEColour)

		self.savedColourECtrl = self.colourECtrl.GetValue()
		self.colourCtrl.Bind(wx.EVT_COLOURPICKER_CHANGED, self.onColour)

		return self.colourECtrl, self.colourCtrl

	def onKelvin(self, evt):
		if self.updatingKelvin:
			self.updatingKelvin = False
		else:
			val = self.kelvinCtrl.GetValue()
			if val >= 1700 and val <= 27000:
				self.savedKelvin = val
				self.colourCtrl.SetColour(self.plugin.VALIDKELVIN[self.savedKelvin-1700])
			self.SetReturnColour()
		evt.Skip()

	def onEKelvin(self, evt):
		val = self.kelvinCtrl.GetValue()
		if val < 1700: self.kelvinCtrl.SetValue(1700)
		if  val > 27000: self.kelvinCtrl.SetValue(27000)

		if self.kelvinECtrl.GetValue():
			self.colourCtrl.SetColour(self.plugin.VALIDKELVIN[self.kelvinCtrl.GetValue()-1700])
			self.kelvinCtrl.Enable(True)
			self.colourECtrl.SetValue(False)
		else:
			self.colourECtrl.SetValue(self.savedColourECtrl)
			self.colourCtrl.SetColour(self.savedColour)

		self.savedKelvin = self.kelvinCtrl.GetValue()
		self.savedkelvinECtrl = self.kelvinECtrl.GetValue()
		self.SetReturnColour()
		evt.Skip()

	def onColour(self, evt):
		kelvin = self.colourCtrl.GetKelvin()
		self.updatingKelvin = True
		self.kelvinCtrl.SetValue(kelvin)
		self.SetReturnColour()
		evt.Skip()

	def onEColour(self, evt):
		if self.colourECtrl.GetValue():
			self.kelvinECtrl.SetValue(False)
			self.kelvinCtrl.Enable(False)
			self.colourCtrl.SetColour(self.savedColour)
		else:
			self.savedColour = self.colourCtrl.GetColour()
			self.kelvinECtrl.SetValue(self.savedkelvinECtrl)
			self.kelvinCtrl.Enable(self.savedkelvinECtrl)
			if self.savedkelvinECtrl:
				self.colourCtrl.SetColour(self.savedKelvin)

		self.savedColourECtrl = self.colourECtrl.GetValue()
		self.SetReturnColour()
		evt.Skip()

	def SetReturnColour(self):
		if self.savedkelvinECtrl or self.savedColourECtrl:
			self.returnColour = self.colourCtrl.GetValue()
		else: self.returnColour = None

	def GetHTMLColour(self):
		if self.returnNone: return self.returnColour
		else: return self.colourCtrl.GetValue()
		
class ColourPickerCtrl(wx.ColourPickerCtrl):

	def __init__(self, panel, plugin, color, size, *args, **kwargs):
		self.plugin = plugin
		super(ColourPickerCtrl, self).__init__(panel, *args, **kwargs)
		self.SetSize(size)
		self.SetColour(color)

	def GetValue(self):
		return self.GetColour().GetAsString(wx.C2S_NAME|wx.C2S_HTML_SYNTAX)

	def GetKelvin(self):
		try: return self.plugin.VALIDKELVIN.index(self.GetColour())+1700
		except: return 0