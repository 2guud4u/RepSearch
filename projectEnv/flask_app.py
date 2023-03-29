from flask import *
from searchCode import searchItem
from flask import Flask
app = Flask(__name__)


@app.route("/results", methods=['GET', 'POST'])#search results
def results():
    if request.method == "POST":
        searchVal = request.form.get("sVal")

        result=searchItem(searchVal)


    return render_template("results.html", result=result)

@app.route("/")
def index():

    return render_template("index.html")