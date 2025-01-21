from GameCreation.random_but_next import CreateGameRandomBut
from ShipHit.hit_logic import check_hit
import pandas as pd


class TargetedStrategy:
    def __init__(self):
        self.hit = []
        self.shots = []
        bot = CreateGameRandomBut()
        self.randomly_grid = bot.board_grid()[0]
        self.player_grid = pd.DataFrame(' ', index=range(1, 11), columns=range(1, 11))
        self.boats = [2, 3, 3, 4, 5]
        self.offsets = [(1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (1, 3), (1, 3), (2, 1), (3, 2)]

    def main(self):
        for x_offset, y_offset in self.offsets:
            if len(self.hit) == 17:
                break

            for x in range(x_offset, 11, 3):
                for y in range(y_offset, 11, 3):
                    if self.player_grid.at[x, y] == ' ':
                        self.player_grid = check_hit(self.randomly_grid, self.player_grid, x, y, self.hit, self.shots)
                        if len(self.hit) >= 17:
                            break
        return len(set(self.shots))
