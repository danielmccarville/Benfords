# Benfords
Benfords is a Python library built to assist with using Benford's Law.



## Usage
Benfords allows you two do two things: to calculate the expected probability of digits, and to extract the actual digits from your data.

You can use Benfords to easily calculate the expected probability of digit combinations in any position:

```python
import benfords

#How often should '1' be the first significant digit?
expectation(1,1) #Returns 0.3010.... (30.1%)

#How often should '1' be the third significant digit?
expectation(1, 3) #Returns 0.1013..... (10.1%)

#How often should '19' be the second and third digits?
expectation(19, 2) #Returns 0.0666..... (6.7%)
```

Benfords can also extract actual digits from your data. It currently accepts scalars (integers and floats), lists, as well as 1-dimensional numpy arrays.
```python
test = [5, 0.321, -2989.2, -0.00001]

#FSD() returns the first significant digit as floats. For a list, it returns a 1d numpy array containing floats.
fsd(9) #Returns 9.0
fsd(test) #Returns array([5., 3., 2., 1.])

#NSD() returns the nth digit of your data. It always returns a numpy array containing strings.
#What's the second data of 9.1?
nsd(9.1, 2) #Returns array(['1'])

nsd(test, 4) #Returns array(['0', '1', '8', '0']

```

## Roadmap
Phase 1 of Benfords focused on implementing basic digit functions. Phase 2 will implement descriptive comparisons such as those commonly seen in accounting and fraud investigations. New functions will create plots comparing the actual and expected digit frequencies, as well as output summary tables.

Phase 3 will implement hypothesis testing and some other more advanced features.

## License
[MIT](https://choosealicense.com/licenses/mit/)
