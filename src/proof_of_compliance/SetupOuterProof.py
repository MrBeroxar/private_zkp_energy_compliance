from ZokCommandRunnerOuter import ZokCommandRunnerOuter

"""
Needs to be only invoked once to create the zokrates setup and corresponding output files
"""


class ZoKratesSetupRunner:
    def run_setup(self):
        zok_command_runner = ZokCommandRunnerOuter()

        compile_command = "zokrates compile --curve bw6_761 -i outer_proof.zok"

        setup_command = "zokrates setup --proving-scheme gm17 --backend ark"

        zok_command_runner.run_outer_proof_command([compile_command, setup_command])


if __name__ == "__main__":
    setup_runner = ZoKratesSetupRunner()
    setup_runner.run_setup()
