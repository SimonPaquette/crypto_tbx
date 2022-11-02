"""
Simon Paquette
300044038
CSI 4108
Assignment 3
"""

import random

# https://pypi.org/project/cryptography/
from cryptography.hazmat.primitives.asymmetric import rsa


#!##################################################################
#! Q1
#!##################################################################


class Elgamal:
    def __init__(self, prime_q: int, root: int):
        self.prime_q = prime_q
        self.root = root
        self.xa = None
        self.ya = None
        self.k = None
        self.K = None

    def __repr__(self):
        return str(vars(self))

    def set_xa(self, xa=None):
        if xa is not None:
            self.xa = xa
        else:
            self.xa = random.randint(2, self.prime_q - 2)
        self._set_ya()

    def _set_ya(self):
        self.ya = (self.root**self.xa) % self.prime_q

    def set_k(self, k=None):
        if k is not None:
            self.k = k
        else:
            self.k = random.randint(1, self.prime_q - 1)
        self._set_K()

    def _set_K(self):
        self.K = (self.ya**self.k) % self.prime_q

    def get_private_key(self):
        return self.xa

    def get_public_key(self):
        return (self.prime_q, self.root, self.ya)

    def encrypt(self, message: int):
        c1 = (self.root**self.k) % self.prime_q
        c2 = (self.K * message) % self.prime_q
        return (c1, c2)

    def decrypt(self, ciphertext: tuple[int, int]):
        c1, c2 = ciphertext
        K = (c1**self.xa) % self.prime_q
        M = (c2 * pow(base=K, exp=-1, mod=self.prime_q)) % self.prime_q
        return M


# print("\nQUESTION 1\n")

# toy_version = Elgamal(prime_q=89, root=13)
# toy_version.set_xa()
# toy_version.set_k(37)
# print(toy_version)


# cipher = toy_version.encrypt(56)
# print("cipher:", cipher)
# message = toy_version.decrypt(cipher)
# print("message:", message)
# print("public key:", toy_version.get_public_key())
# print("private key:", toy_version.get_private_key())


#!##################################################################
#! Q2
#!##################################################################


def get_n_bit_odd_number(n_bits: int) -> tuple[int, str]:
    number = 0
    while number % 2 == 0:
        number = random.randint(2 ** (n_bits - 1), (2**n_bits) - 1)
        binary = f"{number:b}"
    return (number, binary)


def miller_rabin(odd_integer: int, confidence: int) -> bool:

    # Make sure odd integer and test>0
    assert odd_integer % 2 == 1
    assert confidence > 0

    # Find k and q with k>=0 and q odd where n - 1 = (2^k) * (q)
    k = 0
    reduction = odd_integer - 1
    while reduction % 2 == 0:
        reduction /= 2
        k += 1
    q = (odd_integer - 1) // (2**k)

    # Do t=confidence miller-rabin test
    for i in range(confidence):

        # Select random integer a, 1 < a < n - 1
        a = random.randint(2, odd_integer - 2)

        # Test
        inconclusive = False

        if (a**q) % odd_integer == 1:
            inconclusive = True
            continue

        for j in range(k):
            if (a ** (2**j * q)) % odd_integer == odd_integer - 1:
                inconclusive = True
                break

        if not inconclusive:
            return False

    return True


# print("\nQUESTION 2\n")
# for _ in range(10):
#     integer, binary = get_n_bit_odd_number(14)
#     probable_prime = miller_rabin(integer, 5)
#     print(f"Is {integer:<6} a probable prime? {probable_prime}")
#     # The prob of error is < (1/4)^t = 0.09765625%


#!##################################################################
#! Q3
#!##################################################################

# * 3.a. https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/


private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024 * 2)
private_numbers = private_key.private_numbers()
key_size = private_key.key_size
p = private_numbers.p
q = private_numbers.q
d = private_numbers.d
dmp1 = private_numbers.dmp1
dmq1 = private_numbers.dmq1
iqmp = private_numbers.iqmp
public_key = private_key.public_key()
public_numbers = public_key.public_numbers()
n = public_numbers.n
e = public_numbers.e


# *  3.b. https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/
