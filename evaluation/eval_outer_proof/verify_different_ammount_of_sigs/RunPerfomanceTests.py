import os
import pandas as pd
import subprocess
import time

from ZokCommandRunner import ZokCommandRunner


class RunPerformanceTests(ZokCommandRunner):
    def __init__(self, subfolders):
        super().__init__()
        self.subfolders = subfolders
        self.results = []

    def _run_command_with_timing(self, command, cwd):
        start_time = time.time()
        result = subprocess.run(
            command, shell=True, cwd=cwd, capture_output=True, text=True
        )
        duration = time.time() - start_time
        return duration, result.stdout + result.stderr, result.returncode

    def run_tests(self):
        original_base_dir = self.base_dir
        for subfolder in self.subfolders:
            subfolder_path = os.path.join(original_base_dir, subfolder)
            if not os.path.exists(subfolder_path):
                print(f"Subfolder does not exist: {subfolder_path}")
                continue

            metrics = {"subfolder": subfolder}

            commands = [
                (
                    "compute-witness",
                    "zokrates compute-witness --abi --stdin < input.json",
                ),
                (
                    "generate-proof",
                    "zokrates generate-proof --proving-scheme gm17 --backend ark",
                ),
                ("verify", "zokrates verify"),
            ]

            for command_name, command in commands:
                duration, output, returncode = self._run_command_with_timing(
                    command, subfolder_path
                )
                if returncode != 0:
                    print(f"Command failed in {subfolder}: {command}")
                metrics[f"time in s: {command_name}"] = duration

            self.results.append(metrics)

        self.export_to_csv()

    def export_to_csv(self, filename="performance_results.csv"):
        df = pd.DataFrame(self.results)
        df = df[
            [
                "subfolder",
                "time in s: compute-witness",
                "time in s: generate-proof",
                "time in s: verify",
            ]
        ]
        csv_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename
        )
        if os.path.exists(csv_file_path):
            df.to_csv(csv_file_path, mode="a", header=False, index=False)
        else:
            df.to_csv(csv_file_path, index=False)


# Example usage
subfolders = ["1", "2", "4", "8", "32"]
tester = RunPerformanceTests(subfolders)
tester.run_tests()
