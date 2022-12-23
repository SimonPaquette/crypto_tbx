"""
Cryptographic pseudo random number generator implementation
"""


class BBS:
    """
    Blum Blum Shub number generator
    """

    def __init__(self, pq: int, seed: int):
        """
        parameters initialization

        Args:
            pq (int): modulo n
            seed (int): a random seed number
        """
        self.pq = pq
        self.xi = seed
        self.iter = 0

    def next(self) -> None:
        """
        generate next number in the PRNG algo
        """
        result = (self.xi**2) % self.pq
        bit = result % 2

        print(
            f"X{self.iter} = ({self.xi})^2 mod {self.pq} = {result} => b{self.iter} = {bit}"
        )

        self.xi = result
        self.iter += 1

    def generate(self, length: int) -> None:
        """
        generate n bit of PRNG

        Args:
            length (int): n bits
        """
        for _ in range(length):
            self.next()


class LCG:
    """linear congruential generator"""

    def __init__(self, a: int, c: int, mod: int, seed: int):
        """
        parameters initialization

        Args:
            a (int): slope
            c (int): constant
            mod (int): modulo n
            seed (int): a random seed number
        """
        self.a = a
        self.c = c
        self.mod = mod
        self.xi = seed
        self.iter = 0

    def next(self) -> None:
        """
        generate next number in the PRNG algo
        """

        result = (self.a * self.xi) % self.mod

        print(f"X{self.iter} = ({self.a}*{self.xi}) mod {self.mod} = {result}")

        self.xi = result
        self.iter += 1

    def generate(self, length: int) -> None:
        """
        generate n bit of PRNG

        Args:
            length (int): n bits
        """
        for _ in range(length):
            self.next()
