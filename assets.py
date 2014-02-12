from sdl2.ext.resources import Resources
import sdl2.ext as sdl2ext
from animation import Animation
HOUSERESOURCES = Resources(__file__, "resources/house")
PLAYER1RESOURCES = Resources(__file__, "resources/player1")
MAPRESOURCES = Resources(__file__, 'resources/map')
RESOURCES = Resources(__file__, 'resources')


class Assets:
    def __init__(self, factory):
        self.factory = factory

    def load_items(self):
        self.charactor = self.factory.from_image(RESOURCES.get_path("player1.png"))
        # self.npc1 = self.factory.from_color(sdl2ext.Color(255, 0, 0), size=(32, 32))
        self.npc1 = self.factory.from_image(RESOURCES.get_path("player2.png"))
        self.npc2 = self.factory.from_image(RESOURCES.get_path("monster.png"))

        self.house1 = self.factory.from_image(RESOURCES.get_path("house.png"))

        self.desert1 = self.factory.from_image(MAPRESOURCES.get_path('desert1.png'))

        # self.player1_ani_down = Animation(10, [self.factory.from_image(PLAYER1RESOURCES.get_path("player1_d0.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_d1.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_d2.png"))])

        # self.player1_ani_left = Animation(10, [self.factory.from_image(PLAYER1RESOURCES.get_path("player1_l0.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_l1.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_l2.png"))])

        # self.player1_ani_right = Animation(10, [self.factory.from_image(PLAYER1RESOURCES.get_path("player1_r0.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_r1.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_r2.png"))])

        # self.player1_ani_up = Animation(10, [self.factory.from_image(PLAYER1RESOURCES.get_path("player1_u0.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_u1.png")),
        #                                     self.factory.from_image(PLAYER1RESOURCES.get_path("player1_u2.png"))])
