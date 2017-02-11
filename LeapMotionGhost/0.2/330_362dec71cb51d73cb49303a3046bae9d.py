import eg

eg.RegisterPlugin(
    name = "LeapMotionGhost",
    author = "Lucleonhart",
    version = "0.2",
    kind = "other",
    description = "Handle Events from the LeapMotion Controller"
)

#Leap imports
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from threading import Event, Thread

class LeapMotionGhost(eg.PluginBase):
    def __start__(self):
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadLoop,
            args=(self.stopThreadEvent, )
        )
        thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()

    def ThreadLoop(self, stopThreadEvent):
        listener = SampleListener()
        listener.setParent(self)
        controller = Leap.Controller()
        controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
        controller.add_listener(listener)
        
        while not stopThreadEvent.isSet():
            stopThreadEvent.wait(0.005)
        
        controller.remove_listener(listener)
        
    def DoEvent(self, EventName):
        self.TriggerEvent(EventName)

class SampleListener(Leap.Listener):
    global _parent
    def setParent(self, parent):
        global _parent
        _parent = parent

    def on_init(self, controller):
        print "LeapMotion - Initialized"

    def on_exit(self, controller):
        print "LeapMotion - Exited"

    def on_connect(self, controller):
        print "LeapMotion - Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        #controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "LeapMotion - Disconnected"

    def on_frame(self, controller):
        global _parent
        global _lastX
        global _lastY
        global _circle_angle
        threshold = 150
        circle_threshold = 60
        
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.empty:
            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)
                    
                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counterclockwise"
                        
                    if(circle.state == Leap.Gesture.STATE_START):
                        _circle_angle = 0

                    if(_circle_angle * Leap.RAD_TO_DEG <= circle_threshold):
                        if circle.state != Leap.Gesture.STATE_START:
                            previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                            _circle_angle +=  (circle.progress - previous_update.progress) * 2 * Leap.PI
                            
                        if(_circle_angle * Leap.RAD_TO_DEG > circle_threshold):
                            if(clockwiseness == "clockwise"):
                                _parent.DoEvent("CircleClockwise")
                            else:
                                _parent.DoEvent("CircleCounterClockwise")
                        #print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (gesture.id, self.state_string(gesture.state), circle.progress, circle.radius, _circle_angle * Leap.RAD_TO_DEG, clockwiseness)
                        
                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    screentap = ScreenTapGesture(gesture)
                    _parent.DoEvent("ScreenTap")
        
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
                        
            if not fingers.empty:
                # Get the first finger
                finger = fingers[0]
                fingerPos = finger.tip_position
                x = fingerPos.x
                y = fingerPos.y
                
                if(_lastX == 0):
                    _lastX = x
                    _lastY = y
                else:
                    vx = _lastX - x
                    vy = _lastY - y
                    
                    if(vx > threshold or vx < -threshold or vy > threshold or vy < -threshold):
                        _lastX = x
                        _lastY = y
                        
                        if(abs(vx) > abs(vy)):
                            # Movement in x was bigger than movement in y
                            if(vx < 0):
                                # Right
                                #print "SwipeRight"
                                _parent.DoEvent("SwipeRight")
                            else:
                                # Left
                                print "SwipeLeft"
                                _parent.DoEvent("SwipeLeft")
                        else:
                            # Movement in y was bigger than movement in x
                            if(vy < 0):
                                # Up
                                if(len(fingers) > 4):
                                    # Full Hand Up!
                                    #print "Back"
                                    _parent.DoEvent("Back")
                                else:
                                    # Normal
                                    #print "SwipeUp"
                                    _parent.DoEvent("SwipeUp")
                            else:
                                # Down
                                #print "SwipeDown"
                                _parent.DoEvent("SwipeDown")
            else:
                _lastX = 0
                _lastY = 0
            
        else:
            _lastX = 0
            _lastY = 0

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
