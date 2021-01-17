from math import log
from random import uniform
from collections import Counter
import numpy

testSmall = [5, 0.321, -2989.2, -0.00001]

testLarge = []

def testData():
    for i in range(0,1000):
        a = uniform(0,1)
        b = 10.0**a
        testLarge.append(b)

# Functions
def benfords(data):
    """
    Given a set of data, extract the significant digits and compare to Benford's Law.
    """
    results = dict()
    sigdigits = fsd(data)
    sigcounts = Counter(sigdigits)

    for i in range(1,10):   #Digits 1-9
        theoretical = expectation(i, position=1)
        empirical = sigcounts[float(i)]/sigdigits.size

        results[str(i)] = [theoretical, empirical]

    return results

    # Current state: first sig digit only. Next, add the ability to choose the starting position and number of digits.

    

def expectation(digit, position=1):
    """
    Given a non-zero integer, return the probability of a natural number starting with that digit as described by Benford's Law.
    """
    if float(digit).is_integer() is False or float(position).is_integer() is False:
        raise TypeError
    else:
        if position == 1:
            try:
                term = (digit+1)/digit
                return log(term, 10)
            except ZeroDivisionError as e:
                print(e)
        if position > 1:
            start = 10**(position-2)
            stop = (10**(position-1))-1

            value = 0
            for i in range(start, stop+1):
                term = 1+(1/((10*i)+digit))
                value += log(term, 10)

            return value

def fsd(data):
    """
    Given a numpy array, list or number, return the first significant digits of that data.
    """
    if type(data) == int:
        if data == 0:
            return "Zero has no first-significant digit. Please ensure your data has no zeros."
    elif type(data) == float:
        if data == 0.0:
            return "Zero has no first-significant digit. Please ensure your data has no zeros."
    elif 0 in data:
        return "Zero has no first-significant digit. Please ensure your data has no zeros."

    return numpy.floor(10**(numpy.log10(numpy.abs(data))-numpy.floor(numpy.log10(numpy.abs(data)))))

def nsd(data, position):
    """
    Given some data and the position of the digit desired, return the digit.
    """
    def np_slicer(a, start, end):
        b = a.view((str,1)).reshape(len(a),-1)[:,start:end]
        return numpy.fromstring(b.tostring(), dtype=(str, end-start))

    if isinstance(data, (float, int)):
        data = numpy.array([data])
    if isinstance(data, list):
        data = numpy.array(data)

    positive = numpy.absolute(data) #remove negative sign

    data_np = []
    for i in positive:
        data_np.append(numpy.format_float_scientific(i, precision=15, unique=False))
        
    data_np = numpy.array(data_np)
    clean_string = numpy.char.replace(data_np, '.', '')
    truncated = np_slicer(clean_string, 0, 14)

    return np_slicer(truncated, position-1, position)


