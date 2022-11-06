import math
import random

import numpy as np
import pandas as pd


def _bin(dec_val: int, length: int) -> str:
    return format(dec_val, f"0{length}b")


def _dec(bin_val: str) -> int:
    return int(bin_val, 2)


def is_prime(n: int) -> bool:
    assert n > 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def prime_factors(n: int) -> list:

    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n / 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n / i
    if n > 2:
        factors.append(int(n))
    return factors


def phi(n: int) -> int:
    if is_prime(n):
        return n - 1
    primes = prime_factors(n)

    df = pd.value_counts(np.array(primes))

    value = 1
    for prime, power in zip(list(df.index), df.values):
        value *= prime**power - prime ** (power - 1)

    return value


def print_all(df: pd.DataFrame) -> None:
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    print(df)
    pd.reset_option("display.max_rows", None)
    pd.reset_option("display.max_columns", None)


def primitive_roots(modulo: int) -> None:

    data = {"a": list(range(1, modulo))}
    for power in range(2, modulo):
        col_name = f"a^{power}"
        values = []
        for value in range(1, modulo):
            values.append((value**power) % modulo)
        data[col_name] = values

    df = pd.DataFrame(data).set_index("a")

    print_all(df)

    phi_value = phi(modulo)
    roots = []
    for index, val in enumerate(df.index):
        try:
            at_power = df.values[index].tolist().index(1)
            at_power += 2
            if at_power == phi_value:
                roots.append(val)
        except ValueError:
            pass

    print(f"\nThere is {len(roots)} Primitve roots of {modulo}: {roots}")


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


def n_test_miller_rabin(bits: int) -> int:
    return 0.5 * math.log(2**bits)


def discrete_log(base: int, value: int, modulo: int):
    N = None
    if not N:
        N = 1 + int(math.sqrt(modulo))

    # initialize baby_steps table
    baby_steps = {}
    baby_step = 1
    for r in range(N + 1):
        baby_steps[baby_step] = r
        baby_step = baby_step * base % modulo

    # now take the giant steps
    giant_stride = pow(base, (modulo - 2) * N, modulo)
    giant_step = value
    for q in range(N + 1):
        if giant_step in baby_steps:
            return q * N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % modulo
    return "No Match"
