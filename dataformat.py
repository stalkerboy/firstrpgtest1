from sdl2.rect import SDL_Rect


class CharactorData:
    def __init__(self, ai=False, pos=(0, 0), size=(32,32), state=0, direction=0, velocity=(0, 0)):
        self.ai = ai
        self.posx, self.posy = pos
        self.sizew, self.sizeh = size
        self.state = state
        self.direction = direction
        self.vx, self.vy = velocity


class SpriteData:
    def __init__(self, sprite, ani_count, frame_rate=20, img_startpos=(0, 0)):
        self.sprite = sprite

        self.frame_rate = frame_rate
        self.ani_count = ani_count
        self.srcrect = SDL_Rect()
        self.img_startx, self.img_starty = img_startpos


class ViewRect:
    def __init__(self, is_subject=False):
        self.rect = SDL_Rect(0, 0, 640, 480)
        self.is_subject = is_subject


class FrameCount:
    def __init__(self):
        self.count = 0
