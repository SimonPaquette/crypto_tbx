import math

from arithmetic import NumeralArithmetic
from utils import phi


class RSA:
    def __init__(
        self,
        public_key_e: int = None,
        private_key_d: int = None,
        prime_p: int = None,
        prime_q: int = None,
        pq: int = None,
    ):
        self.public_key_e = public_key_e
        self.private_key_d = private_key_d
        self.prime_p = prime_p
        self.prime_q = prime_q
        self.pq = pq

        if (pq is None) and (prime_p is not None) and (prime_q is not None):
            self.pq = prime_p * prime_q

        self.phi = phi(self.pq)

    def __repr__(self):
        return str(vars(self))

    def _valid_public_key_e(self):
        assert isinstance(self.public_key_e, int)
        assert self.public_key_e > 1
        assert self.public_key_e < self.phi
        assert math.gcd(self.public_key_e, self.phi) == 1

    def _valid_private_key_d(self):
        assert isinstance(self.private_key_d, int)
        assert self.private_key_d > 1
        assert self.private_key_d < self.phi
        assert ((self.public_key_e * self.private_key_d) % self.phi) == 1

    def _valid_pq(self):
        assert isinstance(self.pq, int)

    def select_keys(self):
        assert self.public_key_e is None
        assert self.private_key_d is None

        for i in range(self.phi - 1, 1, -1):
            try:
                self.public_key_e = i
                self._valid_public_key_e()
                self.private_key_d = NumeralArithmetic.find_inverse(
                    self.public_key_e, self.phi, False
                )
                self._valid_private_key_d()
                assert self.public_key_e != self.private_key_d
                break
            except AssertionError:
                pass
            except ZeroDivisionError:
                pass

    def set_keys(self, public_key: int):
        self.public_key_e = public_key
        self._valid_public_key_e()
        self.private_key_d = NumeralArithmetic.find_inverse(
            self.public_key_e, self.phi, False
        )
        self._valid_public_key_e()
        self._valid_private_key_d()

    def encrypt(self, message: int) -> int:
        assert isinstance(message, int)
        assert message > 0
        assert message < self.phi
        self._valid_public_key_e()
        self._valid_pq()

        c = pow(base=message, exp=self.public_key_e, mod=self.pq)
        return c

    def decrypt(self, ciphertext: int) -> int:
        assert isinstance(ciphertext, int)
        self._valid_private_key_d()
        self._valid_pq()

        m = pow(base=ciphertext, exp=self.private_key_d, mod=self.pq)
        return m

    def decrypt_CRT(self, ciphertext: int) -> None:
        vp = pow(ciphertext, self.private_key_d % (self.prime_p - 1), self.prime_p)
        vq = pow(ciphertext, self.private_key_d % (self.prime_q - 1), self.prime_q)
        xp = self.prime_q * pow(self.prime_q, -1, self.prime_p)
        xq = self.prime_p * pow(self.prime_p, -1, self.prime_q)
        plaintext = (vp * xp + vq * xq) % self.pq

        print(
            f"vp = c^(d mod p-1) mod p = {ciphertext}^({self.private_key_d} mod {self.prime_p-1}) mod {self.prime_p} = {vp}"
        )
        print(
            f"vq = c^(d mod q-1) mod q = {ciphertext}^({self.private_key_d} mod {self.prime_q-1}) mod {self.prime_q} = {vq}"
        )
        print(f"xp = q * q^-1 mod p = {xp}")
        print(f"xq = p * p^-1 mod q = {xq}")
        print(
            f"Plaintext = (vp*xp + vq*xq) mod n = ({vp}*{xp} + {vq}*{xq}) mod {self.pq} = {plaintext}"
        )
