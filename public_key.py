import math

from arithmetic import NumeralArithmetic
from utils import phi


def fast_modular_expo(exponent: int, value: int = None, mod: int = None) -> None:
    expos = f"{exponent:b}"

    n_multiplications = 0
    for expo in expos:
        if expo == "0":
            n_multiplications += 1
        elif expo == "1":
            n_multiplications += 2

    print("n_multiplications:", n_multiplications)

    if value is not None and mod is None:
        f = 1
        for expo in expos:
            f = f * f
            if expo == "1":
                f = f * value
        print("result:", f)

    if value is not None and mod is not None:
        f = 1
        for expo in expos:
            f = (f * f) % mod
            if expo == "1":
                f = (f * value) * mod
        print("result:", f)


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

        c = (message**self.public_key_e) % self.pq
        return c

    def decrypt(self, ciphertext: int) -> int:
        assert isinstance(ciphertext, int)
        self._valid_private_key_d()
        self._valid_pq()

        m = (ciphertext**self.private_key_d) % self.pq
        return m


rsa = RSA(prime_p=17, prime_q=11, public_key_e=7, private_key_d=23)

rsa = RSA(prime_p=7, prime_q=997)
rsa.set_keys(5971)
c = rsa.encrypt(88)
m = rsa.decrypt(c)
print(c)
print(m)

print(rsa)
