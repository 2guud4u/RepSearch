from flask import *
from searchCode import searchItem, loadMore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import glob 
import time
from flask_cors import CORS
import json

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#from dataModels import db, Product

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./posts.db"


db = SQLAlchemy(app)
cur_form = {}
app.secret_key = 'your-secret-key'

def serialize(self):
        return {"url": self.url,
                "rating": self.rating,
                "title": self.title,
                "wtc": self.wtc,
                "post_id": self.post_id,
                "cached": self.cached}

 
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
    if "fromResults" in request.form:
        result = loadMore()
    
            
           
    for r in result:
         print(r)
    return jsonify(result[0].serialize())




@app.route("/loading", methods=['GET', 'POST'])
def loading():
    gifList = glob.glob("static/gifs/*.gif")
    session['form_data'] = request.form
    
    return render_template("loading.html", gifList=gifList)

if __name__ == "__main__":
    app.run(debug=True)