
import sys

try:
    import sdl2.events
    from assets import Assets
    from systems import CollisionSystem, PlayerSystem, NPCSystem, FrameCountSystem, RenderSystem, ViewSystem, ViewReciveSystem, BackgroundSystem, ForegroundSystem
    from firstworld import FirstWorld, Player, NPC, Background

except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)


def fps_delay(fps, frames):
    """ fps_delay """
    frames = frames + 1
    ticks = sdl2.timer.SDL_GetTicks()

    # print('fps: {}'.format((frames / ticks) * 1000), end='\r')

    delay = frames / (fps / 1000) - ticks
    if delay < 0:
        delay = 1
    sdl2.timer.SDL_Delay(int(delay))

    return frames


def run():
    """ run """

    sdl2.ext.common.init()

    window = sdl2.ext.window.Window('', size=(640, 480))
    window.show()

    renderer = sdl2.ext.sprite.RenderContext(window)
    factory = sdl2.ext.sprite.SpriteFactory(sdl2.ext.sprite.TEXTURE, renderer=renderer)

    assets = Assets(factory)
    assets.load_items()

    world = FirstWorld()
    player_system = PlayerSystem()
    npc_system = NPCSystem(0, 0, 640, 480)
    framecount_system = FrameCountSystem()
    collision_system = CollisionSystem()

    viewrecive_system = ViewReciveSystem(640, 480)
    view_system = ViewSystem()

    render_system = RenderSystem(renderer)
    background_system = BackgroundSystem(renderer)
    foreground_system = ForegroundSystem(renderer)

    world.add_system(player_system)
    world.add_system(npc_system)
    world.add_system(collision_system)

    world.add_system(viewrecive_system)
    world.add_system(view_system)

    world.add_system(background_system)
    world.add_system(render_system)
    world.add_system(foreground_system)

    world.add_system(framecount_system)

    user = Player(world, id_='player1', pos=(100, 100), obj_size=(32,32), sprite=assets.charactor, img_size=(32,32), ani_num=3)
    npc1 = NPC(world, id_='npc1', pos=(200, 200), obj_size=(32,32), sprite=assets.npc1, img_size=(32,32), ani_num=3)
    npc2 = NPC(world, id_='npc2', pos=(300, 300), obj_size=(32,32), sprite=assets.npc2, img_size=(32,32), ani_num=3, img_startpos=(32*3, 32*4))
    npc3 = NPC(world, id_='npc3', pos=(50, 50), obj_size=(32,32), sprite=assets.npc1, img_size=(32,32), ani_num=3, img_startpos=(0, 32*4))
    desert = Background(world, 'desert', assets.desert1, (1280, 1280))

    npc1.animationdata.frame_rate = 5
    npc2.animationdata.frame_rate = 35
    npc3.animationdata.frame_rate = 65

    running = True
    while running:
        for event in sdl2.ext.common.get_events():
            if event.type == sdl2.events.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.events.SDL_KEYDOWN:
                user.charactordata.state = 1

                if event.key.keysym.sym == sdl2.keycode.SDLK_UP:
                    user.charactordata.vy = -10
                    user.charactordata.direction = 3
                elif event.key.keysym.sym == sdl2.keycode.SDLK_DOWN:
                    user.charactordata.vy = 10
                    user.charactordata.direction = 0
                elif event.key.keysym.sym == sdl2.keycode.SDLK_LEFT:
                    user.charactordata.vx = -10
                    user.charactordata.direction = 1
                elif event.key.keysym.sym == sdl2.keycode.SDLK_RIGHT:
                    user.charactordata.vx = 10
                    user.charactordata.direction = 2
            elif event.type == sdl2.events.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.keycode.SDLK_UP, sdl2.keycode.SDLK_DOWN, sdl2.keycode.SDLK_LEFT, sdl2.keycode.SDLK_RIGHT):
                    user.charactordata.vy = user.charactordata.vx = 0
                    user.charactordata.state = 0
        world.process()

    sdl2.ext.common.quit()


if __name__ == '__main__':
    run()
