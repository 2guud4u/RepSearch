from flask import *
from searchCode import searchItem, loadMore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import glob 
import time

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#from dataModels import db, Product

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./posts.db"


db = SQLAlchemy(app)
cur_form = {}
app.secret_key = 'your-secret-key'


@app.route("/results", methods=['GET', 'POST'])#search results
def results():
    #down here to avoid circular imports
    from databases.dataModels import Product
    
    with app.app_context():
        db.create_all()
    info = session.get('form_data')
    if "fromIndex" in info:
        
            searchVal = info.get("sVal")
            
            result=searchItem(db, searchVal)
            #if no results
            if len(result) == 0:
                return render_template("empty.html", searchVal=searchVal)
    if "fromResults" in info:
        result = loadMore()
    #store info into database
    date = datetime.now().time()
    for item in result:
        if item.cached == False:
            data = Product(post_id=item.post_id,
                            score=item.rating, 
                            date_updated=date,
                            title=item.title, 
                            url=item.url)
            db.session.merge(data)  # Add the instance to the session
            db.session.commit()  # Commit the session to persist the data in the database
         
            print("added",item.post_id,"to cache")
    
    return render_template("results.html", result=result)

@app.route("/")
def index():
    
   
    return render_template("index.html")

@app.route("/loading", methods=['GET', 'POST'])
def loading():
    gifList = glob.glob("static/gifs/*.gif")
    session['form_data'] = request.form
    
    return render_template("loading.html", gifList=gifList)






