

class Sniper:
    def __init__(self, randomly_grid, player_grid, x, y):
        self.randomly_grid = randomly_grid
        self.player_grid = player_grid
        self.x = x
        self.y = y
        self.water_hit = []
        self.boat_hit = []
        self.visited = set()

    def sink_boat(self):
        # the flow makes the function shoot first at its right and then left until it hits the water
        x, y = self.boat_hit[0]
        x_new, y_new = self.boat_hit[1]

        # if it's a horizontal position
        if x == x_new:
            n = 1
            while True:
                y_min = min(y, y_new)
                if 1 <= y_min - n <= 10:
                    if not self.player_grid.loc[x, y_min - n] == ' ':
                        n += 1
                        continue
                    if not self.randomly_grid.loc[x, y_min - n] == 'x':
                        self.water_hit.append((x, y_min - n))
                        break
                    self.boat_hit.append((x, y_min - n))
                    n += 1
                    continue
                break

            n = 1
            while True:
                y_max = max(y, y_new)
                if 1 <= y_max + n <= 10:
                    if not self.player_grid.loc[x, y_max + n] == ' ':
                        n += 1
                        continue
                    if not self.randomly_grid.loc[x, y_max + n] == 'x':
                        self.water_hit.append((x, y_max + n))
                        break
                    self.boat_hit.append((x, y_max + n))
                    n += 1
                    continue
                break

        # if it's a vertical position
        elif y == y_new:
            n = 1
            while True:
                x_min = min(x, x_new)
                if 1 <= x_min - n <= 10:
                    if not self.player_grid.loc[x_min - n, y] == ' ':
                        n += 1
                        continue
                    if not self.randomly_grid.loc[x_min - n, y] == 'x':
                        self.water_hit.append((x_min - n, y))
                        break
                    self.boat_hit.append((x_min - n, y))
                    n += 1
                    continue
                break

            n = 1
            while True:
                x_max = max(x, x_new)
                if 1 <= x_max + n <= 10:
                    if not self.player_grid.loc[x_max + n, y] == ' ':
                        n += 1
                        continue
                    if not self.randomly_grid.loc[x_max + n, y] == 'x':
                        self.water_hit.append((x_max + n, y))
                        break
                    self.boat_hit.append((x_max + n, y))
                    n += 1
                    continue
                break
        return

    def snipe(self):
        self.boat_hit.append((self.x, self.y))
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # check all directions until we get a hit
        for dir_x, dir_y in directions:
            check_x = self.x + dir_x
            check_y = self.y + dir_y

            if 1 <= check_x <= 10 and 1 <= check_y <= 10:
                if not self.player_grid.loc[check_x, check_y] == ' ':
                    continue
                if self.randomly_grid.loc[check_x, check_y] == '-':
                    self.water_hit.append((check_x, check_y))
                    continue

                # hit recorder in boat_hit list
                self.boat_hit.append((check_x, check_y))
                # we try sinking the boat shooting on the same axis
                self.sink_boat()
                return self.water_hit, self.boat_hit
            continue
        return self.water_hit, self.boat_hit
