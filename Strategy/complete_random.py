from GameCreation.random_but_next import CreateGameRandomBut
import pandas as pd
import random


class TargetedStrategy:
    def __init__(self):
        bot = CreateGameRandomBut()
        self.hit = []
        self.misses = []
        self.randomly_grid = bot.board_grid()[0]
        self.player_grid = pd.DataFrame(' ', index=range(1, 11), columns=range(1, 11))

    def main(self):
        while len(self.hit) != 17:
            x = random.choice(self.player_grid.index)
            y = random.choice(self.player_grid.columns)
            # check players grid
            if not self.player_grid.loc[x, y] == ' ':
                continue
            if self.randomly_grid.loc[x, y] == 'x':
                self.player_grid.at[x, y] = '[]'
                self.hit.append((x, y))
                continue
            self.player_grid.at[x, y] = '-'
            self.misses.append((x, y))
        return len(self.misses) + 17
