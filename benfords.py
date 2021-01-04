from math import log
import numpy

test = [5, 0.321, -2989.2, -0.00001]

# Functions
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
    Given a pandas dataframe, numpy array, list or number, return the first significant digits of that data.
    """
    if type(data) == int:
        if data == 0:
            return "Zero has no first-significant digit. Please ensure your data has no zeros."
    elif 0 in data:
        return "Zero has no first-significant digit. Please ensure your data has no zeros."

    return int(numpy.floor(10**(numpy.log10(numpy.abs(data))-numpy.floor(numpy.log10(numpy.abs(data))))))

def nsd(data, position):
    """
    Given some data and the position of the digit desired, return the digit.
    """
    format_string = "{:.15e}"

    scientific_notation = format_string.format(abs(data)) #Change to scientific notation and remove negative sign
    value_string = scientific_notation.replace('.', '')[0:14] #Remove decimal point and limit to 14 characters
    
    return value_string[position-1]

    """
    nsd() currently works for scalars, but not lists, numpy arrays, or pandas dataframes. I think numpy format_float_scientific will help here.
    """
    

