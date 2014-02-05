
import sys

try:
    import sdl2.events
    from assets import Assets
    from systems import MappingSystem, PlayerSystem, NPCSystem, FrameCountSystem, RenderSystem, ViewSystem, BackgroundSystem, ForegroundSystem
    from firstworld import FirstWorld, Player, NPCPlayer, Background

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
    mapping_system = MappingSystem()

    render_system = RenderSystem(renderer)
    view_system = ViewSystem()
    background_system = BackgroundSystem(renderer)
    foreground_system = ForegroundSystem(renderer)

    world.add_system(framecount_system)
    world.add_system(player_system)
    world.add_system(npc_system)
    world.add_system(mapping_system)

    world.add_system(view_system)
    world.add_system(background_system)
    world.add_system(render_system)
    world.add_system(foreground_system)

    user = Player(world, assets.charactor, ani_count=3, img_startpos=(0, 0), size=(32,32), pos=(100, 100), name='player')
    npc1 = NPCPlayer(world, assets.npc1, ani_count=3, img_startpos=(0, 0), size=(32,32), pos=(200, 200), name='npc1')
    npc2 = NPCPlayer(world, assets.npc1, ani_count=3, img_startpos=(32*3, 32*4), size=(32,32), pos=(300, 300), name='npc2')
    monster = NPCPlayer(world, assets.monster, ani_count=3, img_startpos=(0, 32*4), size=(32,32), pos=(50, 50), name='npc3')
    desert = Background(world, assets.desert1)

    npc1.spritedata.frame_rate = 5
    npc2.spritedata.frame_rate = 35
    monster.spritedata.frame_rate = 65

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
