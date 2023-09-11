from flask import *
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Path for our main Svelte page
@app.route("/rand")
def hello():
    return str(random.randint(0, 100)) + " is a random number"


if __name__ == "__main__":
    app.run(debug=True)