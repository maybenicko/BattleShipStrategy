import time
from GameCreation.random_but_next import CreateGameRandomBut
from ShipHit.hit_logic import check_hit
import pandas as pd
import random


class TargetedStrategy:
    def __init__(self):
        bot = CreateGameRandomBut()
        self.randomly_grid = bot.board_grid()[0]
        self.hit = []
        self.shots = []
        self.player_grid = pd.DataFrame(' ', index=range(1, 11), columns=range(1, 11))

    def main(self):
        while len(self.hit) != 17:
            x = random.choice(self.player_grid.index)
            y = random.choice(self.player_grid.columns)
            # check players grid
            if self.player_grid.at[x, y] == ' ' and (x, y) not in self.shots:
                self.player_grid = check_hit(self.randomly_grid, self.player_grid, x, y, self.hit, self.shots)
        return len(set(self.shots))


