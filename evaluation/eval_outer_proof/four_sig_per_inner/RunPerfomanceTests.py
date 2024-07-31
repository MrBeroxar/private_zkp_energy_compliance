import os
import json
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

    def _extract_constraints(self, compile_output):
        for line in compile_output.split("\n"):
            if "Number of constraints:" in line:
                try:
                    return int(line.split(":")[-1].strip())
                except ValueError:
                    return None
        return None

    def _extract_inputs_size(self, proof_path):
        try:
            with open(proof_path, "r") as file:
                proof_data = json.load(file)
                inputs_size = len(proof_data.get("inputs", []))
            return inputs_size
        except FileNotFoundError:
            return None

    def run_tests(self):
        original_base_dir = self.base_dir
        for subfolder in self.subfolders:
            subfolder_path = os.path.join(original_base_dir, subfolder)
            if not os.path.exists(subfolder_path):
                print(f"Subfolder does not exist: {subfolder_path}")
                continue

            proof_path = os.path.join(subfolder_path, "proof.json")
            metrics = {"number of inner proofs": subfolder}

            commands = [
                ("compile", "zokrates compile --curve bw6_761 -i test.zok"),
                ("setup", "zokrates setup --proving-scheme gm17 --backend ark"),
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
                if command_name == "compile":
                    constraints = self._extract_constraints(output)
                    metrics["constraints"] = (
                        constraints if constraints is not None else "Error extracting"
                    )

            inputs_size = self._extract_inputs_size(proof_path)
            metrics["proof inputs arraysize"] = inputs_size

            self.results.append(metrics)

        self.export_to_csv()

    def export_to_csv(
        self,
        filename="evaluation_number_inner_proofs_final_with_one_inp_and_four_sig.csv",
    ):
        df = pd.DataFrame(self.results)
        df = df[
            [
                "number of inner proofs",
                "proof inputs arraysize",
                "constraints",
                "time in s: compile",
                "time in s: setup",
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
subfolders = ["one", "two", "four"]
tester = RunPerformanceTests(subfolders)
tester.run_tests()
