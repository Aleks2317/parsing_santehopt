from flask import Flask
from pars import parsing_go

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')

@app.route('/hello')
def hello():
    return 'to go "/parsing"'


@app.route('/parsing')
def parsing():
    print('asldfjalsdjflajsd;fj')

    return parsing_go()

if __name__ == '__main__':
    # Run the app server on localhost:3000
    app.run('localhost', 3000)