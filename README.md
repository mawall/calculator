Simple calculator for expressions in prefix (polish) and fully parenthesized infix notation

* Assumes space separated tokens as input
* Supports addition, subtraction, multiplication and division
* Does not handle divisions by zero
* Includes minimal REST interface


#### Dependencies
* Python 3.8
* Flask
* PyTest

Run interface with
```Bash
export FLASK_APP=main.py
FLASK_DEBUG=1 python -m flask run
```

Run tests with `python -m pytest `
