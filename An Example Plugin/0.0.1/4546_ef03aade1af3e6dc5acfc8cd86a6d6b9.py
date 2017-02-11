import eg

eg.RegisterPlugin(
	name = "An Example Plugin",
	author = "Bob P",
	version = "0.0.1",
	kind = "other",
	description = "This is an example plugin",
)


eg.RegisterPlugin()


class MyNewPlugin(eg.PluginBase):

    def __init__(self):
        self.AddAction(HelloWorld)


class HelloWorld(eg.ActionBase):

    def __call__(self):
        print "Hello World!"
