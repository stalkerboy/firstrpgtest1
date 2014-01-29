from sdl2.ext.ebs import World, Entity
from dataformat import CharactorData, FrameCount, ViewRect, SpriteData


class FirstWorld(World):
    def __init__(self) :
        super().__init__()

    def process(self):
        super().process()


class Player(Entity):
    def __init__(self, world, sprite, ani_count, img_startpos, pos, size):
        self.spritedata = SpriteData(sprite=sprite, ani_count=ani_count, img_startpos=img_startpos)
        self.charactordata = CharactorData(pos=pos, size=size)
        self.framecount = FrameCount()
        self.viewrect = ViewRect(is_subject=True)


class NPCPlayer(Entity):
    def __init__(self, world, sprite, ani_count, img_startpos, pos, size):
        self.spritedata = SpriteData(sprite=sprite, ani_count=ani_count, img_startpos=img_startpos)
        self.charactordata = CharactorData(pos=pos, size=size, ai=True, state=1, velocity=(1, 0))
        self.charactordata.direction = 2
        self.framecount = FrameCount()
        self.viewrect = ViewRect()
