import struct
from zokrates_pycrypto.curves import Decaf377
from zokrates_pycrypto.eddsa import PrivateKey, PublicKey


class SignatureGenerator:

    key = 5145218980968378210524378404035776788013036277399811805365337506608398016000

    def __init__(self, consumption, production):
        self.consumption = consumption
        self.production = production

    @staticmethod
    def arrays_to_bytes(arrays):
        fmt = ">" + "I" * len(arrays)
        return struct.pack(fmt, *arrays)

    def sign_parts(self, parts=2):
        part_size = len(self.consumption) // parts
        signatures = []
        sk = PrivateKey(self.key, curve=Decaf377)
        pk = PublicKey.from_private(sk)

        for i in range(parts):
            start = i * part_size
            end = (i + 1) * part_size
            raw_msg = self.arrays_to_bytes(
                self.consumption[start:end] + self.production[start:end]
            )
            sig = sk.sign(raw_msg)
            signatures.append(sig)

        return signatures, pk
