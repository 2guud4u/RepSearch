from flask import *
from searchCode import searchItem
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#from dataModels import db, Product

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./posts.db"


db = SQLAlchemy(app)




@app.route("/results", methods=['GET', 'POST'])#search results
def results():
    #down here to avoid circular imports
    from dataModels import Product
    with app.app_context():
        db.create_all()
    if request.method == "POST":
        searchVal = request.form.get("sVal")
        
        result=searchItem(searchVal)
        #if no results
        if len(result) == 0:
            return render_template("empty.html", searchVal=searchVal)
       
    #store info into database
        date = datetime.now().time()
        for item in result:
            
            data = Product(post_id=item.post_id,
                            score=item.rating, 
                            date_updated=date,
                            title=item.title, 
                            url=item.url)
            db.session.add(data)  # Add the instance to the session
            db.session.commit()  # Commit the session to persist the data in the database

    return render_template("results.html", result=result)

@app.route("/")
def index():

    return render_template("index.html")

