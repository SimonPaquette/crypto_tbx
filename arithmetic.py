import utils


class PolynomialArithmetic:
    @classmethod
    def list_to_poly(cls, poly: list) -> str:
        power = len(poly)
        poly_str = ""
        for i in poly:
            power -= 1

            if i != 1 or power == 0:
                poly_str += f"{i}"
            if power > 1:
                poly_str += f"x^{power} + "
            elif power == 1:
                poly_str += "x + "

        return poly_str

    @classmethod
    def add(cls, field: int, poly1: list, poly2: list) -> list:
        result = [(x + y) % field for x, y in zip(poly1, poly2)]
        return result

    @classmethod
    def substract(cls, field: int, poly1: list, poly2: list) -> list:
        result = [(x - y) % field for x, y in zip(poly1, poly2)]
        return result

    @classmethod
    def find_multiplier(cls, field: int, multiplicand: int, product: int) -> int:
        for multiplier in range(field):
            if (multiplicand * multiplier) % field == product:
                return multiplier
        return 1

    @classmethod
    def multiply_by_int(cls, field: int, polynomial: list, integer: int) -> list:
        result = [(x * integer) % field for x in polynomial]
        return result

    @classmethod
    def multiply(cls, field: int, poly1: list, poly2: list) -> list:

        bits = []
        for y_index, y in enumerate(reversed(poly2)):
            bit = (
                [0] * (len(poly2) - y_index - 1)
                + [(x * y) % field for x in poly1]
                + [0] * y_index
            )
            bits.append(bit)

        result = bits[0]
        for bit in bits[1:]:
            result = cls.add(field, result, bit)

        return result

    @classmethod
    def print_pipeline(
        cls, multiplier, power, divisor, dividend, multiplication, substraction
    ):
        str_multiplier = cls.list_to_poly([multiplier] + [0] * power).split("+")[0]
        str_divisor = cls.list_to_poly(divisor)
        str_dividend = cls.list_to_poly(dividend)
        str_multiplication = cls.list_to_poly(multiplication)
        str_substraction = cls.list_to_poly(substraction)
        len_divisor = len(str_divisor)
        len_dividend = len(str_dividend)
        len_first_number = len(str_dividend.split("+")[0]) + 4

        print()
        print(" " * len_divisor, str_multiplier)
        print(" " * len_divisor, "-" * (len_dividend + 2))
        print(str_divisor, "|", str_dividend)
        print(" " * (len_divisor + 2), str_multiplication)
        print(" " * (len_divisor + 2), "-" * len_dividend)
        print(" " * (len_divisor + len_first_number), str_substraction)
        print()

    @classmethod
    def div_pipeline(
        cls, field: int, dividend: list, divisor: list, calc_gcd: bool = True
    ) -> None:

        if len(dividend) == 1:
            print("GCD =", cls.list_to_poly(divisor))
            return

        if len(dividend) == len(divisor) - 1:
            if not calc_gcd:
                return
            print("-------------------------------------")
            cls.div_pipeline(field, divisor, dividend, calc_gcd)
            return

        multiplier = cls.find_multiplier(field, divisor[0], dividend[0])
        power = len(dividend) - len(divisor)
        multiplication = cls.multiply_by_int(field, divisor, multiplier)
        multiplication += [0] * power
        substraction = cls.substract(field, dividend, multiplication)
        substraction = substraction[1:]

        cls.print_pipeline(
            multiplier, power, divisor, dividend, multiplication, substraction
        )

        cls.div_pipeline(field, substraction, divisor, calc_gcd)


class NumeralArithmetic:
    @classmethod
    def print_euclidean(cls, iterations: list) -> None:

        for iteration in iterations:
            msg = "{} = {}({}) + {}"
            print(msg.format(*iteration))

    @classmethod
    def print_ext_euclidean(cls, iterations: list) -> None:
        for iteration in iterations:
            msg = "1 = {}({})+{}({})"
            print(msg.format(*iteration))

    @classmethod
    def euclidean(cls, n: int, modulo: int) -> list:

        iterations = [(modulo, n, modulo // n, modulo % n)]

        iteration = iterations[-1]
        while iteration[3] != 1:
            modulo = iteration[1]
            n = iteration[3]
            iteration = (modulo, n, modulo // n, modulo % n)
            iterations.append(iteration)
        return iterations

    @classmethod
    def ext_euclidean(cls, euclidean: list) -> list:

        iterations = [(0, 0, 0, 1)]

        for elem in reversed(euclidean):
            iteration = (
                elem[0],
                iterations[-1][3],
                elem[1],
                -elem[2] * iterations[-1][3] + iterations[-1][1],
            )
            iterations.append(iteration)
        return iterations[1:]

    @classmethod
    def find_inverse(cls, n: int, modulo: int, pprint: bool = True) -> int:
        euclidean_step = cls.euclidean(n, modulo)
        ext_euclidean_step = cls.ext_euclidean(euclidean_step)
        last_step = ext_euclidean_step[-1]
        inverse = last_step[3] % last_step[0]
        if pprint:
            cls.print_euclidean(euclidean_step)
            print("--------------------")
            cls.print_ext_euclidean(ext_euclidean_step)
            print("--------------------")
            print(f"1+{last_step[0]}(-{last_step[1]}) = {last_step[2]}({last_step[3]})")
            print(f"1 mod {last_step[0]} = {last_step[2]}({last_step[3]})")
            print(f"{last_step[2]}^-1 = {inverse} mod {last_step[0]}")
            print()
        return inverse

    @classmethod
    def chinese_remainder(cls, M: int) -> list:

        primes = utils.prime_factors(M)
        c_val = []
        for index1, prime1 in enumerate(primes):
            val = 1
            for index2, prime2 in enumerate(primes):
                if index1 != index2:
                    val *= prime2
            if val % prime1 != 1:
                inverse = NumeralArithmetic.find_inverse(val, prime1, pprint=False)
                val *= inverse
            c_val.append(val)
        # print(f"PRIMES: {primes} => C VAL: {c_val}")
        return (primes, c_val)

    @classmethod
    def to_tuple_repr(cls, M: int, num: int) -> list:
        tuple_val = []
        primes, _ = cls.chinese_remainder(M)
        for prime in primes:
            tuple_val.append(num % prime)
        return tuple_val

    @classmethod
    def from_tuple_repr(cls, M: int, tup: list) -> int:
        _, c_vals = cls.chinese_remainder(M)
        num = 0
        for index, c_val in enumerate(c_vals):
            num += c_val * tup[index]
        return num % M


NumeralArithmetic.chinese_remainder(2431)
print(NumeralArithmetic.to_tuple_repr(2431, 593))
a = NumeralArithmetic.to_tuple_repr(2431, 1813)
print(NumeralArithmetic.from_tuple_repr(2431, a))
