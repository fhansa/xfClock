import pygame
#
#   Base of Modules in xfClock
#
class moduleBase:   

    def __init__(self, app):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.modulePath = ""
        self._config = {}
        self.app = app
        pass  

    ## ----------------------------------------------------
    ##  Lifecycle stubs - override in subclass to implement module
    ##  
    def on_init(self):
        pass   
    def on_render(self, surface):
        pass
    def on_loop(self):
        pass
    def on_message(self):
        pass
    def on_cleanup(self):
        pass

    ## ----------------------------------------------------
    ##  Exposed properties
    ##

    ## Module configuration
    @property   
    def config(self):
         return self._config
    @config.setter
    def config(self,value):
        # merge default config and new config
        # value will always overwrite
        self._config = { **self._config, **value }

    ## Rect for the module
    @property
    def rect(self):
        return ((self.x, self.y), (self.width, self.height))
    @rect.setter
    def rect(self, value):
        self.x = value[0][0]
        self.y = value[0][1]
        self.width = value[1][0]
        self.height = value[1][1]

    ## Easy access to position and size
    @property
    def position(self):
        return (self.x, self.y)
    @property
    def size(self):
        return (self.width, self.height)


    ## ----------------------------------------------------
    ##  Helpers
    ##

    ## Transform image to new size but keep aspect rate    
    def aspect_scale(self, img,bx,by):
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