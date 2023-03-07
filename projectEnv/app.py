from flask import *
from searchCode import searchItem
from flask import Flask
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])#search front page 
def home():
    return "Hello, Flask!"

@app.route("/results/<name>", methods=['GET', 'POST'])#search results
def results(name):
    result=str(searchItem(name)[0])
   
    return render_template("results.html", result=result)

@app.route("/index/<input>")
def index(input):

    return render_template("index.html", input = input)

