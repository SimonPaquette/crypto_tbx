import pandas as pd


class FiniteField:
    def __init__(self, elems: list):
        self.elems = elems

    def _test_closure(self, operator: str) -> bool:
        elems = self.elems
        for a in elems:
            for b in elems:
                if operator == "+":
                    if a + b not in elems:
                        return False
                if operator == "*":
                    if a * b not in elems:
                        return False
        return True

    def _test_associativity(self, operator: str) -> bool:
        elems = self.elems
        for a in elems:
            for b in elems:
                for c in elems:
                    if operator == "+":
                        if a + (b + c) != (a + b) + c:
                            return False
                    if operator == "*":
                        if a * (b * c) != (a * b) * c:
                            return False
        return True

    def _test_identity(self, operator: str) -> bool:
        elems = self.elems
        cond = 0
        for a in elems:
            for e in elems:
                if operator == "+":
                    if a + e == e + a and a + e == a:
                        cond += 1
                        break
                if operator == "*":
                    if a * e == e * a and a * e == a:
                        cond += 1
                        break
        return cond == len(elems)

    def _test_inverse(self, operator: str) -> bool:
        elems = self.elems
        cond = 0
        for a in elems:
            for e in elems:
                if operator == "+":
                    if a + e == 0:
                        cond += 1
                        break
                if operator == "*":
                    if a * e == 1:
                        cond += 1
                        break
        return cond == len(elems)

    def _test_commutativity(self, operator: str) -> bool:
        elems = self.elems

        for a in elems:
            for b in elems:
                if operator == "+":
                    if a + b != b + a:
                        return False
                if operator == "*":
                    if a * b != b * a:
                        return False
        return True

    def _test_distributivity(self) -> bool:
        elems = self.elems
        for a in elems:
            for b in elems:
                for c in elems:
                    if a * (b + c) != a * b + a * c:
                        return False
        return True

    def _test_no_zero_divisor(self) -> bool:
        elems = self.elems
        for a in elems:
            for b in elems:
                if a * b == 0:
                    if a != 0 and b != 0:
                        return False
        return True

    def is_group(self) -> bool:
        group = (
            self._test_closure("+")
            and self._test_associativity("+")
            and self._test_identity("+")
            and self._test_inverse("+")
        )
        return group

    def is_abelian_group(self) -> bool:
        abelian_group = self.is_group() and self._test_commutativity("+")
        return abelian_group

    def is_ring(self) -> bool:
        ring = (
            self.is_abelian_group()
            and self._test_closure("*")
            and self._test_associativity("*")
            and self._test_distributivity()
        )
        return ring

    def is_commutative_ring(self) -> bool:
        commutative_ring = self.is_ring() and self._test_commutativity("*")
        return commutative_ring

    def is_integral_domain(self) -> bool:
        integral_domain = (
            self.is_commutative_ring()
            and self._test_identity("*")
            and self._test_no_zero_divisor()
        )
        return integral_domain

    def is_field(self) -> bool:
        field = self.is_integral_domain() and self._test_identity("*")


def print_all(df: pd.DataFrame) -> None:
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    print(df)
    pd.reset_option("display.max_rows", None)
    pd.reset_option("display.max_columns", None)


def primitive_roots(modulo: int) -> pd.DataFrame:

    data = {"a": list(range(1, modulo))}

    for power in range(2, modulo):
        col_name = f"a^{power}"
        values = []
        for value in range(1, modulo):
            values.append((value**power) % modulo)
        data[col_name] = values

    df = pd.DataFrame(data).set_index("a")

    return df


def list_to_poly(poly: list) -> str:
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


def find_multiplier(field: int, multiplicand: int, product: int) -> int:
    for multiplier in range(field):
        if (multiplicand * multiplier) % field == product:
            return multiplier
    return None


def multiply(field: int, polynomial: list, integer: int) -> list:
    result = [(x * integer) % field for x in polynomial]
    return result


def substract(field: int, poly1: list, poly2: list) -> list:
    result = [(x - y) % field for x, y in zip(poly1, poly2)]
    return result


def print_pipeline(multiplier, power, divisor, dividend, multiplication, substraction):
    str_multiplier = list_to_poly([multiplier] + [0] * power).split("+")[0]
    str_divisor = list_to_poly(divisor)
    str_dividend = list_to_poly(dividend)
    str_multiplication = list_to_poly(multiplication)
    str_substraction = list_to_poly(substraction)
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


def div_pipeline(field: int, dividend: list, divisor: list) -> None:

    if len(dividend) == 1:
        print("GCD =", list_to_poly(divisor))
        return

    if len(dividend) == len(divisor) - 1:
        print("-------------------------------------")
        div_pipeline(field, divisor, dividend)
        return

    multiplier = find_multiplier(field, divisor[0], dividend[0])
    power = len(dividend) - len(divisor)
    multiplication = multiply(field, divisor, multiplier)
    multiplication += [0] * power
    substraction = substract(field, dividend, multiplication)
    substraction = substraction[1:]

    print_pipeline(multiplier, power, divisor, dividend, multiplication, substraction)

    div_pipeline(field, substraction, divisor)


FIELD = 101
DIVISOR = [1, 97, 40, 38]
DIVIDEND = [1, 88, 73, 83, 51, 67]

div_pipeline(FIELD, DIVIDEND, DIVISOR)
# print_all(primitive_roots(13))
