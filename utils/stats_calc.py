import os
import json
import statistics
import matplotlib.pyplot as plt


class StrategyStatistics:
    def __init__(self, file_names):
        self.file_names = file_names
        self.current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.database_folder = os.path.join(self.current_folder, "Database")

        if not os.path.exists(self.database_folder):
            raise FileNotFoundError(f"The folder 'Database' does not exist in {self.current_folder}.")

    def extract_data_from_json(self):
        all_data = {}
        for file_name, strategy_name in self.file_names:
            file_path = os.path.join(self.database_folder, file_name)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data[strategy_name] = data["results"]
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading {file_name}: {e}")
                all_data[strategy_name] = []
        return all_data

    @staticmethod
    def calculate_statistics(data):
        stats = {}
        for strategy_name, results in data.items():
            if results:
                stats[strategy_name] = {
                    'min': min(results),
                    'max': max(results),
                    'mean': round(statistics.mean(results), 2),
                    'median': statistics.median(results),
                    'mode': statistics.mode(results) if len(set(results)) > 1 else None,
                    'std_dev': round(statistics.stdev(results), 2) if len(results) > 1 else None,
                    'range': max(results) - min(results),
                    'count': len(results)
                }
        return stats

    @staticmethod
    def display_statistics_comparison(stats):
        headers = ["Metric"] + list(stats.keys())
        metrics = ["Min", "Max", "Mean", "Median", "Mode", "Std_dev", "Range", "Sum", "Count"]

        print(f"{'':<15}", end="")
        for strategy in headers[1:]:
            print(f"{strategy:<20}", end="")
        print()

        for metric in metrics:
            print(f"{metric:<15}", end="")
            for strategy in stats.keys():
                value = stats[strategy].get(metric.lower(), 'N/A')
                if value is None:
                    value = 'N/A'
                print(f"{value:<20}", end="")
            print()

    def plot_histograms(self, data):
        plt.style.use('dark_background')
        plt.figure(figsize=(10, 6))
        colors = ['red', 'blue', 'green', 'purple', 'orange']

        for idx, (strategy_name, results) in enumerate(data.items()):
            if results:
                plt.hist(results, color='black', ec=colors[idx], bins=10, alpha=0.5, label=strategy_name, linewidth=2,
                         density=True)

        plt.title('Normalized Histogram of Moves by Strategy', color='white')
        plt.xlabel('Moves Required', color='white')
        plt.ylabel('Density', color='white')
        plt.legend()
        output_path = os.path.join(self.current_folder, 'stats.png')
        plt.savefig(output_path)
        plt.show()


def main():
    file_names = [
        ("results_completely_random.json", "Completely Random"),
        ("results_random_logic.json", "Random with Hunt"),
        ("results_every_other.json", "Every Other"),
        ("results_every_two.json", "Every Two"),
        ("results_probability.json", "Probability Based")
    ]

    stats_calculator = StrategyStatistics(file_names)

    data = stats_calculator.extract_data_from_json()
    stats = stats_calculator.calculate_statistics(data)

    stats_calculator.display_statistics_comparison(stats)
    print('')
    stats_calculator.plot_histograms(data)
