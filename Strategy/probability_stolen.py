from GameCreation.random_but_next import CreateGameRandomBut
import pandas as pd
import requests
import random


class TargetedStrategy:
    def __init__(self):
        bot = CreateGameRandomBut()
        data = bot.board_grid()
        self.best_starting_prob = [(5, 5), (5, 6), (6, 6), (6, 5)]
        self.next_shot = ()
        self.ship_loc = data[1]
        self.hits = []
        self.misses = []
        self.randomly_grid = data[0]
        self.player_grid = pd.DataFrame(' ', index=range(1, 11), columns=range(1, 11))
        self.sunk_ships = ['null', 'false', 'false', 'false', 'false', 'false']
        self.layout = [
            [],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def check_sunk_ships(self):
        for ship_length, ship_coords_list in self.ship_loc.items():
            for ship_coords in ship_coords_list:
                if all(coord in self.hits for coord in ship_coords):
                    self.ship_loc.pop(ship_length)
                    self.sunk_ships[ship_length] = 'true'
                    return ship_length
        return 6

    def get_probabilities(self, hit, coord):
        if hit:
            hit_shot = self.check_sunk_ships()
            self.layout[coord[0]][coord[1]] = hit_shot
        else:
            self.layout[coord[0]][coord[1]] = -1

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryjxKimBWj0srHXiSB",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        body = "------WebKitFormBoundaryjxKimBWj0srHXiSB\r\nContent-Disposition: form-data; name=\"layout\"\r\n\r\n" \
               + str(self.layout).replace(' ', '') + "\r\n------WebKitFormBoundaryjxKimBWj0srHXiSB\r\nContent-Dispo" \
               "sition: form-data; name=\"sunkShips\"\r\n\r\n" + str(self.sunk_ships).replace("'", "").replace(' ',
               '') + "\r\n------WebKitFormBoundaryjxKimBWj0srHXiSB\r\nContent-Disposition: form-data; name=\"proces" \
               "sTime\"\r\n\r\n3\r\n------WebKitFormBoundaryjxKimBWj0srHXiSB\r\nContent-Disposition: form-data; nam" \
                     "e=\"doSkew\"\r\n\r\nundefined\r\n------WebKitFormBoundaryjxKimBWj0srHXiSB--\r\n"

        r = requests.post("https://cliambrown.com/scripts/battleship_process.php", headers=headers, data=body)
        if r.json()['status'] == 'error':
            return
        same = True
        while same:
            best_cell = random.choice(r.json()['bestSquares'])
            if best_cell in self.hits:
                continue
            self.next_shot = (best_cell[0], best_cell[1])
            same = False

    def main(self):
        x, y = random.choice(self.best_starting_prob)
        if self.randomly_grid.loc[x, y] == 'x':
            self.hits.append((x, y))
            self.get_probabilities(True, (x, y))
        else:
            self.misses.append((x, y))
            self.get_probabilities(False, (x, y))

        while len(self.hits) != 17:
            x = self.next_shot[0]
            y = self.next_shot[1]
            if self.randomly_grid.loc[x, y] == 'x':
                self.hits.append((x, y))
                self.get_probabilities(True, (x, y))
            else:
                self.misses.append((x, y))
                self.get_probabilities(False, (x, y))
        return len(self.misses) + 17


bot = TargetedStrategy()
bot.main()
