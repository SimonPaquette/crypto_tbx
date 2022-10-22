from unittest import result


class Blum:
    def __init__(self, pq, seed):
        self.pq = pq
        self.xi = seed
        self.iter = 0

    def next(self):
        result = (self.xi**2) % self.pq
        bit = result % 2

        print(
            f"X{self.iter} = ({self.xi})^2 mod {self.pq} = {result} => b{self.iter} = {bit}"
        )

        self.xi = result
        self.iter += 1

    def generate(self, length):
        for _ in range(length):
            self.next()


P = 911
Q = 991
N = P * Q
SEED = 613

blum = Blum(N, SEED)

blum.generate(15)


# TODO: linear congruential generator
