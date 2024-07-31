import subprocess
import os

class ZokCommandRunner:
    def __init__(self):
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(current_script_dir, "zok_code")

    def run_zokrates_command_in_subdirs(self, file_name, commands):
        subdirs = [
            d
            for d in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, d))
            and d.startswith("household_")
        ]
        print(f"Base directory: {self.base_dir}")  # Debug print
        for subdir in subdirs:
            subdir_path = os.path.join(self.base_dir, subdir)
            target_file_path = os.path.join(subdir_path, file_name)
            print(f"Attempting to run commands in: {subdir_path}")  # Debug print
            if os.path.exists(target_file_path):
                for command in commands:
                    self._run_command(command, subdir_path)
            else:
                print(f"{file_name} not found in {subdir}")

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
