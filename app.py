from dotenv import load_dotenv
from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/')
def main_page():
    return render_template('index.html')

from routes import *

if __name__ == "__main__":
    app.run(port=7777, debug=True, host="127.0.0.1")