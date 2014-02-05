from sdl2.ext.ebs import World, Entity
from dataformat import ObjectData, CharactorData, SpriteData, AnimationData, FrameCount


class FirstWorld(World):
    def __init__(self) :
        super().__init__()

    def process(self):
        super().process()


class Player(Entity):
    def __init__(self, world, id_, pos, obj_size, sprite, img_size, ani_num):
        self.charactordata = CharactorData(id_=id_, type='PLAYER', pos=pos, size=obj_size, state=1)
        self.animationdata = AnimationData(sprite=sprite, type='ANI', size=img_size, ani_num=ani_num, is_subject=True)
        self.framecount = FrameCount()


class NPC(Entity):
    def __init__(self, world, id_, pos, obj_size, sprite, img_size, ani_num, img_startpos=(0,0)):
        self.charactordata = CharactorData(id_=id_, type='NPC', pos=pos, size=obj_size, velocity=(1,0), direction=2)
        self.animationdata = AnimationData(sprite=sprite, type='ANI', size=img_size, ani_num=ani_num, img_startpos = img_startpos)
        self.framecount = FrameCount()


class Background(Entity):
    def __init__(self, world, id_, sprite, img_size):
        self.objectdata = ObjectData(id_=id_, type='BACK')
        self.spritedata = SpriteData(sprite=sprite, type="SPR", size=img_size)


class Foreground(Entity):
    def __init__(self, world, id_, pos, obj_size, sprite, img_size):
        self.objectdata = ObjectData(id_=id_, type='FORE', pos=pos, size=obj_size)
        self.spritedata = SpriteData(sprite=sprite, type="SPR", size=img_size)
