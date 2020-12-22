from math import log

# Functions
def expectation(d):
    """
    Given a non-zero integer, return the probability of a natural number starting with that digit as described by Benford's Law.
    """
    if float(d).is_integer() is False:
        raise TypeError
    else:
        try:
            term = (d+1)/d
            return log(term, 10)
        except ZeroDivisionError as e:
            print(e)
