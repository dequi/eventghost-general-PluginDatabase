import rxvxxx
from rxvxxx import *		#I know this looks bad.  This is a result of not knowing how to fix the prototype problem.

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
	name = "Yamaha RX-V",
	author = "Jason Kloepping",
	version = "26.5.2013",
	kind = "external",
	createMacrosOnAdd = True,
	url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3382&sid=a9e116c8f1b66b8a4a96d4da98719a7a",
	description = "Adds actions to control Yamaha RX-V and some other receivers.",
)

SENDACTIONS = (   
	("MZ_VolumeUp_0.5", "Volume Up 0.5db", "Increase the volume one step (0.5 dB)", "MZ_VolumeUp_0.5"),
	("MZ_VolumeDown_0.5", "Volume Down 0.5db", "Decrease the volume one step (0.5 dB)", "MZ_VolumeDown_0.5"),
	("MZ_VolumeUp_1.0", "Volume Up 1.0dB", "Increase the volume 1.0 dB", "MZ_VolumeUp_1.0"),
	("MZ_VolumeDown_1.0", "Volume Down 1.0dB", "Decrease the volume 1.0 dB", "MZ_VolumeDown_1.0"),
	("MZ_VolumeUp_1.5", "Volume Up 1.5dB", "Increase the volume 1.5 dB", "MZ_VolumeUp_1.5"),
	("MZ_VolumeDown_1.5", "Volume Down 1.5dB", "Decrease the volume 1.5 dB", "MZ_VolumeDown_1.5"),
	("MZ_VolumeUp_2.0", "Volume Up 2.0dB", "Increase the volume 2.0 dB", "MZ_VolumeUp_2.0"),
	("MZ_VolumeDown_2.0", "Volume Down 2.0dB", "Decrease the volume 2.0 dB", "MZ_VolumeDown_2.0"),
	("MZ_VolumeUp_2.5", "Volume Up 2.5dB", "Increase the volume 2.5 dB", "MZ_VolumeUp_2.5"),
	("MZ_VolumeDown_2.5", "Volume Down 2.5dB", "Decrease the volume 2.5 dB", "MZ_VolumeDown_2.5"),
	("MZ_VolumeUp_3.0", "Volume Up 3.0dB", "Increase the volume 3.0 dB", "MZ_VolumeUp_3.0"),
	("MZ_VolumeDown_3.0", "Volume Down 3.0dB", "Decrease the volume 3.0 dB", "MZ_VolumeDown_3.0"),
	("MZ_VolumeUp_3.5", "Volume Up 3.5dB", "Increase the volume 3.5 dB", "MZ_VolumeUp_3.5"),
	("MZ_VolumeDown_3.5", "Volume Down 3.5dB", "Decrease the volume 3.5 dB", "MZ_VolumeDown_3.5"),
	("MZ_VolumeUp_4.0", "Volume Up 4.0dB", "Increase the volume 4.0 dB", "MZ_VolumeUp_4.0"),
	("MZ_VolumeDown_4.0", "Volume Down 4.0dB", "Decrease the volume 4.0 dB", "MZ_VolumeDown_4.0"),
	("MZ_VolumeUp_4.5", "Volume Up 4.5dB", "Increase the volume 4.5 dB", "MZ_VolumeUp_4.5"),
	("MZ_VolumeDown_4.5", "Volume Down 4.5dB", "Decrease the volume 4.5 dB", "MZ_VolumeDown_4.5"),
	("MZ_VolumeUp_5.0", "Volume Up 5.0dB", "Increase the volume 5.0 dB", "MZ_VolumeUp_5.0"),
	("MZ_VolumeDown_5.0", "Volume Down 5.0dB", "Decrease the volume 5.0 dB", "MZ_VolumeDown_5.0"),
	("MZ_ToggleMute", "Toggle Mute", "Toggles mute state", "MZ_ToggleMute"),
	("MZ_PowerOff", "Power Off", "Powers off machine", "MZ_PowerOff"),
	("MZ_PowerStandby", "Power Standby", "Turns machine to standby", "MZ_PowerStandby"),
	("MZ_PowerOn", "Power On", "Powers on machine", "MZ_PowerOn"),
	("MZ_ToggleOnStandby", "Toggle On / Standby", "Toggles machine between on and standby", "MZ_ToggleOnStandby"),
	("MZ_Source_HDMI1", "Source HDMI1", "Changes source to HDMI1", "MZ_Source_HDMI1"),
	("MZ_Source_HDMI2", "Source HDMI2", "Changes source to HDMI2", "MZ_Source_HDMI2"),
	("MZ_Source_HDMI3", "Source HDMI3", "Changes source to HDMI3", "MZ_Source_HDMI3"),
	("MZ_Source_HDMI4", "Source HDMI4", "Changes source to HDMI4", "MZ_Source_HDMI4"),
	("MZ_Source_HDMI5", "Source HDMI5", "Changes source to HDMI5", "MZ_Source_HDMI5"),
	("MZ_Source_V-AUX", "Source V-AUX", "Changes source to V-AUX", "SMZ_ource_V-AUX"),
	("MZ_Source_AV1", "Source AV1", "Changes source to AV1", "MZ_Source_AV1"),
	("MZ_Source_AV2", "Source AV2", "Changes source to AV2", "MZ_Source_AV2"),
	("MZ_Source_AV3", "Source AV3", "Changes source to AV3", "MZ_Source_AV3"),
	("MZ_Source_AV4", "Source AV4", "Changes source to AV4", "MZ_Source_AV4"),
	("MZ_Source_AV5", "Source AV5", "Changes source to AV5", "MZ_Source_AV5"),
	("MZ_Source_AV6", "Source AV6", "Changes source to AV6", "MZ_Source_AV6"),
	("MZ_Source_TUNER", "Source Tuner", "Changes source to radio", "SMZ_ource_TUNER"),
	("MZ_Source_DOCK", "Source DOCK", "Changes source to DOCK", "MZ_Source_DOCK"),
	("MZ_Source_AUDIO1", "Source AUDIO1", "Changes source to AUDIO1", "MZ_Source_AUDIO1"),
	("MZ_Source_AUDIO2", "Source AUDIO2", "Changes source to AUDIO2", "MZ_Source_AUDIO2"),
	("MZ_Source_SIRIUS", "Source SIRIUS", "Changes source to SIRIUS", "MZ_Source_SIRIUS"),
	("MZ_Source_PC", "Source PC", "Changes source to PC", "MZ_Source_PC"),
	("MZ_Straight", "Straight", "Straight", "MZ_Straight"),
	("MZ_SurroundDecode", "Surround Decode", "Surround Decode", "MZ_SurroundDecode"),
	("MZ_ToggleStraightAndDecode", "Toggle Straight And Decode", "Toggles between Straight and Sourround Decode", "MZ_ToggleStraightAndDecode"),
	("MZ_ToogleEnhancer", "Toggle Enhancer", "Toggles the enhancer on and off", "MZ_ToggleEnhancer"),
	#("NextSource", "Next Source", "Goes to the next source", "NextSource"),
	#("PreviousSource", "Previous Source", "Goes to the previous source", "PreviousSource"),
	#("ToggleSleep", "Toggle Sleep", "Toggles sleep mode", "ToggleSleep"),
	("MZ_NextRadioPreset", "Next Radio Preset", "Goes to next radio preset, or if radio is not on, it turns it on. Also wraps when you go past the last preset.", "MZ_NextRadioPreset"),
	("MZ_PreviousRadioPreset", "Previous Radio Preset", "Goes to previous radio preset, or if radio is not on, it turns it on. Also wraps to the end when you go past the first preset.", "MZ_PreviousRadioPreset"),
	("MZ_ToggleRadioAMFM", "Toggle Radio AM / FM", "Toggles radio between AM and FM", "MZ_ToggleRadioAMFM"),
	("MZ_RadioAutoFreqUp", "Radio Auto Freq Up", "Auto increases the radio frequency", "MZ_RadioAutoFreqUp"),
	("MZ_RadioAtuoFreqDown", "Radio Auto Freq Down", "Auto decreases the radio frequency", "MZ_RadioAutoFreqDown"),
	("MZ_RadioFreqUp", "Radio Freq Up", "Increases the radio frequency", "MZ_RadioFreqUp"),
	("MZ_RadioFreqDown", "Radio Freq Down", "Decreases the radio frequency", "MZ_RadioFreqDown"),
	("MZ_Scene1", "Scene 1", "Changes the current scene to be Scene 1", "MZ_Scene1"),
	("MZ_Scene2", "Scene 2", "Changes the current scene to be Scene 2", "MZ_Scene2"),
	("MZ_Scene3", "Scene 3", "Changes the current scene to be Scene 3", "MZ_Scene3"),
	("MZ_Scene4", "Scene 4", "Changes the current scene to be Scene 4", "MZ_Scene4"),
	("MZ_Scene5", "Scene 5", "Changes the current scene to be Scene 5", "MZ_Scene5"),
	("MZ_Scene6", "Scene 6", "Changes the current scene to be Scene 6", "MZ_Scene6"),
	("MZ_Scene7", "Scene 7", "Changes the current scene to be Scene 7", "MZ_Scene7"),
	("MZ_Scene8", "Scene 8", "Changes the current scene to be Scene 8", "MZ_Scene8"),
	("MZ_Scene9", "Scene 9", "Changes the current scene to be Scene 9", "MZ_Scene9"),
	("MZ_Scene10", "Scene 10", "Changes the current scene to be Scene 10", "MZ_Scene10"),
	("MZ_Scene11", "Scene 11", "Changes the current scene to be Scene 11", "MZ_Scene11"),
	("MZ_Scene12", "Scene 12", "Changes the current scene to be Scene 12", "MZ_Scene12"),
	#from this point I added
	("MZ_Cursor_Up", "Cursor Up", "Button Up on remote", "MZ_Cursor_Up"),
	("MZ_Cursor_Down", "Cursor Down", "Button Down on remote", "MZ_Cursor_Down"),
	("MZ_Cursor_Left", "Cursor Left", "Button Left on remote", "MZ_Cursor_Left"),
	("MZ_Cursor_Right", "Cursor Right", "Button Right on remote", "MZ_Cursor_Right"),
	("MZ_Cursor_Enter", "Cursor Enter", "Button Enter on remote", "MZ_Cursor_Enter"),
	("MZ_Cursor_Return", "Cursor Return", "Button Return on remote", "MZ_Cursor_Return"),
	("MZ_Cursor_Level", "Cursor Level", "Button Level on remote", "MZ_Cursor_Level"),
	("MZ_Cursor_On_Screen", "Cursor On Screen", "Button On_Screen on remote", "MZ_Cursor_On_Screen"),
	("MZ_Cursor_Option", "Cursor Option", "Button Option on remote", "MZ_Cursor_Option"),
	("MZ_Cursor_Top_Menu", "Cursor Top Menu", "Button Top_Menu on remote", "MZ_Cursor_Top_Menu"),
	("MZ_Cursor_Pop_Up_Menu", "Cursor Pop Up Menu", "Button Pop_Up_Menu on remote", "MZ_Cursor_Pop_Up_Menu"),
	("MZ_NumChar_1", "NumChar 1", "Button 1 on remote", "MZ_NumChar_1"),
	("MZ_NumChar_2", "NumChar 2", "Button 2 on remote", "MZ_NumChar_2"),
	("MZ_NumChar_3", "NumChar 3", "Button 3 on remote", "MZ_NumChar_3"),
	("MZ_NumChar_4", "NumChar 4", "Button 4 on remote", "MZ_NumChar_4"),
	("MZ_NumChar_5", "NumChar 5", "Button 5 on remote", "MZ_NumChar_5"),
	("MZ_NumChar_6", "NumChar 6", "Button 6 on remote", "MZ_NumChar_6"),
	("MZ_NumChar_7", "NumChar 7", "Button 7 on remote", "MZ_NumChar_7"),
	("MZ_NumChar_8", "NumChar 8", "Button 8 on remote", "MZ_NumChar_8"),
	("MZ_NumChar_9", "NumChar 9", "Button 9 on remote", "MZ_NumChar_9"),
	("MZ_NumChar_0", "NumChar 0", "Button 0 on remote", "MZ_NumChar_0"),
	("MZ_NumChar_+10", "NumChar +10", "Button +10 on remote", "MZ_NumChar_+10"),
	("MZ_NumChar_ENT", "NumChar ENT", "Button ENT on remote", "MZ_NumChar_ENT"),
	("MZ_Operation_Stop", "Operation Stop", "Button Stop on Remote", "MZ_Operation_Stop"),
	("MZ_Operation_Pause", "Operation Pause", "Button Pause on Remote", "MZ_Operation_Pause"),
	("MZ_Operation_Play", "Operation Play", "Button Play on Remote", "MZ_Operation_Play"),
	("MZ_Operation_Search-", "Operation Search-", "Button Search- (Hold) on Remote", "MZ_Operation_Search-"),
	("MZ_Operation_Search+", "Operation Search+", "Button Search+ (Tag) on Remote", "MZ_Operation_Search+"),
	("MZ_Operation_Skip-", "Operation Skip-", "Button Skip- on Remote", "MZ_Operation_Skip-"),
	("MZ_Operation_Skip+", "Operation Skip+", "Button Skip+ on Remote", "MZ_Operation_Skip+"),
	("MZ_Operation_FM", "Operation FM", "Button FM on Remote", "MZ_Operation_FM"),
	("MZ_Operation_AM", "Operation AM", "Button AM on Remote", "MZ_Operation_AM")
	)


GETACTIONS = (
	("MZ_Get_Basic_Mute", "MZ Get Basic Mute", "Get status of Mute", "MZ_Get_Basic_Mute"),
	("MZ_Get_Basic_Sleep", "MZ Get Basic Sleep", "Get status of Sleep", "MZ_Get_Basic_Sleep"),
	("MZ_Get_Basic_Power", "MZ Get Basic Power", "Get status of Power", "MZ_Get_Basic_Power"),
	("MZ_Get_Basic_Enhancer", "MZ Get Basic Enhancer", "Get status of Enhancer", "MZ_Get_Basic_Enhancer"),
	("MZ_Get_Basic_Title", "MZ Get Basic Title", "Get status of Title", "MZ_Get_Basic_Title"),
	("MZ_Get_Basic_Sound_Program", "MZ Get Basic Sound Program", "Get status of Sound_Program", "MZ_Get_Basic_Sound_Program"),
	("MZ_Get_Basic_Straight", "MZ Get Basic Straight", "Get status of Straight", "MZ_Get_Basic_Straight"),
	("MZ_Get_Basic_Val", "MZ Get Basic Val", "Get status of Val", "MZ_Get_Basic_Val"),
	("MZ_Get_Basic_Exp", "MZ Get Basic Exp", "Get status of Exp", "MZ_Get_Basic_Exp"),
	("MZ_Get_Basic_Unit", "MZ Get Basic Unit", "Get status of Unit", "MZ_Get_Basic_Unit"),
	("MZ_Get_Basic_3D_Cinema_DSP", "MZ Get Basic 3D Cinema DSP", "Get status of _3D_Cinema_DSP", "MZ_Get_Basic_3D_Cinema_DSP"),
	("MZ_Get_Basic_Dialogue_Lift", "MZ Get Basic Dialogue Lift", "Get status of Dialogue_Lift", "MZ_Get_Basic_Dialogue_Lift"),
	("MZ_Get_Basic_Party_Info", "MZ Get Basic Party Info", "Get status of Party_Info", "MZ_Get_Basic_Party_Info"),
	("MZ_Get_Basic_Mode", "MZ Get Basic Mode", "Get status of Mode", "MZ_Get_Basic_Mode"),
	("MZ_Get_Basic_Adaptive_DRC", "MZ Get Basic Adaptive DRC", "Get status of Adaptive_DRC", "MZ_Get_Basic_Adaptive_DRC"),
	("MZ_Get_Basic_Current", "MZ Get Basic Current", "Get status of Current", "MZ_Get_Basic_Current"),
	("MZ_Get_Basic_Src_Number", "MZ Get Basic Src Number", "Get status of Src_Number", "MZ_Get_Basic_Src_Number"),
	("MZ_Get_Basic_Input_Sel", "MZ Get Basic Input Sel", "Get status of Input_Sel", "MZ_Get_Basic_Input_Sel"),
	("MZ_Get_Tuner_Feature_Availability", "MZ Get Tuner Feature Availability", "Get status of Feature_Availability", "MZ_Get_Tuner_Feature_Availability"),
	("MZ_Get_Tuner_Val", "MZ Get Tuner Val", "Get status of Val", "MZ_Get_Tuner_Val"),
	("MZ_Get_Tuner_Band", "MZ Get Tuner Band", "Get status of Band", "MZ_Get_Tuner_Band"),
	("MZ_Get_Tuner_Exp", "MZ Get Tuner Exp", "Get status of Exp", "MZ_Get_Tuner_Exp"),
	("MZ_Get_Tuner_Unit", "MZ Get Tuner Unit", "Get status of Unit", "MZ_Get_Tuner_Unit"),
	("MZ_Get_Tuner_FM_Mode", "MZ Get Tuner FM Mode", "Get status of FM_Mode", "MZ_Get_Tuner_FM_Mode"),
	("MZ_Get_Tuner_Stereo", "MZ Get Tuner Stereo", "Get status of Stereo", "MZ_Get_Tuner_Stereo"),
	("MZ_Get_Tuner_Tuned", "MZ Get Tuner Tuned", "Get status of Tuned", "MZ_Get_Tuner_Tuned"),
	("MZ_Get_Tuner_Search_Mode", "MZ Get Tuner Search Mode", "Get status of Search_Mode", "MZ_Get_Tuner_Search_Mode"),
	("MZ_Get_Tuner_Preset_Sel", "MZ Get Tuner Preset Sel", "Get status of Preset_Sel", "MZ_Get_Tuner_Preset_Sel"),
	("MZ_Get_PC_Feature_Availability", "MZ Get PC Feature Availability", "Get status of Feature_Availability", "MZ_Get_PC_Feature_Availability"),
	("MZ_Get_PC_Artist", "MZ Get PC Artist", "Get status of Artist", "MZ_Get_PC_Artist"),
	("MZ_Get_PC_Album", "MZ Get PC Album", "Get status of Album", "MZ_Get_PC_Album"),
	("MZ_Get_PC_Song", "MZ Get PC Song", "Get status of Song", "MZ_Get_PC_Song"),
	("MZ_Get_PC_Playback_Info", "MZ Get PC Playback Info", "Get status of Playback_Info", "MZ_Get_PC_Playback_Info"),
	("MZ_Get_PC_Format", "MZ Get PC Format", "MZ_Get status of Format", "MZ_Get_PC_Format"),
	("MZ_Get_PC_ID", "MZ Get PC ID", "Get status of ID", "MZ_Get_PC_ID"),
	("MZ_Get_PC_URL", "MZ Get PC URL", "Get status of URL", "MZ_Get_PC_URL")
	)


Z2SENDACTIONS = (   
	("Z2_VolumeUp_0.5", "Z2 Volume Up 0.5db", "Increase the volume one step (0.5 dB)", "Z2_VolumeUp_0.5"),
	("Z2_VolumeDown_0.5", "Z2 Volume Down 0.5db", "Decrease the volume one step (0.5 dB)", "Z2_VolumeDown_0.5"),
	("Z2_VolumeUp_1.0", "Z2 Volume Up 1.0dB", "Increase the volume 1.0 dB", "Z2_VolumeUp_1.0"),
	("Z2_VolumeDown_1.0", "Z2 Volume Down 1.0dB", "Decrease the volume 1.0 dB", "Z2_VolumeDown_1.0"),
	("Z2_VolumeUp_1.5", "Z2 Volume Up 1.5dB", "Increase the volume 1.5 dB", "Z2_VolumeUp_1.5"),
	("Z2_VolumeDown_1.5", "Z2 Volume Down 1.5dB", "Decrease the volume 1.5 dB", "Z2_VolumeDown_1.5"),
	("Z2_VolumeUp_2.0", "Z2 Volume Up 2.0dB", "Increase the volume 2.0 dB", "Z2_VolumeUp_2.0"),
	("Z2_VolumeDown_2.0", "Z2 Volume Down 2.0dB", "Decrease the volume 2.0 dB", "Z2_VolumeDown_2.0"),
	("Z2_VolumeUp_2.5", "Z2 Volume Up 2.5dB", "Increase the volume 2.5 dB", "Z2_VolumeUp_2.5"),
	("Z2_VolumeDown_2.5", "Z2 Volume Down 2.5dB", "Decrease the volume 2.5 dB", "Z2_VolumeDown_2.5"),
	("Z2_VolumeUp_3.0", "Z2 Volume Up 3.0dB", "Increase the volume 3.0 dB", "Z2_VolumeUp_3.0"),
	("Z2_VolumeDown_3.0", "Z2 Volume Down 3.0dB", "Decrease the volume 3.0 dB", "Z2_VolumeDown_3.0"),
	("Z2_VolumeUp_3.5", "Z2 Volume Up 3.5dB", "Increase the volume 3.5 dB", "Z2_VolumeUp_3.5"),
	("Z2_VolumeDown_3.5", "Z2 Volume Down 3.5dB", "Decrease the volume 3.5 dB", "Z2_VolumeDown_3.5"),
	("Z2_VolumeUp_4.0", "Z2 Volume Up 4.0dB", "Increase the volume 4.0 dB", "Z2_VolumeUp_4.0"),
	("Z2_VolumeDown_4.0", "Z2 Volume Down 4.0dB", "Decrease the volume 4.0 dB", "Z2_VolumeDown_4.0"),
	("Z2_VolumeUp_4.5", "Z2 Volume Up 4.5dB", "Increase the volume 4.5 dB", "Z2_VolumeUp_4.5"),
	("Z2_VolumeDown_4.5", "Z2 Volume Down 4.5dB", "Decrease the volume 4.5 dB", "Z2_VolumeDown_4.5"),
	("Z2_VolumeUp_5.0", "Z2 Volume Up 5.0dB", "Increase the volume 5.0 dB", "Z2_VolumeUp_5.0"),
	("Z2_VolumeDown_5.0", "Z2 Volume Down 5.0dB", "Decrease the volume 5.0 dB", "Z2_VolumeDown_5.0"),
	("Z2_ToggleMute", "Z2 Toggle Mute", "Toggles mute state", "Z2_ToggleMute"),
	("Z2_PowerOff", "Z2 Power Off", "Powers off machine", "Z2_PowerOff"),
	("Z2_PowerOn", "Z2 Power On", "Powers on machine", "Z2_PowerOn"),
	("Z2_Source_V-AUX", "Z2 Source V-AUX", "Changes source to V-AUX", "Z2_Source_V-AUX"),
	("Z2_Source_AV1", "Z2 Source AV1", "Changes source to AV1", "Z2_Source_AV1"),
	("Z2_Source_AV2", "Z2 Source AV2", "Changes source to AV2", "Z2_Source_AV2"),
	("Z2_Source_AV3", "Z2 Source AV3", "Changes source to AV3", "Z2_Source_AV3"),
	("Z2_Source_AV4", "Z2 Source AV4", "Changes source to AV4", "Z2_Source_AV4"),
	("Z2_Source_AV5", "Z2 Source AV5", "Changes source to AV5", "Z2_Source_AV5"),
	("Z2_Source_AV6", "Z2 Source AV6", "Changes source to AV6", "Z2_Source_AV6"),
	("Z2_Source_TUNER", "Z2 Source Tuner", "Changes source to radio", "Z2_Source_TUNER"),
	("Z2_Source_DOCK", "Z2 Source DOCK", "Changes source to DOCK", "Z2_Source_DOCK"),
	("Z2_Source_AUDIO1", "Z2 Source AUDIO1", "Changes source to AUDIO1", "Z2_Source_AUDIO1"),
	("Z2_Source_AUDIO2", "Z2 Source AUDIO2", "Changes source to AUDIO2", "Z2_Source_AUDIO2"),
	("Z2_Source_SIRIUS", "Z2 Source SIRIUS", "Changes source to SIRIUS", "Z2_Source_SIRIUS"),
	("Z2_Source_PC", "Z2 Source PC", "Changes source to PC", "Z2_Source_PC"),
	("Z2_Scene1", "Z2 Scene 1", "Changes the current scene to be Scene 1", "Z2_Scene1"),
	("Z2_Scene2", "Z2 Scene 2", "Changes the current scene to be Scene 2", "Z2_Scene2"),
	("Z2_Scene3", "Z2 Scene 3", "Changes the current scene to be Scene 3", "Z2_Scene3"),
	("Z2_Scene4", "Z2 Scene 4", "Changes the current scene to be Scene 4", "Z2_Scene4"),
	("Z2_Scene5", "Z2 Scene 5", "Changes the current scene to be Scene 5", "Z2_Scene5"),
	("Z2_Scene6", "Z2 Scene 6", "Changes the current scene to be Scene 6", "Z2_Scene6"),
	("Z2_Scene7", "Z2 Scene 7", "Changes the current scene to be Scene 7", "Z2_Scene7"),
	("Z2_Scene8", "Z2 Scene 8", "Changes the current scene to be Scene 8", "Z2_Scene8"),
	("Z2_Scene9", "Z2 Scene 9", "Changes the current scene to be Scene 9", "Z2_Scene9"),
	("Z2_Scene10", "Z2 Scene 10", "Changes the current scene to be Scene 10", "Z2_Scene10"),
	("Z2_Scene11", "Z2 Scene 11", "Changes the current scene to be Scene 11", "Z2_Scene11"),
	("Z2_Scene12", "Z2 Scene 12", "Changes the current scene to be Scene 12", "Z2_Scene12"),
	("Z2_Cursor_Up", "Cursor Up", "Button Up on remote", "Z2_Cursor_Up"),
	("Z2_Cursor_Down", "Cursor Down", "Button Down on remote", "Z2_Cursor_Down"),
	("Z2_Cursor_Left", "Cursor Left", "Button Left on remote", "Z2_Cursor_Left"),
	("Z2_Cursor_Right", "Cursor Right", "Button Right on remote", "Z2_Cursor_Right"),
	("Z2_Cursor_Enter", "Cursor Enter", "Button Enter on remote", "Z2_Cursor_Enter"),
	("Z2_Cursor_Return", "Cursor Return", "Button Return on remote", "Z2_Cursor_Return"),
	("Z2_Cursor_Level", "Cursor Level", "Button Level on remote", "Z2_Cursor_Level"),
	("Z2_Cursor_On_Screen", "Cursor On Screen", "Button On_Screen on remote", "Z2_Cursor_On_Screen"),
	("Z2_Cursor_Option", "Cursor Option", "Button Option on remote", "Z2_Cursor_Option"),
	("Z2_Cursor_Top_Menu", "Cursor Top Menu", "Button Top_Menu on remote", "Z2_Cursor_Top_Menu"),
	("Z2_Cursor_Pop_Up_Menu", "Cursor Pop Up Menu", "Button Pop_Up_Menu on remote", "Z2_Cursor_Pop_Up_Menu"),
	("Z2_NumChar_1", "NumChar 1", "Button 1 on remote", "Z2_NumChar_1"),
	("Z2_NumChar_2", "NumChar 2", "Button 2 on remote", "Z2_NumChar_2"),
	("Z2_NumChar_3", "NumChar 3", "Button 3 on remote", "Z2_NumChar_3"),
	("Z2_NumChar_4", "NumChar 4", "Button 4 on remote", "Z2_NumChar_4"),
	("Z2_NumChar_5", "NumChar 5", "Button 5 on remote", "Z2_NumChar_5"),
	("Z2_NumChar_6", "NumChar 6", "Button 6 on remote", "Z2_NumChar_6"),
	("Z2_NumChar_7", "NumChar 7", "Button 7 on remote", "Z2_NumChar_7"),
	("Z2_NumChar_8", "NumChar 8", "Button 8 on remote", "Z2_NumChar_8"),
	("Z2_NumChar_9", "NumChar 9", "Button 9 on remote", "Z2_NumChar_9"),
	("Z2_NumChar_0", "NumChar 0", "Button 0 on remote", "Z2_NumChar_0"),
	("Z2_NumChar_+10", "NumChar +10", "Button +10 on remote", "Z2_NumChar_+10"),
	("Z2_NumChar_ENT", "NumChar ENT", "Button ENT on remote", "Z2_NumChar_ENT"),
	("Z2_Operation_Stop", "Operation Stop", "Button Stop on Remote", "Z2_Operation_Stop"),
	("Z2_Operation_Pause", "Operation Pause", "Button Pause on Remote", "Z2_Operation_Pause"),
	("Z2_Operation_Play", "Operation Play", "Button Play on Remote", "Z2_Operation_Play"),
	("Z2_Operation_Search-", "Operation Search-", "Button Search- (Hold) on Remote", "Z2_Operation_Search-"),
	("Z2_Operation_Search+", "Operation Search+", "Button Search+ (Tag) on Remote", "Z2_Operation_Search+"),
	("Z2_Operation_Skip-", "Operation Skip-", "Button Skip- on Remote", "Z2_Operation_Skip-"),
	("Z2_Operation_Skip+", "Operation Skip+", "Button Skip+ on Remote", "Z2_Operation_Skip+"),
	("Z2_Operation_FM", "Operation FM", "Button FM on Remote", "Z2_Operation_FM"),
	("Z2_Operation_AM", "Operation AM", "Button AM on Remote", "Z2_Operation_AM")
	)


Z2GETACTIONS = (
	("Z2_Get_Basic_Mute", "Z2 Get Basic Mute", "Get status of Mute", "Z2_Get_Basic_Mute"),
	("Z2_Get_Basic_Sleep", "Z2 Get Basic Sleep", "Get status of Sleep", "Z2_Get_Basic_Sleep"),
	("Z2_Get_Basic_Power", "Z2 Get Basic Power", "Get status of Power", "Z2_Get_Basic_Power"),
	("Z2_Get_Basic_Enhancer", "Z2 Get Basic Enhancer", "Get status of Enhancer", "Z2_Get_Basic_Enhancer"),
	("Z2_Get_Basic_Title", "Z2 Get Basic Title", "Get status of Title", "Z2_Get_Basic_Title"),
	("Z2_Get_Basic_Sound_Program", "Z2 Get Basic Sound Program", "Get status of Sound_Program", "Z2_Get_Basic_Sound_Program"),
	("Z2_Get_Basic_Straight", "Z2 Get Basic Straight", "Get status of Straight", "Z2_Get_Basic_Straight"),
	("Z2_Get_Basic_Val", "Z2 Get Basic Val", "Get status of Val", "Z2_Get_Basic_Val"),
	("Z2_Get_Basic_Exp", "Z2 Get Basic Exp", "Get status of Exp", "Z2_Get_Basic_Exp"),
	("Z2_Get_Basic_Unit", "Z2 Get Basic Unit", "Get status of Unit", "Z2_Get_Basic_Unit"),
	("Z2_Get_Basic_3D_Cinema_DSP", "Z2 Get Basic 3D Cinema DSP", "Get status of _3D_Cinema_DSP", "Z2_Get_Basic_3D_Cinema_DSP"),
	("Z2_Get_Basic_Dialogue_Lift", "Z2 Get Basic Dialogue Lift", "Get status of Dialogue_Lift", "Z2_Get_Basic_Dialogue_Lift"),
	("Z2_Get_Basic_Party_Info", "Z2 Get Basic Party Info", "Get status of Party_Info", "Z2_Get_Basic_Party_Info"),
	("Z2_Get_Basic_Mode", "Z2 Get Basic Mode", "Get status of Mode", "Z2_Get_Basic_Mode"),
	("Z2_Get_Basic_Adaptive_DRC", "Z2 Get Basic Adaptive DRC", "Get status of Adaptive_DRC", "Z2_Get_Basic_Adaptive_DRC"),
	("Z2_Get_Basic_Current", "Z2 Get Basic Current", "Get status of Current", "Z2_Get_Basic_Current"),
	("Z2_Get_Basic_Src_Number", "Z2 Get Basic Src Number", "Get status of Src_Number", "Z2_Get_Basic_Src_Number"),
	("Z2_Get_Basic_Input_Sel", "Z2 Get Basic Input Sel", "Get status of Input_Sel", "Z2_Get_Basic_Input_Sel"),
	)

class ActionPrototype(eg.ActionClass):
	def __call__(self):
		try:
			print self.value
			value = self.value
			if value[:3] == "MZ_":
				value = value.replace('MZ_','')
				print "in main zone"
				if value[:3] == "Get":
					self.plugin.rxv.get_action(value, ACTION_BUTTON)	#receiving actions
					return eg.globals.YamahaReturn
				else:
					self.plugin.rxv.send_action(value, ACTION_BUTTON)	#send actions
			elif value[:3] == "Z2_":
				value = value.replace('Z2_','')
				print "in zone 2"
				if value[:3] == "Get":
					self.plugin.rxv.get_z2_action(value, ACTION_BUTTON)	#receiving actions
					return eg.globals.YamahaReturn
				else:
					self.plugin.rxv.send_z2_action(value, ACTION_BUTTON)	#send actions
		except:
			raise self.Exceptions.ProgramNotRunning

class RXV(eg.PluginClass):

	class text:
		actionGroupName = "Actions"
		actionGroupDescription = (
			"Here you find actions for changing the receiver."
		)
		infoGroupName = "Information"
		infoGroupDescription = (
			"Here you find actions that query different aspects of the receiver."
		)
		z2GroupName = "Zone 2"
		z2GroupDescription = (
			"Here you find actions that query different aspects of the receiver."
		)
		z2actionGroupName = "Zone 2 Actions"
		z2actionGroupDescription = (
			"Here you find actions that query different aspects of the receiver."
		)
		z2infoGroupName = "Zone 2 Information"
		z2infoGroupDescription = (
			"Here you find actions that query different aspects of the receiver."
		)

	def __init__(self):
		group = self.AddGroup(
			self.text.actionGroupName,
			self.text.actionGroupDescription
		)
		group2 = self.AddGroup(
			self.text.infoGroupName,
			self.text.infoGroupDescription
		)
		zone2 = self.AddGroup(
			self.text.z2GroupName,
			self.text.z2GroupDescription
		)
		zone2send = zone2.AddGroup(
			self.text.z2actionGroupName,
			self.text.z2actionGroupDescription
		)
		zone2get = zone2.AddGroup(
			self.text.z2infoGroupName,
			self.text.z2infoGroupDescription
		)
		group.AddActionsFromList(SENDACTIONS, ActionPrototype)	#this is for sending commands
		group2.AddActionsFromList(GETACTIONS, ActionPrototype)	#this is for commands receiving information
		zone2send.AddActionsFromList(Z2SENDACTIONS, ActionPrototype)	#this is for sending commands ZONE 2
		zone2get.AddActionsFromList(Z2GETACTIONS, ActionPrototype)	#this is for commands receiving information ZONE 2
		self.rxv = RXVClient()

	def Configure(self, IPAddress = "192.168.0.0", Port = "80"):
		panel = eg.ConfigPanel()
		IPAControl = wx.TextCtrl(panel, -1, IPAddress)
		panel.sizer.Add(IPAControl, 1, wx.EXPAND)
		IPPControl = wx.TextCtrl(panel, -1, Port)
		panel.sizer.Add(IPPControl, 1, wx.EXPAND)
		while panel.Affirmed():
			panel.SetResult(
				IPAControl.GetValue(),
				IPPControl.GetValue()
			)
		self.__start__(IPAddress, Port)

	def __start__(self, IPAddress, Port):
		self.IPAddress = IPAddress
		self.Port = Port
		rxvxxx.IP_ADDRESS = IPAddress
		rxvxxx.PORT = Port