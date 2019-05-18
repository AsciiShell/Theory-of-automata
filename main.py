import sys

bitNumCount = 4
codeBase = [8, 4, 2, 1]
codeAdd = 6
# codeBase = [2,4,2,1]
# codeAdd = 0
print("Configuration: {}{:+d}".format("".join(map(str, codeBase)), codeAdd))


class ColorPrint:

    @staticmethod
    def print_fail(message, end='\n'):
        sys.stdout.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end='\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end='\n'):
        sys.stdout.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end='\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end='\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)


def generate_numbers():
    numb = dict()
    for i in range(2 ** bitNumCount):
        bits = tuple(map(int, "{0:0{width}b}".format(i, width=bitNumCount)))
        val = sum([bits[i] * codeBase[i] for i in range(len(bits))])
        if val not in numb:
            numb[val] = bits
    return numb


def int_to_bits(n):
    return numbers[n % 10 + codeAdd]


def print_matrix(m):
    print()
    for line in m:
        print(*line, sep="\t")


class BitNum:
    def __init__(self, value, extra=None):
        if type(value) == int:
            while value < 0:
                value = 9 - abs(value)
            self.bits = int_to_bits(value)
        elif type(value) == str:
            self.bits = list(map(int, value))
        elif type(value) == list:
            self.bits = value
        else:
            raise TypeError
        if extra is None:
            if len(self.bits) == bitNumCount + 1:
                self.extra = self.bits[-1]
                self.bits = self.bits[:-1]
        self.extra = 0
        assert len(self.bits) == bitNumCount

    def __add__(self, other):
        if type(other) != BitNum:
            raise TypeError
        result = [0] * (bitNumCount + 1)
        for i in range(len(self.bits), 0, -1):
            result[i] += self.bits[i - 1] + other.bits[i - 1]
            if result[i] > 1:
                result[i] -= 2
                result[i - 1] += 1
                # For debugging
        return BitNum(result[1:], result[0])

    def __sub__(self, other):
        if type(other) != BitNum:
            raise TypeError
        result = [0] * (bitNumCount + 1)
        for i in range(len(self.bits), 0, -1):
            result[i] += self.bits[i - 1] - other.bits[i - 1]
            if result[i] > 1:
                result[i] -= 2
                result[i - 1] += 1
                # For debugging
            if result[i] < 0:
                for j in range(i):
                    result[j] += 1
                result[i] += 2
        return BitNum(result[1:], result[0])

    def __str__(self):
        return "{}".format("".join(map(str, self.bits)))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        for i in range(len(self.bits)):
            if self.bits[i] != other.bits[i]:
                return False
        return self.extra == other.extra

    def equal(self, other):
        for i in range(len(self.bits)):
            if self.bits[i] != other.bits[i]:
                return False
        return True

    def print(self, end='\t', nonzero_mark=True):
        if self.bits.count(1) == 0 and not nonzero_mark:
            ColorPrint.print_pass(str(self), end)
        else:
            ColorPrint.print_info(str(self), end)


class Matrix:
    __last_line = None

    def __begin(self, val='', end='\t\t|\t'):
        if type(val) != str:
            val = str(val)
        if self.__last_line != val:
            self.__last_line = val
            ColorPrint.print_info(val, end=end)
        else:
            ColorPrint.print_info('', end=end)

    def print(self, print_int=True, print_bin=True, print_fix=True):
        self.__begin()
        print(*range(10), sep="\t\t")
        print("=" * 90)
        for i in range(10):

            if print_int:
                self.__begin(i)
                for j in range(10):
                    BitNum(i + j).print()
                ColorPrint.print_info('')
            if print_bin:
                self.__begin(i)
                for j in range(10):
                    (BitNum(i) + BitNum(j)).print()
                ColorPrint.print_info('')
            if print_fix:
                self.__begin(i)
                for j in range(10):
                    (BitNum(i + j) - (BitNum(i) + BitNum(j))).print(nonzero_mark=False)
                ColorPrint.print_info('')


numbers = generate_numbers()
if codeBase == [2, 4, 2, 1]:
    numbers[0] = (0, 0, 0, 0)
    numbers[1] = (0, 0, 0, 1)
    numbers[2] = (0, 0, 1, 0)
    numbers[3] = (0, 0, 1, 1)
    numbers[4] = (0, 1, 0, 0)
    numbers[5] = (1, 0, 1, 1)
    numbers[6] = (1, 1, 0, 0)
    numbers[7] = (1, 1, 0, 1)
    numbers[8] = (1, 1, 1, 0)
    numbers[9] = (1, 1, 1, 1)
else:
    print("Check your alphabet!!!")
alphabet = [BitNum(i) for i in range(10)]
print("Alphabet:\n\t", end="")
print(*alphabet, sep="\n\t")
print()
alphabet_ = [BitNum(-i) for i in range(10)]
print("Alphabet neg\nWarning!!!\nNeg Zero works wrong\nAlphabet neg:\n\t", end="")
print(*alphabet_, sep="\n\t")
print()

# Matrix().print(print_int=True)

def big_bit_num(n):
    r = []
    sign = 1 if n >= 0 else -1
    for i in str(abs(n)):
        r.append(BitNum(int(i) * sign))
    return r


def print_big_bit_num(n):
    r = big_bit_num(n)
    s = str(n)
    s += " " * (6 - len(s))
    print(s, *r, sep="\t")


def proc_sum(a, b):
    print_big_bit_num(a)
    print_big_bit_num(b)
    print_big_bit_num(a + b)
    print()


proc_sum(357, 421)
proc_sum(357, -194)
proc_sum(468, -743)
proc_sum(-246, -571)

proc_sum(753, 864)
proc_sum(-642, -428)