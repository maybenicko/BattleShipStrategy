import pandas as pd
from GameCreation.random_but_next import CreateGameRandomBut


class TargetedStrategy:
    def __init__(self):
        self.random_grid = CreateGameRandomBut().board_grid()[0]
        self.prob_grid = pd.DataFrame(0, index=range(1, 11), columns=range(1, 11))
        self.hit_grid = pd.DataFrame(0, index=range(1, 11), columns=range(1, 11))
        self.miss_grid = pd.DataFrame(0, index=range(1, 11), columns=range(1, 11))
        self.ships = [5, 4, 3, 3, 2]

    def loc_prob(self, ship):
        probabilities = []

        # Check rows
        for x in range(1, 11):
            for start_y in range(1, 12 - ship):
                # possible ship placement
                segment_y = range(start_y, start_y + ship)
                hits = []
                empty_cell = 0

                for y in segment_y:
                    if self.miss_grid.loc[x, y] == 0:
                        if self.hit_grid.loc[x, y] == 1:
                            hits.append(y)
                        empty_cell += 1

                # calculation of probabilities and appending them in the prob_matrix
                if empty_cell == ship:
                    prob_matrix = pd.DataFrame(0.0, index=range(1, 11), columns=range(1, 11))
                    if hits:
                        multiplier = 4 * len(hits)
                    else:
                        multiplier = 1
                    for y in segment_y:
                        if y not in hits:
                            prob_matrix.at[x, y] = float(ship) * multiplier
                        else:
                            prob_matrix.at[x, y] = 0
                    probabilities.append(prob_matrix)

        # Check columns
        for y in range(1, 11):
            for start_x in range(1, 12 - ship):
                segment_x = range(start_x, start_x + ship)
                hits = []
                empty_cell = 0

                for x in segment_x:
                    if self.miss_grid.loc[x, y] == 0:
                        if self.hit_grid.loc[x, y] == 1:
                            hits.append(x)
                        empty_cell += 1

                if empty_cell == ship:
                    prob_matrix = pd.DataFrame(0.0, index=range(1, 11), columns=range(1, 11))
                    if hits:
                        multiplier = 4 * len(hits)
                    else:
                        multiplier = 1
                    for x in segment_x:
                        if x not in hits:
                            prob_matrix.at[x, y] = float(ship) * multiplier
                        else:
                            prob_matrix.at[x, y] = 0
                    probabilities.append(prob_matrix)

        total_prob_matrix = pd.DataFrame(0, index=range(1, 11), columns=range(1, 11))
        for prob_matrix in probabilities:
            total_prob_matrix += prob_matrix
        return total_prob_matrix

    def get_prob(self):
        total_prob = pd.DataFrame(0, index=range(1, 11), columns=range(1, 11))
        for ship in self.ships:
            total_prob += self.loc_prob(ship)
        return total_prob

    def get_target(self):
        target = self.prob_grid.stack().idxmax()
        return target

    def turn(self, turn_count, hits):
        if hits >= 17 or turn_count >= 100:
            return turn_count

        self.prob_grid = self.get_prob()
        x, y = self.get_target()

        if self.random_grid.loc[x, y] == 'x':
            hits += 1
            self.hit_grid.at[x, y] = 1
            self.prob_grid.at[x, y] = 0
        else:
            self.miss_grid.at[x, y] = 2

        return self.turn(turn_count + 1, hits)

    def main(self):
        total_moves = self.turn(0, 0)
        return total_moves
