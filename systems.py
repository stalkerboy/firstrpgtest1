from sdl2.ext.ebs import Applicator, System
from sdl2.rect import SDL_Rect
import sdl2.timer
import sdl2.render
from dataformat import ObjectData, CharactorData, SpriteData, AnimationData, FrameCount


class RenderSystem(Applicator):
    def __init__(self, renderer):
        super().__init__()
        self.componenttypes = (ObjectData, SpriteData)
        self.renderer = renderer

    def process(self, world, componentsets):
        # self.renderer.clear(sdl2ext.Color(100, 100, 100))
        for odata, sdata in componentsets:
            if odata.type != 'BACK' and odata.type != 'FORE':

                distrect = SDL_Rect(odata.posx - sdata.viewrect.x, odata.posy - sdata.viewrect.y, odata.sizew, odata.sizeh)
                sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, sdata.srcrect, distrect)
        # sdl2.render.SDL_RenderPresent(self.renderer.renderer)


class BackgroundSystem(Applicator):
    def __init__(self, renderer):
        super().__init__()
        self.componenttypes = (ObjectData, SpriteData)
        self.renderer = renderer
        self.viewrect = SDL_Rect()

    def process(self, world, componentsets):
        for odata, sdata in componentsets:
            if odata.type == 'BACK':
                sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, sdata.viewrect, None)


class ForegroundSystem(Applicator):
    def __init__(self, renderer):
        super().__init__()
        self.componenttypes = (ObjectData, SpriteData)
        self.renderer = renderer

    def process(self, world, componentsets):
        for odata, sdata in componentsets:
            # if sdata.type == 'FOREGROUND':
            #     sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, srcrect, distrect)
            pass
        sdl2.render.SDL_RenderPresent(self.renderer.renderer)


class ViewReciveSystem(Applicator):
    def __init__(self, view_sizew, view_sizeh, mapsizew, mapsizeh):
        super().__init__()
        self.componenttypes = (SpriteData, CharactorData)
        self.view_sizew = view_sizew
        self.view_sizeh = view_sizeh
        self.mapsizew = mapsizew
        self.mapsizeh = mapsizeh

    def process(self, world, componentsets):
        viewx, viewy = 0, 0
        for sdata, cdata in componentsets:
            if sdata.is_subject:
                if cdata.posx < 0 or cdata.posx > self.mapsizew or cdata.posy < 0 or cdata.posy > self.mapsizeh:
                    continue

                if cdata.posx - self.view_sizew//2 < 0:
                    viewx = 0
                elif cdata.posx + self.view_sizew//2 > self.mapsizew:
                    viewx = self.mapsizew - self.view_sizew
                else:
                    viewx = cdata.posx-self.view_sizew//2

                if cdata.posy - self.view_sizeh//2 < 0:
                    viewy = 0
                elif cdata.posy + self.view_sizeh//2 > self.mapsizeh:
                    viewy = self.mapsizeh - self.view_sizeh
                else:
                    viewy = cdata.posy-self.view_sizeh//2

                sdata.viewrect = SDL_Rect(viewx, viewy, self.view_sizew, self.view_sizeh)
                break


class ViewSystem(System):
    def __init__(self):
        super().__init__()
        self.componenttypes = (SpriteData,)
        self.viewposx, self.viewposy = 0, 0
        self.viewrect = SDL_Rect()

    def process(self, world, components):
        for sdata in components:
            if isinstance(sdata, AnimationData) and sdata.is_subject:
                self.viewrect = sdata.viewrect
                break
        for sdata in components:
            sdata.viewrect = self.viewrect


class CollisionSystem(Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (ObjectData, SpriteData)
        self.mapdata = {}

    def process(self, world, componentsets):
        for odata, sdata in componentsets:

            self.mapdata[odata.id_] = (odata.posx, odata.posy, odata.posx+odata.sizew, odata.posy+odata.sizeh)

            if isinstance(odata, CharactorData):
                tempposx = odata.posx
                tempposy = odata.posy
                odata.posx += odata.vx
                odata.posy += odata.vy
                self.mapdata[odata.id_] = (odata.posx, odata.posy, odata.posx+odata.sizew, odata.posy+odata.sizeh)

                if self._overlap(odata.id_):
                    odata.posx = tempposx
                    odata.posy = tempposy
                self.mapdata[odata.id_] = (odata.posx, odata.posy, odata.posx+odata.sizew, odata.posy+odata.sizeh)

    def _overlap(self, oid):
        left, top, right, bottom = self.mapdata[oid]
        for id_, area in self.mapdata.items():
            mdleft, mdtop, mdright, mdbottom = area
            if oid == id_:
                continue
            elif left < mdright and right > mdleft and top < mdbottom and bottom > mdtop:
                return True
        return False


class NPCSystem(Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super().__init__()
        self.componenttypes = (CharactorData, AnimationData, FrameCount)
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for cdata, adata, framecount in componentsets:
            if cdata.type != 'NPC':
                continue
            if cdata.posx >= self.maxx - cdata.sizew:
                cdata.vx = -1
                cdata.direction = 1
            elif cdata.posx <= self.minx:
                cdata.vx = 1
                cdata.direction = 2

            srcx = adata.img_startx + ((framecount.count // adata.frame_rate) % adata.ani_num) * cdata.sizew
            srcy = adata.img_starty + cdata.direction * cdata.sizeh
            adata.srcrect = SDL_Rect(srcx, srcy, adata.sizew, adata.sizeh)


class StaticObjectSystem(Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (ObjectData, SpriteData)

    def process(self, world, componentsets):
        for odata, sdata in componentsets:
            if odata.type != 'STOBJECT':
                continue
            sdata.srcrect = SDL_Rect(sdata.img_startx, sdata.img_starty, sdata.sizew, sdata.sizeh)


class PlayerSystem(Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (CharactorData, AnimationData, FrameCount)
        self.srcx = 0
        self.srcy = 0

    def process(self, world, componentsets):
        for cdata, adata, framecount in componentsets:
            if cdata.type != 'PLAYER':
                continue
            if cdata.state == 1:
                self.srcx = adata.img_startx + ((framecount.count // adata.frame_rate) % adata.ani_num) * cdata.sizew
                self.srcy = adata.img_starty + cdata.direction * cdata.sizeh
            adata.srcrect = SDL_Rect(self.srcx, self.srcy, adata.sizew, adata.sizeh)



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
