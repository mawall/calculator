from calculator import calculate_prefix
from calculator import calculate_infix

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/prefix')
def prefix():
    return render_template('index.html', current_type='Prefix', other_type='Infix')


@app.route('/infix')
def infix():
    return render_template('index.html', current_type='Infix', other_type='Prefix')


def calculate(func, current_type, other_type):
    error = False
    s = request.form.get("finput", type=str)
    try:
        result = func(s)
    except ValueError as e:
        error = True
        result = 'ERROR - ' + str(e)

    return render_template('index.html',
                           current_type=current_type,
                           other_type=other_type,
                           result=result,
                           error=error)


@app.route("/prefix/submit", methods=['POST'])
def submit_prefix_calculation():
    return calculate(calculate_prefix, current_type='Prefix', other_type='Infix')


@app.route("/infix/submit", methods=['POST'])
def submit_infix_calculation():
    return calculate(calculate_infix, current_type='Infix', other_type='Prefix')


if __name__ == '__main__':
    pass
