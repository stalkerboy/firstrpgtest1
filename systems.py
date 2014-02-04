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
        self.renderer.clear(sdl2ext.Color(100, 100, 100))
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

    def process(self, world, components):
        for sdata in components:
            if sdata.type == 'FOREGROUND':
                sdl2.render.SDL_RenderCopy(self.renderer.renderer, sdata.sprite.texture, sdata.srcrect, None)


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
            elif cdata.state == 1 and not self._overlap(cdata.name):
                # temp_posx, temp_posy = cdata.posx + cdata.vx, cdata.posy + cdata.vy
                cdata.posx += cdata.vx
                cdata.posy += cdata.vy

                # cdata.posx = max(self.minx, cdata.posx)
                # cdata.posy = max(self.miny, cdata.posy)

                # pmaxx = cdata.posx + cdata.sizew
                # pmaxy = cdata.posy + cdata.sizeh
                # if pmaxx > self.maxx:
                #     cdata.posx = self.maxx - cdata.sizew
                # if pmaxy > self.maxy:
                #     cdata.posy = self.maxy - cdata.sizeh

    def _overlap(self, cname):
        left, top, right, bottom = self.mapdata[cname]
        for name, area in self.mapdata.items():
            mdleft, mdtop, mdright, mdbottom = area
            if cname == name:
                continue
            elif left < mdright and right > mdleft and top < mdbottom and bottom > mdtop:
                return True
        return False


        # left, top, right, bottom = sprite.area
        # bleft, btop, bright, bbottom = self.ball.sprite.area

        # return bleft < right and bright > left and \
        #     btop < bottom and bbottom > top


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


class CollisionSystem(Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = (Velocity, sdl2ext.Sprite)
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        sprite = item[1]
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return bleft < right and bright > left and \
            btop < bottom and bbottom > top

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if len(collitems) != 0:
            self.ball.velocity.vx = -self.ball.velocity.vx

            sprite = collitems[0][1]
            ballcentery = self.ball.sprite.y + \
                self.ball.sprite.size[1] // 2
            halfheight = sprite.size[1] // 2
            stepsize = halfheight // 10
            degrees = 0.7
            paddlecentery = sprite.y + halfheight
            if ballcentery < paddlecentery:
                factor = (paddlecentery - ballcentery) // stepsize
                self.ball.velocity.vy = -int(round(factor * degrees))
            elif ballcentery > paddlecentery:
                factor = (ballcentery - paddlecentery) // stepsize
                self.ball.velocity.vy = int(round(factor * degrees))
            else:
                self.ball.velocity.vy = -self.ball.velocity.vy

        if self.ball.sprite.y <= self.miny or \
                self.ball.sprite.y + self.ball.sprite.size[1] >= self.maxy:
            self.ball.velocity.vy = -self.ball.velocity.vy

        if self.ball.sprite.x <= self.minx or \
                self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxx:
            self.ball.velocity.vx = -self.ball.velocity.vx