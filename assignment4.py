"""
Simon Paquette
300044038
CSI 4108
Assignment 4

Before executing the python file, need to install the Sympy library (https://www.sympy.org/en/index.html):
    pip install sympy
    or
    conda install sympy
"""

import hmac
import math
import random
from hashlib import sha1, sha512

import sympy

#!##################################################################
#! Q1 - HMAC-SHA-512
#!##################################################################


def to_bytes(int_val: int) -> bytes:
    byteorder = "big"
    bytes_len = math.ceil(int_val.bit_length() / 8)
    bytes_val = int_val.to_bytes(bytes_len, byteorder)
    return bytes_val


def to_int(bytes_val: bytes) -> int:
    byteorder = "big"
    int_val = int.from_bytes(bytes_val, byteorder)
    return int_val


def xor(bytes1: bytes, bytes2: bytes) -> bytes:
    int1, int2 = to_int(bytes1), to_int(bytes2)
    int_output = int1 ^ int2
    bytes_output = to_bytes(int_output)
    return bytes_output


def hmac_sha_512(k: bytes, m: bytes) -> str:
    H = sha512
    block_size = 128
    ipad = b"\x36" * block_size
    opad = b"\x5C" * block_size
    k = k.ljust(block_size, b"\0")

    ipad_xor = xor(k, ipad)
    concat_msg = ipad_xor + m
    inner_hash = H(concat_msg)
    opad_xor = xor(k, opad)
    concat_all = opad_xor + inner_hash.digest()
    outer_hash = H(concat_all)
    return outer_hash.hexdigest()


m = b"I am using this input string to test my own implementation of HMAC-SHA-512."
k = b"A new totally random and secret key!"


# Show Result
print()
print("----------")
print("QUESTION 1")
print("----------")
print()
print("Result from hmac library:")
print(hmac.new(k, m, sha512).hexdigest())
print()
print("Result from my own implementation:")
print(hmac_sha_512(k, m))
print()


#!##################################################################
#! Q2 - DSA
#!##################################################################

exit()


class DSA:
    prime_p_bit_length = 1024
    prime_q_bit_length = 160
    hash_fun = sha1

    def __init__(
        self,
        p: int = None,
        q: int = None,
        h: int = None,
        g: int = None,
        x: int = None,
        y: int = None,
    ):

        if p is None or q is None:
            self.set_primes()
        else:
            self.p = p
            self.q = q

        self.h = h

        if g is None:
            self.set_generator()

        if x is None:
            self.set_private_key()

        if y is None:
            self.set_public_key()

    def set_primes(self):
        q_list = sympy.primerange(
            2 ** (DSA.prime_q_bit_length - 1), 2**DSA.prime_q_bit_length
        )

        for q_tmp in q_list:

            # get a random p value of 1024 bits from a random q
            # HERE: prove that q divide p-1
            p_tmp = q_tmp * 2 ** (DSA.prime_p_bit_length - DSA.prime_q_bit_length) + 1

            # test that p is prime
            if not sympy.isprime(p_tmp):
                continue

            # HERE: test that q^2 does not divide p-1
            if (p_tmp - 1) % (q_tmp**2) == 0:
                continue

            p = p_tmp
            q = q_tmp

            break

        self.p = p
        self.q = q

    def set_generator(self):

        if self.h is None:
            self.h = random.randint(2, self.p - 1)

        g = -1
        while g <= 1:
            g = pow(base=self.h, exp=(self.p - 1) // self.q, mod=self.p)
        self.g = g

    def set_private_key(self):
        self.x = random.randint(2, self.q - 1)

    def set_public_key(self):
        self.y = pow(base=self.g, exp=self.x, mod=self.p)

    def sign(self, message, k: int = None) -> tuple:

        if k is not None:
            assert k > 1 and k < self.q - 1
        else:
            k = random.randint(2, self.q - 1)

        r = pow(base=self.g, exp=k, mod=self.p) % self.q

        k_1 = pow(k, -1, self.q)
        # k_1 = k_1.to_bytes(k_1.bit_length() // 8 + 1, "big")
        xr = self.x * r
        xr = xr.to_bytes(xr.bit_length() // 8 + 1, "big")
        s = (
            int.from_bytes((DSA.hash_fun(message).digest() + xr), "big") * k_1
        ) % self.q

        return (r, s)

    def verify(self, signature: tuple, message) -> bool:
        s_1 = pow(signature[1], -1, self.q)
        u1 = (int.from_bytes(DSA.hash_fun(message).digest(), "big") * s_1) % self.q
        u2 = (signature[0] * s_1) % self.q
        validation = (
            pow(self.g, u1, self.p) * pow(self.y, u2, self.p) % self.p
        ) % self.q
        return validation == signature[0]


m = b"522346828557612"
dsa = DSA()
k = 1234567

signature = dsa.sign(m, k)
print("Signature:", signature)
verification = dsa.verify(signature, m)
print("Valid sign:", verification)

#!##################################################################
#! Q3 - DSA SECURITY
#!##################################################################

m2 = b"8161474912883"  # convert int to byte instead
signature_2 = dsa.sign(m2, k)
print("Signature_2:", signature_2)


#!##################################################################
#! Q4 - HASH FUNCTION & BLOCK CIPHER
#!##################################################################
