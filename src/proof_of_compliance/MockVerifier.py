from ZokCommandRunnerOuter import ZokCommandRunnerOuter
import subprocess


class MockVerifier:
    def run_setup(self):
        zok_command_runner = ZokCommandRunnerOuter()

        verify_command = "zokrates verify"

        try:
            zok_command_runner.run_outer_proof_command([verify_command])
            print("Proof-of-Compliance verification was successful. The community's renewable energy consumption is sufficient and does not exceed the policy threshold!")
        except subprocess.CalledProcessError as e:
            print(f"The community is not compliant! Verification failed with exit status {e.returncode}")
            print(f"Error message: {e.output}")


if __name__ == "__main__":
    setup_runner = MockVerifier()
    setup_runner.run_setup()
