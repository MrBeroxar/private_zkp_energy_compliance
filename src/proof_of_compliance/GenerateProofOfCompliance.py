import os
import json
from ZokCommandRunnerOuter import ZokCommandRunnerOuter


class GenerateProofOfCompliance:
    def __init__(self, energyLimit):
        self.energyLimit = energyLimit
        self.zok_command_runner = ZokCommandRunnerOuter()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    # Creates input.json files in each household folder
    def generate_input_json(self, numHouseholds, output_path):
        household_paths = [
            os.path.join("inner_proofs", f"household_{i}")
            for i in range(1, numHouseholds + 1)
        ]

        data = {"proofs": [], "keys": []}
        for path in household_paths:
            proof_path = os.path.join(self.script_dir, path, "proof.json")
            key_path = os.path.join(self.script_dir, path, "verification.key")

            with open(proof_path, "r") as proof_file:
                proof_data = json.load(proof_file)
                data["proofs"].append(
                    {"proof": proof_data["proof"], "inputs": proof_data["inputs"]}
                )

            with open(key_path, "r") as key_file:
                key_data = json.load(key_file)
                key_data.pop("scheme", None)
                key_data.pop("curve", None)
                data["keys"].append(key_data)

        data_with_limit = [
            data,
            str(self.energyLimit),
        ]

        output_full_path = os.path.join(self.script_dir, output_path)
        with open(output_full_path, "w") as outfile:
            json.dump(data_with_limit, outfile, indent=2)

    def run_outer_proof_commands(self):
        commands = [
            "zokrates compute-witness --abi --stdin < input.json",
            "zokrates generate-proof --proving-scheme gm17 --backend ark",
        ]
        self.zok_command_runner.run_outer_proof_command(commands)


if __name__ == "__main__":
    generator = GenerateProofOfCompliance(
        energyLimit=50000
    )  # Renewable energy treshold which the community should not exceed
    numHouseholds = 4
    generator.generate_input_json(numHouseholds, "outer_proof/input.json")
    generator.run_outer_proof_commands()
