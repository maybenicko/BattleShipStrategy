from GameCreation.random_but_next import CreateGameRandomBut
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors


class TargetedStrategy:
    def __init__(self):
        bot = CreateGameRandomBut()
        self.hit = []
        self.misses = []
        data = bot.board_grid()
        self.randomly_grid = data[0]
        self.ship_loc = data[1]
        self.ship_loc_human = {
            'Carrier': [],
            'Battleship': [],
            'Cruiser': [],
            'Submarine': [],
            'Destroyer': []
        }
        self.player_grid = pd.DataFrame(' ', index=range(1, 11), columns=range(1, 11))
        self.x = None
        self.y = None

    def normalize(self):
        names = ['Carrier', 'Battleship', 'Cruiser', 'Submarine', 'Destroyer']
        for i, key in enumerate(names, start=1):
            if i in self.ship_loc:
                self.ship_loc_human[key] = self.ship_loc[i][0]

    def check_sunk(self):
        for ship, coord_list in self.ship_loc_human.items():
            if all(coord in self.hit for coord in coord_list):
                print(f'{ship.upper()} HAS BEEN SUNK.')
                for coord in coord_list:
                    self.hit.remove(coord)

    def show_plot(self, turn):
        # fix the fucking colors them ain't working
        mapping = {' ': 0, '[]': 1, '-': 2}
        grid_numeric = self.player_grid.applymap(lambda x: mapping.get(x, 0))
        cmap = colors.ListedColormap(['white', 'blue', 'lightgrey'])

        plt.figure(figsize=(8, 8))
        ax = sns.heatmap(
            grid_numeric,
            cmap=cmap,
            linewidths=0.5,
            linecolor='black',
            cbar=False,
            square=True
        )

        ax.set_xticklabels(range(1, 11), fontsize=12)
        ax.set_yticklabels(range(1, 11), fontsize=12)
        plt.title(f"Battleship Board - Turn {turn}", fontsize=16)
        plt.xlabel("Columns", fontsize=14)
        plt.ylabel("Rows", fontsize=14)

        plt.show()

    def ask_coordinates(self):
        user_input = input("Enter your move as 'row,column' (x,y): ").strip()

        row, column = map(int, user_input.split(','))
        if 1 <= row <= 10 and 1 <= column <= 10:
            self.x = row
            self.y = column
            return True
        else:
            print(f'"{(self.x, self.y)}" invalid coordinate.')
            return False

    def main(self):
        print(self.randomly_grid)
        turn = 0
        self.normalize()
        while len(self.hit) != 17:

            if not self.ask_coordinates():
                continue

            # check players grid
            if not self.player_grid.loc[self.x, self.y] == ' ':
                print(f'({(self.x, self.y)}) has already been shot.')
                continue

            if self.randomly_grid.loc[self.x, self.y] == 'x':
                self.player_grid.at[self.x, self.y] = '[]'
                self.hit.append((self.x, self.y))
                print(f'HIT {self.x, self.y}!')
                self.check_sunk()
            else:
                self.player_grid.at[self.x, self.y] = '-'
                self.misses.append((self.x, self.y))
                print(f'MISS {self.x, self.y}!')

            turn += 1
            self.show_plot(turn)

        return print(f'Total moves: {len(self.misses) + 17}. Accuracy: {17 / len(self.misses) + 17}.')
