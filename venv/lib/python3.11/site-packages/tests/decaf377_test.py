import unittest

from os import urandom

from zokrates_pycrypto.fields import BLS12_377Field as FQ
from zokrates_pycrypto.curves import Decaf377 as JubJub


JUBJUB_C = JubJub.JUBJUB_C
JUBJUB_E = JubJub.JUBJUB_E


class TestJubjub(unittest.TestCase):
    def _point_g(self):
        return JubJub.generator()

    # Hardcoded for now till we have automatic test generation for ZoKrates test framework
    def _fe_rnd(self):
        return [FQ(1234), FQ(5678), FQ(7890)]

    def test_double(self):
        G = self._point_g()
        G_times_2 = G.mult(2)
        G_dbl = G.add(G)
        self.assertEqual(G_times_2, G_dbl)

    # test taken form: https://protocol.penumbra.zone/main/crypto/decaf377.html
    def test_cyclic(self):
        G = self._point_g()
        scalar = 2111115437357092606062206234695386632838870926408408195193685246394721360383
        self.assertEqual(G.mult(JUBJUB_C).mult(scalar), JubJub.infinity())

    def test_multiplicative(self):
        G = self._point_g()
        a, b, _ = self._fe_rnd()
        A = G.mult(a)
        B = G.mult(b)

        ab = (a.n * b.n) % JUBJUB_E
        AB = G.mult(FQ(ab))
        self.assertEqual(A.mult(b), AB)
        self.assertEqual(B.mult(a), AB)

    def test_multiplicative_associativity(self):
        G = self._point_g()

        a, b, c = self._fe_rnd()

        res1 = G.mult(a).mult(b).mult(c)
        res2 = G.mult(b).mult(c).mult(a)
        res3 = G.mult(c).mult(a).mult(b)

        self.assertEqual(res1, res2)
        self.assertEqual(res2, res3)
        self.assertEqual(res1, res3)

    def test_identities(self):
        G = self._point_g()
        self.assertEqual(G + JubJub.infinity(), G)
        self.assertEqual(G + G.neg(), JubJub.infinity())


if __name__ == "__main__":
    unittest.main()
