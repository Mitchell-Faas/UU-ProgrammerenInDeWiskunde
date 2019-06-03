# To-do:    How do I add integers to fractions etc?
#           Is it okay to use in-place modification for binary operations?

class breuk:
    def __init__(self, numerator=0, denominator=1):
        self.numerator = numerator
        self.denominator = denominator
    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)
    # x<y
    def __lt__(self,other):
        if self.numerator/self.denominator < other.numerator/other.denominator:
            return True
        else:
            return False
    # x<=y
    def __le__(self,other):
        if self.numerator/self.denominator <= other.numerator/other.denominator:
            return True
        else:
            return False
    # x==y
    def __eq__(self,other):
        if self.numerator == other.numerator and self.denominator == other.denominator:
            return True
        else:
            return False
    # x!=y
    def __ne__(self,other):
        if self.numerator == other.numerator and self.denominator == other.denominator:
            return False
        else:
            return True
    # x>y
    def __gt__(self,other):
        if self.numerator/self.denominator > other.numerator/other.denominator:
            return True
        else:
            return False
    # x>=y
    def __ge__(self,other):
        if self.numerator/self.denominator >= other.numerator/other.denominator:
            return True
        else:
            return False

    # Unary arithmetic operations
    def __neg__(self):
        self.numerator = -self.numerator
        return self
    def __pos__(self):
        self.numerator = +self.numerator
        return self
    def __abs__(self):
        self.numerator = abs(self.numerator)
        return self

    # Binary arithmetic operations
    # a/b + c/d = (ad + cb) / bd
    def __add__(self, other):
        self.numerator , self.denominator = self.numerator*other.denominator + other.numerator*self.denominator , self.denominator*other.denominator
        self.normalize()
        return self
    # a/b - c/d = (ad - cb) / bd
    def __sub__(self, other):
        self.numerator , self.denominator = self.numerator*other.denominator - other.numerator*self.denominator , self.denominator*other.denominator
        self.normalize()
        return self
    # a/b * c/d = ac / bd
    def __mul__(self, other):
        self.numerator , self.denominator = self.numerator*other.numerator , self.denominator*other.denominator
        self.normalize()
        return self
    # a/b / c/d = ad / bc
    def __truediv__(self, other):
        self.numerator , self.denominator = self.numerator*other.denominator , self.denominator*other.numerator
        self.normalize()
        return self

    # Binary arithmetic operations, reversed
    # a/b + c/d = (ad + cb) / bd
    def __radd__(self, other):
        self.numerator , self.denominator = other.numerator*self.denominator + self.numerator*other.denominator , other.denominator*self.denominator
        self.normalize()
        return self
    # a/b - c/d = (ad - cb) / bd
    def __rsub__(self, other):
        self.numerator , self.denominator = other.numerator*self.denominator - self.numerator*other.denominator , other.denominator*self.denominator
        self.normalize()
        return self
    # a/b * c/d = ac / bd
    def __rmul__(self, other):
        self.numerator , self.denominator = other.numerator*self.numerator , other.denominator*self.denominator
        self.normalize()
        return self
    # a/b / c/d = ad / bc
    def __rtruediv__(self, other):
        self.numerator , self.denominator = other.numerator*self.denominator , other.denominator*self.numerator
        self.normalize()
        return self

    # Casting to integer and float
    def __int__(self):
        return int(self.numerator / self.denominator)
    def __float__(self):
        return float(self.numerator / self.denominator)

    # Deel beide argumenten door hun grootste gemene deler
    def normalize(self):
        a = max(self.numerator,self.denominator)
        b = min(self.numerator, self.denominator)

        def euclidesalg(a,b):
            while a >= b:
                a -= b

            if a == 0:
                return b
            else:
                return euclidesalg(b,a)
        # Gives largest common divisor of a and b
        lcd = euclidesalg(a,b)
        self.numerator = self.numerator // lcd
        self.denominator = self.denominator // lcd



