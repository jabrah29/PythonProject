from flask import Flask
import time

from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "works"

time.sleep(2)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
