import os


class ZoKratesCodeGenerator:
    def __init__(self, array_size):
        if array_size % 8 != 0:
            raise ValueError("Array size must be a multiple of 8.")
        self.array_size = array_size

    ###############Inner Proofs##############

    def generate_code_inner(self):
        signatures_required = self.array_size // 8
        zok_code = """from "ecc/decaf377.zok" import verifyEddsa;\n"""
        zok_code += """import "utils/casts/u32_to_field.zok" as u32_to_field;\n\n"""
        zok_code += "def main("
        for i in range(1, signatures_required + 1):
            zok_code += f"private field[2] R{i}, private field S{i}, "
        zok_code += "private field[2] A, "
        zok_code += f"private u32[{self.array_size}] Consumption, private u32[{self.array_size}] Production, field netResult){{\n"
        for i in range(1, signatures_required + 1):
            zok_code += f"    assert(verifyEddsa(R{i}, S{i}, A, Consumption[{(i-1)*8}..{i*8}], Production[{(i-1)*8}..{i*8}]));\n"
        zok_code += "    u32 mut sumConsumption = 0;\n    u32 mut sumProduction = 0;\n"
        zok_code += f"    for u32 i in 0..{self.array_size} {{\n        sumConsumption = sumConsumption + Consumption[i];\n        sumProduction = sumProduction + Production[i];\n    }}\n"
        zok_code += "    field fieldSumConsumption = u32_to_field(sumConsumption);\n    field fieldSumProduction = u32_to_field(sumProduction);\n"
        zok_code += "    field calculatedNetResult = fieldSumConsumption - fieldSumProduction;\n    assert(calculatedNetResult == netResult);\n}\n"
        return zok_code

    def write_to_file_inner(self, folder_name, file_name):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        target_dir = os.path.join(
            script_dir, "..", "proof_of_compliance", "inner_proofs", folder_name
        )
        os.makedirs(target_dir, exist_ok=True)
        full_path = os.path.join(target_dir, file_name)
        with open(full_path, "w") as file:
            file.write(self.generate_code_inner())
        print(f"ZoKrates code written to {full_path}")

    def generate_files_for_households(self, num_households):
        num_sigs = self.array_size // 8
        for i in range(1, num_households + 1):
            folder_name = f"household_{i}"
            file_name = f"household_proof_{num_sigs}_signatures.zok"
            self.write_to_file_inner(folder_name, file_name)

    ###########Outer Proof##############

    def generate_outer_proof_code(self, num_households):
        proof_inputs = 1
        verification_key_size = proof_inputs + 1
        code = f"""from "snark/gm17" import main as verify, Proof, VerificationKey;

        const u32 PROOF_INPUTS = {proof_inputs};
        const u32 VERIFICATION_KEY_SIZE = {verification_key_size};
        const u32 NUM_PROOFS = {num_households};
        const field prime_bs = 8444461749428370424248824938781546531375899335154063827935233455917409239041;

        struct PrivateInputs {{
            Proof<PROOF_INPUTS>[NUM_PROOFS] proofs;
            VerificationKey<VERIFICATION_KEY_SIZE>[NUM_PROOFS] keys;
        }}

        def convert_negative_num_from_bls_to_bw(field bls_num) -> field{{
        field diff = prime_bs - bls_num;
        field bw_num = 0 - diff;
    return bw_num;
}}

def main(private PrivateInputs privateInputs, field limit) {{
    field mut totalNetResult = 0;

    for u32 i in 0..NUM_PROOFS {{
        assert(verify(privateInputs.proofs[i], privateInputs.keys[i]));
        field householdNetResult = privateInputs.proofs[i].inputs[PROOF_INPUTS-1];
        totalNetResult = totalNetResult + (householdNetResult >= 100000000 ? convert_negative_num_from_bls_to_bw(householdNetResult) : householdNetResult); //assuming no householdNetResult is above 100000000
    }}
    assert(totalNetResult <= limit); //assuming that the community does not have a negative net result
}}
"""
        return code

    def write_outer_proof_to_file(self, num_households, file_name="outer_proof.zok"):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        target_dir = os.path.join(
            script_dir, "..", "proof_of_compliance", "outer_proof"
        )
        os.makedirs(target_dir, exist_ok=True)
        full_path = os.path.join(target_dir, file_name)
        code = self.generate_outer_proof_code(num_households)
        with open(full_path, "w") as file:
            file.write(code)
        print(f"Outer proof ZoKrates code written to {full_path}")


## Example usage for outer proof:
num_households = 4
generator = ZoKratesCodeGenerator(array_size=16)
generator.write_outer_proof_to_file(num_households)
generator.generate_files_for_households(num_households)
