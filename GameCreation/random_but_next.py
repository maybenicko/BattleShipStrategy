import random
import pandas as pd


class CreateGameRandomBut:
    def __init__(self):
        self.grid = pd.DataFrame('-', index=range(1, 11), columns=range(1, 11))
        self.boats = [5, 4, 3, 3, 2]
        self.ship_loc = {}

    # boat placing function
    def place_boat(self, x_og, y_og, orientation, ship_og, n):
        coordinates = []

        x = x_og
        y = y_og
        ship = ship_og

        if orientation == 'H':
            if not 10 - y >= ship:
                return False

            # select what horizontal space to check
            if y != 1 and y != 10 and y != 9:
                ship += 2
                y -= 1
            elif y == 1:
                ship += 1
            elif y == 9:
                ship += 1
                y -= 1
            elif y == 10:
                return False

            # vertical conditions
            if x == 1:
                locs = [0, 1]
            elif x == 10:
                locs = [-1, 0]
            else:
                locs = [-1, 0, 1]

            for loc in locs:
                for i in range(ship):
                    # check if there is enough horizontal space
                    if self.grid.loc[x + loc, y + i] == 'x':
                        return False

            for i in range(ship_og):
                self.grid.at[x_og, y_og + i] = 'x'
                coordinates.append((x_og, y_og + i))
            self.ship_loc[n] = self.ship_loc.get(n, []) + [coordinates]
            return True

        if orientation == 'V':
            if not 10 - x >= ship:
                return False

            # select what vertical space to check
            if x != 1 and x != 10 and x != 9:
                ship += 2
                x -= 1
            elif x == 1:
                ship += 1
            elif x == 9:
                ship += 1
                x -= 1
            elif x == 10:
                return False

            # horizontal conditions
            if y == 1:
                locs = [0, 1]
            elif y == 10:
                locs = [-1, 0]
            else:
                locs = [-1, 0, 1]

            for loc in locs:
                for i in range(ship):
                    # check if there is enough vertical space
                    if self.grid.loc[x + i, y + loc] == 'x':
                        return False

            for i in range(ship_og):
                self.grid.at[x_og + i, y_og] = 'x'
                coordinates.append((x_og + i, y_og))
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
