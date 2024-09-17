from flask import Flask, render_template

import ShedulerService

app = Flask(__name__)


def main():
    return render_template('manual_start.html')


@app.route('/')
def index(name=None):
    return render_template('manual_start.html', name=name)

@app.route('/run_all')
def run_all(name=None):
    ShedulerService.job_function()
    return render_template('manual_start.html', name=name)

@app.route('/run_rubric_cl')
def run_rubric_cl(name=None):
    ShedulerService.job_function_rubric_cl()
    return render_template('manual_start.html', name=name)


@app.route('/run_appeal')
def run_appeal(name=None):
    ShedulerService.job_function_appeal_date()
    return render_template('manual_start.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug = True
