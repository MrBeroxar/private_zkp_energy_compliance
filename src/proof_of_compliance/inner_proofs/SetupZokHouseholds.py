import ZokCommandRunner

"""
Needs to only invoked once to create the zokrates setup and corresponding output files
"""


class ZoKratesSetupRunner:

    def run_setup(self):

        zok_command_runner = ZokCommandRunner.ZokCommandRunner()

        compile_command = (
            "zokrates compile -i household_proof_2_signatures.zok -c bls12_377"
        )
        setup_command = "zokrates setup -b ark -s gm17"

        zok_command_runner.run_zokrates_command_in_subdirs(
            "household_proof_2_signatures.zok", [compile_command, setup_command]
        )


if __name__ == "__main__":
    ZoKratesSetupRunner().run_setup()
