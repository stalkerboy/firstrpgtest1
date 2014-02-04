from sdl2.ext.ebs import World, Entity
from dataformat import CharactorData, FrameCount, SpriteData


class FirstWorld(World):
    def __init__(self) :
        super().__init__()

    def process(self):
        super().process()


class Player(Entity):
    def __init__(self, world, sprite, ani_count, img_startpos, pos, size, name):
        self.spritedata = SpriteData(sprite=sprite, ani_count=ani_count, img_startpos=img_startpos)
        self.charactordata = CharactorData(name=name, pos=pos, size=size, is_subject=True)
        self.framecount = FrameCount()


class NPCPlayer(Entity):
    def __init__(self, world, sprite, ani_count, img_startpos, pos, size, name):
        self.spritedata = SpriteData(sprite=sprite, ani_count=ani_count, img_startpos=img_startpos)
        self.charactordata = CharactorData(name=name, pos=pos, size=size, state=1, velocity=(1, 0))
        self.charactordata.direction = 2
        self.framecount = FrameCount()
