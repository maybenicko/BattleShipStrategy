import os
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


file_names = [
    ("results_completely_random.json", "red", "Completely Random"),
    ("results_random_logic.json", "blue", "Random with Hunt"),
    ("results_every_other.json", "yellow", "Every Other"),
    ("results_every_two.json", "green", "Every Two"),
    ("results_probability.json", "pink", "Probability Based")
]

current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_folder = os.path.join(current_folder, "Database")

if not os.path.exists(database_folder):
    raise FileNotFoundError(f"The folder 'Database' does not exist in {current_folder}.")


def graph():
    plt.figure(figsize=(10, 6))
    plt.gcf().set_facecolor('black')
    plt.gca().set_facecolor('black')

    for file_name, color, name in file_names:
        file_path = os.path.join(database_folder, file_name)

        if not os.path.exists(file_path):
            print(f"Warning: {file_name} not found in the 'Database' folder.")
            continue

        with open(file_path, "r") as f:
            try:
                result = json.load(f)['results']
            except KeyError as e:
                print(f"Error: Missing key {e} in {file_name}")
                continue
            except json.JSONDecodeError as e:
                print(f"Error decoding {file_name}: {e}")
                continue

        if len(result) > 0:
            unique_moves, counts = np.unique(result, return_counts=True)
            total_games = len(result)
            percentages = (np.cumsum(counts) / total_games) * 100
            sorted_indices = np.argsort(unique_moves)
            sorted_moves = unique_moves[sorted_indices]
            sorted_percentages = percentages[sorted_indices]

            if len(sorted_moves) > 1:
                f = interp1d(sorted_moves, sorted_percentages, kind='linear', bounds_error=False, fill_value=(0, 100))
                x = np.linspace(sorted_moves.min(), sorted_moves.max(), 500)
                y = f(x)
                y = np.clip(y, 0, 100)

                plt.plot(x, y, color=color, linewidth=1, label=f'{name} [{len(result)}]')

    plt.xlabel('Moves Required', fontsize=12, color='white')
    plt.ylabel('Percentage (%)', fontsize=12, color='white')
    plt.title('Average Moves Distribution', fontsize=14, color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.grid(True, color='white')
    plt.legend(fontsize=10, loc='upper left', facecolor='black', edgecolor='white', labelcolor='white')
    output_path = os.path.join(current_folder, 'plot.png')
    plt.savefig(output_path)
    plt.show()
