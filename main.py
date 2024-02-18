import pygame
import sys
import random
import json
import os

pygame.init()

window_width = 800
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))
screen_colour = (0, 0, 0)

highest_score = 0

savedata = {'highest_score': 0}


def create_data_json():
    data = {"highest_score": 0}

    with open('data/data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def load_data():
    if os.path.exists('data/data.json'):
        with open('data/data.json', 'r') as json_file:
            return json.load(json_file)
    else:
        create_data_json()
        return {"highest_score": 0}


def update_data(e_data, score):
    e_data["highest_score"] = score
    save_data(e_data)


def save_data(data):
    with open('data/data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def draw_text(text, x, y, colour, size):
    font = pygame.font.SysFont("Comic Sans MS", size, bold=True)
    text_surface = font.render(text, False, colour)
    text_surface.get_size()
    screen.blit(text_surface, (x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/mario.png")
        self.size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (self.size[0] / 20, self.size[1] / 20))
        self.size = self.image.get_rect().size
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.points = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.size[0] / 2
        self.rect.y = pos[1] - self.size[1] / 2
        collision = pygame.sprite.spritecollide(self, coin_group, True)
        if collision:
            for coin in collision:
                if coin.which_coin == 'gold':
                    self.points += 1
                    for i in range(respawn_coins()):
                        coin = Coin('gold')
                        coin_group.add(coin)
                elif coin.which_coin == 'platinum':
                    self.points += 5


class Red_button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.restart = None
        self.window_open_time = pygame.time.get_ticks()
        self.orig_image = pygame.image.load("images/button.png")
        self.image = self.orig_image
        self.size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (self.size[0] / 9, self.size[1] / 9))
        self.size = self.image.get_rect().size
        self.rect = self.image.get_rect()
        self.rect.center = (400, 450)
        self.restart = False

    def update(self):
        if (self.rect.x < pygame.mouse.get_pos()[0] < self.rect.x + self.size[0]) and \
                self.rect.y < pygame.mouse.get_pos()[1] < self.rect.y + self.size[1]:
            old_pos = self.rect.center
            self.image = self.orig_image
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / 7, self.size[1] / 7))
            self.size = self.image.get_rect().size
            self.rect = self.image.get_rect()
            self.rect.center = old_pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.window_open_time = pygame.time.get_ticks()
                player.points = 0
                for sprite in coin_group:
                    sprite.kill()
                for i in range(2):
                    coin = Coin('gold')
                    coin_group.add(coin)
                self.restart = False

        else:
            old_pos = self.rect.center
            self.image = self.orig_image
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / 9, self.size[1] / 9))
            self.size = self.image.get_rect().size
            self.rect = self.image.get_rect()
            self.rect.center = old_pos


class Coin(pygame.sprite.Sprite):
    def __init__(self, which_coin):
        pygame.sprite.Sprite.__init__(self)
        self.which_coin = which_coin

        if self.which_coin == 'gold':
            self.scale = 10
            self.image = pygame.image.load("images/coin.png")
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / self.scale, self.size[1] / self.scale))
        elif self.which_coin == 'platinum':
            self.scale = 50
            self.image = pygame.image.load("images/platinum_coin.png")
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / self.scale, self.size[1] / self.scale))
        else:
            print("WRONG NAMING")
        self.size = self.image.get_rect().size
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(0, window_width - self.size[0]), random.randint(0, window_height - self.size[1]))
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        if self.which_coin == 'platinum' and pygame.time.get_ticks() - self.creation_time > 5000:
            self.kill()

        if self.scale > 5 and self.which_coin == "gold":
            self.scale -= 0.2
            self.grow()
        elif self.scale > 25 and self.which_coin == "platinum":
            self.scale -= 0.2
            self.grow()

    def grow(self):
        old_pos = self.rect.center
        if self.which_coin == 'gold':
            self.image = pygame.image.load("images/coin.png")
        else:
            self.image = pygame.image.load("images/platinum_coin.png")
        self.size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (self.size[0] / self.scale, self.size[1] / self.scale))
        self.rect = self.image.get_rect()
        self.rect.center = old_pos


player_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

for i in range(2):
    coin = Coin('gold')
    coin_group.add(coin)


def respawn_coins():
    return random.choice([1, 2])


player = Player()
player_group.add(player)

red_button = Red_button()
button_group.add(red_button)

last_time = 0
restart = False

existing_data = load_data()
highest_score = existing_data['highest_score']
while True:
    if pygame.time.get_ticks() - last_time > 5000:
        coin = Coin('platinum')
        coin_group.add(coin)
        last_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if player.points > highest_score:
                highest_score = player.points
            pygame.quit()
            sys.exit()

    if not red_button.restart:
        screen.fill(screen_colour)
        player_group.update()
        coin_group.update()
        timer = (16000 + red_button.window_open_time) - pygame.time.get_ticks()
        coin_group.draw(screen)
        player_group.draw(screen)
        draw_text(f"Points:{player.points}", 75, 80, (255, 255, 255), 35)
        draw_text(f"Timer:{int(timer / 1000)}", 550, 80, (255, 255, 255), 35)

        if player.points > highest_score:
            highest_score = player.points
            save_data(highest_score)
            update_data(existing_data, highest_score)
            existing_data["highest_score"] = highest_score

        if pygame.time.get_ticks() > 15000 + red_button.window_open_time:
            screen.fill(screen_colour)
            draw_text(f"Highest Score: {highest_score}", 250, 280, (255, 255, 255), 50)
            draw_text(f"Final Score: {player.points}", 250, 350, (255, 255, 255), 50)
            red_button.restart = True

    if red_button.restart:
        button_group.update()
        button_group.draw(screen)

    pygame.display.update()
