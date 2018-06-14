#
#   Base of Modules in xfClock
#
class moduleBase:
    def __init__(self):
        pass    
    def on_init(self, app):
        pass   
    def on_render(self, app):
        pass
    def on_loop(self):
        pass
    def on_message(self):
        pass

    @property 
    def config(self):
        return self._config

    @config.setter
    def config(self,value):
        # TODO: merge default config and new config
        self._config = value