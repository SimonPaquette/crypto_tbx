class FiniteField:
    def __init__(self, elems: list, mod: int = None):
        self.elems = elems
        self.mod = mod
        if mod:
            print("The function with modulo is not implemented yet")

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
        return field
