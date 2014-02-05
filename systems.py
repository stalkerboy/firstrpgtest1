from sdl2.ext.ebs import Applicator, System
from sdl2.rect import SDL_Rect
import sdl2.timer
import sdl2.render
import sdl2.ext as sdl2ext
from dataformat import CharactorData, FrameCount, SpriteData


class RenderSystem(Applicator):
    def __init__(self, renderer):
        super().__init__()
        self.componenttypes = (SpriteData, CharactorData)
        self.renderer = renderer
        self.viewposx = 0
        self.viewposy = 0

    def process(self, world, componentsets):
        # self.renderer.clear(sdl2ext.Color(100, 100, 100))
        for sdata, cdata in componentsets:
            srcrect = sdata.srcrect
            if cdata.is_subject:
                self.viewposx, self.viewposy = sdata.viewrect.x, sdata.viewrect.y = cdata.posx, cdata.posy
            if sdata.type == 'SPRITE':
                distrect = SDL_Rect(cdata.posx - self.viewposx, cdata.posy - self.viewposy, cdata.sizew, cdata.sizeh)
                sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, srcrect, distrect)
        # sdl2.render.SDL_RenderPresent(self.renderer.renderer)


class BackgroundSystem(System):
    def __init__(self, renderer):
        super().__init__()
        self.componenttypes = (SpriteData,)
        self.renderer = renderer
        self.viewrect = SDL_Rect()

    def process(self, world, components):
        for sdata in components:
            if sdata.type == 'BACKGROUND':
                print(sdata.viewrect)
                sdata.viewrect.w, sdata.viewrect.h = 640, 480
                sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, sdata.viewrect, None)


class ForegroundSystem(System):
    def __init__(self, renderer):
        super().__init__()
        self.componenttypes = (SpriteData,)
        self.renderer = renderer

    def process(self, world, components):
        for sdata in components:
            # if sdata.type == 'FOREGROUND':
            #     sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, srcrect, distrect)
            pass
        sdl2.render.SDL_RenderPresent(self.renderer.renderer)


class ViewSystem(Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (SpriteData, CharactorData)
        self.viewrect = SDL_Rect()
        self.viewposx = 0
        self.viewposy = 0

    def process(self, world, componentsets):
        for sdata, cdata in componentsets:
            if cdata.is_subject:
                self.viewposx, self.viewposy = sdata.viewrect.x, sdata.viewrect.y = cdata.posx, cdata.posy

            if sdata.type == 'SPRITE':
                self.viewrect = sdata.viewrect
                break
        for sdata in componentsets:
            if sdata.type != 'SPRITE':
                sdata.viewrect = self.viewrect


class MappingSystem(System):
    def __init__(self):
        super().__init__()
        self.componenttypes = (CharactorData,)
        self.mapdata = {}

    def process(self, world, componentsets):
        for cdata in componentsets:

            self.mapdata[cdata.name] = (cdata.posx, cdata.posy, cdata.posx+cdata.sizew, cdata.posy+cdata.sizeh)

            if cdata.state == 0:
                continue
            elif cdata.state == 1 :
                tempposx = cdata.posx
                tempposy = cdata.posy
                cdata.posx += cdata.vx
                cdata.posy += cdata.vy
                self.mapdata[cdata.name] = (cdata.posx, cdata.posy, cdata.posx+cdata.sizew, cdata.posy+cdata.sizeh)

                if self._overlap(cdata.name):
                    cdata.posx = tempposx
                    cdata.posy = tempposy
                self.mapdata[cdata.name] = (cdata.posx, cdata.posy, cdata.posx+cdata.sizew, cdata.posy+cdata.sizeh)

    def _overlap(self, cname):
        left, top, right, bottom = self.mapdata[cname]
        for name, area in self.mapdata.items():
            mdleft, mdtop, mdright, mdbottom = area
            if cname == name:
                continue
            elif left < mdright and right > mdleft and top < mdbottom and bottom > mdtop:
                return True
        return False


class NPCSystem(Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super().__init__()
        self.componenttypes = (CharactorData, SpriteData, FrameCount)
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for cdata, sdata, framecount in componentsets:
            if cdata.type != 'NPC':
                continue
            if cdata.posx >= self.maxx - cdata.sizew:
                cdata.vx = -1
                cdata.direction = 1
            elif cdata.posx <= self.minx:
                cdata.vx = 1
                cdata.direction = 2

            srcx = sdata.img_startx + ((framecount.count // sdata.frame_rate) % sdata.ani_count) * cdata.sizew
            srcy = sdata.img_starty + cdata.direction * cdata.sizeh
            sdata.srcrect = SDL_Rect(srcx, srcy, cdata.sizew, cdata.sizeh)


class PlayerSystem(Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (CharactorData, SpriteData, FrameCount)
        self.srcx = 0
        self.srcy = 0

    def process(self, world, componentsets):
        for cdata, sdata, framecount in componentsets:
            if cdata.type != 'PLAYER':
                continue
            if cdata.state == 1:
                self.srcx = sdata.img_startx + ((framecount.count // sdata.frame_rate) % sdata.ani_count) * cdata.sizew
                self.srcy = sdata.img_starty + cdata.direction * cdata.sizeh
            sdata.srcrect = SDL_Rect(self.srcx, self.srcy, cdata.sizew, cdata.sizeh)


class FrameCountSystem(System):
    def __init__(self):
        self.componenttypes = (FrameCount,)

    def process(self, world, components):
        for frame in components:
            frame.count = self.fps_delay(60, frame.count)

    def fps_delay(self, fps, frames):
        """ fps_delay """
        frames = frames + 1
        ticks = sdl2.timer.SDL_GetTicks()

        # print('fps: {}'.format((frames / ticks) * 1000), end='\r')

        delay = frames / (fps / 1000) - ticks
        if delay < 0:
            delay = 1
        sdl2.timer.SDL_Delay(int(delay))

        return frames
