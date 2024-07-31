import subprocess
import os


class ZokCommandRunnerOuter:
    def __init__(self):
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(current_script_dir, "outer_proof")

    def run_outer_proof_command(self, commands):

        for command in commands:
            subprocess.run(
                command,
                shell=True,
                cwd=self.base_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

    def _run_command(self, command, cwd):
        try:
            subprocess.run(
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
