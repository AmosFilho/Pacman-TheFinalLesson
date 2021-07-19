import pygame
from Models.utils import Utils

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - Utils.TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - Utils.TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        self.on_coin()

    def draw(self):
        pygame.draw.circle(self.app.screen, Utils.PLAYER_COLOUR, (int(self.pix_pos.x),
                                                                  int(self.pix_pos.y)), self.app.cell_width // 2 - 2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, Utils.PLAYER_COLOUR, (30 + 20 * x, Utils.HEIGHT - 15), 7)

    def on_coin(self):
        for coin in self.app.coins:
            if self.grid_pos == coin.pos:
                if int(self.pix_pos.x + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                    if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                        self.eat_coin(coin)
                        return
                if int(self.pix_pos.y + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                    if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                        self.eat_coin(coin)
                        return

    def eat_coin(self, coin):
        self.current_score += 1
        self.app.coins.remove(coin)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + Utils.TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   Utils.TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        if int(self.pix_pos.x + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
