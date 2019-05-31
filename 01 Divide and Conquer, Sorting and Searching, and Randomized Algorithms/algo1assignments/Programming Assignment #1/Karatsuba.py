def karatsuba(x, y):
    """
    Karatsuba Algorithm for integer multiplication. Modified for more generalized cases.
    Return a string to represent the multiplication result.

    x, y: integers
    """

    if len(str(x)) < len(str(y)):
        x, y = y, x

    if len(str(y)) == 1:
        return x * y
    else:
        m1, m2 = len(str(x))//2, len(str(y))//2
        a, b = str(x)[:m1], str(x)[m1:]
        c, d = str(y)[:m2], str(y)[m2:]
        a, b, c, d = int(a), int(b), int(c), int(d)

        ## Step1: a * c
        step1 = karatsuba(a, c)
        ## Step2: b * d
        step2 = karatsuba(b, d)
        ## Step3: a * d
        step3 = karatsuba(a, d)
        ## Step4: b * c
        step4 = karatsuba(b, c)
        ## Result
        re = step1 * 10**(m1 + m2) + step2 + step3 * 10**(m1) + step4 * 10**(m2)
        return re

if __name__ == "__main__":
    import time
    x = 3141592653589793238462643383279502884197169399375105820974944592
    y = 2718281828459045235360287471352662497757247093699959574966967627
    print(karatsuba(x, y))
    ## output: 8539734222673567065463550869546566658024009975042118184861434467387572312875659028530566081829886466081423120380952806582723184