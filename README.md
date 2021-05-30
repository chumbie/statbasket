# Stat Basket

Stat Basket is a small statistics package intended for use with student projects 
or small datasets (<1 mil data points). It is implemented with pure python, 
so no external dependencies are required.

stat-basket includes two classes, StatMe and StatBasket.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install stat-basket.

```bash
pip install statbasket
```

## Usage
Using the StatBasket class generates all statistical data on initialization.
```python
from statbasket.statbasket import StatBasket

data = (13, 26, 41, 35, 12)
# Store statistics in object as attributes
basket = StatBasket(data)
print(basket.mean)

Output:
25.4
```
Alternatively, if you want to perform specific calculations on-the-fly, 
without performing the entire batch at once, you can use the StatMe class 
of methods:
```python
from statbasket.statmethods import StatMe

data = (13, 26, 41, 35, 12)
# Perform single operation on data
mean = StatMe.get_mean(data)
print(mean)

Output:
25.4
```
For a full list of available attributes and methods, view the individual class docstrings.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)