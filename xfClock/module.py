#
#   Base of Modules in xfClock
#
class moduleBase:
    def __init__(self):
        self._width = 0
        self._height = 0
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
    
    @property 
    def width(self):
        return self._width]
    @width.setter
    def width(self, value):
        self._width = value

    @property 
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        self._height = value

    @property
    def rect(self):
        return (self.width, self.height)
    
    @rect.setter
    def rect(self, value):
        self.width = value[0]
        self.height = value[1]
