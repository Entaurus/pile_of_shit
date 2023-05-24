import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1200, 760))
pygame.display.set_caption("test")
icon = pygame.image.load("slime-forward1.png")
pygame.display.set_icon(icon)

#Код с анимациями передвижения
bg = pygame.image.load("bg.png").convert()

walk_right = [
    pygame.image.load("slime-forward1.png").convert_alpha(),
    pygame.image.load("slime-forward2.png").convert_alpha(),
    pygame.image.load("slime-forward3.png").convert_alpha(),
    pygame.image.load("slime-forward4.png").convert_alpha(),
    pygame.image.load("slime-forward5.png").convert_alpha(),
]

walk_left = [
    pygame.image.load("slime-backward1.png").convert_alpha(),
    pygame.image.load("slime-backward2.png").convert_alpha(),
    pygame.image.load("slime-backward3.png").convert_alpha(),
    pygame.image.load("slime-backward4.png").convert_alpha(),
    pygame.image.load("slime-backward5.png").convert_alpha(),
]

jump_anim = [
    pygame.image.load("slime-jump1.png").convert_alpha(),
    pygame.image.load("slime-jump2.png").convert_alpha(),
    pygame.image.load("slime-jump3.png").convert_alpha(),
    pygame.image.load("slime-jump4.png").convert_alpha(),
    pygame.image.load("slime-jump5.png").convert_alpha(),
]

#Код с интерфейсом жизней
lives_left = [
    pygame.image.load("lives0.png").convert_alpha(),
    pygame.image.load("lives1.png").convert_alpha(),
    pygame.image.load("lives2.png").convert_alpha(),
    pygame.image.load("lives3.png").convert_alpha(),
]

#Код с анимациями подбираемых сердчек хп
blobs_anim = [
    pygame.image.load("blobs1.png").convert_alpha(),
    pygame.image.load("blobs2.png").convert_alpha(),
    pygame.image.load("blobs3.png").convert_alpha(),
]


enemy = pygame.image.load("enemy-sprite.png").convert_alpha()

#массивы мусора который мы накидываем на экран
enemy_list_in_game = []
blobs_list_in_game = []

#счетчики для кадров анимаций
player_anim_count = 0
blobs_anim_count = 0
bg_x = 0

#скорость и перемещение игрока
player_speed = 17
player_x = 150
player_y = 500
lives = 3

#прыжки
is_jump = False
jump_count = 12

miliseconds_until_spawn = 2000
miliseconds_until_lives = 5000

#спавним роботов
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, miliseconds_until_spawn)

#спавним блобов
blobs_timer = pygame.USEREVENT + 3
pygame.time.set_timer(blobs_timer, miliseconds_until_lives)

invulnerability_timer = pygame.USEREVENT + 2
pygame.time.set_timer(invulnerability_timer, 2000)

#счет чтобы у наших стараний был смысл
score = 0
score_increment = 3

#Текстовая фигня
label = pygame.font.Font('Roboto.ttf', 40)
lose_label = label.render('Game over!', False, (139, 219, 127))
restart_label = label.render('Try again?', False, (139, 219, 127))
restart_label_rect = restart_label.get_rect(topleft = (500, 300))
rules_label = label.render('Press LEFT and RIGHT arrows to move. Press SPACE to jump.', False, (139, 219, 127))
win_label = label.render('You won!', False, (139, 219, 127))
ready_label = label.render('Press here to start!', False, (139, 219, 127))
ready_label_rect = restart_label.get_rect(topleft = (425, 300))

last_update = 0  # since you are just starting the program there is no time that was past.

#геймплей = игра, running = само окно игры и цикл
gameplay = False
ready = False
win = False
invulnerability = False
running = True
while running:

    IMAGE_INTERVAL = 100  # This is the amount of miliseconds that will represent the time to change the picture.
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    
    screen.blit(bg,(bg_x,0))
    screen.blit(bg,(bg_x + 1200,0))
    
    if gameplay and ready:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        score += 1

        if enemy_list_in_game:
            for (i, el) in enumerate (enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 8

                if el.x <= -10:
                    enemy_list_in_game.pop(i)

                if player_rect.colliderect(el) and invulnerability == False:
                    lives -= 1
                    invulnerability = True
                    enemy_list_in_game.pop(i)

        if blobs_list_in_game:
            for (i, el) in enumerate (blobs_list_in_game):
                screen.blit(blobs_anim[blobs_anim_count], el)
                el.x -= 8

                if el.x <= -10:
                    blobs_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    invulnerability = True
                    blobs_list_in_game.pop(i)
                    if lives < 3:
                        lives += 1
                    else:
                        score += 1000

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if invulnerability:
                walk_left[player_anim_count].set_alpha(100) 
            else:
                walk_left[player_anim_count].set_alpha(255) 
            screen.blit(walk_left[player_anim_count],(player_x,player_y))
        elif is_jump == True:
            if invulnerability:
                jump_anim[player_anim_count].set_alpha(100) 
            else:
                jump_anim[player_anim_count].set_alpha(255) 
            screen.blit(jump_anim[player_anim_count],(player_x,player_y))
        else:
            if invulnerability:
                walk_right[player_anim_count].set_alpha(100) 
            else:
                walk_right[player_anim_count].set_alpha(255) 
            screen.blit(walk_right[player_anim_count],(player_x,player_y))


        if keys[pygame.K_LEFT] and player_x > 25:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x <600:
            player_x += player_speed
        
        if lives == 0:
            gameplay = False
    
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -12:
                if jump_count >0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 12

        if player_anim_count == 4:
            player_anim_count = 0
        else:
            if pygame.time.get_ticks() - last_update > IMAGE_INTERVAL:    
                player_anim_count += 1
                last_update = pygame.time.get_ticks()

        if blobs_anim_count == 2:
            blobs_anim_count = 0
        else:
            if pygame.time.get_ticks() - last_update > IMAGE_INTERVAL:
                blobs_anim_count +=1
                last_update = pygame.time.get_ticks()

        bg_x -= 8
        if bg_x <= -1200:
            bg_x = 0

        #Интерфейс
        score_label = label.render(f'Score: {score}', True, (139, 219, 127))
        screen.blit(score_label, (10,10))
        screen.blit(lives_left[lives], (900, 20))

        if score >= 10000:
            win = True
            gameplay = False

    elif ready == False:
        screen.fill((21, 17, 39))
        screen.blit(rules_label, (45, 200))
        screen.blit(ready_label, ready_label_rect)
        if ready_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            ready = True
            gameplay = True    
    elif score < 10000:
        screen.fill((21, 17, 39))
        screen.blit(lose_label, (500, 200))
        screen.blit(restart_label, restart_label_rect)
        score_label = label.render(f'Score: {score}', True, (139, 219, 127))
        screen.blit(score_label, (500,400))

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            win = False
            gameplay = True
            player_x = 150
            enemy_list_in_game.clear()
            score = 0
            lives = 3

    elif win == True:
            gameplay = False
            screen.fill((21, 17, 39))
            screen.blit(win_label, (500, 200))
            screen.blit(ready_label, ready_label_rect)
            if ready_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                win = False
                ready = True
                gameplay = True   
                player_x = 150
                enemy_list_in_game.clear()
                score = 0
                live = 3
        
    pygame.display.update()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(1202, 571)))
            pygame.time.set_timer(enemy_timer, miliseconds_until_spawn)
            miliseconds_until_spawn = random.randint(1000,5000)
        if event.type == blobs_timer:
            blobs_list_in_game.append(blobs_anim[blobs_anim_count].get_rect(topleft=(1202, 638)))
            pygame.time.set_timer(blobs_timer, miliseconds_until_lives)
            miliseconds_until_lives = random.randint(10000,30000)
        if event.type == invulnerability_timer:
            invulnerability = False
 
pygame.quit()