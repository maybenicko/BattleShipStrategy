import time
import json
import os
import Strategy.user
from Strategy.randomly_with_logic import TargetedStrategy as RandomLogic
from Strategy.complete_random import TargetedStrategy as CompleteRandom
from Strategy.every_two import TargetedStrategy as EveryTwo
from Strategy.every_other import TargetedStrategy as EveryOther
from Strategy.probability_meh import TargetedStrategy as ProbabilityBased
import utils.plot_graph
import utils.stats_calc


class Menu:
    def __init__(self):
        current_folder = os.getcwd()
        self.database_folder = os.path.join(current_folder, "Database")

        if not os.path.exists(self.database_folder):
            raise FileNotFoundError(f"The folder 'Database' does not exist in {current_folder}.")

        self.file_data = {
            "results_completely_random.json": [],
            "results_random_logic.json": [],
            "results_every_other.json": [],
            "results_every_two.json": [],
            "results_probability.json": []
        }
        self.start_time = None

    @staticmethod
    def display_menu():
        print('[0] Exit')
        print('[1] Completely random')
        print('[2] Random game but with hit logic')
        print('[3] Shooting every other cell')
        print('[4] Shooting every two cell')
        print('[5] Probability based game (about 7.8s per obs)')
        print('[6] Compare all (probability not supported)')
        print('[7] Plot graph and statistics')
        print('[8] Play by yourself!')
        print('[9] Get statistics')

    def update_results_json(self):
        for file_name, results in self.file_data.items():
            file_path = os.path.join(self.database_folder, file_name)
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {"results": []}

            data["results"].extend(results)
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

    def progress(self, iteration, obs):
        milestones = {
            0.25: "⬛⬜⬜⬜",
            0.5: "⬛⬛⬜⬜",
            0.75: "⬛⬛⬛⬜",
            1: "⬛⬛⬛⬛"
        }

        for fraction, message in milestones.items():
            if iteration == round(obs * fraction):
                print(f'Progress: {message}')
                self.update_results_json()
                return True
        return False

    @staticmethod
    def graph_and_stats():
        utils.plot_graph.graph()

    @staticmethod
    def play_user():
        Strategy.user.TargetedStrategy().main()

    @staticmethod
    def get_stats():
        utils.stats_calc.main()

    def run_strategy(self, strategy_class, file_key):
        result = strategy_class().main()
        self.file_data[file_key].append(result)
        return

    def run(self, mode, obs):
        strategies = {
            1: (CompleteRandom, "results_completely_random.json"),
            2: (RandomLogic, "results_random_logic.json"),
            3: (EveryOther, "results_every_other.json"),
            4: (EveryTwo, "results_every_two.json"),
            5: (ProbabilityBased, "results_probability.json"),
        }

        self.start_time = time.time()

        if 0 < mode < 6:
            strategy_class, file_key = strategies[mode]

            for iteration in range(obs + 1):
                self.run_strategy(strategy_class, file_key)
                if self.progress(iteration, obs):
                    self.file_data[file_key] = []
            elapsed_time = round(time.time() - self.start_time)
            print(f'Time elapsed: {elapsed_time}s\n')
            return

        elif mode == 6:
            obs_tot = obs * (len(strategies) - 1)
            iteration_tot = 0

            for strategy_class, file_key in list(strategies.values())[:4]:

                for iteration in range(obs + 1):
                    iteration_tot += 1
                    self.run_strategy(strategy_class, file_key)
                    if self.progress(iteration_tot, obs_tot):
                        self.file_data[file_key] = []

            elapsed_time = round(time.time() - self.start_time)
            print(f'Time elapsed: {elapsed_time}s\n')
            return
        else:
            print('Invalid mode!')
            return

    def main(self):
        while True:
            self.display_menu()
            user_input = input('\nSelect the strategy you want to use: ')
            if not user_input.isdigit():
                print(f'Invalid input. "{user_input}" is not a valid integer.')
                continue

            mode = int(user_input)
            if mode == 0:
                break
            elif mode == 7:
                self.graph_and_stats()
            elif mode == 8:
                self.play_user()
                continue
            elif mode == 9:
                self.get_stats()
                continue
            elif 1 <= mode <= 6:
                obs = input('Enter the number of observations: ')
                if not obs.isdigit():
                    print(f'Invalid input. "{obs}" is not a valid integer.')
                    continue

                print('')
                self.run(mode, int(obs))
            else:
                print(f'Invalid option: {mode}')


bot = Menu()
bot.main()
