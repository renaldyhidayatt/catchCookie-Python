import sys
import pygame
import os
import random
from Food import Food
from Player import Player


IMAGE_PATHS = {
    'gold': os.path.join(os.getcwd(), 'resources/images/gold.png'),
    'apple': os.path.join(os.getcwd(), 'resources/images/apple.png'),
    'background': os.path.join(os.getcwd(), 'resources/images/background.jpg'),
    'player': [os.path.join(os.getcwd(), 'resources/images/%d.png' % i) for i in range(1, 11)]
}

AUDIO_PATHS = {
    'bgm': os.path.join(os.getcwd(), 'resources/audios/bgm.mp3'),
    'get': os.path.join(os.getcwd(), 'resources/audios/get.wav'),
}

FONT_PATH = os.path.join(os.getcwd(), 'resources/font/font.TTF')

HIGHEST_SCORE_RECORD_FILEPATH = 'highest.rec'

SCREENSIZE = (800, 600)

BACKGROUND_COLOR = (0, 160, 233)

FPS = 30



def showEndInteface(screen, score, highest_score):
    font_big = pygame.font.Font(FONT_PATH, 60)
    font_small = pygame.font.Font(FONT_PATH, 40)
    text_title = font_big.render(F'Time is up!', True, (255,0,0))

    text_title_rect = text_title.get_rect()
    text_title_rect.centerx = screen.get_rect().centerx
    text_title_rect.centery = screen.get_rect().centery - 100
    text_score = font_small.render(f"Score: {score}, Highest Score: {highest_score}", True, (255, 0, 0))
    
    text_score_rect = text_score.get_rect()
    text_score_rect.centerx = screen.get_rect().centerx
    text_score_rect.centery = screen.get_rect().centery - 10
    text_tip = font_small.render(f"Enter Q to quit game or  R to restart it", True, (255, 0, 0))
    
    
    text_tip_rect = text_tip.get_rect()
    text_tip_rect.centerx = screen.get_rect().centerx
    text_tip_rect.centery = screen.get_rect().centery +60
    text_tip_count = 0
    text_tip_freq = 10
    text_tip_show_flag = True
    
    clock = pygame.time.Clock()

    while True:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_r:
                    return

        screen.blit(text_title, text_title_rect)
        screen.blit(text_score, text_score_rect)

        if text_tip_show_flag:
            screen.blit(text_tip, text_tip_rect)

        text_tip_count += 1
        
        if text_tip_count % text_tip_freq == 0:
            text_tip_count = 0
            text_tip_show_flag = not text_tip_show_flag
        pygame.display.flip()
        clock.tick(FPS)


def initGame():
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("catch coins")

    game_images = {}

    for key,value in IMAGE_PATHS.items():
        if isinstance(value, list):
            images = []
            for item in value: images.append(pygame.image.load(item))
            game_images[key] = images
        else:
            game_images[key] = pygame.image.load(value)

    game_sounds = {}

    for key,value in AUDIO_PATHS.items():
        if key == 'bgm': continue
        game_sounds[key] = pygame.mixer.Sound(value)

    return screen, game_images, game_sounds


def main():
    screen, game_images, game_sounds = initGame()

    pygame.mixer.music.load(AUDIO_PATHS['bgm'])
    pygame.mixer.music.play(-1, 0.0)

    font = pygame.font.Font(FONT_PATH, 40)

    player = Player(game_images['player'], position=(375, 520))

    food_sprites_group = pygame.sprite.Group()
    generate_food_freq = random.randint(10,20)
    generate_food_count = 0

    score = 0
    highest_score = 0 if not os.path.exists(HIGHEST_SCORE_RECORD_FILEPATH) else int(open(HIGHEST_SCORE_RECORD_FILEPATH).read())

    clock = pygame.time.Clock()
    

    while True:
        screen.fill(0)
        screen.blit(game_images['background'], (0,0)) 

        countdown_text = 'Count down: ' + str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str((90000- pygame.time.get_ticks()) // 1000 % 60).zfill(2)
        countdown_text = font.render(countdown_text, True, (0,0,0))
        countdown_rect = countdown_text.get_rect()
        countdown_rect.topright =  [SCREENSIZE[0]-30, 5]
        screen.blit(countdown_text, countdown_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            player.move(SCREENSIZE, 'left')
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            player.move(SCREENSIZE, 'right')

        
        generate_food_count += 1

        if generate_food_count > generate_food_freq:
            generate_food_freq = random.randint(10, 20)
            generate_food_count = 0
            food = Food(game_images, random.choice(['gold',] * 10 + ['apple']), SCREENSIZE)
            food_sprites_group.add(food)

        
        for food in food_sprites_group:
            if food.update(): food_sprites_group.remove(food)

        
        for food in food_sprites_group:
            if pygame.sprite.collide_mask(food, player):
                game_sounds['get'].play()
                food_sprites_group.remove(food)
                score += food.score
                if score > highest_score: highest_score = score

        player.draw(screen)


        food_sprites_group.draw(screen)


        score_text = f'Score: {score}, Highest: {highest_score}'
        score_text = font.render(score_text, True, (0,0,0))
        score_rect = score_text.get_rect()
        score_rect.topleft = [5, 5]
        screen.blit(score_text, score_rect)
        
        if pygame.time.get_ticks() >= 90000:
            break
        
        pygame.display.flip()
        clock.tick(FPS)
    
    fp = open(HIGHEST_SCORE_RECORD_FILEPATH, 'w')
    fp.write(str(highest_score))
    fp.close()
    return showEndInteface(screen, score, highest_score)



if __name__ == '__main__':
    while main():
        pass
        