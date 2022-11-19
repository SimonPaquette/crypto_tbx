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
    """
    Convert an integer to a bytes

    Args:
        int_val (int): an integer

    Returns:
        bytes: the integer in a bytes format
    """
    byteorder = "big"
    bytes_len = math.ceil(int_val.bit_length() / 8)
    bytes_val = int_val.to_bytes(bytes_len, byteorder)
    return bytes_val


def to_int(bytes_val: bytes) -> int:
    """
    Convert a bytes to an integer

    Args:
        bytes_val (bytes): a bytes

    Returns:
        int: the bytes in int format
    """
    byteorder = "big"
    int_val = int.from_bytes(bytes_val, byteorder)
    return int_val


def xor(bytes1: bytes, bytes2: bytes) -> bytes:
    """
    Bitwise XOR apply to a pair of bytes
    This built-in bitwise (^) operator is only useable for integer

    Args:
        bytes1 (bytes): bytes value 1
        bytes2 (bytes): bytes value 2

    Returns:
        bytes: XOR bytes value
    """
    int1, int2 = to_int(bytes1), to_int(bytes2)
    int_output = int1 ^ int2
    bytes_output = to_bytes(int_output)
    return bytes_output


def hmac_sha_512(k: bytes, m: bytes) -> str:
    """
    Implementation of HMAC using SHA-512

    Args:
        k (bytes): secret key
        m (bytes): message input

    Returns:
        str: the hexdigest of the message
    """
    # Define system parameters
    H = sha512
    block_size = 128
    ipad = b"\x36" * block_size
    opad = b"\x5C" * block_size

    # key padding
    k = k.ljust(block_size, b"\0")

    # Algo
    ipad_xor = xor(k, ipad)
    concat_msg = ipad_xor + m
    inner_hash = H(concat_msg)
    opad_xor = xor(k, opad)
    concat_all = opad_xor + inner_hash.digest()
    outer_hash = H(concat_all)

    return outer_hash.hexdigest()


# Define param
m = b"I am using this input string to test my own implementation of HMAC-SHA-512."
k = b"A new totally random, secure and secret key!"

# Implementation
lib_hmac = hmac.new(k, m, sha512).hexdigest()
my_hmac = hmac_sha_512(k, m)

# Show Result
print()
print("----------")
print("QUESTION 1")
print("----------")
print()
print("Message:", m)
print("Key:    ", k)
print()
print("Result from hmac library:")
print(lib_hmac)
print()
print("Result from my own implementation:")
print(my_hmac)
print()


#!##################################################################
#! Q2 - DSA
#!##################################################################


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

        # get a list of 160-bits prime to be checked for valid parameters
        q_list = sympy.primerange(
            2 ** (DSA.prime_q_bit_length - 1), 2**DSA.prime_q_bit_length
        )

        for q_tmp in q_list:

            # get a random p value of 1024 bits from a random q
            # HERE: get a value where q divide p-1
            # easier to do this way, instead of trying to find a q that divide p-1
            p_tmp = q_tmp * 2 ** (DSA.prime_p_bit_length - DSA.prime_q_bit_length) + 1

            # test that p is prime
            if not sympy.isprime(p_tmp):
                continue

            # HERE: test that q^2 does not divide p-1
            if (p_tmp - 1) % (q_tmp**2) == 0:
                continue

            # if the code run this, that means the previous condition were passed
            # and that we correctly identify prime p and prime q
            p = p_tmp
            q = q_tmp
            break

        self.p = p
        self.q = q

    def set_generator(self):

        if self.h is None:
            self.h = random.randint(2, self.p - 1)

        # set generator of the form: g = h^((p-1)/q) mod q
        g = -1
        while g <= 1:
            g = pow(base=self.h, exp=(self.p - 1) // self.q, mod=self.p)
        self.g = g

    def set_private_key(self):

        self.x = random.randint(2, self.q - 1)

    def set_public_key(self):

        # set public key as y = g^x mod p
        self.y = pow(base=self.g, exp=self.x, mod=self.p)

    def sign(self, message: int, k: int = None) -> tuple[int, int]:

        if k is not None:
            assert k > 1 and k < self.q - 1
        else:
            k = random.randint(2, self.q - 1)

        # calculate r = (g^k mod p) mod q
        r = pow(base=self.g, exp=k, mod=self.p) % self.q

        # calculate s = ([H(m) +xr] k^-1) mod q
        inner_hash = DSA.hash_fun(to_bytes(message)).digest()
        xr = self.x * r
        k_inv = pow(k, -1, self.q)
        concat = to_int(inner_hash) + (xr)
        mult = concat * k_inv
        s = mult % self.q

        # generate signature
        return (r, s)

    def verify(self, signature: tuple[int, int], message: int) -> bool:

        r, s = signature

        # algo
        s_inv = pow(s, -1, self.q)
        hash_m = to_int(DSA.hash_fun(to_bytes(message)).digest())
        u1 = (hash_m * s_inv) % self.q
        u2 = (r * s_inv) % self.q

        # validation step
        g_u1 = pow(self.g, u1, self.p)
        y_u2 = pow(self.y, u2, self.p)
        validation = ((g_u1 * y_u2) % self.p) % self.q

        return validation == r


# Define param
m = 522346828557612
k = 12345

# Implementation
dsa = DSA()
signature = dsa.sign(m, k)
verification = dsa.verify(signature, m)

# Show Result
print()
print("----------")
print("QUESTION 2")
print("----------")
print()
print("Bit lenght prime p =", dsa.p.bit_length())
print("Bit lenght prime q =", dsa.q.bit_length())
print()
print("Signature 1:", signature)
print("Valid signature:", verification)
print()


#!##################################################################
#! Q3 - DSA SECURITY
#!##################################################################


def find_k(m1: int, m2: int, s1: int, s2: int, q: int) -> int:
    """
    From 2 signatures that use the same unknown secret number k,
    extract the secret number k

    Args:
        m1 (int): first message
        m2 (int): seconde message
        s1 (int): s part of the first message's signature
        s2 (int): s part of the second message's signature
        q (int): public prime q

    Returns:
        int: found secret number k
    """
    hash_m1 = to_int(DSA.hash_fun(to_bytes(m1)).digest())
    hash_m2 = to_int(DSA.hash_fun(to_bytes(m2)).digest())
    found_k = ((hash_m1 - hash_m2) * (pow(s1 - s2, -1, q))) % q
    return found_k


def find_x(k: int, m: int, signature: tuple[int, int], q: int) -> int:
    """
    With a know secret number k, extract the private key

    Args:
        k (int): secret dsa number
        m (int): message
        signature (tuple[int, int]): message's signature (r,s)
        q (int): public prime q

    Returns:
        int: found private key x
    """
    r, s = signature
    hash_m = to_int(DSA.hash_fun(to_bytes(m)).digest())
    found_x = ((k * s - hash_m) * (pow(r, -1, q))) % q
    return found_x


# Define param
m2 = 8161474912883
signature_2 = dsa.sign(m2, k)

# Implementation
found_k = find_k(m, m2, signature[1], signature_2[1], dsa.q)
found_x = find_x(found_k, m2, signature_2, dsa.q)

# Show Result
print()
print("----------")
print("QUESTION 3")
print("----------")
print()
print("Signature 2:", signature_2)
print()
print("Is found k equal to the k used?", found_k == k)
print("Is found x equal to the x used?", found_x == dsa.x)
print()


#!##################################################################
#! Q4 - HASH FUNCTION & BLOCK CIPHER
#!##################################################################

# Answer in the pdf
