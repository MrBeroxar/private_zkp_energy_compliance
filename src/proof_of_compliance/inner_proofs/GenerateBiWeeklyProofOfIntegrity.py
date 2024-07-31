import os
import json
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.append(project_root_dir)

from mock_meter.GaussianMockDataGenerator import GaussianMockDataGenerator
from mock_meter.SignatureGenerator import SignatureGenerator
from mock_meter.ZokInputGenerator import ZokInputGenerator
from proof_of_compliance.inner_proofs.ZokCommandRunner import ZokCommandRunner

"""
Class is set to biweekly (and not semi-anually as proposed in thesis) for simplicity, as it would take otherwise 70 Minutes to generate a proof
"""


class GenerateBiWeeklyProofOfIntegrity:
    def __init__(self):
        self.zok_command_runner = ZokCommandRunner()

    def generate_input_files(self):
        base_dir = os.path.join(project_root_dir, "proof_of_compliance", "inner_proofs")
        subdirs = [
            d
            for d in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("household_")
        ]
        for subdir in subdirs:
            subdir_path = os.path.join(base_dir, subdir)
            zok_file = self._find_zok_file(subdir_path)
            if zok_file:
                sizeofinnerproof = (
                    16  # needs to be changed if more signatures get added
                )
                consume_data, produce_data, netResult = GaussianMockDataGenerator(
                    sizeofinnerproof
                ).get_gaussian_mock_data(10, 5)
                signatures, public_key = SignatureGenerator(
                    consume_data, produce_data
                ).sign_parts()
                input_data = ZokInputGenerator(
                    consume_data, produce_data, netResult, signatures, public_key
                ).generate_json_output()

                input_json_path = os.path.join(subdir_path, "input.json")
                with open(input_json_path, "w") as f:
                    f.write(input_data)

    def run_zokrates_commands(self):
        base_dir = os.path.join(project_root_dir, "proof_of_compliance", "inner_proofs")
        subdirs = [
            d
            for d in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("household_")
        ]
        for subdir in subdirs:
            subdir_path = os.path.join(base_dir, subdir)
            input_json_path = os.path.join(subdir_path, "input.json")
            if os.path.exists(input_json_path):
                commands = [
                    f"zokrates compute-witness --abi --stdin < {input_json_path}",
                    "zokrates generate-proof -b ark -s gm17",
                ]
                for command in commands:
                    self.zok_command_runner._run_command(command, subdir_path)

    def _find_zok_file(self, subdir_path):
        for file in os.listdir(subdir_path):
            if file.startswith("household_proof_") and file.endswith(".zok"):
                return file
        return None


if __name__ == "__main__":
    generator = GenerateBiWeeklyProofOfIntegrity()
    generator.generate_input_files()
    generator.run_zokrates_commands()
