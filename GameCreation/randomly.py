import random
import pandas as pd


class CreateGameRandom:
    def __init__(self):
        self.grid = pd.DataFrame('-', index=range(1, 11), columns=range(1, 11))
        self.boats = [5, 4, 3, 3, 2]
        self.ship_loc = {}

    # boat placing function
    def place_boat(self, x, y, orientation, ship, n):
        coordinates = []

        if orientation == 'H':
            if not 10 - y + 1 >= ship:
                return False

            for i in range(ship):
                # check if there is enough horizontal space
                if self.grid.loc[x, y + i] == 'x':
                    return False
            for i in range(ship):
                self.grid.at[x, y + i] = 'x'
                coordinates.append((x, y + i))
            self.ship_loc[n] = self.ship_loc.get(n, []) + [coordinates]
            return True

        if orientation == 'V':
            if not 10 - x + 1 >= ship:
                return False

            for i in range(ship):
                # check if there is enough vertical space
                if self.grid.loc[x + i, y] == 'x':
                    return False
            for i in range(ship):
                self.grid.at[x + i, y] = 'x'
                coordinates.append((x + i, y))
            self.ship_loc[n] = self.ship_loc.get(n, []) + [coordinates]
            return True

    # board grid manager
    # x = access rows values
    # y = access column values
    def board_grid(self):
        i = 1
        for ship in self.boats:
            placed = False
            while not placed:
                x = random.choice(self.grid.index)
                y = random.choice(self.grid.columns)
                orientation = random.choice(['H', 'V'])

                if self.place_boat(x, y, orientation, ship, i):
                    i += 1
                    placed = True
        return self.grid, self.ship_loc
