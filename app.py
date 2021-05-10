# First we imported the Flask class. An instance of this
# - class will be our WSGI application.
from flask import Flask

# Next we create an instance of this class. The first argument
# - is the name of the application’s module or package. __name__ is
# - a convenient shortcut for this that is appropriate for most cases.
# - This is needed so that Flask knows where to look for resources
# - such as templates and static files.
app = Flask(__name__)


# We then use the route() decorator to tell Flask what
# - URL should trigger our function.
@app.route('/')
def hello_world():
    return 'Hello World!'


# he function returns the message we want to display in the user’s browser.
# - The default content type is HTML, so HTML in the string will be rendered
# - by the browser.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
