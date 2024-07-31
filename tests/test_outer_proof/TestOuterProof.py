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

class TestOuterProof(unittest.TestCase):
    def setUp(self):
        self.zok_runner = ZokCommandRunner()
        self.base_dir = self.zok_runner.base_dir
        self.check_and_run_setup()
        self.input_files = {
            "total_netresult_is_8_but_one_proof_has_neg_netresult.json": True,  # assert netresult 16 + netresult -8 <= 8
            "total_netresult_is_8_but_one_proof_has_neg_netresult_and_limit_is_to_low.json": False,  # assert netresult 16 + netresult -8 <= 7
            "faulty_inner_proof.json": False,
        }

    def check_and_run_setup(self):
        proving_key_path = os.path.join(self.base_dir, "proving.key")
        if not os.path.exists(proving_key_path):
            print("proving.key not found, running setup...")
            self.run_setup()

    def run_setup(self):
        compile_command = "zokrates compile --curve bw6_761 -i outer_proof.zok"
        setup_command = "zokrates setup --proving-scheme gm17 --backend ark"
        self.zok_runner._run_command(compile_command, self.base_dir)
        self.zok_runner._run_command(setup_command, self.base_dir)

    def _run_compute_witness(self, input_file, cwd):
        command = f"zokrates compute-witness --abi --stdin < inputs/{input_file}"
        result = subprocess.run(
            command, shell=True, cwd=cwd, capture_output=True, text=True
        )
        return result.returncode == 0

    def test_outer_proof(self):
        for input_file, should_pass in self.input_files.items():
            result = self._run_compute_witness(input_file, self.base_dir)
            if should_pass:
                self.assertTrue(result, f"{input_file} should pass but failed.")
            else:
                self.assertFalse(result, f"{input_file} should fail but passed.")


if __name__ == "__main__":
    unittest.main()
