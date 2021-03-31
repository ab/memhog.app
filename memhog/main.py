from flask import Flask

from .lib import hog_memory

app = Flask(__name__)


@app.route("/")
def root():
    return "Hello, you probably want /hog"


@app.route("/hog")
def hog():
    # Hog all memory, 0.2 sec wait
    hog_memory(interval=0.2, cap=False)
