# -- Import Flask dependency
from flask import Flask

# -- Create Flask instance
app = Flask(__name__)

# -- Define root 
@app.route('/')

# -- Create function "Hello World"
def hello_world():
	return 'Hello world'
