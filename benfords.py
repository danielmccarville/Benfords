from math import log
from random import uniform
from collections import Counter
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Functions
def plot(inputdata, digits, y_col_actual, y_col_expected, save=False):

    plt.rcParams['patch.force_edgecolor']=True

    ax1 = sns.barplot(
        data=inputdata,
        x = digits,
        y = y_col_actual,
        color = '#B2E8C2',
        label='Actual Data'
        )
    ax1.set(ylabel='Relative Frequency')

    ax2 = sns.lineplot(
        data=inputdata,
        x = digits,
        y = y_col_expected,
        ax = ax1,
        zorder = 5,
        color = 'black',
        style=True,
        dashes=[(2,2)],
        markers=True,
        label='Benfords Law',
        )

    handles, labels = ax2.get_legend_handles_labels()
    labels[1] = "_True"

    # Matplotlib returns a warning, because we used a label with an _.
    # This is desirable, so the warning is suppressed.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=UserWarning)    
        ax2.legend(handles, labels)

    plt.show()


def benfords(data, start_position=1, length=1, output_csv=False, output_plot=False):
    """
    Given a set of data, extract the significant digits and compare to Benford's Law.
    """
    temp_results = []
    sigdigits = nsd(data, start_position, length)
    sigcounts = Counter(sigdigits)

    if (length==1) and (start_position > 1):
        digit_min = 0
    else:
        digit_min = 10**(length-1)
    
    digit_max = 10**(length)-1

    if start_position > 1:
        digit_min = 0

    for i in range(digit_min,digit_max+1):
        theoretical = expectation(i, position=start_position)
        empirical = sigcounts[str(i)]/sigdigits.size
        difference = empirical - theoretical

        temp_results.append([str(i), theoretical, empirical, difference])

    results = pd.DataFrame(temp_results, columns=['Digit', 'Expected Value', 'Actual Value', 'Difference'])
    results.set_index('Digit')

    if output_csv is True:
        results.to_csv('Benfords Law output.csv', index=False)

    if output_plot is True:
        plot(results, 'Digit', 'Actual Value', 'Expected Value', save=False)
        
    return results


def deviate(x):
    """
    Returns a random Benford-distributed deviate.
    """
    def single_deviate():
        u = 0
        while not (0 < u < 1):
            u = uniform(0,1)

        return 10**u

    results = []
    for i in range(0, x):
        results.append(single_deviate())

    return results
        



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

    return numpy.array(numpy.floor(10**(numpy.log10(numpy.abs(data))-numpy.floor(numpy.log10(numpy.abs(data))))))

def nsd(data, position, length=1):
    """
    Given some data and the position of the digit desired, return the digit.
    """
    def np_slicer(a, start, end):
        b = a.view((str,1)).reshape(len(a),-1)[:,start:end]
        return numpy.frombuffer(b.tobytes(), dtype=(str, end-start))

    if isinstance(data, (float, int)):
        data = numpy.array([data])
    if isinstance(data, (list, pd.DataFrame)):
        data = numpy.array(data)

    positive = numpy.absolute(data) #remove negative sign

    number_zeroes = numpy.count_nonzero(positive==0)
    if number_zeroes > 0:
        return "Zero has no significant digits. Please ensure your data has no zeroes."

    data_np = []
    for i in positive:
        data_np.append(numpy.format_float_scientific(i, precision=15, unique=False))
        
    data_np = numpy.array(data_np)
    clean_string = numpy.char.replace(data_np, '.', '')
    truncated = np_slicer(clean_string, 0, 14)

    return np_slicer(truncated, position-1, position-1+length)


# test data
# testSmall = [5, 0.321, -2989.2, -0.00001, 0]
# testLarge = deviate(100)



