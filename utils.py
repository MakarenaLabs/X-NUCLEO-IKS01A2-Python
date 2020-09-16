def twoComplements(reg1, reg2):
    # Simple function to elaborate simple 2-Complements using 2 values/registers without any external library
    n = reg1 << 8 | reg2

    if bin(n).startswith('0b1') and len(bin(n))-2 == 16:
        # negate n
        n = n - 0b1111111111111111
        # reduce n
        n = n - 1
        return n

    return n
