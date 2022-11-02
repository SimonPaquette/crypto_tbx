"""
Simon Paquette
300044038
CSI 4108
Assignment 3
"""

import random
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh, ec, padding, rsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

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


toy_version = Elgamal(prime_q=89, root=13)
toy_version.set_xa()
toy_version.set_k(37)

m1 = 56
c1 = toy_version.encrypt(m1)
p1 = toy_version.decrypt(c1)


print()
print("----------")
print("QUESTION 1")
print("----------")
print()
print(toy_version)
print("Input message:", m1)
print("cipher:", c1)
print("Output plaintext:", p1)
print("public key:", toy_version.get_public_key())
print("private key:", toy_version.get_private_key())


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


print()
print("----------")
print("QUESTION 2")
print("----------")
print()
for _ in range(10):
    integer, binary = get_n_bit_odd_number(14)
    probable_prime = miller_rabin(integer, 5)
    print(f"Is {integer:<6} a probable prime? {probable_prime}")
print()
# The prob of error is < (1/4)^t = 0.09765625%
# compare to https://primes.utm.edu/lists/small/10000.txt


#!##################################################################
#! Q3
#!##################################################################
# * library: https://pypi.org/project/cryptography/
# * doc: https://cryptography.io/en/latest/hazmat/primitives/


# ? 3.a. RSA


key_size = 1024 * 2
e = 65537
m = b"466921883457309"
private_key = rsa.generate_private_key(public_exponent=e, key_size=key_size)
private_numbers = private_key.private_numbers()
public_key = private_key.public_key()
public_numbers = public_key.public_numbers()
p = private_numbers.p
q = private_numbers.q
d = private_numbers.d
dmp1 = private_numbers.dmp1
dmq1 = private_numbers.dmq1
iqmp = private_numbers.iqmp
n = public_numbers.n
oaep = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
)
ciphertext = public_key.encrypt(plaintext=m, padding=oaep)
plaintext = private_key.decrypt(ciphertext=ciphertext, padding=oaep)


# ? 3.b. ECC

ECDH_START_TIME = time.time()
# Alice ECDH
alice_private_key = ec.generate_private_key(curve=ec.SECP256R1())
alice_private_numbers = alice_private_key.private_numbers()
alice_public_key = alice_private_key.public_key()
alice_public_numbers = alice_public_key.public_numbers()
alice_private_value = alice_private_numbers.private_value
alice_x = alice_public_numbers.x
alice_y = alice_public_numbers.y
# Bob ECDH
bob_private_key = ec.generate_private_key(curve=ec.SECP256R1())
bob_private_numbers = bob_private_key.private_numbers()
bob_public_key = bob_private_key.public_key()
bob_public_numbers = bob_public_key.public_numbers()
bob_private_value = bob_private_numbers.private_value
bob_x = bob_public_numbers.x
bob_y = bob_public_numbers.y
# ECDH exchange
alice_shared_key = alice_private_key.exchange(
    algorithm=ec.ECDH(), peer_public_key=bob_public_key
)
bob_shared_key = bob_private_key.exchange(
    algorithm=ec.ECDH(), peer_public_key=alice_public_key
)
ECDH_END_TIME = time.time()
ECDH_TIME = ECDH_END_TIME - ECDH_START_TIME


DH_START_TIME = time.time()
# DH parameters
parameters = dh.generate_parameters(generator=2, key_size=512)
parameter_numbers = parameters.parameter_numbers()
p = parameter_numbers.p
g = parameter_numbers.g
q = parameter_numbers.q
# Alice DH
alice_private_key = parameters.generate_private_key()
alice_private_numbers = alice_private_key.private_numbers()
alice_public_key = alice_private_key.public_key()
alice_public_numbers = alice_public_key.public_numbers()
alice_private_value = alice_private_numbers.x
alice_public_value = alice_public_numbers.y
# Bob DH
bob_private_key = parameters.generate_private_key()
bob_private_numbers = bob_private_key.private_numbers()
bob_public_key = bob_private_key.public_key()
bob_public_numbers = bob_public_key.public_numbers()
bob_private_value = bob_private_numbers.x
bob_public_value = bob_public_numbers.y
# DH exchange
alice_shared_key = alice_private_key.exchange(peer_public_key=bob_public_key)
bob_shared_key = bob_private_key.exchange(peer_public_key=alice_public_key)
DH_END_TIME = time.time()
DH_TIME = DH_END_TIME - DH_START_TIME


# Show Result
print()
print("------------")
print("QUESTION 3 B")
print("------------")
print()
print(f"Shared secret s compute by Alice:\n{alice_shared_key}")
print()
print(f"Shared secret s compute by Bob:\n{bob_shared_key}")
print()
print(f"Computing time of s with ECDH: {ECDH_TIME}")
print(f"Computing time of s with DH:   {DH_TIME}")
print()
