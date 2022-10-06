# Tyler Burkhardt tjb6ha

import gamebox
import pygame
import random

camera = gamebox.Camera(800, 600)
cameraspeed = 3
cameratop = 0

dead = False

playerscore = 0
playerspeed = 10
player = gamebox.from_color(400, 25, "green", 40, 40)

scoreypos = 575

floorypos = 200
floorcount = 0
floors = [gamebox.from_color(random.randrange(-400, 350), floorypos, "black", 800, 20)]
floorsR = [gamebox.from_color(floors[0].x + 900, floorypos, "black", 800, 20)]


def tick(keys):
    global dead

    if not dead:
        # globals
        global playerscore
        global playerspeed
        global floorypos
        global scoreypos
        global cameratop
        global floorcount

        # floor
        for floor in floors:
            if floorypos < 600 + cameratop:
                floorypos += 150
                floors.append(gamebox.from_color(random.randrange(-400, 350), floorypos, "black", 800, 20))
                floorcount += 1
                floorsR.append(gamebox.from_color(floors[floorcount].x + 900, floorypos, "black", 800, 20))


        # score
        playerscore += 0.05
        score = gamebox.from_text(25, scoreypos, str(int(playerscore)), 40, "red")
        scoreypos += cameraspeed

        # controls and boundaries
        if pygame.K_LEFT in keys:
            player.x -= playerspeed
        if pygame.K_RIGHT in keys:
            player.x += playerspeed

        if player.x < 0:
            player.x = 0
        if player.x > 800:
            player.x = 800
        if player.y > 600 + cameratop:
            player.speedy = 0

        # gravity
        player.speedy += 0.75
        player.move_speed()

        # player touching platform
        for floor in floors:
            player.move_to_stop_overlapping(floor)
        for floor in floorsR:
            player.move_to_stop_overlapping(floor)

        # camera
        camera.clear("white")
        camera.draw(score)
        camera.draw(player)
        camera.y += cameraspeed
        for floor in floors:
            camera.draw(floor)
        for floor in floorsR:
            camera.draw(floor)

        # check if dead
        cameratop += cameraspeed
        if player.bottom < cameratop:
            dead = True

    else:
        camera.draw(gamebox.from_text(400, 250 + cameratop, "Game Over", 100, "red"))

    camera.display()


gamebox.timer_loop(30, tick)
