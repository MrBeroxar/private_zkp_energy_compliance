import os
import subprocess
import unittest


class ZokCommandRunner:
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zok_code")

    def _run_command(self, command, cwd):
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"Command '{command}' executed successfully in {cwd}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command '{command}' in {cwd}: {e}")
            print(f"Stderr: {e.stderr.decode()}")


class TestInnerProof(unittest.TestCase):
    def setUp(self):
        self.zok_runner = ZokCommandRunner()
        self.base_dir = self.zok_runner.base_dir
        self.check_and_run_setup()
        self.input_files = {
            "negative_netresult.json": True,
            "wrong_sig.json": False,
            "wrong_netresult.json": False,
        }

    def check_and_run_setup(self):
        proving_key_path = os.path.join(self.base_dir, "proving.key")
        if not os.path.exists(proving_key_path):
            print("proving.key not found, running setup...")
            self.run_setup()

    def run_setup(self):
        compile_command = "zokrates compile -i test.zok -c bls12_377"
        setup_command = "zokrates setup -b ark -s gm17"
        self.zok_runner._run_command(compile_command, self.base_dir)
        self.zok_runner._run_command(setup_command, self.base_dir)

    def _run_compute_witness(self, input_file, cwd):
        command = f"zokrates compute-witness --abi --stdin < inputs/{input_file}"
        result = subprocess.run(
            command, shell=True, cwd=cwd, capture_output=True, text=True
        )
        return result.returncode == 0

    def test_inner_proof(self):
        for input_file, should_pass in self.input_files.items():
            result = self._run_compute_witness(input_file, self.base_dir)
            self.assertEqual(
                result, should_pass, f"{input_file} did not yield the expected result."
            )


if __name__ == "__main__":
    unittest.main()
