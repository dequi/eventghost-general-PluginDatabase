eg.RegisterPlugin(
    name = "Process Watcher",
    author = "Bitmonster & DranDane",
    version = "1.0.",
    description = (
        "Generates events if a process is created or destoyed"
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABuklEQVR42o1Sv0tCYRQ9"
        "L1FccpCEB73wVy1NjTrUPxD1lgZp0dWKaAhXxWhoyWgoIUjHBEH65RSE0CAUgWIPLAqR"
        "gkAQIQXR8nW/Z0ai6btweJfDd847934fhz8VCARkqCjTmBGra+sc67kOGQqFZIfDMVCo"
        "1WphMpng9/vxkMvi9u6e4zp/ZmStVkOpVOor1mg00Ol0CIfDKBQK/Q1isRhcLhedJpIn"
        "vHXkI+D5SUSj+0in0wMM4mSw6WqL9whLhHeCYAA/tobo9twQgxsyEMjglUj6IE7YIJxQ"
        "gk9K8DwsgTLCMjGGdvJxJibMUgJ+hUaYGWyQSCQQDO7+ZO8uo1EHn8/2v4Hb7UYmkxl4"
        "jY1GA9lsFrlcDl+fDZxfJNsGHo9H1QNiVa/XlQSiuIAp2wS466ukHNjaUauHXq+H0+n8"
        "HYPrzF+pVHriSpLUxbGHJAgCIpFIr0EqlYI0KmH6Y1o5XC6XaaFBpW+1WqhWq7BYLLRI"
        "X9ciFQNRFJHP53FoO4T3xdsTu9lsolgswm63Kz1b9tPTI6xmAVzk+Eg+PbtUvQNWstxS"
        "xHv7B+1bEBfnVd8CK6vFrIhZ/w1wBAQrC42uqQAAAABJRU5ErkJggg=="
    ),
)

from eg.cFunctions import GetProcessDict
from threading import Thread
from time import sleep
from os.path import splitext
import threading
from eg.WinApi.Dynamic import (
# functions:
    CreateEvent,
    PulseEvent,
)

class Process(eg.PluginClass):

    def __start__(self):
        self.stopEvent = CreateEvent(None, 1, 0, None)
        self.startException = None
        startupEvent = threading.Event()
        self.thread = threading.Thread(
            target=self.ThreadLoop, 
            name="ProcessWatcherThread", 
            args=(startupEvent,)
        )
        self.thread.start()
        startupEvent.wait(3)
        if self.startException is not None:
            raise self.Exception(self.startException)
              
    def __stop__(self):
        if self.thread is not None:
            PulseEvent(self.stopEvent)
            self.thread.join(5.0)

    def ThreadLoop(self, stopThreadEvent):
        oldProcesses = GetProcessDict()
        oldPids = set(oldProcesses.iterkeys())
   
        while True:
            newProcesses = GetProcessDict()
            newPids = set(newProcesses.iterkeys())
            for pid in newPids.difference(oldPids):
                name = splitext(newProcesses[pid])[0]
                eg.TriggerEvent("Created." + name, prefix="Process")
            for pid in oldPids.difference(newPids):
                name = splitext(oldProcesses[pid])[0]
                eg.TriggerEvent("Destroyed." + name, prefix="Process")
            oldProcesses = newProcesses
            oldPids = newPids
            sleep(0.1)
