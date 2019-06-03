class breuk:
    def __init__(self, top=0, bot=1):
        self.top = top
        self.bot = bot

        self._reduce()

    # Casting

    def __str__(self):
        return str(self.top) + '/' + str(self.bot)

    def __int__(self):
        return self.top // self.bot

    def __float__(self):
        return self.top / self.bot

    # Unary operations

    def __neg__(self):
        return breuk(-self.top, self.bot)

    def __pos__(self):
        return breuk(self.top, self.bot)

    def __abs__(self):
        return breuk(abs(self.top), abs(self.bot))

    def __invert__(self):
        return breuk(top=self.bot, bot=self.top)

    # Binary operations

    def __add__(self, other):
        if type(other) == breuk:
            top = (self.top*other.bot + other.top*self.bot)
            bot = self.bot * other.bot
            return breuk(top, bot)

        if type(other) == int:
            return breuk(self.top + other*self.bot, self.bot)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + -self

    def __mul__(self, other):
        if type(other) == breuk:
            return breuk(self.top*other.top, self.bot*other.bot)
        if type(other) == int:
            return breuk(other*self.top, self.bot)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) == breuk:
            return self.__mul__(~other)  # Inverts other
        if type(other) == int:
            return breuk(self.top, other*self.bot)

    def __rtruediv__(self, other):
        # Type must be int
        if type(other) == int:
            return breuk(top=other * self.bot, bot=self.top)
        return

    # Comparisons

    def __gt__(self, other):
        return float(self) > float(other)

    def __ge__(self, other):
        return float(self) >= float(other)

    def __eq__(self, other):
        return float(self) == float(other)

    def __ne__(self, other):
        return float(self) != float(other)

    def __le__(self, other):
        return float(self) <= float(other)

    def __lt__(self, other):
        return float(self) < float(other)

    # Helper functions

    def _reduce(self):
        div = self._find_GCD(self.top, self.bot)
        self.top //= div
        self.bot //= div

    def _find_GCD(self, a, b):
        a, b = abs(a), abs(b)

        while a > 0 and b > 0:
            if a >= b:
                a -= b
            else:
                b -= a

        return b


if __name__ == '__main__':
    p = breuk(2, 3)
    q = breuk(123, 456)
    r = 2-p
    print(r)
    print(abs(r))
    print(float(r))
