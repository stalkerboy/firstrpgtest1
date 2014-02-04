from sdl2.rect import SDL_Rect


class CharactorData:
    def __init__(self, name, pos=(0, 0), size=(32,32), state=0, direction=0, velocity=(0, 0), type='NPC', is_subject=False):
        self.name = name

        self.posx, self.posy = pos
        self.sizew, self.sizeh = size
        self.state = state
        self.direction = direction
        self.vx, self.vy = velocity
        self.type = type
        self.is_subject = is_subject


class SpriteData:
    def __init__(self, sprite, ani_count, frame_rate=20, img_startpos=(0, 0), type='SPRITE'):

        self.srcrect = SDL_Rect()

        self.sprite = sprite
        self.ani_count = ani_count
        self.frame_rate = frame_rate
        self.img_startx, self.img_starty = img_startpos

        self.type = type
        self.viewrect = SDL_Rect()


class FrameCount:
    def __init__(self):
        self.count = 0
