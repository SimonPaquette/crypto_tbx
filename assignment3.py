"""
Simon Paquette
300044038
CSI 4108
Assignment 3

Before executing the python file, need to install the Cryptography library (https://pypi.org/project/cryptography/):
    pip install cryptography
    or
    conda install cryptography
"""


import random
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh, ec, padding, rsa

#!##################################################################
#! Q1 - Elgamal public key encryption algorithm
#!##################################################################


class Elgamal:
    """
    Elgamal public key encryption algorithm
    """

    def __init__(self, prime_q: int, root: int) -> None:
        """
        Public Key Crypto

        Args:
            prime_q (int): prime number
            root (int): primitive root of prime_q
        """
        self.prime_q: int = prime_q
        self.root: int = root
        self.xa: int = None
        self.ya: int = None
        self.k: int = None
        self.K: int = None

    def __repr__(self) -> str:
        """
        Object printable

        Returns:
            str: object description
        """
        txt = f"System Parameters:\n"
        txt += f" - Public Key: (q={self.prime_q}, root={self.root}, Ya={self.ya})\n"
        txt += f" - Private Key: (Xa={self.xa})\n"
        txt += f" - Random One-Time Key: (k={self.k}, K={self.K})\n"
        return txt

    def set_xa(self, xa: int = None) -> None:
        """
        Generate a random integer XA (private key)

        Args:
            xa (int, optional): specific XA. Defaults to None.
        """
        if xa is not None:
            self.xa = xa
        else:
            self.xa = random.randint(2, self.prime_q - 2)  # 1 < XA < q - 1.
        self._set_ya()

    def _set_ya(self) -> None:
        """
        Compute YA (public key)
        """
        self.ya = pow(base=self.root, exp=self.xa, mod=self.prime_q)

    def set_k(self, k: int = None) -> None:
        """
        Generate a random integer k

        Args:
            k (int, optional): specific k. Defaults to None.
        """
        if k is not None:
            self.k = k
        else:
            self.k = random.randint(1, self.prime_q - 1)  # 1 <= k <= q - 1
        self._set_K()

    def _set_K(self) -> None:
        """
        Compute K (one-time key)
        """
        self.K = pow(base=self.ya, exp=self.k, mod=self.prime_q)

    def get_private_key(self) -> int:
        """
        Getter

        Returns:
            int: private key
        """
        return self.xa

    def get_public_key(self) -> tuple[int, int, int]:
        """
        Getter

        Returns:
            tuple[int,int,int]: public key
        """
        return (self.prime_q, self.root, self.ya)

    def encrypt(self, message: int) -> tuple[int, int]:
        """
        Encrypt a message using Elgamal algo

        Args:
            message (int): plaintext

        Returns:
            tuple[int, int]: ciphertext
        """
        c1 = pow(base=self.root, exp=self.k, mod=self.prime_q)
        c2 = (self.K * message) % self.prime_q
        return (c1, c2)

    def decrypt(self, ciphertext: tuple[int, int]) -> str:
        """
        Decrypt a cipher using Elgamal algo

        Args:
            ciphertext (tuple[int, int]): ciphertext
        Returns:
            str: plaintext
        """
        c1, c2 = ciphertext
        K = pow(base=c1, exp=self.xa, mod=self.prime_q)
        M = (c2 * pow(base=K, exp=-1, mod=self.prime_q)) % self.prime_q
        return M


q = 89
root = 13
k = 37
toy_version = Elgamal(prime_q=q, root=root)
toy_version.set_xa()
toy_version.set_k(k)

m1 = 56
c1 = toy_version.encrypt(m1)
p1 = toy_version.decrypt(c1)

m2 = 32  # Assumption
c2 = toy_version.encrypt(m2)
p2 = pow(base=c1[1], exp=-1, mod=q) * c2[1] * m1 % q


# Show Result
print()
print("----------")
print("QUESTION 1")
print("----------")
print()
print(toy_version)
print("Input message1:", m1)
print("Cipher1:", c1)
print("Output plaintext1:", p1)
print()
print("From Cipher2:", c2)
print(
    f"Compute Plaintext2={m2} knowing the encryption used the same k=37 : ({pow(base=c1[1], exp=-1, mod=q)}*{c2[1]}*{m1})%{q} = {p2}"
)
print()


#!##################################################################
#! Q2 - Miller-Rabin probabilistic primality testing algorithm
#!##################################################################


def get_n_bit_odd_number(n_bits: int) -> tuple[int, str]:
    """
    Get a random odd number of lenght n bits

    Args:
        n_bits (int): lenght of the integer

    Returns:
        tuple[int, str]: a random number in the format (DEC, BIN)
    """
    number = 0
    while number % 2 == 0:
        number = random.randint(2 ** (n_bits - 1), (2**n_bits) - 1)
        binary = f"{number:b}"
    return (number, binary)


def miller_rabin(odd_integer: int, confidence: int) -> bool:
    """
    Miller-Rabin probabilistic primality testing algorithm

    Args:
        odd_integer (int): a number to test if it is prime
        confidence (int): run the test t times

    Returns:
        bool: odd_integer is a prime
    """

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
    for _ in range(confidence):

        # Select random integer a, 1 < a < n - 1
        a = random.randint(2, odd_integer - 2)

        # Test
        inconclusive = False

        if pow(base=a, exp=q, mod=odd_integer) == 1:
            inconclusive = True
            continue

        for j in range(k):
            if (a ** (2**j * q)) % odd_integer == odd_integer - 1:
                inconclusive = True
                break

        if not inconclusive:
            return False

    return True


# Show Result
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
print("The prob of error is < (1/4)^t = 0.09765625%")
print("Compare to https://primes.utm.edu/lists/small/10000.txt")
print()


#!##################################################################
#! Q3 - RSA & ECC
#!##################################################################
# * library: https://pypi.org/project/cryptography/
# * doc: https://cryptography.io/en/latest/hazmat/primitives/


# ? 3.a. RSA


# Variables and algo setting
key_size = 1024 * 2
e = 65537
message_bytes = b"466921883457309"
message_int = 466921883457309
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

# Encryption with "Cryptography" library
RSA_LIB_ENCRYPT_START = time.perf_counter()
ciphertext_bytes = public_key.encrypt(plaintext=message_bytes, padding=oaep)
RSA_LIB_ENCRYPT_END = time.perf_counter()
RSA_LIB_ENCRYPT_TIME = RSA_LIB_ENCRYPT_END - RSA_LIB_ENCRYPT_START

# Encryption using algo seen in class
RSA_MAN_ENCRYPT_START = time.perf_counter()
ciphertext_int = pow(base=message_int, exp=e, mod=n)
RSA_MAN_ENCRYPT_END = time.perf_counter()
RSA_MAN_ENCRYPT_TIME = RSA_MAN_ENCRYPT_END - RSA_MAN_ENCRYPT_START

# Decryption with "Cryptography" library
RSA_LIB_DECRYPT_START = time.perf_counter()
plaintext_bytes = private_key.decrypt(ciphertext=ciphertext_bytes, padding=oaep)
RSA_LIB_DECRYPT_END = time.perf_counter()
RSA_LIB_DECRYPT_TIME = RSA_LIB_DECRYPT_END - RSA_LIB_DECRYPT_START

# Decryption using CRT
RSA_MAN_CRT_DECRYPT_START = time.time()
vp = pow(ciphertext_int, d % (p - 1), p)
vq = pow(ciphertext_int, d % (q - 1), q)
xp = q * pow(q, -1, p)
xq = p * pow(p, -1, q)
plaintext_int_crt = (vp * xp + vq * xq) % n
RSA_MAN_CRT_DECRYPT_END = time.time()
RSA_MAN_CRT_DECRYPT_TIME = RSA_MAN_CRT_DECRYPT_END - RSA_MAN_CRT_DECRYPT_START

# Decryption using algo seen in class
RSA_MAN_DECRYPT_START = time.perf_counter()
plaintext_int = pow(base=ciphertext_int, exp=d, mod=n)
RSA_MAN_DECRYPT_END = time.perf_counter()
RSA_MAN_DECRYPT_TIME = RSA_MAN_DECRYPT_END - RSA_MAN_DECRYPT_START


# Show Result
print()
print("------------")
print("QUESTION 3 A")
print("------------")
print()
print(f"Encryption with Cryptography Library; Time to compute: {RSA_LIB_ENCRYPT_TIME}")
print(f"Encryption with Python Pow;           Time to compute: {RSA_MAN_ENCRYPT_TIME}")
print(
    f"Decryption with Cryptography Library: {plaintext_bytes} \n{'':<38}Time to compute: {RSA_LIB_DECRYPT_TIME}"
)
print(
    f"Decryption with Python Pow and CRT:   {plaintext_int_crt} \n{'':<38}Time to compute: {RSA_MAN_CRT_DECRYPT_TIME}"
)
print(
    f"Decryption with Python Pow:           {plaintext_int} \n{'':<38}Time to compute: {RSA_MAN_DECRYPT_TIME}"
)
print()


# ? 3.b. ECC

ECDH_START_TIME = time.perf_counter()
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
ECDH_END_TIME = time.perf_counter()
ECDH_TIME = ECDH_END_TIME - ECDH_START_TIME


DH_START_TIME = time.perf_counter()
# DH parameters
parameters = dh.generate_parameters(generator=2, key_size=2048)
parameter_numbers = parameters.parameter_numbers()
p = parameter_numbers.p
g = parameter_numbers.g
q = parameter_numbers.q
# Alice DH
alice_dh_private_key = parameters.generate_private_key()
alice_dh_private_numbers = alice_dh_private_key.private_numbers()
alice_dh_public_key = alice_dh_private_key.public_key()
alice_dh_public_numbers = alice_dh_public_key.public_numbers()
alice_dh_private_value = alice_dh_private_numbers.x
alice_dh_public_value = alice_dh_public_numbers.y
# Bob DH
bob_dh_private_key = parameters.generate_private_key()
bob_dh_private_numbers = bob_dh_private_key.private_numbers()
bob_dh_public_key = bob_dh_private_key.public_key()
bob_dh_public_numbers = bob_dh_public_key.public_numbers()
bob_dh_private_value = bob_dh_private_numbers.x
bob_dh_public_value = bob_dh_public_numbers.y
# DH exchange
alice_dh_shared_key = alice_dh_private_key.exchange(peer_public_key=bob_dh_public_key)
bob_dh_shared_key = bob_dh_private_key.exchange(peer_public_key=alice_dh_public_key)
DH_END_TIME = time.perf_counter()
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
print(f"Computing time of s with ECDH (key_size=256, security=128bits): {ECDH_TIME}")
print(f"Computing time of s with DH  (key_size=2048, security=112bits): {DH_TIME}")
print()
print("ECDH 256key_size = 128 bit security")
print("ECDH 224key_size = 112 bit security")
print("DH 2048key_size = 112 bit security")
print()
