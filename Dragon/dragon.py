# Tyler Burkhardt tjb6ha

import gamebox
import pygame
import random

camera = gamebox.Camera(600, 600)
dragon_images = gamebox.load_sprite_sheet("dragon.png", 2, 1)
dragon = gamebox.from_image(300, 300, dragon_images[0])
enemy_list = [gamebox.from_image(0, random.randrange(25, 575), "enemy.png")]
dragon_speed = 10
fire_size = 20
fireball_list = [gamebox.from_color(650, 650, "red", fire_size, fire_size),
                 gamebox.from_color(650, 650, "orange", fire_size, fire_size),
                 gamebox.from_color(650, 650, "yellow", fire_size, fire_size),
                 gamebox.from_color(650, 650, "orange", fire_size, fire_size),
                 gamebox.from_color(650, 650, "red", fire_size, fire_size)]
dead = False
color = 0
count = 0


def tick(keys):
    global color
    global count
    global dead
    global enemy_list
    camera.clear("grey")
    dragon.image = dragon_images[0]

    if not dead:
        # controls
        if pygame.K_UP in keys:
            dragon.y -= dragon_speed
        if pygame.K_DOWN in keys:
            dragon.y += dragon_speed
        if pygame.K_LEFT in keys:
            dragon.x -= dragon_speed
        if pygame.K_RIGHT in keys:
            dragon.x += dragon_speed

        # shoot fireball
        if pygame.K_SPACE in keys:
            dragon.image = dragon_images[1]
            color += 1
            if color >= 5:
                color = 0
            fireball_list[color].speedx = -30
            fireball_list[color].x = dragon.x - 50
            fireball_list[color].y = dragon.y

        # boundaries
        if dragon.y < 0:
            dragon.y = 0
        if dragon.y > 600:
            dragon.y = 600
        if dragon.x < 0:
            dragon.x = 0
        if dragon.x > 600:
            dragon.x = 600

        # move and reset fireball
        for fireball in fireball_list:
            fireball.move_speed()
            if fireball.x <= -50:
                fireball.speedx = 0

        # creating enemies
        for enemy in enemy_list:
            enemy.speedx = 5 + (count/200)
            enemy.move_speed()
        if len(enemy_list) - 1 < int(count):
            enemy_list.append(gamebox.from_image(0, random.randrange(25, 575), "enemy.png"))

        # death
        for enemy in enemy_list:
            for fireball in fireball_list:
                if fireball.touches(enemy):
                    if enemy in enemy_list:
                        enemy_list.remove(enemy)
                if enemy.x > 615:
                    dead = True

        # camera
        for fireball in fireball_list:
            camera.draw(fireball)
        camera.draw(dragon)
        for enemy in enemy_list:
            camera.draw(enemy)
        camera.display()

        count += 0.05

    else:
        gameover = gamebox.from_text(300, 250, "Game Over", 50, "red")
        restart = gamebox.from_text(300, 350, "Press r to restart", 30, "red")
        camera.draw(gameover)
        camera.draw(restart)
        camera.display()
        if pygame.K_r in keys:
            dead = False
            enemy_list = [gamebox.from_image(0, random.randrange(25, 575), "enemy.png")]
            count = 0


gamebox.timer_loop(30, tick)
