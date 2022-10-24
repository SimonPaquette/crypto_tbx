from unittest import result


class BBS:
    def __init__(self, pq: int, seed: int):
        self.pq = pq
        self.xi = seed
        self.iter = 0

    def next(self) -> None:
        result = (self.xi**2) % self.pq
        bit = result % 2

        print(
            f"X{self.iter} = ({self.xi})^2 mod {self.pq} = {result} => b{self.iter} = {bit}"
        )

        self.xi = result
        self.iter += 1

    def generate(self, length: int) -> None:
        for _ in range(length):
            self.next()


class LCG:
    def __init__(self, a: int, c: int, mod: int, seed: int):
        self.a = a
        self.c = c
        self.mod = mod
        self.xi = seed
        self.iter = 0

    def next(self) -> None:

        result = (self.a * self.xi) % self.mod

        print(f"X{self.iter} = ({self.a}*{self.xi}) mod {self.mod} = {result}")

        self.xi = result
        self.iter += 1

    def generate(self, length: int) -> None:
        for _ in range(length):
            self.next()
