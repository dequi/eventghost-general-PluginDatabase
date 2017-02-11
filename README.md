# EventGhost Plugin Database

This is an attempt to create a list of [EventGhost](https://github.com/EventGhost/EventGhost) plugins that were posted to the [EventGhost forum](http://www.eventghost.org/forum).

>> Note: None of this code is my own work, credit goes to all dedicated people on the [EventGhost forum](http://www.eventghost.org/forum), and the authors of each plugin.

## Why ?

* to be able to update the EventGhost [Plugin](https://github.com/EventGhost/EventGhost/wiki/Plugins) list.
* to create an online backup of possibly *'forgotten'*, *'unmaintained'* or *'unavailable anywhere else'* EventGhost plugins if something happens to the forum.

## How ?

It was started from a backup I was able to make, when I was *briefly* granted admin access. 
I parsed all posted `.py` attachments looking for `eg.RegisterPlugin()` and extracting `name` and `version` information. 
Then doing the same for all compressed archive attachments `.zip`, `.rar`, `.7z`, `.tgz` by automatically extracting them and parse all containing `.py` files.

From here on out it's mainly a manual effort to clean up the list further.