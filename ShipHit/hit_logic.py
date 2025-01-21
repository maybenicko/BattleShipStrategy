from ShipHit.sniper_around import Sniper


def update_grid(player_grid, hit_data, hit, shots):
    # water [(2, 5), (3, 4), (2, 2), (2, 5)]
    miss_hits = hit_data[0]
    shots += miss_hits
    # hit [(2, 4), (2, 3)]
    boat_hits = hit_data[1]
    shots += boat_hits
    hit += boat_hits

    # writing the recorder shots
    if len(miss_hits) > 0:
        for miss in miss_hits:
            x, y = miss
            player_grid.at[x, y] = '-'

    for hit_point in boat_hits:
        player_grid.at[hit_point] = '[]'
    return player_grid


def check_hit(randomly_grid, player_grid, x, y, hit, shots):
    # check if we hit something
    if randomly_grid.loc[x, y] == 'x':
        player_grid.at[x, y] = '[]'
        # we introduce the hunting process
        bots = Sniper(randomly_grid, player_grid, x, y)
        hit_data = bots.snipe()
        player_grid = update_grid(player_grid, hit_data, hit, shots)
    else:
        player_grid.at[x, y] = '-'
        shots.append((x, y))

    return player_grid
