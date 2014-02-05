from sdl2.rect import SDL_Rect


class ObjectData:
    def __init__(self, id_, type, pos=(0, 0), size=(0,0)):
        self.id_ = id_
        self.posx, self.posy = pos
        self.sizew, self.sizeh = size
        self.type = type


class CharactorData(ObjectData):
    def __init__(self, id_, type, pos=(0, 0), size=(0,0), state=0, direction=0, velocity=(0, 0)):
        super().__init__(id_, type, pos, size)
        self.state = state
        self.direction = direction
        self.vx, self.vy = velocity


class SpriteData:
    def __init__(self, sprite, type, img_startpos=(0, 0), size=(0, 0)):

        self.srcrect = SDL_Rect()
        self.sprite = sprite
        self.img_startx, self.img_starty = img_startpos
        self.sizew, self.sizeh = size

        self.type = type
        self.viewrect = SDL_Rect()


class AnimationData(SpriteData):
    def __init__(self, sprite, type, img_startpos=(0, 0), size=(0, 0), ani_num=1, frame_rate=20, is_subject=False):
        super().__init__(sprite=sprite, type=type, img_startpos=img_startpos, size=size)
        self.ani_num = ani_num
        self.frame_rate = frame_rate

        self.is_subject = is_subject


class FrameCount:
    def __init__(self):
        self.count = 0
