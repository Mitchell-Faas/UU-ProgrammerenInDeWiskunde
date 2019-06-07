# To-do:    How do I add integers to fractions etc?
#           Is it okay to use in-place modification for binary operations?

class breuk:
    def euclidesalg(self, a, b):
        while a > 0 and b > 0:
            if a > b:
                a -= b
            else:
                b -= a
        return a


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
        numerator = -self.numerator
        return breuk(numerator, self.denominator)
    def __pos__(self):
        numerator = +self.numerator
        return breuk(numerator,self.denominator)
    def __abs__(self):
        numerator = abs(self.numerator)
        return breuk(numerator,self.denominator)

    # Binary arithmetic operations
    # a/b + c/d = (ad + cb) / bd
    def __add__(self, other):
        numerator, denominator = self.numerator*other.denominator + other.numerator*self.denominator , self.denominator*other.denominator
        output = breuk(numerator,denominator)
        output.normalize()
        return output
    # a/b - c/d = (ad - cb) / bd
    def __sub__(self, other):
        numerator , denominator = self.numerator*other.denominator - other.numerator*self.denominator , self.denominator*other.denominator
        output = breuk(numerator,denominator)
        output.normalize()
        return output
    # a/b * c/d = ac / bd
    def __mul__(self, other):
        numerator , denominator = self.numerator*other.numerator , self.denominator*other.denominator
        output = breuk(numerator,denominator)
        output.normalize()
        return output
    # a/b / c/d = ad / bc
    def __truediv__(self, other):
        numerator , denominator = self.numerator*other.denominator , self.denominator*other.numerator
        output = breuk(numerator,denominator)
        output.normalize()
        return output

    # Binary arithmetic operations, reversed
    # a/b + c/d = (ad + cb) / bd
    def __radd__(self, other):
        numerator , denominator = other.numerator*self.denominator + self.numerator*other.denominator , other.denominator*self.denominator
        output = breuk(numerator,denominator)
        output.normalize()
        return output
    # a/b - c/d = (ad - cb) / bd
    def __rsub__(self, other):
        numerator , denominator = other.numerator*self.denominator - self.numerator*other.denominator , other.denominator*self.denominator
        output = breuk(numerator,denominator)
        output.normalize()
        return output
    # a/b * c/d = ac / bd
    def __rmul__(self, other):
        numerator , denominator = other.numerator*self.numerator , other.denominator*self.denominator
        output = breuk(numerator,denominator)
        output.normalize()
        return output
    # a/b / c/d = ad / bc
    def __rtruediv__(self, other):
        numerator , denominator = other.numerator*self.denominator , other.denominator*self.numerator
        output = breuk(numerator,denominator)
        output.normalize()
        return output

    # Casting to integer and float
    def __int__(self):
        return int(self.numerator / self.denominator)
    def __float__(self):
        return float(self.numerator / self.denominator)

    # Deel beide argumenten door hun grootste gemene deler
    def normalize(self):
        a = abs(max(self.numerator,self.denominator))
        b = abs(min(self.numerator, self.denominator))

        # Gives largest common divisor of a and b
        lcd = self.euclidesalg(a,b)
        self.numerator = self.numerator // lcd
        self.denominator = self.denominator // lcd



