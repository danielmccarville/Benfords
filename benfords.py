from math import log
from random import uniform
from collections import Counter
import csv
import numpy

testSmall = [5, 0.321, -2989.2, -0.00001]

testLarge = []

def testData():
    for i in range(0,1000):
        a = uniform(0,1)
        b = 10.0**a
        testLarge.append(b)

# Functions
def benfords(data, start_position=1, output_csv=False):
    """
    Given a set of data, extract the significant digits and compare to Benford's Law.
    """
    results = dict()
    sigdigits = nsd(data, start_position)
    sigcounts = Counter(sigdigits)

    digit_min = 1
    digit_max = 9

    if start_position > 1:
        digit_min = 0

    for i in range(digit_min,digit_max+1):
        theoretical = expectation(i, position=start_position)
        empirical = sigcounts[str(i)]/sigdigits.size

        results[str(i)] = [theoretical, empirical]

    if output_csv is True:
        with open('Benfords Law output.csv', mode='w', newline='') as outputfile:
            writer = csv.writer(outputfile, delimiter = ',')
            headers = ['Digit', 'Expected from Benfords Law', 'Actual from Data', 'Difference']
            writer.writerow(headers)
            
            for key,value in results.items():
                output_values = []
                output_values.append(key)
                for i in value:
                    output_values.append(i)
                output_values.append(value[1]-value[0])
                writer.writerow(output_values)
        
    return results

    # Current state: first sig digit only. Next, add the ability to choose the starting position and number of digits.


def deviate():
    """
    Returns a random Benford-distributed deviate.
    """
    u = 0
    while not (0 < u < 1):
        u = uniform(0,1)

    return 10**u

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


