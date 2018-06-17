import pygame
#
#   Base of Modules in xfClock
#
class moduleBase:   
    ##
    ##  Lifecycle
    ##
    def __init__(self):
        self._width = 0
        self._height = 0
        self.modulePath = ""
        self._config = {}
        pass    
    def on_init(self, app):
        pass   
    def on_render(self, app, surface):
        pass
    def on_loop(self, app):
        pass
    def on_message(self):
        pass

    ##
    ##  Exposed properties
    ##
    @property   
    def config(self):
         return self._config

    @config.setter
    def config(self,value):
        # merge default config and new config
        # value will always overwrite
        self._config = { **self._config, **value }
    
    @property 
    def width(self):
        return self._width
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
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property 
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value

    @property
    def rect(self):
        return (self.width, self.height)
    @rect.setter
    def rect(self, value):
        self.x = value[0][0]
        self.y = value[0][1]
        self.width = value[1][0]
        self.height = value[1][1]

    @property
    def position(self):
        return (self.x, self.y)
    
    @property
    def size(self):
        return (self.width, self.height)


    ##
    ##  Helpers
    ##

    # Transform and keep aspect rate    
    def aspect_scale(self, img,bx,by):
        """ Scales 'img' to fit into box bx/by.
        This method will retain the original image's aspect ratio """
        ix,iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx/float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by/float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx/float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return pygame.transform.scale(img, (int(sx),int(sy)))   